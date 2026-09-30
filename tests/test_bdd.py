from pathlib import Path
from pytest_bdd import scenarios, given, when, then, parsers
from src.validators import null_count, duplicate_count, orphan_keys
from src.reconciliation import reconcile

FEATURES = str(Path(__file__).resolve().parents[1] / "features")
scenarios(FEATURES)

@given("the customer source data is available")
def customer_available(customers): return customers
@given("the transaction source data is available")
def transaction_available(transactions): return transactions
@given("customer and transaction source data are available")
def both_available(customers, transactions): return customers, transactions
@given("valid source datasets are available")
def valid_sources(customers, transactions): return customers, transactions

@when("I validate customer identifiers", target_fixture="result")
def validate_customer_ids(customers): return null_count(customers,'customer_id'), duplicate_count(customers,'customer_id')
@then("customer identifiers should be non-null and unique")
def customer_ids_ok(result): assert result == (0,0)
@when("I validate mandatory customer fields", target_fixture="result")
def validate_customer_fields(customers): return null_count(customers,'email')
@then("customer email should not be null")
def customer_email_ok(result): assert result == 0
@when("I validate transaction identifiers", target_fixture="result")
def validate_tx_ids(transactions): return null_count(transactions,'transaction_id'), duplicate_count(transactions,'transaction_id')
@then("transaction identifiers should be non-null and unique")
def tx_ids_ok(result): assert result == (0,0)
@when("I validate transaction customer references", target_fixture="result")
def validate_refs(customers, transactions): return orphan_keys(transactions, customers,'customer_id','customer_id')
@then("every transaction customer should exist in customer data")
def refs_ok(result): assert result == set()
@when("I load them into the local warehouse", target_fixture="result")
def load_demo(transactions): return reconcile(transactions, transactions.copy(),'amount')
@then("source and target row counts should match")
def counts_match(result): assert result.source_count == result.target_count
@then("transaction amount totals should match")
def totals_match(result): assert abs(result.source_total-result.target_total) < .01
