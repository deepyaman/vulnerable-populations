"""Transform the raw master table to make it suitable for estimators."""
import operator
from functools import reduce
from typing import Any, Dict, List, Optional

import pandas as pd


def filter_rows(
    df: pd.DataFrame, filters: Optional[Dict[str, List[Any]]] = None
) -> pd.DataFrame:
    """Filter the rows of a DataFrame by a combined group of conditions.

    Args:
        df: A pandas DataFrame to subset according to specified filters.
        filters: A mapping of column names to permitted values. Defaults
            to an empty mapping to return unfiltered.

    Returns:
        A pandas DataFrame view containing selected rows, or a deep copy
            of the original input DataFrame if `filters` is empty.

    """
    if filters is None:
        filters = {}
    copied = df.copy()
    if not filters:
        return copied
    return copied[
        reduce(operator.and_, (copied[col].isin(vals) for col, vals in filters.items()))
    ]


def dropna(df: pd.DataFrame) -> pd.DataFrame:
    """Call `pandas.DataFrame.dropna`, ignoring any always-null columns.

    Args:
        df: A pandas DataFrame optionally containing NA entries to drop.

    Returns:
        The input DataFrame with rows containing missing values removed.

    """
    return df.dropna(subset=df.columns[df.notna().any()])
