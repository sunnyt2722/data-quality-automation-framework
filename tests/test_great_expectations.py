import pandas as pd

from src.gx_validation import (
    validate_customers,
    validate_transactions,
)


def test_customer_great_expectations_validation():
    customers = pd.read_csv(
        "dbt_project/seeds/customers.csv"
    )

    assert validate_customers(customers)


def test_transaction_great_expectations_validation():
    transactions = pd.read_csv(
        "dbt_project/seeds/transactions.csv"
    )

    assert validate_transactions(transactions)