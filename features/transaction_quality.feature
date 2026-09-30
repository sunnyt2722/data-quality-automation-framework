Feature: Transaction data quality
  Scenario: Transaction identifiers are complete and unique
    Given the transaction source data is available
    When I validate transaction identifiers
    Then transaction identifiers should be non-null and unique

  Scenario: Transaction customers exist
    Given customer and transaction source data are available
    When I validate transaction customer references
    Then every transaction customer should exist in customer data

  Scenario: Source data reconciles with the warehouse load
    Given valid source datasets are available
    When I load them into the local warehouse
    Then source and target row counts should match
    And transaction amount totals should match
