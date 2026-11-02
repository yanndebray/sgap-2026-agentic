# 01_logistic_baseline-skd016-tune-c
- Experiment: 01_logistic_baseline
- Source: audit:01_logistic_baseline:checks.SKD016
- Triage: open
- Question: Does tuning the regularization strength of the logistic regression improve held-out log-loss?
- Why now: The digest says: "[SKD016] Estimator not tuned. Estimator(s) left at default settings; consider tuning: ['C'] for LogisticRegression."
- What changes: Search the inverse regularization strength `C` of the logistic regression with the group-aware validation that the design locked, then evaluate the best value once on the test table.
- Open gaps: The locked fold choice is `predefined`, so how to validate a search on the training table without concatenating test (grouping by `SampleID`) is not decided. The page gives no range for `C`.
