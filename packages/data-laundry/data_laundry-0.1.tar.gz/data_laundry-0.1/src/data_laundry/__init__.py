import pandas as pd
import re


class NoDataError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidInput(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def __is_clean(df):
    for _, dtype in df.dtypes.to_dict().items():
        if "ArrowDtype" not in type(dtype).__name__:
            return False

    for col in df.columns:
        if len(re.findall(r"\W+", col)) > 0:
            return False

    return True


def __launder_df(df, **kwargs) -> pd.DataFrame:
    # Change dtype backend to pyarrow
    df = df.convert_dtypes(dtype_backend="pyarrow")

    # Cleanup column names
    df.rename(
        columns={key: re.sub(r"\W+", "_", key.strip()).lower() for key in df.columns},
        inplace=True,
    )

    # Select columns from df
    if "select_columns" in kwargs.keys():
        columns = [
            re.sub(r"\W+", "_", col.strip()).lower() for col in kwargs["select_columns"]
        ]
    else:
        columns = df.columns

    return df[columns]


def __launder_path(path, **kwargs) -> pd.DataFrame:
    df: pd.DataFrame

    if path[-3:] == "csv":
        df = pd.read_csv(path, dtype_backend="pyarrow", **kwargs)

    elif path[-4:] == "xlsx":
        df = pd.read_excel(path, dtype_backend="pyarrow", **kwargs)

    elif path[-7:] == "xlsx":
        df = pd.read_parquet(path, dtype_backend="pyarrow", **kwargs)

    else:
        raise NoDataError(
            "Invalid file to parse. Supported filetypes are csv, xlsx, and parquet."
        )

    return df


def __get_sql_dtype(dtype) -> str:
    match dtype:
        case "string[pyarrow]":
            return "VARCHAR(MAX)"
        case "int64[pyarrow]":
            return "BIGINT"
        case "double[pyarrow]":
            return "DECIMAL(18, 3)"
        case "timestamp[ns][pyarrow]":
            return "date"
        case "null[pyarrow]":
            return "VARCHAR(MAX)"

        case _:
            raise Exception(f"Unknown dtype: {dtype}")


def convert_to_sql(
    df,
    table_name="tmp",
    output_path=".",
    step=1000,
) -> None:
    if type(df) is not pd.DataFrame:
        raise InvalidInput(
            f"Invalid input passed to function convert_to_sql. Expected pd.DataFrame but got {type(df)}"
        )

    if not __is_clean(df):
        df = launder(df)

    s = f"DROP TABLE IF EXISTS #{table_name};\nCREATE TABLE #{table_name} (\n"

    for i, (key, dtype) in enumerate(df.dtypes.to_dict().items()):
        s += f"""\t{'' if i == 0 else ', '}{key} {__get_sql_dtype(dtype)}\n"""
    s += ");\n\n"
    with open(f"{output_path}/clipboard.txt", "w") as f:
        f.write(s)

    row_writer = []

    for row in df.values:
        row_concat = []

        for val in row:
            if type(val) is pd.Timestamp:
                row_concat.append(f"'{val.strftime('%Y-%m-%d')}'")
            elif type(val) is str:
                row_concat.append(
                    "'"
                    + val.strip()
                    .replace("'NULL'", "NULL")
                    .replace("''", "NULL")
                    .replace("'", "''")
                    + "'"
                )
            elif val is pd.NA or val is None:
                row_concat.append("NULL")
            else:
                row_concat.append(str(val))

        row_writer.append("(" + ", ".join(row_concat) + ")")

    with open(f"{output_path}/clipboard.txt", "a") as f:
        for i in range(0, len(row_writer), step):
            writer = ", ".join(row_writer[i : i + step])
            f.write(f"""INSERT INTO #{table_name} VALUES \n\t{writer} \n;\n""")

    print(f"Written to: {output_path}/clipboard.txt")


def launder(*args, **kwargs) -> pd.DataFrame:
    launder_kwargs_list = ["select_columns"]

    launder_kwargs = {}

    for k in launder_kwargs_list:
        if k in kwargs.keys():
            launder_kwargs[k] = kwargs.pop(k)

    if type(args[0]) is str:
        df = __launder_path(args[0], **kwargs)

    elif type(args[0]) is pd.DataFrame:
        df = args[0]

    else:
        raise InvalidInput(
            f"Called launder on unexpected input. Expected str: /path/to/file or pd.DataFrame. Got {type(args[0])}"
        )

    return __launder_df(df, **launder_kwargs)
