---
title: "Release Notes"
chapter: "The E-utilities In-Depth: Parameters, Syntax and More"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter4/#chapter4.Release_Notes"
---
# Release Notes

## EFetch; ELink JSON ouput: June 24, 2015

- EFetch now supports ClinVar and GTR
- ELink now provides output in JSON format

## ESearch &sort; JSON output format: February 14, 2014

- ESearch now provides a supported **sort** parameter
- EInfo, ESearch and ESummary now provide output data in JSON format

## ECitMatch, EInfo Version 2.0, EFetch: August 9, 2013

- ECitMatch is a new E-utility that serves as an API to the PubMed [batch citation matcher](https://www.ncbi.nlm.nih.gov/pubmed/batchcitmatch)
- EInfo has an updated XML output that includes two new fields: \<IsTruncatable\> and \<IsRangeable\>
- EFetch now supports the BioProject database.

## EFetch Version 2.0. Target release date: February 15, 2012

- EFetch now supports the following databases: biosample, biosystems and sra
- EFetch now has defined default values for &retmode and &rettype for all supported databases (please see [Table 1](https://www.ncbi.nlm.nih.gov/sites/books/NBK25499/table/chapter4.T._valid_values_of__retmode_and/?report=objectonly) for all supported values of these parameters)
- EFetch no longer supports &retmode=html; requests containing &retmode=html will return data using the default &retmode value for the specified database (&db)
- EFetch requests including &rettype=docsum return XML data equivalent to ESummary output

## Release of new Genome database: November 9, 2011

- Entrez Genome has been completely redesigned, and database records now correspond to a species rather than an individual chromosome sequence. Please see full details of the change at <https://www.ncbi.nlm.nih.gov/About/news/17Nov2011.html>
- Old Genome IDs are no longer valid. A file is available on the NCBI FTP site that maps old Genome IDs to Nucleotide GIs: [ftp.ncbi.nih.gov/genomes/old_genomeID2nucGI](ftp://ftp.ncbi.nih.gov/genomes/old_genomeID2nucGI)
- EFetch no longer supports retrievals from Genome (db=genome).
- The ESummary XML for Genome has been recast to reflect the new data model.
- To view the new search fields and links supported for the new Genome database, please see <https://eutils.ncbi.nlm.nih.gov/entrez/eutils/einfo.fcgi?db=genome>

## ESummary Version 2.0. November 4, 2011

- ESummary now supports a new, alternative XML presentation for Entrez document summaries (DocSums). The new XML is unique to each Entrez database and generally contains more extensive data about the record than the original DocSum XML.
- There are no plans at present to discontinue the original DocSum XML, so developers can continue to use this presentation, which will remain the default.
- Version 2.0 XML is returned when &version=2.0 is included in the ESummary URL.
