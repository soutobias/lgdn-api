from pathlib import Path
import duckdb

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "embeddings.db"


class DuckDBService:
    """Service to manage DuckDB connection with spatial extension."""

    def __init__(self, db_path: str = DB_PATH):
        """Initialize DuckDB connection with spatial extension."""
        self.conn = duckdb.connect(db_path, read_only=True)
        # Install and load spatial extension
        self.conn.execute("INSTALL spatial;")
        self.conn.execute("LOAD spatial;")
