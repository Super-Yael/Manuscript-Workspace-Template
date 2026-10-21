---
name: entrez
description: Use when searching, retrieving, linking, or extracting records from NCBI Entrez databases with Entrez Direct (EDirect) or the E-utilities, especially for PubMed, nucleotide, protein, and related biological data.
---
# Entrez

Use this skill for reproducible, command-line-oriented access to NCBI Entrez. The complete local source material is copied under `references/entrez/`; read only the relevant reference files for the current task instead of loading the whole collection.

## Working conventions

- First identify the target database, query or identifier list, desired record format, and expected output size.
- For PubMed literature searches with structured local outputs, use the bundled Python script below. For other databases or large query partitioning, use EDirect.
- Prefer the EDirect pipeline `esearch` → `esummary` or `efetch` for ordinary searches and retrievals. Use `epost` for a large or pre-existing UID list, `elink` for related records, and `einfo` when database fields or valid search terms are unclear.
- Use `xtract` to extract named values from XML and to keep nested fields associated with their parent record. Set explicit separators, defaults, and record patterns when producing tabular output.
- For large result sets, use the Entrez history server (`usehistory`, `WebEnv`, and `QueryKey`/`query_key`) or batch retrieval with `retstart` and `retmax`; do not assume that one request returns every record.
- Keep raw responses and derived tables distinguishable. Record the database, query, retrieval date, command or endpoint, format, and any filters needed to reproduce the result.
- Supply an identifying email and API key when the chosen interface supports them. Respect the current NCBI request limits, avoid aggressive parallel requests, URL-encode query parameters, and use bounded retries with backoff for transient failures.
- Check that the requested database and output format are compatible before parsing. Validate counts, identifiers, empty results, and malformed or partial responses before using the data downstream.

## Common command shapes

```bash
# Search and fetch records
esearch -db pubmed -query 'influenza haemophilus' -retmax 20 \
  | efetch -format docsum

# Fetch sequence records by accession or UID
efetch -db nuccore -id 'NM_000000.1' -format fasta
efetch -db protein -id 'NP_000000.1' -format gp

# Extract fields from XML
efetch -db pubmed -id 'PMID1,PMID2' -format xml \
  | xtract -pattern PubmedArticle -element MedlineCitation/PMID
```

Adjust database names, identifiers, query syntax, and formats to the task. Treat the examples as command shapes, not as valid biological identifiers.

## Reference routing

- Read `references/entrez/README.md` for the local source map.
- For EDirect installation, shell pipelines, biological records, sequence work, XML extraction, or Python integration, read the relevant files in `references/entrez/chapter-06-entrez-direct-e-utilities-on-the-unix-command-line/`.
- For E-utility purpose, usage requirements, request parameters, and API combinations, read the relevant files in chapters 02–04.
- For short end-to-end examples, read chapters 01 and 03.
- The copied reference collection is source material, not generated project output; do not rewrite it while performing an Entrez task.

## Bundled PubMed search

Use `scripts/search_pubmed.py` (Python 3, standard library only) for reproducible literature searches. Run it from the caller's workspace. It embeds no project paths.

```sh
python3 <skill-dir>/scripts/search_pubmed.py --query-file query.txt --output results
```

Configuration precedence: CLI query/output > process environment > the selected `--env-file` (default `.env`) > caller's `.env.example` > operational defaults. Config files contain literal `KEY=value`, optional matching quotes, full-line comments; no shell execution, interpolation, `export`, or inline comments. Relative paths use the current working directory.

- `NCBI_EMAIL`: required real contact email when a query is supplied; `NCBI_TOOL`: identifying name without spaces.
- `NCBI_API_KEY`: optional. Empty uses a ceiling of 3 requests/second; present uses a ceiling of 10. A supplied key must actually be valid; the script does not obtain or validate account keys in advance.
- `NCBI_REQUESTS_PER_SECOND=auto`: select the ceiling automatically, or supply a lower positive rate. Higher-than-allowed rates are rejected. Throttling is per process; avoid concurrent scripts sharing the same IP/key allowance.
- `NCBI_TIMEOUT_SECONDS`, `NCBI_MAX_RETRIES`: timeout and bounded retry count. Retries cover HTTP 429/transient server errors and transport/XML failures, with backoff. Invalid credentials and other permanent HTTP failures stop immediately.
- `ENTREZ_QUERY` or `ENTREZ_QUERY_FILE`: query text or UTF-8 query file. An explicit missing query file is an error; no query/empty content skips without network or output directories.
- `ENTREZ_OUTPUT_DIR`: required unless `--output` is supplied. Each search creates a unique UTC-timestamped run directory.
- `ENTREZ_DATABASE=pubmed`: this script only exports PubMed literature. Other Entrez databases use the existing reference workflows.
- `ENTREZ_MAX_RECORDS`: maximum selected hits, `0` for all; `ENTREZ_BATCH_SIZE`: records per EFetch batch (1–1000); `ENTREZ_SORT`: ESearch sort.

Each run saves `query.txt`, `esearch.xml`, `ids.txt`, batched `records-*.xml`, `records.tsv`, `records.bib` and `search.json`. The TSV columns are pmid, doi, title, authors, journal, year, abstract, url. Missing metadata stays empty. The report distinguishes total hits, selected hits, actual retrieval and whether all hits were retrieved. Interrupted retrievals retain successful raw batches and a failed status; do not treat them as complete.

PubMed ESearch can expose only the first 10,000 hits. If the requested selection exceeds this limit the script fails explicitly; partition the query or use EDirect, never claim full retrieval. Source-derived BibTeX is exported automatically, including abstract (empty if unavailable), rich metadata, DOI-first keys with PMID fallback, and reversible ncbi_xml_base64 for all remaining metadata. This does not certify relevance or invent screening decisions. Parse and verify evidence before selecting citations.

API keys and email are sent via HTTPS POST and excluded from metadata/logs. Search results may contain copyrighted abstracts; consult [NCBI usage guidance](https://eutilities.github.io/site/API_Key/usageandkey/) and the [NCBI disclaimer](https://www.ncbi.nlm.nih.gov/About/disclaimer.html) before redistribution.

Run script checks with `uv run --with bibtexparser==1.4.3 python -m unittest discover -s <skill-dir>/scripts -p 'test_*.py'`.

## Section-and-point literature workflow

Use `scripts/readme_queries.py --root <references-root>` to discover child section directories. Their README.md files contain point descriptions and fenced queries labelled as three backticks followed by `pubmed POINT_ID`; the next lines contain the literal advanced query, ending with three backticks. Point IDs must be unique within each section and use letters, digits, hyphens or underscores.

The root and chapter names are caller-defined. Each point publishes `<POINT_ID>.bib` alongside its README only after successful retrieval. Raw runs and prior per-query BibTeX are archived in `<section>/.runs/<POINT_ID>/<timestamp>/`. One client enforces rate limits across all points. No sections or queries means no network and no output. All project-specific paths remain in caller config/documentation.

For a direct single query, the search script also accepts `--bib <point-file.bib>` to publish the successful records.bib at a chosen location. Do not write bibliographic records for failed retrievals.

## Cited-only bibliography construction

Use `scripts/build_bibliography.py --main <main.tex> --sources <references-root> --output <reference.bib>`. It requires bibtexparser 1.4.3 (the caller may provision it with uv). The scanner follows explicit input/include/subfile paths, supports literal cite-family keys, optional notes and multicites, ignores comments and common verbatim environments, and rejects nocite{*} or missing sources/keys. Dynamic macros and conditional input selection require explicit source organization rather than guessed expansion.

It searches all non-hidden source .bib files recursively, excluding the output. Match raw keys plus canonical DOI/PMID aliases. For every key actually used, compare every candidate pair: conflicting DOI, PMID or normalized title is an error; absent shared identifiers require matching title, year and author to confirm duplication. Missing evidence is not permission to guess. Report key and source files and stop before replacing output. Confirmed duplicate records merge into one output entry per key with richer fields preserved; dependency entries named by crossref/xref/xdata are included. Ask authors to use one canonical DOI key per work to avoid citing multiple aliases.

Source BibTeX files remain untouched. Generated output is atomic and stable when unchanged. Do not manually concatenate query files or silently resolve same-key/different-paper collisions.
