from src.gx_validation import (
    validate_customers,
    validate_transactions,
    validate_accounts,
    validate_payments
)

def test_customer_great_expectations_validation(customers):
    assert validate_customers(customers)

def test_transaction_great_expectations_validation(transactions):
    assert validate_transactions(transactions)

def test_accounts_great_expectations_validations(accounts):
    assert validate_accounts(accounts)

def test_payments_great_expectations_validations(payments):
    assert validate_payments(payments)