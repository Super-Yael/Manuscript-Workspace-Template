# Shared settings: edit here rather than duplicating paths in scripts.
project <- list(
  seed = 20261021L,
  groups = c("Control", "Treatment"),
  raw = "data/raw/example.csv",
  prepared = "data/derived/measurements.csv",
  summary = "analysis/results/summary.rds",
  figure = "figures/generated/outcome.pdf",
  results_tex = "manuscript/generated/results.tex"
)
