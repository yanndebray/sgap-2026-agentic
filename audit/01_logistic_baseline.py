# %% [markdown]
# # Audit — 01_logistic_baseline: logistic baseline on glass chemistry
#
# Read-only review of the stored report: checks and metrics for this
# experiment.

# %%
import skore

# %% [markdown]
# ## Open the project

# %%
# Hub credentials come from the SKORE_HUB_API_KEY and SKORE_HUB_URI
# environment variables.
project = skore.Project(name="tephra-volcano", mode="hub", workspace="volcanos")
project

# %% [markdown]
# ## List the available reports

# %%
summary = project.summarize()
summary

# %% [markdown]
# ## Load the report

# %%
REPORT_ID = "skore:report:estimator:92029"

report = project.get(REPORT_ID)
report

# %% [markdown]
# ## Persisted report
#
# [Open report](https://skore.probabl.ai/volcanos/tephra-volcano/estimators/92029)
# · hub · id: skore:report:estimator:92029

# %% [markdown]
# ## Checks summary
#
# Automated checks for this report: issues and tips that affect how
# to read the metrics below.

# %%
checks = report.checks.summarize()
checks

# %% [markdown]
# ## Metrics summary
#
# Headline scores for this experiment on the shipped test table.

# %%
metrics = report.metrics.summarize().frame(verbose_name=True, flat_index=False)
metrics

# %% [markdown]
# ## Core audit complete
#
# Checks and metrics above are the first pass. Further views stay
# read-only on this same report.
