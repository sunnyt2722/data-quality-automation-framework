from src.reconciliation import reconcile

def test_source_target_reconciliation(transactions):
    # Demo target is an identity copy; production target would be queried from the warehouse.
    target = transactions.copy()
    result = reconcile(transactions, target, "amount")
    assert result.passed
    assert result.source_count == result.target_count
