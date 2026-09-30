from src.validators import null_count, duplicate_count, invalid_values, orphan_keys

def test_customer_ids_are_complete_and_unique(customers):
    assert null_count(customers, "customer_id") == 0
    assert duplicate_count(customers, "customer_id") == 0

def test_customer_email_is_mandatory(customers):
    assert null_count(customers, "email") == 0

def test_transaction_ids_are_complete_and_unique(transactions):
    assert null_count(transactions, "transaction_id") == 0
    assert duplicate_count(transactions, "transaction_id") == 0

def test_transaction_domain_values(transactions):
    assert invalid_values(transactions, "currency", {"GBP", "EUR"}) == set()
    assert invalid_values(transactions, "status", {"PENDING", "COMPLETED", "FAILED", "REVERSED"}) == set()

def test_transaction_customer_references(customers, transactions):
    assert orphan_keys(transactions, customers, "customer_id", "customer_id") == set()

def test_completed_transaction_amounts_are_positive(transactions):
    bad = transactions[(transactions.status == "COMPLETED") & (transactions.amount <= 0)]
    assert bad.empty
