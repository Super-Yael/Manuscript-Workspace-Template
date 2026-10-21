# 项目约定

这是空白的 R 数据分析与 LaTeX 论文模板。修改前先读 README.md 和相关功能目录的 README.md。

- 按功能组织：data/ 数据，analysis/ 统计，figures/ 图表，manuscript/ 正文，manuscript/references/ 文献，submission/ 投稿。不要按软件新建根级 R/、python/、latex/。
- 按实际需求添加文件，不为跑通模板创建演示数据、示例论文、占位脚本、空输出目录或预设分析方法。
- 从项目根目录运行。Makefile 的可选入口缺失或为空时跳过；已有代码失败时必须报错。新增真实输出时声明输入、输出及依赖。
- 原始数据按来源保存在 data/raw/，不覆盖；派生数据写 data/derived/。记录字典、来源和访问权限。
- data/derived/、analysis/results/、figures/generated/、manuscript/generated/、manuscript/build/、submission/generated/ 专用于可重建输出，不保存手工材料。
- 正文数字和表格从分析结果导出，不手工抄写。需要时添加 manuscript/export-results.R。
- 配置与代码先随功能保存，确需共享时再提取。出现外部 R 依赖时再引入 renv，记录种子与会话信息，不预装无关包。
- 文献检索、格式和输出位置只按 manuscript/references/README.md 维护。通用 skill 不承载项目目录或研究规则，按任务需要加载。
- 不编造结论、文献或作者声明。未知事项由作者补充。
- 改代码后运行 make test check；必要测试随实际功能添加。修改正文或图表后检查实际 PDF；纯文字编辑不增加测试。
- 不提交密钥、敏感数据、受限全文和生成物。投稿材料在 submission/ 按实际需要建立，外部分发由作者决定。
