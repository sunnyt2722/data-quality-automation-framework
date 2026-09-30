import great_expectations as gx
import pandas as pd


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

    return validation_result.success