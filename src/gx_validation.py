
import great_expectations as gx
import pandas as pd


def log_validation_results(dataset_name, validation_result):
    print(f"\n===== {dataset_name.upper()} GX VALIDATION =====")

    for result in validation_result.results:
        config = result.expectation_config

        print("Expectation:", config.type)
        print("Column:", config.kwargs.get("column"))
        print("Passed:", result.success)

        if not result.success:
            print("Failure details:", result.result)
            print("Exception:", result.exception_info)

        print("--------------------------------")

    print("Overall success:", validation_result.success)


def validate_customers(customers: pd.DataFrame) -> bool:
    """Validate customer data using Great Expectations."""

    context = gx.get_context()

    data_source = context.data_sources.add_pandas("customer_source")
    data_asset = data_source.add_dataframe_asset(name="customers")

    batch_definition = data_asset.add_batch_definition_whole_dataframe(
        "customer_batch"
    )

    batch = batch_definition.get_batch(
        batch_parameters={"dataframe": customers}
    )

    suite = gx.ExpectationSuite(name="customer_quality_suite")

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToNotBeNull(
            column="customer_id"
        )
    )

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeUnique(
            column="customer_id"
        )
    )

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToNotBeNull(
            column="email"
        )
    )

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeInSet(
            column="country_code",
            value_set=["GB", "IE"],
        )
    )

    validation_result = batch.validate(suite)
    log_validation_results("customers", validation_result)
    return validation_result.success


def validate_transactions(transactions: pd.DataFrame) -> bool:
    """Validate transaction data using Great Expectations."""

    context = gx.get_context()

    data_source = context.data_sources.add_pandas("transaction_source")
    data_asset = data_source.add_dataframe_asset(name="transactions")

    batch_definition = data_asset.add_batch_definition_whole_dataframe(
        "transaction_batch"
    )

    batch = batch_definition.get_batch(
        batch_parameters={"dataframe": transactions}
    )

    suite = gx.ExpectationSuite(name="transaction_quality_suite")

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToNotBeNull(
            column="transaction_id"
        )
    )

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeUnique(
            column="transaction_id"
        )
    )

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToNotBeNull(
            column="customer_id"
        )
    )

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeInSet(
            column="currency",
            value_set=["GBP", "EUR"],
        )
    )

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeInSet(
            column="status",
            value_set=[
                "PENDING",
                "COMPLETED",
                "FAILED",
                "REVERSED",
            ],
        )
    )

    validation_result = batch.validate(suite)
    log_validation_results("customers", validation_result)
    return validation_result.success



def validate_accounts(accounts: pd.DataFrame) -> bool:
    """Validate accounts data using Great Expectations."""
    context = gx.get_context()

    data_source = context.data_sources.add_pandas("account_source")
    data_asset = data_source.add_dataframe_asset(name="accounts")

    batch_definition = data_asset.add_batch_definition_whole_dataframe(
        "accounts_batch"
    )

    batch = batch_definition.get_batch(
        batch_parameters= {"dataframe": accounts}
    )

    suite = gx.ExpectationSuite(
        name = "account_quality_suite"
    )

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToNotBeNull(
            column="account_id"
        )
    )

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeUnique(
            column="account_id"
        )
    )

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToNotBeNull(
            column="customer_id"
        )
    )

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToNotBeNull(
            column="account_type"
        )
    )

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeInSet(
            column="account_type",
            value_set = ["SAVINGS", "CURRENT"]
        )
    )

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="balance",
            min_value=0
        )
    )

    validation_result = batch.validate(suite)
    log_validation_results("customers", validation_result)
    return validation_result.success

def validate_payments(payments: pd.DataFrame) -> bool:
    context = gx.get_context()
    data_source = context.data_sources.add_pandas("payment_sources")
    data_asset = data_source.add_dataframe_asset(name="payments")

    batch_definition = data_asset.add_batch_definition_whole_dataframe(
        "payments_batch"
    )

    batch = batch_definition.get_batch(
        batch_parameters= {"dataframe": payments}
    )

    suite = gx.ExpectationSuite(
        name= "payments_quality_suite"
    )

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToNotBeNull(
            column="payment_id"
        )
    )

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeUnique(
            column="payment_id"
        )
    )

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToNotBeNull(
            column="customer_id"
        )
    )

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToNotBeNull(
            column="payment_amount"
        )
    )

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="payment_amount",
            min_value=0
        )
    )

    suite.add_expectation(
        gx.expectations.ExpectColumnValuesToBeInSet(
            column="payment_status",
            value_set = ["COMPLETED", "PENDING", "FAILED"]
        )
    )

    validation_result = batch.validate(suite)
    log_validation_results("payments", validation_result)
    return validation_result.success