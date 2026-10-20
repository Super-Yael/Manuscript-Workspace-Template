source("workflow/common.R")

validate_measurements <- function(x) {
  if (!identical(names(x), c("sample_id", "group", "outcome"))) stop("Expected columns: sample_id, group, outcome.")
  if (!nrow(x) || anyNA(x)) stop("Input is empty or has missing values.")
  if (any(!nzchar(trimws(x$sample_id))) || anyDuplicated(x$sample_id)) stop("Sample IDs must be non-empty and unique.")
  if (!is.numeric(x$outcome) || any(!is.finite(x$outcome))) stop("Outcome must contain finite numeric values.")
  if (!setequal(unique(x$group), project$groups)) stop("Unexpected or missing groups.")
  if (any(table(factor(x$group, levels = project$groups)) < 2L)) stop("Each group needs at least two observations.")
  invisible(x)
}

prepare_data <- function(input, output) {
  x <- read.csv(input, check.names = FALSE, na.strings = c("", "NA"))
  validate_measurements(x)
  x <- x[order(match(x$group, project$groups), x$sample_id), ]
  ensure_parent(output)
  write.csv(x, output, row.names = FALSE)
  invisible(x)
}

if (sys.nframe() == 0L) prepare_data(project$raw, project$prepared)
