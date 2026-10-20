# 统计分析

运行 make analysis。run.R 读取整理数据，输出 results/summary.rds；session-info.txt 记录 R、平台、已加载包、随机种子和原始输入 MD5。

示例只计算各组样本量、均值、样本标准差、中位数及范围，不做假设检验。summary.rds 同时保存示例观测值供绘图使用。原始编号按独立样本解释，不能直接套用于配对或重复测量设计。

新研究将建模、诊断和敏感性分析按实际问题拆成此目录内的脚本；在 Makefile 中声明各结果依赖。图形风格放 figures/，论文表格和文字数字的 TeX 导出放 manuscript/，不在分析里拼接正文。
