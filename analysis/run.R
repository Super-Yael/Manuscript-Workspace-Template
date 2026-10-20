source("workflow/common.R")
source("data/prepare.R")

summarize_measurements <- function(x) {
  validate_measurements(x)
  out <- do.call(rbind, lapply(project$groups, function(g) {
    y <- x$outcome[x$group == g]
    data.frame(group = g, n = length(y), mean = mean(y), sd = sd(y),
               median = median(y), min = min(y), max = max(y))
  }))
  rownames(out) <- NULL
  list(summary = out, data = x,
       note = "Synthetic teaching data; descriptive summaries only; no scientific inference.")
}

if (sys.nframe() == 0L) {
  x <- read.csv(project$prepared)
  ensure_parent(project$summary)
  saveRDS(summarize_measurements(x), project$summary, version = 3)
}
