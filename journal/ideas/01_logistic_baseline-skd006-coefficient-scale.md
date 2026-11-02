# 01_logistic_baseline-skd006-coefficient-scale
- Experiment: 01_logistic_baseline
- Source: audit:01_logistic_baseline:checks.SKD006
- Triage: open
- Question: Which chemistry features does the logistic model actually rely on, read on a scale-free importance?
- Why now: The digest says: "[SKD006] Coefficient interpretation. Features are not on the same scale: coefficient magnitudes are not directly comparable as feature importance." The check measures the raw inputs, while the model standardizes numeric columns inside the pipeline.
- What changes: Following the check page: read coefficients on the standardized scale only, or use a scale-free importance such as permutation importance on the test table, and list the most influential oxides and trace elements per volcano.
- Open gaps: The SKD012 permutation-importance check failed to compute on this report, so a separate permutation view may need a different configuration. How the missing-value indicators should be grouped in a ranking is not settled.
