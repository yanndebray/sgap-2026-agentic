"""Learner declaration.

Owns: the function that builds and returns the (unfit) learner,
a `SkrubLearner` produced from a skrub DataOps graph that composes the
steps in `data.py` and `features.py` with the chosen estimator.
Fitting, evaluation, and persistence happen elsewhere.

The source variable is the path of one tephra table. Its `value` is only
a preview, exposed as an optional keyword so the caller can pass an
absolute path resolved from the package root.
"""

from __future__ import annotations

from pathlib import Path

import skrub
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from skrub import selectors as s

from volcano.data import TARGET_COL, load_table
from volcano.features import select_features


def build_learner(table_path_preview: str | Path | None = None):
    """Return the unfit learner for the experiment scripts to consume.

    Parameters
    ----------
    table_path_preview : str or Path or None, optional
        Preview value for the source-bound `skrub.var("table_path", ...)`
        root (an absolute path to `train.csv`). Leave as `None` for fit
        and evaluate runs: the binding passed at evaluation time wins.
    """
    table_path = (
        skrub.var("table_path", value=str(table_path_preview))
        if table_path_preview is not None
        else skrub.var("table_path")
    )
    table = table_path.skb.apply_func(load_table)
    y = table[TARGET_COL].skb.mark_as_y()
    X = table.drop(columns=[TARGET_COL]).skb.mark_as_X()
    X = X.skb.apply_func(select_features)
    X = X.skb.apply(
        SimpleImputer(strategy="median", add_indicator=True),
        cols=s.numeric(),
    )
    X = X.skb.apply(StandardScaler(), cols=s.numeric())
    X = X.skb.apply(
        OneHotEncoder(handle_unknown="ignore", sparse_output=False), cols=s.string()
    )
    predictions = X.skb.apply(LogisticRegression(max_iter=1000), y=y)
    return predictions.skb.make_learner()
