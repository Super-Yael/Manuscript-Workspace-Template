---
title: "Performing a Global Entrez Search"
chapter: "E-utilities Quick Start"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter1/#chapter1.Performing_a_Global_Entrez_Sear"
---
# Performing a Global Entrez Search

    egquery.fcgi?term=<query>

Input: Entrez text query (&term)

Output: XML containing the number of hits in each database.

*Example: Determine the number of records for mouse in Entrez.*

[https://eutils.ncbi.nlm.nih.gov/entrez/eutils/egquery.fcgi?term=mouse\[orgn\]](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/egquery.fcgi?term=mouse%5borgn%5d)

## For More Information

Please see [EGQuery In-Depth](https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter4/#chapter4.EGQuery) for a full description of EGQuery.

## Sample EGQuery Output

    <?xml version="1.0"?>
    <!DOCTYPE Result PUBLIC "-//NLM//DTD eSearchResult, January 2004//EN"
     "https://www.ncbi.nlm.nih.gov/entrez/query/DTD/egquery.dtd">
    <!--
            $Id: egquery_template.xml 106311 2007-06-26 14:46:31Z osipov $
    -->
    <!-- ================================================================= -->
    <Result>
            <Term>mouse[orgn]</Term>
            <eGQueryResult>
                 <ResultItem>
                      <DbName>pubmed</DbName>
                      <MenuName>PubMed</MenuName>
                      <Count>0</Count>
                      <Status>Term or Database is not found</Status>
                 </ResultItem>
                 <ResultItem>
                      <DbName>pmc</DbName>
                      <MenuName>PMC</MenuName>
                      <Count>3823</Count>
                      <Status>Ok</Status>
                 </ResultItem>
    ...
                 <ResultItem>
                      <DbName>nuccore</DbName>
                      <MenuName>Nucleotide</MenuName>
                      <Count>1739903</Count>
                      <Status>Ok</Status>
                 </ResultItem>
                 <ResultItem>
                      <DbName>nucgss</DbName>
                      <MenuName>GSS</MenuName>
                      <Count>2264567</Count>
                      <Status>Ok</Status>
                 </ResultItem>
                 <ResultItem>
                      <DbName>nucest</DbName>
                      <MenuName>EST</MenuName>
                      <Count>4852140</Count>
                      <Status>Ok</Status>
                 </ResultItem>
                 <ResultItem>
                      <DbName>protein</DbName>
                      <MenuName>Protein</MenuName>
                      <Count>255212</Count>
                      <Status>Ok</Status>
                 </ResultItem>
    ...
                 <ResultItem>
                      <DbName>proteinclusters</DbName>
                      <MenuName>Protein Clusters</MenuName>
                      <Count>13</Count>
                      <Status>Ok</Status>
                 </ResultItem>
            </eGQueryResult>
    </Result>
