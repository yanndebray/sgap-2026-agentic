# 01_logistic_baseline-two-populations-log-ratio
- Experiment: 01_logistic_baseline
- Source: design:01_logistic_baseline
- Triage: open
- Question: Does separating the EMP rows (major oxides) from the LA-ICP-MS rows (trace elements), or using log-ratio features, improve the held-out log-loss?
- Why now: The design note left out of scope "no log-ratio transform ... and no handling of the two instrument populations". The EDA found 4,790 EMP rows with 0.7% having `Zr` and 1,092 LA-ICP-MS rows with 0.1% having `SiO2`, and a centered log-ratio raised the volcano-explained variance for `TiO2` from 0.59 to 0.76.
- What changes: Add log-ratio features for the major oxides and the trace-element ratios, and compare a model on the full table with one that treats the two instrument populations separately.
- Open gaps: Whether a separate model per instrument generalizes to a new sample whose instrument is unknown at prediction time is not settled. The literature note on log-ratios rests on abstracts only.
