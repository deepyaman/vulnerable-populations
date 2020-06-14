"""Transform the raw master table to make it suitable for estimators."""
import pandas as pd


def dropna(df: pd.DataFrame) -> pd.DataFrame:
    """Call the `pandas.DataFrame.dropna` method with default arguments.

    Args:
        df: A pandas DataFrame optionally containing NA entries to drop.

    Returns:
        The input DataFrame with rows containing missing values removed.

    """
    return df.dropna()
