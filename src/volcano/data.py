"""Data loading and X-marker wiring.

Owns: how the raw tephra table is read from disk. The target is the
volcano that produced the sample. The loader only describes what data
exists; column choices and cleaning live in `features.py` and the graph.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

TARGET_COL = "Volcano"


def load_table(path: str | Path) -> pd.DataFrame:
    """Read one tephra table (`train.csv` or `test.csv`) with its target."""
    return pd.read_csv(path)
