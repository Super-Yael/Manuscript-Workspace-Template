---
title: "Local PubMed Archive"
chapter: "Entrez Direct: E-utilities on the Unix Command Line"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter6/#chapter6.Local_PubMed_Archive"
---
# Local PubMed Archive

Fetching data from Entrez works well when a few thousand records are needed, but it does not scale for much larger sets of data, where the time it takes to download becomes a limiting factor.

## Local Record Cache

EDirect can now preload 40 million live PubMed records onto an inexpensive external 1 TB solid-state drive (SSD), storing them in indexed archive files. For example, PMID 2539356 would be entry 9356 in:

      /pubmed/Archive/00/02/000253.archive

Each archive contains up to 10,000 individually-compressed source data records in a specific range of identifiers. Preceding those concatenated, independent blocks is a binary array of the cumulative block lengths. This allows rapid random access to any or all of the compressed records in the archive.

The local archive is a completely self-contained turnkey product, with no need to download, configure, and maintain complicated third-party database software.

Set an environment variable in your configuration file(s) to reference a section of your external drive:

      export EDIRECT_LOCAL_ARCHIVE=/Volumes/external_drive_name/

Then run **archive‑pubmed** to download the PubMed release files and save each record on the drive. The initial download may take several hours, depending on your network connection, with initial archiving taking another few hours. Subsequent updates are incremental, and should finish in minutes.

Fetching a set of 144,129 PubMed records from NCBI's network service takes a bit over 30 minutes:

      esearch -db pubmed -query "PNAS [JOUR]" -pub abstract | efetch -format xml

Searching the local indices (see next section) with **xsearch**, and then using **xfetch** to retrieve and decompress the XML records from the local archive, runs in under 7 seconds:

      xsearch -db pubmed -query "PNAS [JOUR] AND has abstract [PROP]" | xfetch

This is more than 250 times faster than using the EUtils servers, and avoids network reliability issues.

Piping to xfetch **‑stream** returns the original compressed records, for a roughly four-fold size reduction of data to send over a network. This would be followed by decompression on the client with **gunzip ‑c**.

Alternatively, using xfetch **‑turbo** precedes each record with an object containing its size in bytes:

      <NEXT_RECORD_SIZE>4027</NEXT_RECORD_SIZE>

Piping these enhanced records to xtract **‑turbo** approximately doubles the speed of the (rate-limiting) record partitioning step, which otherwise uses the Boyer-Moore-Horspool fast string search algorithm.

Running xfetch ‑db pubmed **‑all** retrieves the entire database by piping each ".archive" file through:

      dd ibs=8000 skip=10 2> /dev/null | gunzip -c 2> /dev/null

## Local Search Index

A similar strategy was used to create a local information retrieval system suitable for large data mining queries. Run **archive‑pubmed ‑index** to populate retrieval index files from records stored in the local archive. The initial indexing will also take a few hours. To build a small subset for evaluation, run:

      archive-pubmed -index -custom "J Exp Med [JOUR] AND 2000:2026 [PDAT]"

For PubMed titles and primary abstracts, the indexing process deletes hyphens after specific prefixes, removes accents and diacritical marks, splits words at punctuation characters, corrects encoding artifacts, and spells out Greek letters for easier searching on scientific terms. It then prepares inverted indices with term positions, and uses them to build distributed term lists and postings files.

For example, the term list that includes "cancer" in the title or abstract would be located at:

      /pubmed/Postings/TIAB/c/a/n/c/canc.TIAB.trm

A query on cancer thus only needs to load a very small subset of the total index. The software supports expression evaluation, wildcard truncation, phrase queries, proximity searches, and partial matches.

The **xinfo**, **xsearch**, **xlink**, and **xfilter** scripts provide access to the local search system.

Names of indexed fields, all terms for a given field, and terms plus record counts, are shown by:

      xinfo -fields

      xinfo -terms TITL

      xinfo -totals PROP

Terms are truncated with a trailing asterisk, and can be expanded to show individual postings counts:

      xinfo -count "catabolite repress*"

      xinfo -counts "catabolite repress*"

Query evaluation includes Boolean operations and parenthetical expressions:

      xsearch -query "(literacy AND numeracy) NOT (adolescent OR child)"

Adjacent words in title or abstract fields are treated as a contiguous phrase:

      xsearch -query "selective serotonin reuptake inhibitor [TITL]"

Each plus sign will replace a single word inside a phrase, and runs of tildes indicate the maximum distance between sequential phrases:

      xsearch -query "vitamin c + + common cold"

      xsearch -query "vitamin c ~ ~ common cold"

Ranked partial term matching is available in any field with **‑match**:

      xsearch -match "tn3 transposition immunity [PAIR]" | just-top-hits 1

An exact substring match, without special processing of Boolean operators or indexed field names, can be obtained with ‑title (on the article title) or ‑exact (on the title or abstract):

      xsearch -title "Genetic Control of Biochemical Reactions in Neurospora."

MeSH identifier code, MeSH hierarchy key, and year of publication are also indexed, and MESH field queries are supported by internally mapping to the appropriate CODE or TREE entries:

      xsearch -db pubmed -query "C14.907.617.812* [TREE] AND 2015:2019 [YEAR]"

PMIDs processed through an external source can be reintroduced to a local query pipeline with xfilter:

      | xfilter -db pubmed -query "Monoamine Oxidase [MESH] AND Deficiency [SUBH]" |

## Data Analysis

All query commands return a structured message containing the database name and a list of UIDs, which can be piped directly to xfetch to retrieve the uncompressed records. For example:

      xsearch -db pubmed -query "selective serotonin ~ ~ ~ reuptake inhibit*" |
      xfetch |
      xtract -pattern PubmedArticle -num AuthorList/Author |
      sort-uniq-count -n |
      reorder-columns 2 1 |
      align-columns -g 4 -a lr

performs a proximity search with dynamic wildcard expansion (matching phrases like "selective serotonin and norepinephrine reuptake inhibitors") and fetches 16,088 PubMed records from the local archive. It then prints a frequency table of the number of papers per number of authors (a consortium is treated as a single author):

      0      56
      1    1494
      2    2144
      3    2228
      …

## Data Visualization

The cumulative size of PubMed can be calculated with a running sum of the annual record counts:

      xinfo -db pubmed -totals YEAR |
      print-columns '$2, $1, total += $1' |
      print-columns '$1, log($2)/log(10), log($3)/log(10)' |
      filter-columns '$1 >= 1800 && $1 < YR' |
      xy-plot annual-and-cumulative.png

Exponential growth over time will appear as a roughly linear curve on a semi-logarithmic graph:

![Image chapter6-Image004.jpg](https://www.ncbi.nlm.nih.gov/sites/books/NBK179288/bin/chapter6-Image004.jpg)

The sharp jump after World War II was caused by several factors, including the release of declassified papers, a policy of expanding biomedical research in postwar America, and the introduction of computers that could keep up with the indexing of articles from a broader range of subjects.

## Natural Language Processing

NLM's Biomedical Text Mining Group performs computational analysis to extract chemical, disease, and gene references from article contents (8). NLM indexing of PubMed records assigns Gene Reference into Function (GeneRIF) mappings (9).

Running **archive‑nlmnlp ‑index** periodically (monthly) will automatically refresh any out-of-date support files and then index the connections in CHEM, DISZ, GENE, GRIF, GSYN, and PREF fields:

      xinfo -terms DISZ | grep -i Raynaud

      xinfo -counts "Raynaud* [DISZ]"

      xinfo -query "Raynaud Disease [DISZ]"

## Following Citation Links

Running **archive‑nihocc ‑index** will download the latest NIH Open Citation Collection monthly release and build CITED and CITES indices, the local equivalent of elink ‑cited and ‑cites commands.

Citation links are retrieved by piping one or more PMIDs to xlink **‑target**:

      xsearch -db pubmed -query "Haselkorn R* [AUTH]" |
      xlink -target CITED |

This returns PMIDs for 8,356 articles that cite the original 225 papers. The results are then restricted to a range of recent years, and those records are fetched. The xtract **‑histogram** shortcut builds a journal frequency table from the subsequent articles:

      xfilter -query "2020:2025 [YEAR]" | xfetch |
      xtract -pattern PubmedArticle -histogram Journal/ISOAbbreviation |
      sort-table -nr | head -n 10

The **archive‑pids ‑index** command reads the PubMed local archive's incremental inverted index files, and builds a PMCID index that allows xlink to return PubMed Central identifiers from PMIDs:

      xlink -db pubmed -id 12372140 -target PMCID | xfetch

The xlink **‑ranked** flag produces the same ranked output format as xsearch **‑match**.

## Additional Experimental Archives

Legacy PMC release files are downloaded via FTP by running **archive‑pmc ‑index**, which collects primary author names, citation details, section titles, and full-text paragraphs. It then converts them to the more tractable PMCInfo object, and builds an archive from those derived records.

Similarly, **archive‑taxonomy ‑index** archives novel records assembled from NCBI taxonomy data tables retrieved from the FTP site.

A new database is ready for use once its autonomous archiving script has finished all downloading, conversion, validation, caching, indexing, inversion, collection, merging, and posting steps.
