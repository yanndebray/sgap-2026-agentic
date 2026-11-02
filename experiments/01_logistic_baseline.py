# %% [markdown]
# # 01_logistic_baseline
#
# Baseline attribution of a tephra sample to one of 13 volcanoes: a
# multinomial logistic regression on glass chemistry (major oxides, trace
# elements, ratios) and the analytical technique. Numeric columns are
# median-imputed with missing-value indicators and standardized.
# Identifiers, provenance, flags and coordinates are not inputs.
#
# This cell builds the unfitted learner and writes its pipeline graph.

# %%
from volcano import PROJECT_ROOT
from volcano.pipeline import build_learner

STEM = "01_logistic_baseline"
TRAIN_PATH = PROJECT_ROOT / "data" / "train.csv"
TEST_PATH = PROJECT_ROOT / "data" / "test.csv"
RESULTS = PROJECT_ROOT / "scratch" / "results" / STEM
RESULTS.mkdir(parents=True, exist_ok=True)

# %% [markdown]
# ## Pipeline
#
# The graph loads the training table only. The shipped test table is
# bound later, and is never joined into the training frame.

# %%
learner = build_learner(table_path_preview=TRAIN_PATH)
learner.report(
    eval=False,
    open=False,
    overwrite=True,
    output_dir=RESULTS / "pipeline",
)
learner

# %% [markdown]
# ## Evaluation
#
# The learner is fitted on the training table only, then scored once on the
# shipped test table, whose `SampleID` values do not appear in training.
# The headline is multi-class log-loss.

# %%
import skore

# Hub credentials come from the SKORE_HUB_API_KEY and SKORE_HUB_URI
# environment variables.
project = skore.Project(name="tephra-volcano", mode="hub", workspace="volcanos")

# %%
# The report fits on the training table and keeps it, so a hub report has its
# train data. It scores the shipped test table.
report = skore.EstimatorReport(
    learner,
    train_data={"table_path": str(TRAIN_PATH)},
    test_data={"table_path": str(TEST_PATH)},
)
report.checks.summarize()
project.put(STEM, report)
report
