# Delete generated content only; preserve inputs, sources and environments.
dirs <- c("data/derived", "analysis/results", "figures/generated", "manuscript/generated",
          "manuscript/build", "submission/generated", "workflow/preview")
for (d in dirs) {
  paths <- list.files(d, all.files = TRUE, full.names = TRUE, no.. = TRUE)
  paths <- paths[basename(paths) != ".gitkeep"]
  if (length(paths)) unlink(paths, recursive = TRUE)
}
cat("Generated files removed.\n")
