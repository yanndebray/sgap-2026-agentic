"""Smoke test for `experiments/01_logistic_baseline.py`."""

import math

import pandas as pd
import pytest
from sklearn.metrics import log_loss

from volcano import PROJECT_ROOT
from volcano.data import TARGET_COL
from volcano.pipeline import build_learner

TRAIN_CSV = PROJECT_ROOT / "data" / "train.csv"
N_CLASSES = 13


@pytest.fixture
def train_predict_envs(tmp_path):
    """Fit on most real samples, predict a disjoint set of whole samples.

    Diagnostic by construction: the predict table holds only the rows to
    score, whole samples that are absent from the fit table.
    """
    table = pd.read_csv(TRAIN_CSV)
    sample_ids = sorted(table["SampleID"].unique())
    predict_ids = sample_ids[::15]
    is_predict = table["SampleID"].isin(predict_ids)
    train_csv = tmp_path / "train_slice.csv"
    predict_csv = tmp_path / "predict_slice.csv"
    table[~is_predict].to_csv(train_csv, index=False)
    table[is_predict].to_csv(predict_csv, index=False)
    n_predict_grid_rows = int(is_predict.sum())
    y_true = table.loc[is_predict, TARGET_COL].reset_index(drop=True)
    train_env = {"table_path": str(train_csv)}
    predict_env = {"table_path": str(predict_csv)}
    return train_env, predict_env, n_predict_grid_rows, y_true


def test_01_logistic_baseline(train_predict_envs):
    """One probability row per predict-grid row, with sane log-loss."""
    train_env, predict_env, n_predict_grid_rows, y_true = train_predict_envs

    learner = build_learner()
    learner.fit(train_env)
    predictions = learner.predict(predict_env)
    probabilities = learner.predict_proba(predict_env)

    # HARD: structural correctness, one label and one probability row each.
    assert len(predictions) == n_predict_grid_rows, (
        f"got {len(predictions)} predictions for "
        f"{n_predict_grid_rows} predict-grid rows"
    )
    assert len(probabilities) == n_predict_grid_rows
    assert probabilities.shape[1] == N_CLASSES, probabilities.shape

    # SOFT: the design note has no headline yet, so the comparator is the
    # uniform guess (log of the number of classes). A NaN-poisoned or
    # collapsed model would exceed it.
    classes = sorted(pd.read_csv(TRAIN_CSV)[TARGET_COL].unique())
    smoke_log_loss = log_loss(y_true, probabilities, labels=classes)
    assert smoke_log_loss < math.log(N_CLASSES), (
        f"smoke log-loss {smoke_log_loss:.3f} is not better than a "
        f"uniform guess ({math.log(N_CLASSES):.3f})"
    )
