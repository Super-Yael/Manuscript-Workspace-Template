---
title: "Combining E-utility Calls to Create Entrez Applications"
chapter: "A General Introduction to the E-utilities"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter2/#chapter2.Combining_Eutility_Calls_to_Cre"
---
# Combining E-utility Calls to Create Entrez Applications

The E-utilities are useful when used by themselves in single URLs; however, their full potential is realized when successive E-utility URLs are combined to create a data pipeline. When used within such pipelines, the Entrez History server simplifies complex retrieval tasks by allowing easy data transfer between successive E-utility calls. Listed below are several examples of pipelines produced by combining E-utilities, with the arrows representing the passing of db, WebEnv and query_key values from one E-utility to another. These and related pipelines are discussed in detail in Chapter 3.

## Basic Pipelines

### Retrieving data records matching an Entrez query

[ESearch → ESummary](https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter3/#chapter3.ESearch__ESummaryEFetch)

[ESearch → EFetch](https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter3/#chapter3.ESearch__ESummaryEFetch)

### Retrieving data records matching a list of UIDs

[EPost → ESummary](https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter3/#chapter3.EPost__ESummaryEFetch)

[EPost → EFetch](https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter3/#chapter3.EPost__ESummaryEFetch)

### Finding UIDs linked to a set of records

[ESearch → ELink](https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter3/#chapter3.ESearch__ELink__ESummaryEFetch)

[EPost → ELink](https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter3/#chapter3.EPost__ELink__ESummaryEFetch)

### Limiting a set of records with an Entrez query

[EPost → ESearch](https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter3/#chapter3.EPost__ESearch)

[ELink → ESearch](https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter3/#chapter3.ELink__ESearch)

## Advanced Pipelines

### Retrieving data records in database B linked to records in database A matching an Entrez query

[ESearch → ELink → ESummary](https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter3/#chapter3.ESearch__ELink__ESummaryEFetch)

[ESearch → ELink → EFetch](https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter3/#chapter3.ESearch__ELink__ESummaryEFetch)

### Retrieving data records from a subset of an ID list defined by an Entrez query

[EPost → ESearch → ESummary](https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter3/#chapter3.EPost__ESearch)

[EPost → ESearch → EFetch](https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter3/#chapter3.EPost__ESearch)

### Retrieving a set of data records, defined by an Entrez query, in database B from a larger set of records linked to a list of UIDs in database A

[EPost → ELink → ESearch → ESummary](https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter3/#chapter3.ELink__ESearch)

[EPost → ELink → ESearch → EFetch](https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter3/#chapter3.ELink__ESearch)
