# 正文与排版

运行 make manuscript，最终 PDF 位于 build/main.pdf。

- main.tex：主文档与章节顺序。
- preamble.tex：公共排版设置；适配目标期刊时在这里及文档类中调整。
- sections/：引言、方法、结果、讨论与声明，按内容拆分。
- export-results.R：从分析结果生成数字宏和表格；controlled labels 以外的输入需要转义 TeX 特殊字符。
- generated/：自动生成的 results.tex，不能直接编辑。
- build/：latexmk 管理的 PDF、参考文献和辅助文件，清理后可重建。

默认 pdflatex + BibTeX + natbib，示例正文为英文。中文稿件需要改用支持中文的文档类（如 ctexart）与 XeLaTeX，并把 Makefile 中的 latexmk -pdf 改为 -xelatex；根据实际系统选择字体。

替换期刊模板时保留分析输出接口。所有引用键集中在 manuscript/references/library.bib。正文已有 ControlN、TreatmentN、ControlMean、TreatmentMean 与 SummaryTable 等宏，数字改变会随分析自动更新。
