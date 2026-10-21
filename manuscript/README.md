# 论文

保存研究思路、正文与排版。开始写作时先明确研究问题、分析计划及证据边界，重要变更记录在这里；文件随实际需要建立。

- main.tex：有正文后建立的编译入口；章节和排版文件按文章需要拆分。
- references/：检索与引用约定，按实际章节存放 README 检索式和每论点的 .bib；references/reference.bib 由 make bibliography 按正文引用自动构建，不手工合并。
- export-results.R：需要向正文提供统计数字或表格时添加，读取分析输出，写入 generated/。
- build/：LaTeX 自动编译目录，由 Makefile 创建。

运行 make manuscript。没有 main.tex 时跳过；默认使用 pdflatex，需要 XeLaTeX 时运行 make manuscript LATEX_MODE=-xelatex。编译从仓库根目录执行，TeX 中的项目路径据此填写。
