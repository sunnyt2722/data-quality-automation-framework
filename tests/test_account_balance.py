import pandas as pd

from src.validators import negative_balance_count


def test_account_balances_are_non_negative():
    df = pd.read_csv("dbt_project/seeds/accounts.csv")

    result = negative_balance_count(df)

    assert result == 0, (
        f"Found {result} accounts with negative balances"
    )