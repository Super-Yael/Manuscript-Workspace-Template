---
name: entrez
description: Use when searching, retrieving, linking, or extracting records from NCBI Entrez databases with Entrez Direct (EDirect) or the E-utilities, especially for PubMed, nucleotide, protein, and related biological data.
---
# Entrez

Use this skill for reproducible, command-line-oriented access to NCBI Entrez. The complete local source material is copied under `references/entrez/`; read only the relevant reference files for the current task instead of loading the whole collection.

## Working conventions

- First identify the target database, query or identifier list, desired record format, and expected output size.
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
