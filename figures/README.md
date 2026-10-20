# 图表制作

运行 make figures。render.R 从分析结果读取数据，生成 generated/outcome.pdf，正文直接引用矢量 PDF。图中的每个点是虚构样本，横线是组均值。

统一在绘图脚本中维护颜色、尺寸、字体和标签。新图按语义命名，例如 primary-outcome.pdf；图注及正文引用放 manuscript/sections/。正文表格由 manuscript/export-results.R 生成。多图时在 Makefile 中分别声明依赖，避免修改一张图就重跑全部分析。
