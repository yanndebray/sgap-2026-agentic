# 01_logistic_baseline-skd009-baseline-leakage-check
- Experiment: 01_logistic_baseline
- Source: audit:01_logistic_baseline:checks.SKD009
- Triage: open
- Question: Why does an off-the-shelf HistGradientBoosting baseline score perfectly on the same test table, and is it reading columns that identify the volcano?
- Why now: The digest says: "[SKD009] ... Your model is on par with or better than a HistGradientBoosting baseline. Baseline performance on the test set, for reference: Accuracy=1, ... Log loss=1.17e-06". The check page says the baseline is trained on the same train data as the report's estimator. The EDA found `Event`, `SampleID`, `SampleObservationID` map to a single volcano in 100% of train rows, and all 30 `Event` values appear in both tables.
- What changes: Fit a gradient-boosted model on the same chemistry and technique columns as this baseline (no identifiers, provenance or coordinates) and compare it with this run, to see how much a stronger learner gains once the leak columns are out. A near-perfect score on the raw table would be consistent with identifier columns being read, but this is not verified.
- Open gaps: What the check's baseline had as inputs (the raw table with identifier columns, or the selected columns) is an assumption. Whether a gradient-boosted model on clean columns also gets near zero log-loss is unknown.
