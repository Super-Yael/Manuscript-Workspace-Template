---
title: "Finding Related Data Through Entrez Links"
chapter: "E-utilities Quick Start"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter1/#chapter1.Finding_Related_Data_Through_En"
---
# Finding Related Data Through Entrez Links

## Basic Linking

### Batch mode – finds only one set of linked UIDs

    elink.fcgi?dbfrom=<source_db>&db=<destination_db>&id=<uid_list>

Input: List of UIDs (&id); Source Entrez database (&dbfrom); Destination Entrez database (&db)

Output: XML containing linked UIDs from source and destination databases

*Example: Find one set of Gene IDs linked to nuccore GIs 34577062 and 24475906*

<https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=nuccore&db=gene&id=34577062,24475906>

### ‘By Id’ mode – finds one set of linked UIDs for each input UID

    elink.fcgi?dbfrom=<source_db>&db=<destination_db>&id=<uid1>&id=
    <uid2>&id=<uid3>...

*Example: Find separate sets of Gene IDs linked to nuccore GIs 34577062 and 24475906*

<https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=nuccore&db=gene&id=34577062&id=24475906>

*Note: &db may be a comma-delimited list of databases, so that elink returns multiple sets of linked UIDs in a single call*

## Finding Links to Data from a Previous Search

    esearch.fcgi?db=<source_db>&term=<query>&usehistory=y

    # esearch produces WebEnv value ($web1) and QueryKey value ($key1)

    elink.fcgi?dbfrom=<source_db>&db=<destination_db>&query_key=
    $key1&WebEnv=$web1&cmd=neighbor_history

Input: Source Entrez database (&dbfrom); Destination Entrez database (&db); Web environment (&WebEnv) and query key (&query_key) representing the set of source UIDs on the Entrez history server; Command mode (&cmd)

Output: XML containing Web environments and query keys for each set of linked UIDs

*Note: To achieve ‘By Id’ mode, one must send each input UID as a separate &id parameter in the URL. Sending a WebEnv/query_key set always produces Batch mode behavior (one set of linked UIDs).*

## Finding Computational Neighbors Limited by an Entrez Search

    elink.fcgi?dbfrom=<source_db>&db=<source_db>&id=<uid_list>&term=
    <query>&cmd=neighbor_history

Input: Source Entrez database (&dbfrom); Destination Entrez database (&db); List of UIDs (&id); Entrez query (&term); Command mode (&cmd)

Output: XML containing Web environments and query keys for each set of linked UIDs

*Example: Find protein UIDs that are rat Reference Sequences and that are sequence similar to GI 15718680*

[https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=protein&db=protein&id=15718680&term=rat\[orgn\]+AND+srcdb+refseq\[prop\]&cmd=neighbor_history](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=protein&db=protein&id=15718680&term=rat%5borgn%5d+AND+srcdb+refseq%5bprop%5d&cmd=neighbor_history)

## For More Information

Please see [ELink In-Depth](https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter4/#chapter4.ELink) for a full description of ELink.
