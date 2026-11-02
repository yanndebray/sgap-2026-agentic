# 01_logistic_baseline-skd008-correlated-features
- Experiment: 01_logistic_baseline
- Source: audit:01_logistic_baseline:checks.SKD008
- Triage: open
- Question: Does dropping redundant correlated chemistry columns change the held-out log-loss and keep it stable?
- Why now: The digest says: "[SKD008] Highly correlated input features. 857 pair(s) of features have a Spearman correlation above 0.9." The model keeps both the raw oxides and their normalized copies, plus about 28 trace elements that are missing together.
- What changes: Following the check page's recommendation: drop redundant features (for example keep only normalized oxides, or one element from each strongly correlated trace-element group) and compare log-loss and per-class recall with this run.
- Open gaps: Which of each correlated pair carries the better-quality value for a new sample is a domain question. The check page says dropping may also improve performance but does not promise it.
