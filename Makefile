# Public workflow interface; run from the repository root.
SHELL := /bin/bash
.DEFAULT_GOAL := help
.DELETE_ON_ERROR:
MAKEFLAGS += --no-builtin-rules --warn-undefined-variables

RSCRIPT ?= Rscript
LATEXMK ?= latexmk
R = $(RSCRIPT) --vanilla
SETTINGS = config/project.R workflow/common.R
ANALYSIS_CODE = analysis/run.R data/prepare.R $(SETTINGS)

.PHONY: help doctor data analysis figures manuscript all check test bundle clean restore snapshot
help:
	@echo 'make doctor      Check R and LaTeX tools'
	@echo 'make data        Validate and prepare source data'
	@echo 'make analysis    Calculate results and record R environment'
	@echo 'make figures     Generate the example figure'
	@echo 'make manuscript  Build manuscript/build/main.pdf'
	@echo 'make check       Build and validate the complete workflow'
	@echo 'make test        Check validation and descriptive calculations'
	@echo 'make bundle      Package PDF, sources, inputs and provenance'
	@echo 'make restore     Restore R dependencies with renv (network)'
	@echo 'make snapshot    Record dependencies declared in DESCRIPTION'
	@echo 'make clean       Remove generated files, preserve inputs and sources'

doctor:
	@command -v $(RSCRIPT) >/dev/null || { echo 'Rscript is required'; exit 1; }
	@command -v $(LATEXMK) >/dev/null || { echo 'latexmk is required'; exit 1; }
	@command -v pdflatex >/dev/null || { echo 'pdflatex is required'; exit 1; }
	@$(R) -e 'cat(R.version.string, "\n")'
	@$(LATEXMK) -v | head -4

data: data/derived/measurements.csv
data/derived/measurements.csv: data/raw/example.csv data/prepare.R $(SETTINGS) renv.lock
	$(R) data/prepare.R

analysis: analysis/results/summary.rds analysis/results/session-info.txt
analysis/results/summary.rds: data/derived/measurements.csv $(ANALYSIS_CODE)
	$(R) analysis/run.R
analysis/results/session-info.txt: analysis/results/summary.rds workflow/session.R renv.lock
	$(R) workflow/session.R

figures: figures/generated/outcome.pdf
figures/generated/outcome.pdf: analysis/results/summary.rds figures/render.R $(SETTINGS)
	$(R) figures/render.R

manuscript/generated/results.tex: analysis/results/summary.rds manuscript/export-results.R $(SETTINGS)
	$(R) manuscript/export-results.R

# latexmk tracks all TeX, BibTeX and figure inputs itself and skips unchanged work.
manuscript: figures manuscript/generated/results.tex analysis/results/session-info.txt
	mkdir -p manuscript/build
	$(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=manuscript/build manuscript/main.tex

all: manuscript
check: manuscript
	$(R) workflow/check.R
test:
	$(R) tests/test-pipeline.R
bundle: check
	$(R) submission/package.R
restore:
	$(R) workflow/environment.R restore
snapshot:
	$(R) workflow/environment.R snapshot
clean:
	$(R) workflow/clean.R
