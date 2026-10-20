---
title: "Downloading Full Records"
chapter: "E-utilities Quick Start"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter1/#chapter1.Downloading_Full_Records"
---
# Downloading Full Records

## Basic Downloading

    efetch.fcgi?db=<database>&id=<uid_list>&rettype=<retrieval_type>
    &retmode=<retrieval_mode>

Input: List of UIDs (&id); Entrez database (&db); Retrieval type (&rettype); Retrieval mode (&retmode)

Output: Formatted data records as specified

*Example: Download nuccore GIs 34577062 and 24475906 in FASTA format*

<https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=34577062,24475906&rettype=fasta&retmode=text>

## Downloading Data From a Previous Search

    esearch.fcgi?db=<database>&term=<query>&usehistory=y

    # esearch produces WebEnv value ($web1) and QueryKey value ($key1)

    efetch.fcgi?db=<database>&query_key=$key1&WebEnv=$web1&rettype=
    <retrieval_type>&retmode=<retrieval_mode>

Input: Entrez database (&db); Web environment (&WebEnv) and query key (&query_key) representing a set of Entrez UIDs on the Entrez history server; Retrieval type (&rettype); Retrieval mode (&retmode)

Output: Formatted data records as specified

## Downloading a Large Set of Records

Please see [Application 3](https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter3/#chapter3.Application_3_Retrieving_large) in Chapter 3

Input: Entrez database (&db); Web environment (&WebEnv) and query key (&query_key) representing a set of Entrez UIDs on the Entrez history server; Retrieval start (&retstart), the first record of the set to retrieve; Retrieval maximum (&retmax), maximum number of records to retrieve

Output: Formatted data records as specified

## For More Information

Please see [EFetch In-Depth](https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter4/#chapter4.EFetch) for a full description of EFetch.
