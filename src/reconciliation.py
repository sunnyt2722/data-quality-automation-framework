from dataclasses import dataclass
import pandas as pd

@dataclass(frozen=True)
class ReconciliationResult:
    source_count: int
    target_count: int
    source_total: float
    target_total: float

    @property
    def passed(self) -> bool:
        return self.source_count == self.target_count and abs(self.source_total - self.target_total) < 0.01

def reconcile(source: pd.DataFrame, target: pd.DataFrame, amount_column: str) -> ReconciliationResult:
    return ReconciliationResult(
        len(source), len(target),
        float(source[amount_column].sum()), float(target[amount_column].sum())
    )
