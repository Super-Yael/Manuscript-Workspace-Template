# Manuscript Workspace Template

按研究功能组织的 **R 数据分析 + LaTeX 论文初始仓库**。新文章复用目录、数据校验、分析入口、图表接口、引用管理和编译打包流程，把精力留给研究问题与证据。

自带完整教学流程：12 条虚构数据 → 数据整理 → 描述统计 → 矢量图和结果表 → 自动插入正文数字 → PDF → 本地复现包。示例不含真实研究结论。

## 按功能组织

| 目录 | 功能 | 源文件 | 自动生成位置 |
| --- | --- | --- | --- |
| research/ | 研究问题、方案与决策 | question.md、decisions.md | — |
| manuscript/references/ | 检索、筛选和引用 | README.md、queries/、library.bib | runs/，每次检索独立保存 |
| data/ | 获取、字典与整理 | raw/、dictionary.csv、prepare.R | derived/ |
| analysis/ | 统计分析与诊断 | run.R，后续按问题增加脚本 | results/ |
| figures/ | 图表设计与导出 | render.R | generated/ |
| manuscript/ | 正文、结果表与排版 | main.tex、sections/、preamble.tex、export-results.R | generated/、build/ |
| submission/ | 投稿材料与复现归档 | package.R，后续增加封面信等 | generated/ |
| config/ | 跨步骤公共参数 | project.R | — |
| workflow/ | 环境、校验与清理 | common.R、environment.R、check.R 等 | preview/（页面检查用） |
| tests/ | 关键逻辑校验 | test-pipeline.R | — |
| .agents/skills/ | 项目可用的通用技能 | entrez 与 Nature Skills | — |

代码跟随它服务的功能，例如 data/prepare.R 和 manuscript/export-results.R；不设根级 R/、latex/ 等软件分类目录。

## 首次运行

需要 R（示例验证版本为 4.6.1）、GNU Make、Bash 和含 latexmk、pdflatex、BibTeX 的 TeX 环境。示例仅使用 R 自带包；LaTeX 使用 geometry、lmodern、graphicx、booktabs、natbib、hyperref 和 microtype。macOS 可使用已有的 MacTeX，Linux 可使用 TeX Live。所有命令在仓库根目录执行：

```sh
make doctor
make test check
```

打开 manuscript/build/main.pdf 查看示例。单独输入 make 显示命令说明。

```sh
make data          # 校验并整理数据
make analysis      # 统计结果和 R 会话信息
make figures       # 矢量图
make manuscript    # 论文 PDF
make bundle        # 校验后打包到 submission/generated/
make clean         # 清空生成内容，保留输入、代码和正文
```

Makefile 跟踪输入、代码和输出；上游变化触发相应下游步骤，删除输出后也会重建。LaTeX 内部依赖由 latexmk 跟踪，只有正文变更时不必重跑 R。已有结果不变时跳过重复编译。

## 用于下一篇文章

1. 将本仓库作为模板建立独立新仓库，或复制工作文件并排除 .git、生成目录、renv/library/ 和本地数据缓存。不要让新论文沿用模板仓库的远程地址。
2. 填写 research/question.md，明确观察单位、主要结局、分析计划和主张边界；在 decisions.md 记录重要变更。
3. 替换 data/raw/example.csv 和数据字典，修改 data/prepare.R 校验。更换路径时同时更新 config/project.R 和 Makefile 的文件依赖。
4. 在 analysis/ 实现实际方法，在 figures/ 制作图表，通过 manuscript/export-results.R 输出结果表与正文数字，避免手工抄写。
5. 替换正文、作者及声明。适配期刊文档类与 preamble.tex；检索遵循 manuscript/references/README.md，正式引用集中在 library.bib。
6. 运行 make test check，查看 PDF 页面，再运行 make bundle。投稿材料按目标期刊要求补齐。

研究规模增加后，按实际分析问题继续细分功能目录，并在 Makefile 增加目标。

## 环境与复现

- config/project.R 集中保存路径、分组和随机种子。
- analysis/results/session-info.txt 保存 R 会话、平台、已加载包、种子与输入 MD5。
- renv.lock 提供 R 4.6.1 的无第三方分析包基线；它不安装 R 或 TeX。
- 需要外部 R 包时，把直接依赖写到 DESCRIPTION 的 Imports 字段，使用 make restore 初始化隔离环境；在项目环境安装所需包后，运行 make snapshot 锁定版本。另一台机器运行 make restore 恢复。
- make restore / snapshot 需要 renv，缺失时从 CRAN 安装，可能联网。日常示例构建不要求先执行它们。提交 renv.lock 及激活脚本，不提交项目包库。
- 统计方法改变时同步修改测试；tests/ 的教学数值预期应随示例被真实研究校验替换。

## 文件管理

输入、代码、正文和锁文件纳入 Git；派生数据、统计输出、图表、编译中间文件及归档默认忽略。输出可由源文件重建，不手工修改。

真实数据不一定适合入库或分发。替换示例前调整忽略规则和 submission/package.R 的白名单。manuscript/references/runs/ 和 manuscript/references/fulltext/ 默认保留本地。API key、邮箱等配置不写入脚本、检索记录或归档。

make bundle 包含当前工作区源文件、示例原始输入、结果和 PDF；PROVENANCE.txt 记录基准提交及未提交状态，MANIFEST.tsv 记录内容校验和。它是本地复现归档，不上传、不发布，也不替代期刊投稿要求。

## 技能与项目规则

已安装 entrez 和 Nature Skills。通用技能提供方法，项目约定放 AGENTS.md 和各功能目录 README.md。检索词、输出字段和位置统一维护在 manuscript/references/README.md，不把某篇论文的目录写进 skill。
