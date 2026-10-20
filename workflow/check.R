source("workflow/common.R")
source("data/prepare.R")
source("analysis/run.R")
x <- read.csv(project$prepared)
a <- readRDS(project$summary)
stopifnot(isTRUE(all.equal(a, summarize_measurements(x))))
required <- c(project$figure, project$results_tex, "manuscript/build/main.pdf",
              "analysis/results/session-info.txt")
stopifnot(all(file.exists(required)), all(file.info(required)$size > 0))
log <- readLines("manuscript/build/main.log", warn = FALSE)
if (any(grepl("undefined references|undefined citations|Citation .* undefined|Overfull", log))) {
  stop("Unresolved references/citations or layout overflow in LaTeX log.")
}
cat("PASS: input, recomputed summaries, figure/table, PDF and LaTeX log.\n")
