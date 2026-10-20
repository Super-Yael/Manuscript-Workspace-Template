source("workflow/common.R")
ensure_parent("analysis/results/session-info.txt")
writeLines(c(capture.output(sessionInfo()), "", paste("Workflow seed:", project$seed),
             paste("Source MD5:", unname(tools::md5sum(project$raw)))),
           "analysis/results/session-info.txt")
