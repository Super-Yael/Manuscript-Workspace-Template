# 文献检索与引用

按“文章章节 → 需要证据的论点 → 高级检索式 → 独立 BibTeX”组织。章节按实际文章建立，不预设名称、数量或结构。

## 记录检索策略

每个大段落建立一个子目录，并在该目录的 README.md 中逐点记录：论点、检索目的、完整高级检索式、限制条件及调整理由。同义词用 OR，不同概念用 AND，按需要组合 MeSH 与标题/摘要字段。

每个检索点使用唯一、稳定的英文编号；同一目录内不得重名。检索式使用带编号的 pubmed 代码块，例如：

````markdown
## P01 — 此处填写需要文献支持的观点

检索目的：此处说明要寻找哪类证据。

```pubmed P01
(概念A[MeSH Terms] OR 同义词A[Title/Abstract]) AND 概念B[Title/Abstract]
```

限制与调整：此处说明理由；不需要的限制不要添加。
````

这只是格式说明，不会执行；实际论点写入对应章节子目录的 README.md。一个点一条检索式，一个点一个 P01.bib。若需要两条独立检索式，为它们分配不同编号。

## 检索并保存 BibTeX

1. 从根目录 .env.example 复制 .env，填写真实 NCBI_EMAIL；NCBI_API_KEY 可选。无 key 每秒最多 3 请求，有有效 key 后自动升至最多 10 请求。限速、超时、重试、批次、排序和最大获取数均在配置文件中设置。
2. 运行 make references。程序扫描 REFERENCES_DIR 下各一级章节目录的 README.md，依次执行所有 pubmed 代码块。
3. 每个点的检索结果写入所在章节的 <点编号>.bib；原始响应、查询、ID、TSV 和数量核对记录写入该章节的 .runs/<点编号>/<UTC时间戳>/。所有查询共用一个限速器。

没有实际章节或检索式时跳过，不联网、不建目录。默认获取全部命中；PubMed ESearch 超过 10000 条时明确报错，须拆分检索或用 EDirect，不能把部分结果标为全部。失败时保留已有响应，旧的论点 BibTeX 不被半成品覆盖；重新检索成功后才替换同名 .bib，历史版本随 .runs/ 中的 records.bib 保留。

BibTeX 保存能取得的题名、作者、期刊、年份、卷期、页码、DOI、PMID、URL、摘要、关键词、MeSH、机构、文献类型、资助等元数据；未映射的 NCBI 信息也通过可还原的 ncbi_xml_base64 扩展字段完整保留。abstract 字段始终存在；来源没有摘要时留空，并标记 abstract_available=false，绝不补写摘要。

检索所得记录是候选文献，不代表已阅读全文或已验证对论点的支持。筛选判断和阅读笔记补充在该章节 README 中。原始响应与全文缓存默认不提交，BibTeX 中的摘要也应按适用权限使用与分享。

## 引用键

- 有 DOI：以去掉 doi.org 前缀、转小写的 DOI 为键，例如 10.1234/example.1。
- DOI 中不适合作为 TeX 键的空白、逗号、花括号、百分号等字符编码为 -uXXXX-，维持稳定的 DOI 派生键。
- 没有 DOI：用 pmid:12345678。其他来源无 DOI/PMID 时保留可追溯的稳定标识，不用易冲突的作者年份随意替代。

以生成的条目键为准，在正文中写 cite、citep、citet、parencite、textcite 等引用命令。不要手动把各检索结果合并成主库。

## 自动构建 reference.bib

运行 make bibliography，或直接 make manuscript：Makefile 在 LaTeX 编译前调用 entrez skill 的构建脚本，从主文档及 input/include/subfile 引入的 TeX 文件收集显式引用键，在所有章节的 .bib 中找出被使用的记录，生成 REFERENCE_BIB（默认 manuscript/references/reference.bib）。其余候选文献不进入输出。引用所需的 crossref/xref/xdata 依赖条目也会一并收集。

默认使用 uv 在隔离环境提供配置中锁定的 bibtexparser，不修改系统 Python。没有主文档时跳过，不安装依赖、不生成空库。

在主文档中只配置这个自动生成的库，例如 BibTeX：

```tex
\bibliography{manuscript/references/reference}
```

或 biblatex：

```tex
\addbibresource{manuscript/references/reference.bib}
```

编译从仓库根目录执行。修改目录配置后同步修改正文中的库路径。reference.bib 是自动生成物，忽略入库，make clean 会删除它；各点 .bib 是保留的检索来源，清理不会删除。

## 重复与冲突

同一引用键命中多个来源时，构建器逐对检查 DOI、PMID、标准化题名等信息：

- 能确认是同一篇：合并为一条，补齐缺失字段，优先保留更完整的内容。
- DOI/PMID 或题名冲突，或者缺少足够信息确认重复：立即报错，显示引用键与来源文件，停止构建及后续 LaTeX 编译。
- 正文引用键不存在：立即报错，不静默丢弃。

不要靠重命名冲突条目掩盖错误，应先核实实际文献及其标识。对同一文献统一使用生成的 DOI 键，避免正文用多个别名重复引用。

构建器读取显式引用与字面量 input/include/subfile 路径，忽略注释和常见 verbatim 环境；宏动态生成的引用/路径需改为明确写法。不支持 nocite{*}，因为它会把未使用候选文献全部纳入。存在复杂条件章节时只把实际使用的章节纳入主文件，避免把未启用内容留给静态扫描推断。
