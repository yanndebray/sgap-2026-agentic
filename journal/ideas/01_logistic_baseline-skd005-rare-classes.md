# 01_logistic_baseline-skd005-rare-classes
- Experiment: 01_logistic_baseline
- Source: audit:01_logistic_baseline:checks.SKD005
- Triage: open
- Question: How does the baseline do on each of the 10 volcanoes flagged as under 10% of the data, judged by log-loss and per-class counts, before accuracy?
- Why now: Accuracy is 0.952, but Reclus has precision 0.53 and Monte Burney recall 0.60 on the test table. The digest says: "[SKD005] Underrepresented classes. Classes ['Michinmahuida', 'Llaima', 'Hudson', 'Monte Burney', 'Reclus', ...] each represent less than 10% of the dataset samples." The EDA found only 5 to 12 independent samples for five volcanoes.
- What changes: Following the recommendation on the check page: report absolute class counts (rows and samples) beside the per-class scores, read the probability-based metric (log-loss) before accuracy, precision and recall, and keep natural prevalence. Do not clear the check by resampling or class weights, since calibrated probabilities are the goal.
- Open gaps: The page suggests collecting more rare-class labels, which is not possible with the shipped tables. Whether the test class mix (34 Michinmahuida samples against 21 in train) matches the future deployment mix is unknown.
