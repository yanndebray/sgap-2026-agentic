# 01_logistic_baseline

## Question / hypothesis

How well does a plain multinomial logistic regression on the glass chemistry and analytical technique attribute a tephra sample from an unseen `SampleID` to one of 13 volcanoes, measured by multi-class log-loss?

## Motivation

- **Sourcing strategy:** user
- **Source(s):**
  - Modeling decisions in the journal: baseline `logistic`, metric multi-class log-loss, deployment on unseen `SampleID`, folds `predefined` (fit on `data/train.csv`, score on `data/test.csv`).
  - `data_analysis/data_analysis.md`: test shares 0 of its 118 `SampleID` values with train, and identifier or provenance columns give the label away.
- **Why this matters:** Every later model needs a reference score on the same held-out samples. A linear model on the chemistry is the simplest honest comparison, and it shows how much the oxides and trace elements carry once identifiers, provenance and coordinates are removed.

## Method

- **Files touched:** `src/volcano/data.py`, `src/volcano/features.py`, `src/volcano/pipeline.py`, `experiments/01_logistic_baseline.py`
- **Change versus baseline (or previous experiment):** First model, so no change. Inputs are the major oxides (raw and normalized), trace elements, ratios, isotope ratios and `AnalyticalTechnique`. `Event`, `SampleID`, `SampleObservationID`, `Authors`, `DOI`, `Location`, section and measurement-run ids, flags, coordinates, `Magnitude`, `VEI` and the dating columns are dropped. Numeric columns are median-imputed with missing-value indicators and standardized, then fed to a multinomial logistic regression.
- **Cross-validation:** the scheme locked under Modeling decisions
  in the journal.
- **Out of scope for this experiment:** No hyperparameter search, no log-ratio transform, no row weighting for the rare classes, and no handling of the two instrument populations (EMP and LA-ICP-MS rows).
- **Pipeline:** <!-- results-embed: pipeline -->

## Risks / things that could invalidate the result

- The test table holds only 118 samples. Five volcanoes have 5 to 12 independent samples in train, so their per-class log-loss is noisy.
- The class mix differs between train and test (Michinmahuida has 34 test samples against 21 in train), so the score depends on which volcanoes are over-represented.
- Missing-value indicators and `AnalyticalTechnique` can reveal the instrument, which correlates with the volcano. They stay in because they are known on a new sample.
- A trace-element row has almost no major oxides and the reverse, so imputed values carry much of the signal for each population.

## Status

- **State:** approved
- **Approved by user on:** 2026-11-02
- **Headline result:** log-loss 0.172 (accuracy 0.952, macro recall 0.918) on test.csv
- **Persisted report:** [Open report](https://skore.probabl.ai/volcanos/tephra-volcano/estimators/92029) · hub · id: skore:report:estimator:92029
- **Audit findings:** 2 issue(s), 3 tip(s) — SKD005 (issue), SKD008 (issue), SKD006 (tip), SKD009 (tip), SKD016 (tip); accuracy 0.952324
- **Implication for next iteration:** The linear baseline already attributes 95% of unseen samples correctly, but the rare volcanoes are weak (Reclus precision 0.53, Monte Burney recall 0.60) and the check's gradient-boosting baseline scores perfectly, which points at identifier columns in the raw table. Next: confirm that with a stronger learner on the same clean columns, drop redundant correlated features, and consider log-ratio features.

## Results

### Report overview

The persisted report is an estimator report: the pipeline was fitted on `train.csv` and scored on the 839 rows of `test.csv`. It gives accuracy 0.952, log-loss 0.172, macro precision 0.916, macro recall 0.918 and macro ROC AUC 0.995. Fit takes under two seconds.

### Checks

Two issues and three tips were raised. Ten of the 13 volcanoes each hold under 10% of the samples (SKD005), and 857 feature pairs have a Spearman correlation above 0.9 (SKD008). A HistGradientBoosting baseline from the checks scores perfectly on the same test table (SKD009), the estimator is at its default `C` (SKD016), and coefficients are not comparable across raw feature scales (SKD006).

### Metrics

## Notebooks

### Evaluation notebook

### Audit notebook
