Feature: Customer data quality
  As a data quality engineer
  I want critical customer attributes validated
  So that downstream banking processes receive trustworthy data

  Scenario: Customer identifiers are complete and unique
    Given the customer source data is available
    When I validate customer identifiers
    Then customer identifiers should be non-null and unique

  Scenario: Customer emails are populated
    Given the customer source data is available
    When I validate mandatory customer fields
    Then customer email should not be null
