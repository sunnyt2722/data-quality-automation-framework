from pathlib import Path

import pandas as pd
import pytest


ROOT = Path(__file__).resolve().parents[1]
SEED_DIR = ROOT / "dbt_project" / "seeds"


@pytest.fixture
def customers():
    """Load the canonical customer dataset."""
    return pd.read_csv(SEED_DIR / "customers.csv")


@pytest.fixture
def transactions():
    """Load the canonical transaction dataset."""
    return pd.read_csv(SEED_DIR / "transactions.csv")