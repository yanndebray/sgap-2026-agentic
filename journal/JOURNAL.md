# JOURNAL

## Status

| Variable | Value |
|---|---|
| Project / dataset | Southern Andes tephra geochemistry — `Volcano` classification (`data/train.csv`, `data/test.csv`) |
| Goal | Predict which volcano a tephra sample came from, evaluated on a held-out set of new samples. |
| Last experiment | 01_logistic_baseline — done |
| Last result | log-loss 0.172 (accuracy 0.952, macro recall 0.918) on test.csv |

## Data understanding

| Variable | Value |
|---|---|
| Status | done — 2026-11-02 |
| Summary | train 6,220 × 95 and test 839 × 95 tephra samples, no duplicate rows; target `Volcano` has 13 imbalanced classes (1,685 down to 77 rows). `Event`, `SampleID` and `SampleObservationID` identify the volcano on their own, and the shipped test table is split by sample (0 of 118 `SampleID` shared with train). Trace elements are missing in ~78% of rows and missingness depends on the volcano. |
| Report | [data_analysis/data_analysis.md](../data_analysis/data_analysis.md) |

## Modeling decisions

| Variable | Value |
|---|---|
| Status | locked |
| Revised on | <date or n/a> |
| Prediction goal | probabilities |
| Deployment | groups |
| Horizon | n/a |
| Gap | n/a |
| Generalize to | SampleID |
| Known at predict | oxides, trace elements, isotopes and AnalyticalTechnique; no identifiers, provenance, flags or coordinates |
| Time role | n/a |
| Metric role | proper_score |
| Metric | multi-class log-loss |
| Baseline | logistic |
| Baseline note | multinomial logistic regression on the chemistry columns |
| Folds | predefined |

## History

| Stem | Intent (one line) | Status | Headline result | Report | Design note |
|---|---|---|---|---|---|
| 01_logistic_baseline | Multinomial logistic regression on glass chemistry and analytical technique, fit on train.csv and scored on test.csv | done | log-loss 0.172 (accuracy 0.952, macro recall 0.918) on test.csv | [Open report](https://skore.probabl.ai/volcanos/tephra-volcano/estimators/92029) · hub · id: skore:report:estimator:92029 | [01_logistic_baseline.md](01_logistic_baseline.md) |

## Ideas

| Question | Status | Experiment | Source |
|---|---|---|---|
| How does the baseline do on each of the 10 volcanoes flagged as under 10% of the data, judged by log-loss and per-class counts, before accuracy? | open | 01_logistic_baseline | audit:01_logistic_baseline:checks.SKD005 |
| Does dropping redundant correlated chemistry columns change the held-out log-loss and keep it stable? | open | 01_logistic_baseline | audit:01_logistic_baseline:checks.SKD008 |
| Which chemistry features does the logistic model actually rely on, read on a scale-free importance? | open | 01_logistic_baseline | audit:01_logistic_baseline:checks.SKD006 |
| Why does an off-the-shelf HistGradientBoosting baseline score perfectly on the same test table, and is it reading columns that identify the volcano? | open | 01_logistic_baseline | audit:01_logistic_baseline:checks.SKD009 |
| Does tuning the regularization strength of the logistic regression improve held-out log-loss? | open | 01_logistic_baseline | audit:01_logistic_baseline:checks.SKD016 |
| Does separating the EMP rows (major oxides) from the LA-ICP-MS rows (trace elements), or using log-ratio features, improve the held-out log-loss? | open | 01_logistic_baseline | design:01_logistic_baseline |

## Backlog

| # | Item | Source |
|---|---|---|
