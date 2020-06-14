"""Define nodes to type the raw data models under the CSBH Dashboard."""
import pandas as pd
from pandas.api.types import is_string_dtype


def _is_percentage_column(column: pd.Series) -> bool:
    return is_string_dtype(column) and column.str.endswith("%").all()


def percentage_to_numeric(df: pd.DataFrame) -> pd.DataFrame:
    return df.apply(
        lambda c: c.str[:-1].astype(float) / 100 if _is_percentage_column(c) else c
    )
