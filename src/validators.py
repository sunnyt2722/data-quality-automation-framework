import pandas as pd


def null_count(df: pd.DataFrame, column: str) -> int:
    """Return the number of null values in a column."""
    return int(df[column].isna().sum())


def duplicate_count(df: pd.DataFrame, column: str) -> int:
    """Return the number of duplicate values in a column."""
    return int(df[column].duplicated().sum())


def invalid_values(
    df: pd.DataFrame,
    column: str,
    allowed: set[str],
) -> set[str]:
    """Return values that are outside the allowed domain."""
    values = set(df[column].dropna().astype(str))
    return values - allowed


def orphan_keys(
    child: pd.DataFrame,
    parent: pd.DataFrame,
    child_key: str,
    parent_key: str,
) -> set:
    """Return child keys that do not exist in the parent dataset."""
    child_values = set(child[child_key].dropna())
    parent_values = set(parent[parent_key].dropna())

    return child_values - parent_values