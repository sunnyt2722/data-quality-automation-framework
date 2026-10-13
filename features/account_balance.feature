Feature: Account balance validation

  Scenario: Accounts must not have negative balances
    Given the accounts dataset is available
    When I validate account balances
    Then all account balances should be non-negative