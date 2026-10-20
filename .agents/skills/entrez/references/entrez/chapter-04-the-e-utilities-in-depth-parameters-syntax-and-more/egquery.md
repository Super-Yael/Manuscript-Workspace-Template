---
title: "EGQuery"
chapter: "The E-utilities In-Depth: Parameters, Syntax and More"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter4/#chapter4.EGQuery"
---
# EGQuery

## Base URL

https://eutils.ncbi.nlm.nih.gov/entrez/eutils/egquery.fcgi

## Function

Provides the number of records retrieved in all Entrez databases by a single text query.

## Required Parameter

### term

Entrez text query. All special characters must be URL encoded. Spaces may be replaced by '+' signs. For very long queries (more than several hundred characters long), consider using an HTTP POST call. See the [PubMed](https://www.ncbi.nlm.nih.gov/sites/books/n/helppubmed/pubmedhelp/#pubmedhelp.Search_Field_Descrip) or [Entrez](https://www.ncbi.nlm.nih.gov/sites/books/n/helpentrez/EntrezHelp/) help for information about search field descriptions and tags. Search fields and tags are database specific.

<https://eutils.ncbi.nlm.nih.gov/entrez/eutils/egquery.fcgi?term=asthma>
