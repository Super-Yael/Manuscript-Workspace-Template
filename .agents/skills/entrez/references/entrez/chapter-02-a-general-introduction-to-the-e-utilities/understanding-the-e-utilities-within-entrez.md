---
title: "Understanding the E-utilities Within Entrez"
chapter: "A General Introduction to the E-utilities"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter2/#chapter2.Understanding_the_Eutilities_Wi"
---
# Understanding the E-utilities Within Entrez

## The E-utilities Access Entrez Databases

The E-utilities access the core search and retrieval engine of the Entrez system and, therefore, are only capable of retrieving data that are already in Entrez. Although the majority of data at NCBI are in Entrez, there are several datasets that exist outside of the Entrez system. Before beginning a project with the E-utilities, check that the desired data can be found within an Entrez database.

## The Entrez System Identifies Database Records Using UIDs

Each Entrez database refers to the data records within it by an integer ID called a UID (unique identifier). Examples of UIDs are GI numbers for Nucleotide and Protein, PMIDs for PubMed, or MMDB-IDs for Structure. The E-utilities use UIDs for both data input and output, and thus it is often critical, especially for advanced data pipelines, to know how to find the UIDs associated with the desired data before beginning a project with the E-utilities.

See [Table 1](https://www.ncbi.nlm.nih.gov/sites/books/NBK25497/table/chapter2.T._entrez_unique_identifiers_ui/?report=objectonly) for a complete list of UIDs in Entrez.

[![Table Icon](https://www.ncbi.nlm.nih.gov/corehtml/pmc/css/bookshelf/2.26/img/table-icon.gif)](https://www.ncbi.nlm.nih.gov/sites/books/NBK25497/table/chapter2.T._entrez_unique_identifiers_ui/?report=objectonly)

### [Table 1](https://www.ncbi.nlm.nih.gov/sites/books/NBK25497/table/chapter2.T._entrez_unique_identifiers_ui/?report=objectonly)

– Entrez Unique Identifiers (UIDs) for selected databases

## Accessing Sequence Records Using Accession.Version Identifiers

NCBI now uses the accession.version identifier rather that the GI number (UID) as the primary identifier for nucleotide and protein sequence records (records in the nuccore, nucest, nucgss, popset, and protein databases). Even so, the E-utilities continue to provide access to these records using either GI numbers or accession.version identifiers. Those E-utilities that accept UIDs as input will also accept accession.version identifiers (for the sequence databases listed above). Those E-utilities that output UIDs can output accession.version identifiers instead by setting the &idtype parameter to “acc”. Finally, EFetch can retrieve *any* sequence record by its accession.version identifier, including sequences that do not have GI numbers. Please see [Chapter 4](https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter4/) for more details about how each E-utility handles accession.version identifers.

## The Entrez Core Engine: EGQuery, ESearch, and ESummary

The core of Entrez is an engine that performs two basic tasks for any Entrez database: 1) assemble a list of UIDs that match a text query, and 2) retrieve a brief summary record called a Document Summary (DocSum) for each UID. These two basic tasks of the Entrez engine are performed by ESearch and ESummary. ESearch returns a list of UIDs that match a text query in a given Entrez database, and ESummary returns DocSums that match a list of input UIDs. A text search in web Entrez is equivalent to ESearch-ESummary. EGQuery is a global version of ESearch that searches all Entrez databases simultaneously. Because these three E-utilities perform the two core Entrez functions, they function for all Entrez databases.

    egquery.fcgi?term=query
    esearch.fcgi?db=database&term=query
    esummary.fcgi?db=database&id=uid1,uid2,uid3,...

## Syntax and Initial Parsing of Entrez Queries

Text search strings entered into the Entrez system are converted into Entrez queries with the following format:

term1\[field1\] **Op** term2\[field2\] **Op** term3\[field3\] **Op** ...

where the terms are search terms, each limited to a particular Entrez field in square brackets, combined using one of three Boolean operators: Op = AND, OR, or NOT. These Boolean operators must be typed in all capital letters.

Example: human\[organism\] AND topoisomerase\[protein name\]

Entrez initially splits the query into a series of items that were originally separated by spaces in the query; therefore it is critical that spaces separate each term and Boolean operator. If the query consists *only* of a list of UID numbers (unique identifiers) or accession numbers, the Entrez system simply returns the corresponding records and no further parsing is performed. If the query contains any Boolean operators (AND, OR, or NOT), the query is split into the terms separated by these operators, and then each term is parsed independently. The results of these searches are then combined according to the Boolean operators.

A full account of how to search Entrez can be found in the [Entrez Help Document](https://www.ncbi.nlm.nih.gov/sites/books/n/helpentrez/EntrezHelp/). Additional information is available from [Entrez Help](https://www.ncbi.nlm.nih.gov/sites/books/n/helpentrez/).

## Entrez Databases: EInfo, EFetch, and ELink

The NCBI Entrez system currently contains 38 databases. EInfo provides detailed information about each database, including lists of the indexing fields in the database and the available links to other Entrez databases.

    einfo.fcgi?db=database

Each Entrez database includes two primary enhancements to the raw data records: 1) software for producing a variety of display formats appropriate to the given database, and 2) links to records in other Entrez databases manifested as lists of associated UIDs. The display format function is performed by EFetch, which generates formatted output for a list of input UIDs. For example, EFetch can produce abstracts from Entrez PubMed or FASTA format from Entrez Protein. EFetch does not yet support all Entrez databases; please see the [EFetch documentation](https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter4/#chapter4.EFetch) for details.

    efetch.fcgi?db=database&id=uid1,uid2,uid3&rettype=report_type&retmode=
    data_mode

The linking function is performed by ELink, which generates a list of UIDs in a specified Entrez database that are linked to a set of input UIDs in either the same or another database. For example, ELink can find Entrez SNP records linked to records in Entrez Nucleotide, or Entrez Domain records linked to records in Entrez Protein.

    elink.fcgi?dbfrom=initial_databasedb=target_database&id=uid1,uid2,uid3

## Using the Entrez History Server

A powerful feature of the Entrez system is that it can store retrieved sets of UIDs temporarily on the servers so that they can be subsequently combined or provided as input for other E-utility calls. The Entrez History server provides this service and is accessed on the Web using either the Preview/Index or History tabs on Entrez search pages. Each of the E-utilities can also use the History server, which assigns each set of UIDs an integer label called a query key (&query_key) and an encoded cookie string called a Web environment (&WebEnv). EPost allows any list of UIDs to be uploaded to the History Server and returns the query key and Web environment. ESearch can also post its output set of UIDs to the History Server, but only if the &usehistory parameter is set to “y”. ELink also can post its output to the History server if &cmd is set to "neighbor_history". The resulting query key and Web environment from either EPost or ESearch can then be used in place of a UID list in ESummary, EFetch, and ELink.

In Entrez, a set of UIDs is represented on the History by three parameters:

    &db = database; &query_key = query key; &WebEnv = web environment

Upload steps that generate a web environment and query key

    esearch.fcgi?db=database&term=query&usehistory=y

    epost.fcgi?db=database&id=uid1,uid2,uid3,...

    elink.fcgi?dbfrom=source_db&db=destination_db&cmd=neighbor_history&id=
    uid1,uid2,...

Download steps that use a web environment and query key

    esummary.fcgi?db=database&WebEnv=webenv&query_key=key

    efetch.fcgi?db=database&WebEnv=webenv&query_key=key&rettype=
    report_type&retmode=data_mode

Link step that uses a web environment and query key

    elink.fcgi?dbfrom=initial_databasedb=target_database&WebEnv=
    webenv&query_key=key

Search step that uses a web environment and a query key in the &term parameter (preceded by \#, encoded as %23)

    esearch.fcgi?db=database&term=%23key+AND+query&WebEnv=webenv&usehistory=y

## Generating Multiple Data Sets on the History Server

Each web environment on the History Server can be associated with any number of query keys. This allows different data sets to be combined with the Boolean operators AND, OR, and NOT, or with another Entrez query. It is important to remember that for two data sets (query keys) to be combined, they must be associated with the same web environment. By default, successive E-utility calls produce query keys that are *not* associated with the same web environment, and so to overcome this, each E-utility call after the initial call must set the &WebEnv parameter to the value of the pre-existing web environment.

Default behavior: These two URLs…

    URL 1: epost.fcgi?db=database&id=uid1,uid2,uid3
    URL 2: esearch.fcgi?db=database&term=query&usehistory=y

will produce two History sets associated with different web environments:

    URL   WebEnv     query_key        UIDs
    1      web1          1        uid1,uid2,uid3
    2      web2          1        uids matching query

Desired behavior: These two URLs…

    URL 1: epost.fcgi?db=database&id=uid1,uid2,uid3
    (extract web1 from the output of URL 1)
    URL 2: esearch.fcgi?db=database&term=query&usehistory=y&WebEnv=web1

will produce two sets associated with the same (new) web environment:

    URL   WebEnv      query_key        UIDs
    1      web2          1        uid1,uid2,uid3
    2      web2          2        uids matching query
