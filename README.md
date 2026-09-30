# Data Quality Automation Framework

A reusable data quality engineering framework demonstrating automated
validation across ingestion, transformation and reconciliation layers using
Python, pytest, Great Expectations, dbt and DuckDB.

The project demonstrates production-oriented data quality engineering
patterns including:

- Dataset validation
- Schema and domain validation
- Referential integrity
- Business-rule validation
- Source-to-target reconciliation
- BDD-based quality requirements
- Automated negative testing
- CI/CD quality gates
- Clear failure reporting

---

## 1. Architecture

```text
                         Source Data
                    customers.csv
                  transactions.csv
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼
       Python / Pandas                dbt seed
             │                           │
             ▼                           ▼
    Great Expectations                DuckDB
             │                           │
     Dataset Validation                 ▼
             │                     Staging Models
             │                    ┌──────┴──────┐
             │                    │             │
             │              stg_customers  stg_transactions
             │                    │             │
             │                    └──────┬──────┘
             │                           ▼
             │              customer_transaction_summary
             │                           │
             │                           ▼
             │                       dbt Tests
             │
             └──────────────┬────────────┘
                            │
                            ▼
                          pytest
               ┌────────────┼────────────┐
               │            │            │
              BDD       Validators   Reconciliation
               │            │            │
               └────────────┼────────────┘
                            ▼
                      CI/CD Quality Gate
                            │
                     PASS / FAIL Build
```

The framework intentionally validates quality at more than one layer.

A source dataset may be structurally valid while still violating a warehouse relationship or business rule. Testing at multiple stages provides defence in depth rather than relying on a single validation mechanism.

---

## 2. Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Core automation language |
| pandas | Dataset loading and manipulation |
| pytest | Test execution and assertions |
| pytest-bdd | BDD/Gherkin-based quality scenarios |
| Great Expectations | Dataset-level expectations |
| dbt | Transformation and warehouse quality testing |
| DuckDB | Lightweight analytical database |
| GitHub Actions | CI/CD quality gate |

Validated locally using:

- Python `3.12.10`
- pytest `8.3.5`
- Great Expectations `1.3.8`
- dbt `1.9.3`
- dbt-duckdb `1.9.2`

---

## 3. Repository Structure

```text
data-quality-automation-framework/
│
├── .github/
│   └── workflows/
│
├── dbt_project/
│   ├── models/
│   │   └── staging/
│   ├── seeds/
│   │   ├── customers.csv
│   │   └── transactions.csv
│   ├── tests/
│   ├── dbt_project.yml
│   └── profiles.yml
│
├── features/
│   └── data_quality.feature
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── gx_validation.py
│   ├── reconciliation.py
│   └── validators.py
│
├── tests/
│   ├── test_bdd.py
│   ├── test_data_quality.py
│   ├── test_great_expectations.py
│   └── test_reconciliation.py
│
├── warehouse/
├── pytest.ini
├── requirements.txt
├── .env.example
└── README.md
```

---

## 4. Data Flow

The sample pipeline contains two primary datasets:

### Customers

Contains customer-level information.

Key quality requirements include:

- `customer_id` must not be null
- `customer_id` must be unique
- email must be populated
- country codes must belong to the supported domain

### Transactions

Contains transaction-level information.

Key quality requirements include:

- `transaction_id` must not be null
- `transaction_id` must be unique
- `customer_id` must not be null
- transaction customer must exist in the customer dataset
- currency must belong to the supported domain
- transaction status must contain an accepted value
- completed transactions must have a positive amount
- transactions must not occur in the future

---

## 5. Data Quality Strategy

The framework applies quality controls across several dimensions.

| Quality Dimension | Example |
|---|---|
| Completeness | Customer and transaction IDs cannot be null |
| Uniqueness | Transaction IDs must be unique |
| Validity | Currency/status must use accepted values |
| Referential Integrity | Transaction customer must exist |
| Business Rules | Completed transaction amount must be positive |
| Timeliness | Future transactions are rejected |
| Reconciliation | Source and target records must reconcile |

This separation allows quality rules to be applied at the layer where they provide the most value.

---

## 6. Python / pytest Validation

Python validators provide lightweight reusable checks for source datasets.

Examples include:

- identifier completeness
- identifier uniqueness
- mandatory fields
- domain validation
- customer-reference validation
- transaction business rules

Run the complete Python suite from the project root:

```powershell
pytest -v
```

Current verified result:

```text
14 passed
```

The suite includes:

- BDD tests
- Python data-quality tests
- Great Expectations tests
- reconciliation tests

---

## 7. Great Expectations

Great Expectations provides an additional declarative dataset-validation layer.

Customer expectations include:

- customer ID is populated
- customer ID is unique
- email is populated
- country code belongs to an accepted set

Transaction expectations include:

- transaction ID is populated
- transaction ID is unique
- customer ID is populated
- currency belongs to an accepted set
- status belongs to an accepted set

The implementation is located in:

```text
src/gx_validation.py
```

and exercised through:

```text
tests/test_great_expectations.py
```

Run only the Great Expectations tests with:

```powershell
pytest tests/test_great_expectations.py -v
```

Verified result:

```text
2 passed
```

---

## 8. BDD Validation

Selected business-readable data quality requirements are expressed using BDD scenarios.

This allows requirements to be communicated using:

```gherkin
Given a customer dataset
When customer identifiers are validated
Then customer identifiers should be complete and unique
```

BDD is intentionally used for business-facing quality behaviour rather than every low-level technical assertion.

This keeps feature files readable while technical checks remain in pytest, dbt and Great Expectations.

---

## 9. dbt Data Pipeline

dbt is responsible for loading the sample datasets, creating transformation models and validating warehouse-level quality.

The project currently contains:

```text
2 seeds
3 models
12 data tests
```

Models include staging representations of customer and transaction data and a downstream customer transaction summary.

---

## 10. dbt Tests

dbt validates warehouse-level constraints including:

### Generic tests

- `not_null`
- `unique`
- `accepted_values`
- `relationships`

### Business-rule tests

Additional SQL-based quality rules validate conditions such as:

- transactions must not occur in the future
- completed transactions must have positive amounts

Current verified result:

```text
PASS=12
WARN=0
ERROR=0
SKIP=0
TOTAL=12
```

---

## 11. Source-to-Target Reconciliation

Reconciliation provides another layer beyond individual column checks.

The framework compares source and target information to detect problems such as:

- missing records
- unexpected additional records
- load discrepancies

This is particularly important in ETL/data pipelines because a transformation can satisfy schema rules while still losing or duplicating data.

Reconciliation logic is separated into:

```text
src/reconciliation.py
```

with automated coverage in:

```text
tests/test_reconciliation.py
```

---

## 12. Local Setup

### Prerequisites

Python 3.12 is recommended.

Create the virtual environment:

```powershell
py -3.12 -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Verify Great Expectations:

```powershell
python -c "import great_expectations as gx; print(gx.__version__)"
```

---

## 13. Running Python Tests

From the repository root:

```powershell
pytest -v
```

Expected result:

```text
14 passed
```

Individual test layers can also be executed independently.

For example:

```powershell
pytest tests/test_data_quality.py -v
```

```powershell
pytest tests/test_great_expectations.py -v
```

```powershell
pytest tests/test_reconciliation.py -v
```

---

## 14. Running dbt

Navigate to:

```powershell
cd dbt_project
```

Validate configuration:

```powershell
dbt debug
```

Load seed data:

```powershell
dbt seed
```

Create models:

```powershell
dbt run
```

Execute data-quality tests:

```powershell
dbt test
```

A combined dbt execution can also be performed with:

```powershell
dbt build
```

The local DuckDB warehouse is created under:

```text
warehouse/
```

---

## 15. Verified Test Results

The framework has been executed locally rather than provided as an untested reference implementation.

### Python

```text
14 tests collected
14 passed
```

This covers:

```text
BDD
Data Quality Validators
Great Expectations
Reconciliation
```

### dbt

```text
2 seeds
3 models
12 data tests
```

Final clean execution:

```text
PASS=12
WARN=0
ERROR=0
SKIP=0
TOTAL=12
```

---

## 16. Negative Testing

Controlled negative testing was performed to verify that the framework detects genuine quality failures rather than only demonstrating successful tests.

### Invalid customer reference

A transaction was modified to reference a customer that did not exist in the customer dataset.

The framework detected the invalid data.

At the Python/Great Expectations layer, the quality suite changed from:

```text
14 passed
```

to:

```text
13 passed
1 failed
```

After restoring the valid data:

```text
14 passed
```

### Referential integrity

A valid numeric but nonexistent customer identifier was introduced into the transaction seed.

The data successfully loaded and the dbt models executed, but the relationship test failed:

```text
relationships_stg_transactions_customer_id...
FAIL
```

This demonstrates that ingestion success does not imply data-quality success.

### Duplicate transaction

During negative testing, dbt also detected a duplicate transaction identifier through:

```text
unique_stg_transactions_transaction_id
FAIL
```

### Schema/type incompatibility

An alphanumeric customer identifier was also introduced into a column represented as numeric in the existing warehouse schema.

dbt/DuckDB rejected the record during seed loading because the incoming value could not be converted to the expected type.

This demonstrates validation at multiple boundaries:

```text
Incoming Data
     │
     ├── Schema / Type Validation
     │
     ├── Dataset Expectations
     │
     ├── Uniqueness
     │
     ├── Referential Integrity
     │
     ├── Business Rules
     │
     └── Reconciliation
```

All intentionally invalid data was removed after negative testing.

The repository remains in a clean passing state.

---

## 17. Fail-Fast Execution

An important pipeline behaviour identified during testing is that downstream commands should not execute when an upstream load fails.

For example:

```text
dbt seed
    │
    ├── PASS → dbt run → dbt test
    │
    └── FAIL → STOP
```

If `dbt seed` fails but execution continues manually, the existing warehouse may still contain data from a previous successful load.

Subsequent `dbt run` or `dbt test` commands could therefore operate against stale data.

A CI/CD implementation should consequently use fail-fast behaviour so that a failed ingestion step prevents downstream validation.

---

## 18. CI/CD Quality Gate

The framework is designed to execute automatically on repository changes.

A typical pipeline is:

```text
Developer Push / Pull Request
             │
             ▼
       Checkout Repository
             │
             ▼
         Python 3.12
             │
             ▼
      Install Dependencies
             │
        ┌────┴────┐
        ▼         ▼
      pytest    dbt seed
        │         │
        │       dbt run
        │         │
        │       dbt test
        │         │
        └────┬────┘
             ▼
        Quality Gate
          │       │
        PASS     FAIL
          │       │
          ▼       ▼
        Merge    Block
```

A quality failure should return a non-zero exit code and fail the pipeline.

This prevents invalid data-model changes or broken quality rules from silently progressing.

---

## 19. Why Multiple Testing Tools?

The tools are intentionally assigned different responsibilities.

### pytest

Acts as the core Python test runner and supports custom validation logic and assertions.

### Great Expectations

Provides reusable dataset-level expectations and expressive data-quality validation.

### dbt

Tests transformed warehouse data and relationships close to the analytical data model.

### pytest-bdd

Makes selected business-critical data quality requirements understandable using Given/When/Then scenarios.

### Reconciliation

Validates that movement between source and target has not unexpectedly changed the dataset.

The objective is not to duplicate every rule in every tool.

Instead, each mechanism is used where it provides the strongest value.

---

## 20. Design Decisions

### DuckDB

DuckDB was selected because it provides SQL and analytical database behaviour without requiring external database infrastructure.

For a foundational assignment this keeps setup reproducible while preserving realistic data-transformation patterns.

### Seed Data

Small deterministic seed datasets make the framework:

- repeatable
- easy to understand
- fast to execute
- suitable for CI/CD

Production systems would replace these with controlled connections to actual source and warehouse environments.

### Modular Validators

Validation, loading and reconciliation logic are separated so they can evolve independently.

This avoids embedding all quality logic directly inside test cases.

### Layered Validation

No single tool is treated as the entire data-quality solution.

Instead:

```text
Source Quality
      ↓
Schema Quality
      ↓
Transformation Quality
      ↓
Business Rules
      ↓
Referential Integrity
      ↓
Reconciliation
```

This provides defence in depth.

---

## 21. Production Considerations

For a production banking data platform, the framework could be extended with:

### Data-volume validation

Large datasets should use database-side aggregation and comparison rather than loading complete datasets into pandas memory.

### Incremental validation

Quality checks could run against changed partitions or processing windows rather than repeatedly scanning entire tables.

### Data observability

Metrics such as the following could be published:

- row-count variance
- null-rate trends
- duplicate-rate trends
- freshness
- schema drift
- reconciliation differences
- quality failure frequency

### Quarantine

Invalid records could be moved into a quarantine dataset rather than silently discarded.

For example:

```text
Incoming Data
      │
      ▼
Quality Validation
   │         │
 PASS       FAIL
   │         │
   ▼         ▼
Warehouse  Quarantine
              │
              ▼
        Investigation
```

### Alerting

CI/CD or production data-pipeline failures could notify engineering teams through the organisation's alerting platform.

### Historical quality results

Validation outcomes could be stored so teams can monitor quality trends rather than only seeing individual pass/fail executions.

---

## 22. Security and PII

The repository uses synthetic sample data.

A production implementation handling banking/customer data should avoid exposing sensitive information in:

- Git repositories
- CI logs
- test reports
- exception messages
- screenshots
- local development files

Credentials should be provided through secure CI/CD secrets or an approved secrets-management platform rather than committed configuration.

Production validation should also minimise unnecessary movement of customer-level data.

Where possible, quality checks should execute close to the data platform and return aggregated validation results rather than extracting sensitive datasets.

---

## 23. Further Improvements

Given additional development time, useful extensions would include:

- schema-contract validation
- automated schema-drift detection
- configurable severity levels
- warning vs blocking quality rules
- reusable Great Expectations suites
- richer validation reports
- historical quality metrics
- data freshness/SLA validation
- partition-level reconciliation
- automated anomaly detection
- containerised execution
- production warehouse adapters
- centralised quality-rule configuration

---

## 24. Summary

This framework demonstrates a layered approach to automated data quality engineering.

It validates data across:

```text
Source datasets
      ↓
Great Expectations
      ↓
Python validation
      ↓
dbt transformation
      ↓
Warehouse tests
      ↓
Business rules
      ↓
Reconciliation
      ↓
CI/CD quality gate
```

The final verified local state is:

```text
Python / pytest
14 / 14 passing

dbt
2 seeds
3 models
12 / 12 data tests passing
```

Controlled negative testing also demonstrated that the framework detects:

- invalid schema/type values
- orphan customer references
- duplicate transaction identifiers
- dataset quality violations

The framework is intentionally small enough to understand and execute locally while demonstrating patterns that can be extended to larger production data platforms.