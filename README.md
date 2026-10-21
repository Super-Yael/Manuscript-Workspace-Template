# Manuscript Workspace Template

空白的 R 数据分析 + LaTeX 论文工作区。按研究功能组织，用到什么再添加什么。

```text
.
├── data/                   数据来源、字典与整理
├── analysis/               统计分析、诊断与校验
├── figures/                图表制作
├── manuscript/             研究思路、正文与排版
│   └── references/         文献检索与引用约定
├── submission/             投稿与返修材料
├── .agents/skills/         已安装的通用技能
├── .env.example            配置项与默认值
├── Makefile                可选流程入口
└── AGENTS.md               协作约定
```

每个功能目录只保留必要说明。没有演示数据、示例论文、预设分析方法或空的依赖锁文件；原始数据、脚本、正文与输出子目录在实际使用时建立。

## 使用

所有可配置项集中在 .env.example。先复制为 .env，填写工具路径和 NCBI 配置；.env 已被 Git 忽略，未复制时使用模板默认值。

```sh
cp .env.example .env
```

所有命令从仓库根目录运行：

```sh
make             # 查看入口
make all         # 按顺序运行已添加的步骤
make test check  # 运行已有测试、构建与校验
```

Makefile 识别以下可选入口，文件缺失或内容为空时打印 SKIP，不要求事先安装 R 或 LaTeX。入口存在时，所需工具缺失或执行失败会报错。

| 命令 | 入口 |
| --- | --- |
| make references | 按各章节 README 的高级检索式生成每个论点的 .bib，无检索式则跳过 |
| make bibliography | 按正文引用从各 .bib 筛选、检查冲突并生成 reference.bib |
| make data | data/prepare.R |
| make analysis | 上游数据步骤，再运行 analysis/run.R |
| make figures | 上游分析步骤，再运行 figures/render.R |
| make manuscript | 上游图表步骤、manuscript/export-results.R、manuscript/main.tex |
| make test | analysis/test.R |
| make check | 构建论文，再运行 analysis/check.R |
| make bundle | 完成 check，再运行 submission/package.R |
| make clean | 删除各目录说明中约定的自动生成目录 |

这些入口是约定，不提前创建占位脚本。只写论文、暂不分析时，直接添加 manuscript/main.tex 即可；上游空步骤自动跳过。没有正文时也可只运行分析。

默认 LaTeX 使用 latexmk -pdf；需要 XeLaTeX 时运行 make manuscript LATEX_MODE=-xelatex。已有 R 脚本在各次调用时执行，LaTeX 的增量编译由 latexmk 管理。需要精确的分析缓存时，再在 Makefile 中添加真实输出文件与依赖规则。

## 开始一篇文章

在独立仓库使用此模板，先在 manuscript/ 记录研究问题与分析计划，再按实际任务添加数据、分析与正文。代码放在它服务的功能目录，不按 R、Python、LaTeX 分目录。

出现外部 R 包依赖时再初始化 renv 并提交真实的 renv.lock；记录随机种子和会话信息。可配置项统一维护在 .env.example，实际值放 .env。

文献按章节建立目录，每个论点在章节 README 中记录高级检索式、保存一个含摘要的 .bib；编译前自动生成仅包含正文引用的 reference.bib，引用键冲突即停止。具体格式与保存位置统一见 manuscript/references/README.md。通用 skill 不保存某篇论文的路径与规则。

生成物默认忽略；原始数据的入库与共享按实际权限决定。投稿和打包方案在有真实材料后确定。make clean 只删除 data/derived/、analysis/results/、figures/generated/、manuscript/generated/、manuscript/build/ 和 submission/generated/，并删除自动生成的 reference.bib；各论点的 .bib 会保留。不要在这些位置保存手工材料。
