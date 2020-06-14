"""Define nodes to type the raw data models under the CSBH Dashboard."""
import pandas as pd
from pandas.api.types import is_string_dtype


def _is_percentage_column(column: pd.Series) -> bool:
    return is_string_dtype(column) and column.str.endswith("%").all()


def percentage_to_numeric(df: pd.DataFrame) -> pd.DataFrame:
    """Identify and convert percentage columns to float representations.

    Args:
        df: A pandas DataFrame optionally containing percentage columns.

    Returns:
        The input DataFrame with percentage columns cast to float types.

    """
    return df.apply(
        lambda c: c.str[:-1].astype(float) / 100 if _is_percentage_column(c) else c
    )
