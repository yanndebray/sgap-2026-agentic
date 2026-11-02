# JOURNAL

## Status

| Variable | Value |
|---|---|
| Project / dataset | Southern Andes tephra geochemistry — `Volcano` classification (`data/train.csv`, `data/test.csv`) |
| Goal | Predict which volcano a tephra sample came from, evaluated on a held-out set of new samples. |
| Last experiment | <NN_name> — <status: planned \| approved \| running \| done \| abandoned> |
| Last result | <one-line headline metric, or "n/a" if not yet run> |

## Data understanding

| Variable | Value |
|---|---|
| Status | done — 2026-11-02 |
| Summary | train 6,220 × 95 and test 839 × 95 tephra samples, no duplicate rows; target `Volcano` has 13 imbalanced classes (1,685 down to 77 rows). `Event`, `SampleID` and `SampleObservationID` identify the volcano on their own, and the shipped test table is split by sample (0 of 118 `SampleID` shared with train). Trace elements are missing in ~78% of rows and missingness depends on the volcano. |
| Report | [data_analysis/data_analysis.md](../data_analysis/data_analysis.md) |

## Modeling decisions

| Variable | Value |
|---|---|
| Status | <missing \| draft \| locked> |
| Revised on | <date or n/a> |
| Prediction goal | <probabilities \| point_labels \| intervals \| point_predictions> |
| Deployment | <iid \| time \| groups> |
| Horizon | <n/a, or one or more number-and-unit values> |
| Gap | <n/a or number and unit> |
| Generalize to | <n/a or column> |
| Known at predict | <n/a or columns> |
| Time role | <n/a \| sort_key \| covariate> |
| Metric role | <imposed \| proper_score \| ranking \| thresholded \| point_error> |
| Metric | <comparison name> |
| Baseline | <one of seasonal_naive, group_mean, logistic, production, dummy> |
| Baseline note | <one short phrase> |
| Folds | <integer at least 1, or predefined> |

## History

| Stem | Intent (one line) | Status | Headline result | Report | Design note |
|---|---|---|---|---|---|

## Ideas

| Question | Status | Experiment | Source |
|---|---|---|---|

## Backlog

| # | Item | Source |
|---|---|---|
