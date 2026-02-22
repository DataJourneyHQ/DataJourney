import intake
from pathlib import Path
from analytics_framework import INTAKE_LOC

_catalog_path = INTAKE_LOC / "catalog_entry.yml"
_catalog = intake.open_catalog(str(_catalog_path))


def list_catalog_entries() -> str:
    """Return all dataset names registered in the intake catalog."""
    entries = list(_catalog)
    return "📦 Available datasets:\n" + "\n".join(f"  • {e}" for e in entries)


def load_dataset(entry_name: str, n_rows: int = 500) -> tuple:
    """
    Load a dataset from the intake catalog.

    Args:
        entry_name: Name of the catalog entry (e.g. 'twilio_stock_price').
        n_rows: Maximum number of rows to load.

    Returns:
        A (DataFrame, error_string) tuple. On success error_string is empty.
    """
    if entry_name not in list(_catalog):
        return None, f"❌ '{entry_name}' not found. Run list_catalog_entries() to see options."
    try:
        df = _catalog[entry_name].read()
        return df.head(n_rows), ""
    except Exception as e:
        return None, f"❌ Failed to load '{entry_name}': {e}"


def profile_dataset(entry_name: str) -> str:
    """
    Return a human-readable profile of a catalog dataset.

    Includes shape, column names, dtypes and basic statistics.

    Args:
        entry_name: Name of the catalog entry.

    Returns:
        Formatted profile string.
    """
    df, err = load_dataset(entry_name)
    if err:
        return err

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    text_cols = df.select_dtypes(include="object").columns.tolist()

    lines = [
        f"📊 Profile: {entry_name}",
        f"  Shape      : {df.shape[0]} rows × {df.shape[1]} columns",
        f"  Numeric    : {numeric_cols}",
        f"  Text/Object: {text_cols}",
        f"  Nulls      : {df.isnull().sum().to_dict()}",
        f"\nStatistics:\n{df.describe(include='all').to_string()}",
    ]
    return "\n".join(lines)
