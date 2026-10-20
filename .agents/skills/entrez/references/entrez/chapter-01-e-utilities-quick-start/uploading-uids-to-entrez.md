---
title: "Uploading UIDs to Entrez"
chapter: "E-utilities Quick Start"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter1/#chapter1.Uploading_UIDs_to_Entrez"
---
# Uploading UIDs to Entrez

## Basic Uploading

    epost.fcgi?db=<database>&id=<uid_list>

Input: List of UIDs (&id); Entrez database (&db)

Output: Web environment (&WebEnv) and query key (&query_key) parameters specifying the location on the Entrez history server of the list of uploaded UIDs

*Example: Upload five Gene IDs (7173,22018,54314,403521,525013) for later processing.*

<https://eutils.ncbi.nlm.nih.gov/entrez/eutils/epost.fcgi?db=gene&id=7173,22018,54314,403521,525013>

## Associating a Set of UIDs with Previously Posted Sets

    epost.fcgi?db=<database1>&id=<uid_list1>

    # epost produces WebEnv value ($web1) and QueryKey value ($key1)

    epost.fcgi?db=<database2>&id=<uid_list2>&WebEnv=$web1

    # epost produces WebEnv value ($web2) that contains the results of both 
    posts ($key1 and $key2)

Input: List of UIDs (&id); Entrez database (&db); Existing web environment (&WebEnv)

Output: Web environment (&WebEnv) and query key (&query_key) parameters specifying the location on the Entrez history server of the list of uploaded UIDs

## For More Information

Please see [EPost In-Depth](https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter4/#chapter4.EPost) for a full description of EPost.

## Sample EPost Output

    <?xml version="1.0"?>
    <!DOCTYPE ePostResult PUBLIC "-//NLM//DTD ePostResult, 11 May 2002//EN"
     "https://www.ncbi.nlm.nih.gov/entrez/query/DTD/ePost_020511.dtd">
    <ePostResult>
    <QueryKey>1</QueryKey>
    <WebEnv>NCID_01_268116914_130.14.18.47_9001_1241798628</WebEnv>
    </ePostResult>
