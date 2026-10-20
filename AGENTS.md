# 项目约定

这是按功能组织的 R 数据分析与 LaTeX 论文模板。先读 README.md 和当前功能目录的 README.md，再修改相关文件。

- 按研究功能放文件。数据准备放 data/，统计方法放 analysis/，绘图放 figures/，论文与排版放 manuscript/，检索与引用放 manuscript/references/。不要新增根级 R/、python/、latex/ 软件分类目录。
- 所有流程从项目根目录运行，用 Makefile 声明输入、输出和依赖。公共设置放 config/project.R。增加输出时补充对应的构建、清理和校验规则。
- data/raw/ 的输入不覆盖修改；清洗另存 data/derived/。真实数据的来源、许可、数据字典和缺失处理必须明确。
- analysis/results/、figures/generated/、manuscript/generated/、manuscript/build/、submission/generated/ 是自动生成目录，不手工修补结果。
- 正文数字与表格通过 manuscript/export-results.R 读取分析输出生成。统计方法改变时同步修改方法部分和必要的校验。
- 示例数据完全虚构。不要把示例结论、伦理、资助、利益冲突或作者信息当作真实声明；未知事项明确留待作者填写。
- R 依赖写入 DESCRIPTION，使用 make snapshot 更新 renv.lock；不要自动给项目加入大批无关包。记录种子和 sessionInfo。
- 文献检索按 manuscript/references/README.md 使用 entrez skill；检索策略、输出格式和目录等项目规则只维护在那里，不写入通用 skill。
- 本地 skill 视为可复用工具，其 SKILL.md 不承载本项目路径和研究规则。仅在任务需要时加载对应 skill。
- 改代码后运行 make test check。修改 TeX 或图表后检查最终 PDF 的实际页面。不需要为纯文字编辑编写测试。
- 不提交密钥、真实敏感数据或受限全文。生成文件通常不提交；发布使用 submission/ 的本地打包入口，由作者决定外部分发。
