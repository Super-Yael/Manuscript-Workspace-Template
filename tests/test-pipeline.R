source("data/prepare.R")
source("analysis/run.R")
x <- read.csv(project$raw)
s <- summarize_measurements(x)$summary
stopifnot(identical(s$n, c(6L, 6L)), abs(s$mean[1] - 10.0166666667) < 1e-9,
          abs(s$mean[2] - 11.5333333333) < 1e-9,
          abs(s$sd[1] - 0.343025752192) < 1e-9)
expect_error <- function(y) stopifnot(inherits(try(validate_measurements(y), silent = TRUE), "try-error"))
y <- x; y$sample_id[2] <- y$sample_id[1]; expect_error(y)
y <- x; y$outcome[1] <- NA; expect_error(y)
y <- x; y$outcome[1] <- Inf; expect_error(y)
y <- x; y$group[1] <- "Typo"; expect_error(y)
y <- x; y$sample_id[1] <- " "; expect_error(y)
y <- x; y$outcome <- as.character(y$outcome); expect_error(y)
expect_error(x[x$group == "Control", ])
expect_error(x[c(1, 7:12), ])
cat("PASS: known descriptive results and invalid-input rejection.\n")
