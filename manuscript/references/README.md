# 文献检索与引用

本目录是论文的文献与引用工作区，统一规定如何使用 entrez skill。skill 本身保留可复用的方法，具体研究问题、检索词、格式和目录约定放在这里。

## 构建检索词

1. 先在 research/question.md 明确研究对象、核心概念、结局、研究类型，以及检索的用途。
2. 将问题拆为概念组：同义词用 OR，概念之间用 AND。需要时组合 MeSH 主题词与标题/摘要自由词，记录字段限定。
3. 先做小规模试检索，检查已知相关文献是否命中、主要误检来源是什么，再调整检索式。不要无理由加入语言、年份或全文可用性限制。
4. 最终检索式以 UTF-8 纯文本保存在 queries/主题名.txt；每次执行产生独立的 runs/日期时间_主题名/ 目录，保留各次版本。

这里只定义项目约定；需要执行检索时读取 entrez skill，根据数据库选择 esearch、efetch、esummary、elink 或 xtract。不要把 PubMed 检索结果直接当作已阅读全文的证据。

## 每次检索的输出

| 文件 | 内容 |
| --- | --- |
| query.txt | 本次实际执行的完整检索式副本 |
| search.json | 数据库、检索时间和时区、完整命令或端点参数（排除凭据）、限制条件、命中数、实际获取数、分页/批次和错误情况 |
| ids.txt | 去重后的 PMID 或对应数据库 UID，每行一个 |
| records.xml | 原始 XML；分批时使用 records-001.xml 等，保留原始响应 |
| records.tsv | UTF-8 表格，字段见下方；使用真正的 Tab 分隔 |
| screening.tsv | 纳入/排除决定、理由、判断者、日期与相关主张；与检索原始表分开 |
| references.bib | 经核验、实际准备引用的条目，稳定引用键 |

records.tsv 至少包含：pmid、doi、title、authors、journal、year、abstract、url。多作者以分号连接，字段内换行和 Tab 转为空格；缺失字段留空，不补造。若数据库不是 PubMed，用 uid 和 database 字段替代 pmid，保留可追溯标识。

对命中数、成功获取数、唯一标识数做核对；说明差异和未完成批次。不要假设单次请求返回了所有结果。检索历史令牌不是长期归档，必须保存查询和实际结果。

## 保存位置与正文引用

以下子目录均相对于 manuscript/references/；文中 research/ 和 Makefile 路径相对于仓库根目录。

- queries/：人工维护的检索策略，不放凭据。
- runs/<YYYYMMDD-HHMMSS_主题>/：一次检索的查询、元数据、原始响应、派生表和筛选记录。默认保留本地，不自动提交到 Git；需要归档时先审查大小和内容，再显式纳入版本管理。
- fulltext/：合法取得的原文和补充材料，默认本地保存；注明来源和对应 PMID/DOI。
- library.bib：论文唯一的正式参考文献库；将检索产出的条目核验去重后合入，正文使用引用键。

每次检索的研究用途和策略调整记录到 research/decisions.md。若检索变成稳定的重复任务，增加 manuscript/references/ 下的脚本及 Makefile 目标，明确输入和输出。邮箱、API key 等配置放环境变量或不入库的 .env，不写进命令记录或数据表。
