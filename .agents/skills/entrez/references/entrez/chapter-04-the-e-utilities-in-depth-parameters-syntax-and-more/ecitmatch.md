---
title: "ECitMatch"
chapter: "The E-utilities In-Depth: Parameters, Syntax and More"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter4/#chapter4.ECitMatch"
---
# ECitMatch

## Base URL

https://eutils.ncbi.nlm.nih.gov/entrez/eutils/ecitmatch.cgi

## Function

Retrieves PubMed IDs (PMIDs) that correspond to a set of input citation strings.

## Required Parameters

### db

Database to search. The only supported value is ‘pubmed’.

### rettype

Retrieval type. The only supported value is ‘xml’.

### bdata

Citation strings. Each input citation must be represented by a citation string in the following format:

journal_title\|year\|volume\|first_page\|author_name\|your_key\|

Multiple citation strings may be provided by separating the strings with a carriage return character (%0D). The *your_key* value is an arbitrary label provided by the user that may serve as a local identifier for the citation, and it will be included in the output. Be aware that all spaces must be replaced by ‘+’ symbols and that citation strings should end with a final vertical bar ‘\|’.

<https://eutils.ncbi.nlm.nih.gov/entrez/eutils/ecitmatch.cgi?db=pubmed&retmode=xml&bdata=proc+natl+acad+sci+u+s+a%7C1991%7C88%7C3248%7Cmann+bj%7CArt1%7C%0Dscience%7C1987%7C235%7C182%7Cpalmenberg+ac%7CArt2%7C>
