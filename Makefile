# 所有命令从仓库根目录执行；入口不存在或为空时跳过。
SHELL := /bin/bash
.DEFAULT_GOAL := help
.DELETE_ON_ERROR:

RSCRIPT ?= Rscript
LATEXMK ?= latexmk
LATEX_MODE ?= -pdf

# 只跳过未实现的步骤；工具缺失和脚本错误必须报错。
define run_r
	@if [ -s "$(1)" ]; then \
		command -v "$(RSCRIPT)" >/dev/null || { echo 'ERROR: 找不到 $(RSCRIPT)'; exit 1; }; \
		"$(RSCRIPT)" "$(1)"; \
	else \
		echo 'SKIP: $(1) 尚未添加内容'; \
	fi
endef

.PHONY: help all data analysis figures manuscript test check bundle clean
help:
	@echo 'make all         按顺序运行已有的数据、分析、图表和论文步骤'
	@echo 'make data        可选入口 data/prepare.R'
	@echo 'make analysis    可选入口 analysis/run.R'
	@echo 'make figures     可选入口 figures/render.R'
	@echo 'make manuscript  可选入口 manuscript/export-results.R 和 main.tex'
	@echo 'make test        可选入口 analysis/test.R'
	@echo 'make check       构建后运行可选入口 analysis/check.R'
	@echo 'make bundle      校验后运行可选入口 submission/package.R'
	@echo 'make clean       仅清理约定的自动生成目录'

all: manuscript

data:
	$(call run_r,data/prepare.R)

analysis: data
	$(call run_r,analysis/run.R)

figures: analysis
	$(call run_r,figures/render.R)

manuscript: figures
	$(call run_r,manuscript/export-results.R)
	@if [ -s manuscript/main.tex ]; then \
		command -v "$(LATEXMK)" >/dev/null || { echo 'ERROR: 找不到 $(LATEXMK)'; exit 1; }; \
		mkdir -p manuscript/build; \
		"$(LATEXMK)" $(LATEX_MODE) -interaction=nonstopmode -halt-on-error -file-line-error -outdir=manuscript/build manuscript/main.tex; \
	else \
		echo 'SKIP: manuscript/main.tex 尚未添加内容'; \
	fi

test:
	$(call run_r,analysis/test.R)

check: manuscript
	$(call run_r,analysis/check.R)

bundle: check
	$(call run_r,submission/package.R)

clean:
	@for dir in data/derived analysis/results figures/generated manuscript/generated manuscript/build submission/generated; do \
		if [ -d "$$dir" ]; then rm -rf -- "$$dir"; echo "CLEAN: $$dir"; fi; \
	done
