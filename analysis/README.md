# 分析

保存统计方法、模型诊断和敏感性分析。分析计划与研究问题保持一致，不预设检验或模型。

需要时添加 run.R，运行 make analysis。可重建结果写 results/。必要的测试放 test.R，结果校验放 check.R，分别由 make test 和 make check 调用。

外部 R 包、随机种子和环境信息随实际分析记录；需要固定环境时再引入 renv。
