---
title: "Searching a Database"
chapter: "E-utilities Quick Start"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter1/#chapter1.Searching_a_Database"
---
# Searching a Database

## Basic Searching

    esearch.fcgi?db=<database>&term=<query>

Input: Entrez database (&db); Any Entrez text query (&term)

Output: List of UIDs matching the Entrez query

*Example: Get the PubMed IDs (PMIDs) for articles about breast cancer published in Science in 2008*

[https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=science\[journal\]+AND+breast+cancer+AND+2008\[pdat\]](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=science%5bjournal%5d+AND+breast+cancer+AND+2008%5bpdat%5d)

## Storing Search Results

    esearch.fcgi?db=<database>&term=<query>&usehistory=y

Input: Any Entrez text query (&term); Entrez database (&db); &usehistory=y

Output: Web environment (&WebEnv) and query key (&query_key) parameters specifying the location on the Entrez history server of the list of UIDs matching the Entrez query

*Example: Get the PubMed IDs (PMIDs) for articles about breast cancer published in Science in 2008, and store them on the Entrez history server for later use*

[https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=science\[journal\]+AND+breast+cancer+AND+2008\[pdat\]&usehistory=y](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=science%5bjournal%5d+AND+breast+cancer+AND+2008%5bpdat%5d&usehistory=y)

## Associating Search Results with Existing Search Results

    esearch.fcgi?db=<database>&term=<query1>&usehistory=y

    # esearch produces WebEnv value ($web1) and QueryKey value ($key1) 

    esearch.fcgi?db=<database>&term=<query2>&usehistory=y&WebEnv=$web1

    # esearch produces WebEnv value ($web2) that contains the results 
    of both searches ($key1 and $key2)

Input: Any Entrez text query (&term); Entrez database (&db); &usehistory=y; Existing web environment (&WebEnv) from a prior E-utility call

Output: Web environment (&WebEnv) and query key (&query_key) parameters specifying the location on the Entrez history server of the list of UIDs matching the Entrez query

## For More Information

Please see [ESearch In-Depth](https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter4/#chapter4.ESearch) for a full description of ESearch.

## Sample ESearch Output

    <?xml version="1.0" ?>
    <!DOCTYPE eSearchResult PUBLIC "-//NLM//DTD eSearchResult, 11 May 2002//EN"
     "https://www.ncbi.nlm.nih.gov/entrez/query/DTD/eSearch_020511.dtd">
    <eSearchResult>
    <Count>255147</Count>   # total number of records matching query
    <RetMax>20</RetMax># number of UIDs returned in this XML; default=20
    <RetStart>0</RetStart># index of first record returned; default=0
    <QueryKey>1</QueryKey># QueryKey, only present if &usehistory=y
    <WebEnv>0l93yIkBjmM60UBXuvBvPfBIq8-9nIsldXuMP0hhuMH-
    8GjCz7F_Dz1XL6z@397033B29A81FB01_0038SID</WebEnv> 
                      # WebEnv; only present if &usehistory=y
          <IdList>
    <Id>229486465</Id>    # list of UIDs returned
    <Id>229486321</Id>
    <Id>229485738</Id>
    <Id>229470359</Id>
    <Id>229463047</Id>
    <Id>229463037</Id>
    <Id>229463022</Id>
    <Id>229463019</Id>
    <Id>229463007</Id>
    <Id>229463002</Id>
    <Id>229463000</Id>
    <Id>229462974</Id>
    <Id>229462961</Id>
    <Id>229462956</Id>
    <Id>229462921</Id>
    <Id>229462905</Id>
    <Id>229462899</Id>
    <Id>229462873</Id>
    <Id>229462863</Id>
    <Id>229462862</Id>
    </IdList>
    <TranslationSet>        # details of how Entrez translated the query
        <Translation>
         <From>mouse[orgn]</From>
         <To>"Mus musculus"[Organism]</To>
        </Translation>
    </TranslationSet>
    <TranslationStack>
       <TermSet>
        <Term>"Mus musculus"[Organism]</Term>
        <Field>Organism</Field>
        <Count>255147</Count>
        <Explode>Y</Explode>
       </TermSet>
       <OP>GROUP</OP>
    </TranslationStack>
    <QueryTranslation>"Mus musculus"[Organism]</QueryTranslation>
    </eSearchResult>

## Searching PubMed with Citation Data

    ecitmatch.cgi?db=pubmed&rettype=xml&bdata=<citations>

Input: List of citation strings separated by a carriage return (%0D), where each citation string has the following format:

journal_title\|year\|volume\|first_page\|author_name\|your_key\|

*Output: A list of citation strings with the corresponding PubMed ID (PMID) appended.*

*Example: Search PubMed for the following ciations:*

Art1: Mann, BJ. (1991) *Proc. Natl. Acad. Sci. USA.* 88:3248

Art2: Palmenberg, AC. (1987) *Science* 235:182

<https://eutils.ncbi.nlm.nih.gov/entrez/eutils/ecitmatch.cgi?db=pubmed&retmode=xml&bdata=proc+natl+acad+sci+u+s+a%7C1991%7C88%7C3248%7Cmann+bj%7CArt1%7C%0Dscience%7C1987%7C235%7C182%7Cpalmenberg+ac%7CArt2%7C>

Sample Output (the PMIDs appear in the rightmost field):

    proc natl acad sci u s a|1991|88|3248|mann bj|Art1|2014248
    science|1987|235|182|palmenberg ac|Art2|3026048

Please see [ECitMatch In-Depth](https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter4/#chapter4.ECitMatch) for a full description of ECitMatch.
