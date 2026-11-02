# %% [markdown]
# # Exploratory data analysis: Southern Andes tephra geochemistry
#
# Overview of `data/train.csv` and `data/test.csv` before choosing a
# learner and a splitter. The goal is to tell which volcano an ash
# (tephra) sample came from. TableReport owns dtypes, missingness,
# univariate distributions, cardinality, and top pairwise associations,
# so they are not re-plotted here.

# %%
import pandas as pd
import seaborn as sns
import skrub

from volcano import PROJECT_ROOT

OUT = PROJECT_ROOT / "data_analysis"
OUT.mkdir(parents=True, exist_ok=True)

TARGET = "Volcano"
RAW = pd.read_csv(PROJECT_ROOT / "data" / "train.csv")
FRAME = RAW
RAW

# %% [markdown]
# ## Table overview: train
#
# Column types, missingness, cardinality, and pairwise associations
# for the training table.

# %%
report = skrub.TableReport(RAW, title="train", verbose=0)
report.write_html(OUT / "data_analysis_train.html")
report

# %% [markdown]
# ## Duplicate rows: train
#
# Exact duplicates inflate counts and can leak across a later split.
# Cleaning belongs in the pipeline, not by dropping rows here.

# %%
n_dup = int(FRAME.duplicated().sum())
duplicate_summary = pd.DataFrame(
    {
        "n_rows": [len(FRAME)],
        "n_duplicate_rows": [n_dup],
        "duplicate_rate": [n_dup / len(FRAME) if len(FRAME) else 0.0],
    }
)
duplicate_summary

# %% [markdown]
# ## Target distribution
#
# Class counts of the volcano that produced each sample.

# %%
y = FRAME[TARGET]
counts = y.value_counts(dropna=False)
target_summary = counts.rename("count").to_frame()
target_summary["rate"] = target_summary["count"] / target_summary["count"].sum()
target_summary

# %%
plot_df = target_summary.reset_index(names=TARGET)
g = sns.catplot(data=plot_df, y=TARGET, x="count", kind="bar", height=5, aspect=1.6)
g.savefig(OUT / "target_distribution.png", bbox_inches="tight")
g

# %% [markdown]
# ## Feature vs target
#
# The twelve numeric columns with the fewest missing values, split
# by volcano. Not every pairwise plot.

# %%
BIVARIATE_CAP = 12
numeric_cols = [c for c in FRAME.select_dtypes("number").columns if c != TARGET]
bivariate_cols = (
    FRAME[numeric_cols].isna().mean().sort_values().index[:BIVARIATE_CAP].tolist()
)
pd.Series(bivariate_cols, name="bivariate_columns")

# %%
long = FRAME.melt(
    id_vars=[TARGET],
    value_vars=bivariate_cols,
    var_name="feature",
    value_name="value",
)
g = sns.catplot(
    data=long,
    y=TARGET,
    x="value",
    col="feature",
    col_wrap=4,
    kind="box",
    sharex=False,
    height=3.2,
    aspect=1.1,
)
g.savefig(OUT / "bivariate_grid.png", bbox_inches="tight")
g

# %% [markdown]
# ## Leakage candidates
#
# Flags only, not a train/test split. A text column whose every value
# appears under a single volcano identifies the class by itself.

# %%
leakage_flags: list[str] = []
for col in FRAME.columns:
    if col == TARGET:
        continue
    rates = FRAME.groupby(y, dropna=False)[col].apply(lambda s: s.isna().mean())
    if rates.max() - rates.min() >= 0.5:
        leakage_flags.append(f"{col} null rate differs by class")
leakage_summary = pd.DataFrame({"flag": leakage_flags or ["none"]})
leakage_summary

# %%
text_cols = [
    c
    for c in FRAME.columns
    if c != TARGET and not pd.api.types.is_numeric_dtype(FRAME[c])
]
purity_rows = []
for col in text_cols:
    n_classes = FRAME.groupby(col)[TARGET].nunique()
    purity_rows.append(
        {
            "column": col,
            "n_values": int(FRAME[col].nunique()),
            "missing_rate": float(FRAME[col].isna().mean()),
            "share_rows_single_volcano": float((FRAME[col].map(n_classes) == 1).mean()),
        }
    )
purity_summary = (
    pd.DataFrame(purity_rows)
    .sort_values("share_rows_single_volcano", ascending=False)
    .head(8)
    .reset_index(drop=True)
)
purity_summary

# %% [markdown]
# ## Table overview: test
#
# The test table that shipped with the data. It is profiled on its own
# and is not concatenated with train.

# %%
RAW_test = pd.read_csv(PROJECT_ROOT / "data" / "test.csv")
FRAME_test = RAW_test
RAW_test

# %%
report_test = skrub.TableReport(RAW_test, title="test", verbose=0)
report_test.write_html(OUT / "data_analysis_test.html")
report_test

# %% [markdown]
# ## Duplicate rows: test
#
# Cleaning belongs in the pipeline, not by dropping rows here.

# %%
n_dup_test = int(FRAME_test.duplicated().sum())
duplicate_summary_test = pd.DataFrame(
    {
        "n_rows": [len(FRAME_test)],
        "n_duplicate_rows": [n_dup_test],
        "duplicate_rate": [n_dup_test / len(FRAME_test) if len(FRAME_test) else 0.0],
    }
)
duplicate_summary_test

# %% [markdown]
# ## Train versus test overlap
#
# Do the same samples (or the same volcanoes) appear on both sides?

# %%
overlap = pd.DataFrame(
    {
        "column": ["SampleID", "Event", "Volcano"],
        "n_values_test": [
            int(FRAME_test[c].nunique()) for c in ["SampleID", "Event", "Volcano"]
        ],
        "n_values_shared_with_train": [
            len(set(FRAME_test[c]) & set(FRAME[c]))
            for c in ["SampleID", "Event", "Volcano"]
        ],
    }
)
overlap

# %% [markdown]
# ## Join keys / coverage
#
# Shared keys and coverage between train and test, a diagnostic and not a
# modelling table.

# %%
left = FRAME
right = FRAME_test
shared = sorted(left.columns.intersection(right.columns))
join_key_summary = pd.DataFrame(
    {
        "column": shared,
        "left_nunique": [int(left[c].nunique(dropna=False)) for c in shared],
        "right_nunique": [int(right[c].nunique(dropna=False)) for c in shared],
    }
)
join_key_summary.sort_values("left_nunique", ascending=False).head(10)

# %%
KEY = "SampleID"
left_set = set(left[KEY].dropna().tolist())
right_set = set(right[KEY].dropna().tolist())
join_coverage = pd.DataFrame(
    {
        "metric": [
            "train_rows",
            "test_rows",
            "train_only_keys",
            "test_only_keys",
            "shared_keys",
        ],
        "value": [
            len(left),
            len(right),
            len(left_set - right_set),
            len(right_set - left_set),
            len(left_set & right_set),
        ],
    }
)
join_coverage

# %% [markdown]
# ## Multivariate interactions
#
# Pairwise views of the six most complete normalized oxides, colored by
# volcano. Rows with a missing oxide are left out of this plot only.

# %%
PAIR_COLS = [
    "SiO2_normalized",
    "K2O_normalized",
    "FeOT_normalized",
    "CaO_normalized",
    "MgO_normalized",
    "TiO2_normalized",
]
pair_df = FRAME[[TARGET, *PAIR_COLS]].dropna()
pair_df.shape

# %%
g = sns.pairplot(
    pair_df,
    hue=TARGET,
    vars=PAIR_COLS,
    corner=True,
    height=2.0,
    plot_kws={"s": 8, "alpha": 0.5},
)
g.savefig(OUT / "interactions.png", bbox_inches="tight")
g

# %% [markdown]
# ## 2D projection (PCA)
#
# Major-oxide columns (at most 25% missing, coordinates excluded),
# median-imputed and standardized for the plot only. No imputed table is
# written and PCA is not used as a preprocessor here.

# %%
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

pca_cols = [
    c
    for c in FRAME.select_dtypes("number").columns
    if c not in {"Latitude", "Longitude", "Magnitude", "VEI"}
    and FRAME[c].isna().mean() <= 0.25
]
pca_num = FRAME[pca_cols]
pca_input = StandardScaler().fit_transform(pca_num.fillna(pca_num.median()))
pca = PCA(n_components=2, random_state=0)
coords = pca.fit_transform(pca_input)
pca_df = pd.DataFrame(coords, columns=["PC1", "PC2"])
pca_df[TARGET] = FRAME[TARGET].to_numpy()
pca_variance = pd.DataFrame(
    {
        "component": ["PC1", "PC2"],
        "explained_variance_ratio": pca.explained_variance_ratio_,
        "n_columns": len(pca_cols),
    }
)
pca_variance

# %%
g = sns.relplot(
    data=pca_df, x="PC1", y="PC2", hue=TARGET, s=10, alpha=0.6, height=6, aspect=1.3
)
g.savefig(OUT / "pca.png", bbox_inches="tight")
g

# %% [markdown]
# ## Hypothesis tests
#
# Kruskal-Wallis for each numeric feature across volcanoes, chi-square for
# each text column with at most 60 values. Read the p-values as a signal,
# not as a modelling decision. With 6,220 rows nearly everything is
# significant, so the statistic is the more useful column.

# %%
from scipy import stats

test_rows = []
for col in FRAME.select_dtypes("number").columns:
    groups = [
        g_[col].dropna().to_numpy()
        for _, g_ in FRAME.groupby(TARGET)
        if g_[col].notna().sum() >= 2
    ]
    if len(groups) >= 2:
        res = stats.kruskal(*groups)
        test_rows.append(
            {
                "feature": col,
                "test": "kruskal",
                "statistic": float(res.statistic),
                "p_value": float(res.pvalue),
                "n_groups": len(groups),
            }
        )
for col in text_cols:
    if FRAME[col].nunique() <= 60 and FRAME[col].notna().sum() > 0:
        table = pd.crosstab(FRAME[col].fillna("<missing>"), FRAME[TARGET])
        chi2, p_value, _, _ = stats.chi2_contingency(table)
        test_rows.append(
            {
                "feature": col,
                "test": "chi2",
                "statistic": float(chi2),
                "p_value": float(p_value),
                "n_groups": int(table.shape[0]),
            }
        )
hypothesis_tests = (
    pd.DataFrame(test_rows)
    .sort_values("statistic", ascending=False)
    .reset_index(drop=True)
)
hypothesis_tests.head(15)

# %% [markdown]
# ## Geo check
#
# Coordinate ranges per volcano. Out-of-range means a latitude beyond
# +/-90 or a longitude beyond +/-180.

# %%
geo_summary = FRAME.groupby(TARGET).agg(
    lat_min=("Latitude", "min"),
    lat_max=("Latitude", "max"),
    lon_min=("Longitude", "min"),
    lon_max=("Longitude", "max"),
    n_missing_coords=("Latitude", lambda s: int(s.isna().sum())),
)
geo_summary["lat_span"] = geo_summary["lat_max"] - geo_summary["lat_min"]
geo_summary["lon_span"] = geo_summary["lon_max"] - geo_summary["lon_min"]
n_out_of_range = int(
    ((FRAME["Latitude"].abs() > 90) | (FRAME["Longitude"].abs() > 180)).sum()
)
geo_summary.assign(n_out_of_range_all=n_out_of_range).round(2)

# %% [markdown]
# ## Subgroup: publication (`Authors`)
#
# Which volcanoes each publication covers, and how many rows. A
# publication that covers a single volcano ties the label to its source.

# %%
subgroup_authors = FRAME.groupby("Authors").agg(
    n_rows=(TARGET, "size"),
    n_volcanoes=(TARGET, "nunique"),
    top_volcano=(TARGET, lambda s: s.value_counts().index[0]),
    top_volcano_share=(TARGET, lambda s: s.value_counts(normalize=True).iloc[0]),
)
subgroup_authors.sort_values("n_rows", ascending=False).round(2)

# %% [markdown]
# ## Text columns
#
# Length and empty-string rate of the free-text columns that are not
# identifiers.

# %%
TEXT_PROFILE_COLS = ["Comments", "Location", "FlagDescription", "DepositColor"]
text_rows = []
for col in TEXT_PROFILE_COLS:
    values = FRAME[col].dropna().astype(str)
    text_rows.append(
        {
            "column": col,
            "missing_rate": float(FRAME[col].isna().mean()),
            "empty_string_rate": float((values.str.strip() == "").mean()),
            "length_median": float(values.str.len().median()),
            "length_max": int(values.str.len().max()),
            "n_values": int(values.nunique()),
        }
    )
text_profile = pd.DataFrame(text_rows)
text_profile

# %% [markdown]
# ## Oxide totals by volcano and technique
#
# `Total` is the sum of the major oxides before normalization. A total far
# from 100 flags a poor analysis, and a shift between techniques flags an
# instrument offset.

# %%
total_by_volcano = FRAME.groupby(TARGET)["Total"].agg(
    ["count", "mean", "std", "min", "max"]
)
total_by_volcano.round(2)

# %%
total_by_technique = (
    FRAME.groupby("AnalyticalTechnique")["Total"]
    .agg(["count", "mean", "std", "min", "max"])
    .sort_values("count", ascending=False)
)
total_by_technique.round(2)

# %% [markdown]
# ## Instrument versus missingness and class
#
# For each analytical technique: how many rows, how many volcanoes, how
# often major oxides and trace elements are present, and how dominant the
# top volcano is.

# %%
instrument_summary = FRAME.groupby("AnalyticalTechnique").agg(
    n_rows=(TARGET, "size"),
    n_volcanoes=(TARGET, "nunique"),
    top_volcano=(TARGET, lambda s: s.value_counts().index[0]),
    top_volcano_share=(TARGET, lambda s: s.value_counts(normalize=True).iloc[0]),
    share_with_SiO2=("SiO2", lambda s: s.notna().mean()),
    share_with_Zr=("Zr", lambda s: s.notna().mean()),
)
instrument_summary.sort_values("n_rows", ascending=False).round(2)

# %% [markdown]
# ## Within- versus between-sample variance
#
# Share of the total variance of each oxide that remains inside a single
# `SampleID` (repeated analyses of one sample), versus the share explained
# by the volcano. A small within-sample share means rows of one sample are
# near copies, so a random row split would leak.

# %%
VARIANCE_COLS = [*PAIR_COLS, "Zr", "Nb", "Ba"]


def variance_shares(frame, col):
    sub = frame[[TARGET, "SampleID", col]].dropna()
    total = float(((sub[col] - sub[col].mean()) ** 2).sum())
    within_sample = float(
        ((sub[col] - sub.groupby("SampleID")[col].transform("mean")) ** 2).sum()
    )
    within_volcano = float(
        ((sub[col] - sub.groupby(TARGET)[col].transform("mean")) ** 2).sum()
    )
    return {
        "column": col,
        "n_rows": int(len(sub)),
        "within_sample_share": within_sample / total,
        "between_volcano_share": 1 - within_volcano / total,
    }


variance_summary = pd.DataFrame([variance_shares(FRAME, c) for c in VARIANCE_COLS])
variance_summary.round(3)

# %% [markdown]
# ## Independent samples per volcano
#
# Rows are repeated analyses, so the number of distinct samples and events
# is the effective sample size of each class.

# %%
samples_per_volcano = FRAME.groupby(TARGET).agg(
    n_rows=("SampleID", "size"),
    n_samples=("SampleID", "nunique"),
    n_events=("Event", "nunique"),
)
samples_per_volcano["rows_per_sample"] = (
    samples_per_volcano["n_rows"] / samples_per_volcano["n_samples"]
)
samples_per_volcano["n_samples_test"] = (
    FRAME_test.groupby(TARGET)["SampleID"].nunique().reindex(samples_per_volcano.index)
)
samples_per_volcano.sort_values("n_samples").round(1)

# %% [markdown]
# ## Log-ratio versus raw separation
#
# Share of variance explained by the volcano (eta squared) for the raw
# normalized oxides and for their centered log-ratio, on rows where the
# eight normalized oxides are all present and positive. Ratios of trace
# elements are compared to their logarithm.

# %%
import numpy as np

CLR_PARTS = [
    "SiO2_normalized",
    "TiO2_normalized",
    "Al2O3_normalized",
    "FeOT_normalized",
    "CaO_normalized",
    "MgO_normalized",
    "K2O_normalized",
    "Na2O_normalized",
]
parts = FRAME[[TARGET, *CLR_PARTS]].dropna()
parts = parts[(parts[CLR_PARTS] > 0).all(axis=1)]
logs = np.log(parts[CLR_PARTS])
clr = logs.sub(logs.mean(axis=1), axis=0)


def eta_squared(values, labels):
    values = pd.Series(values.to_numpy())
    labels = pd.Series(labels.to_numpy())
    total = float(((values - values.mean()) ** 2).sum())
    resid = float(((values - values.groupby(labels).transform("mean")) ** 2).sum())
    return 1 - resid / total


rows = []
for col in CLR_PARTS:
    rows.append(
        {
            "feature": col,
            "eta2_raw": eta_squared(parts[col], parts[TARGET]),
            "eta2_clr": eta_squared(clr[col], parts[TARGET]),
            "n_rows": int(len(parts)),
        }
    )
for col in ["Zr_Nb", "La_Yb"]:
    sub = FRAME[[TARGET, col]].dropna()
    sub = sub[sub[col] > 0]
    rows.append(
        {
            "feature": col,
            "eta2_raw": eta_squared(sub[col], sub[TARGET]),
            "eta2_clr": eta_squared(np.log(sub[col]), sub[TARGET]),
            "n_rows": int(len(sub)),
        }
    )
logratio_summary = pd.DataFrame(rows)
logratio_summary.round(3)
