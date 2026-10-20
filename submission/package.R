source("workflow/common.R")

local({
  stage <- tempfile("manuscript-bundle-")
  dir.create(stage)
  on.exit(unlink(stage, recursive = TRUE), add = TRUE)
  base <- file.path(stage, "manuscript-bundle")
  dir.create(base)
  # Explicit allowlist. Do not distribute .env, Git history, skills or full-text caches.
  inputs <- c("README.md", "AGENTS.md", "Makefile", "DESCRIPTION", "renv.lock",
              "renv/settings.json", "config", "research", "data/README.md",
              "data/dictionary.csv", "data/raw", "data/prepare.R", "analysis/README.md",
              "analysis/run.R", "analysis/results", "figures/README.md",
              "figures/render.R", "figures/generated", "manuscript",
              "workflow", "tests", "submission/README.md", "submission/package.R")
  paths <- unique(unlist(lapply(inputs, function(p) {
    if (dir.exists(p)) list.files(p, recursive = TRUE, all.files = TRUE, full.names = TRUE, no.. = TRUE) else p
  })))
  if (file.exists("renv/activate.R")) paths <- c(paths, "renv/activate.R")
  paths <- paths[file.exists(paths) & !dir.exists(paths)]
  paths <- paths[!grepl("^manuscript/build/|^manuscript/references/(runs|fulltext)/|^workflow/preview/|/\\.gitkeep$", paths)]
  paths <- c(paths, "manuscript/build/main.pdf")
  for (p in paths) {
    target <- file.path(base, p)
    dir.create(dirname(target), recursive = TRUE, showWarnings = FALSE)
    if (!file.copy(p, target)) stop("Copy failed: ", p)
  }
  revision <- system2("git", c("rev-parse", "HEAD"), stdout = TRUE, stderr = FALSE)
  status <- system2("git", c("status", "--short", "--untracked-files=normal"), stdout = TRUE, stderr = FALSE)
  writeLines(c(paste("Created (UTC):", format(Sys.time(), tz = "UTC", usetz = TRUE)),
               paste("Base commit:", revision), "Working tree status:", status,
               "", "Contains current working files, including uncommitted changes.",
               "Rebuild: cd manuscript-bundle && make check",
               "Review actual data permissions before sharing this local bundle."),
             file.path(base, "PROVENANCE.txt"))
  checksums <- tools::md5sum(file.path(base, paths))
  write.table(data.frame(md5 = unname(checksums), path = paths),
              file.path(base, "MANIFEST.tsv"), sep = "\t", row.names = FALSE, quote = FALSE)
  archive <- file.path(getwd(), "submission/generated/manuscript-bundle.tar.gz")
  ensure_parent(archive)
  old <- setwd(stage)
  on.exit(setwd(old), add = TRUE, after = FALSE)
  utils::tar(archive, files = "manuscript-bundle", compression = "gzip", tar = "internal")
  cat("Created", archive, "\n")
})
