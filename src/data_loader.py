from pathlib import Path
import duckdb


def load_csv_to_duckdb(csv_path: Path, table: str, db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with duckdb.connect(str(db_path)) as con:
        con.execute(f"CREATE OR REPLACE TABLE {table} AS SELECT * FROM read_csv_auto(?)", [str(csv_path)])


def query_scalar(db_path: Path, sql: str):
    with duckdb.connect(str(db_path)) as con:
        return con.execute(sql).fetchone()[0]
