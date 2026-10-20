args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 1L || !args %in% c("restore", "snapshot")) stop("Use restore or snapshot.")
if (!requireNamespace("renv", quietly = TRUE)) install.packages("renv", repos = "https://cloud.r-project.org")
if (args == "restore") {
  renv::restore(project = ".", prompt = FALSE)
} else {
  renv::snapshot(project = ".", type = "explicit", prompt = FALSE)
}
if (!file.exists("renv/activate.R")) renv::activate(project = ".")
