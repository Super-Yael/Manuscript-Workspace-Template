---
title: "Getting Database Statistics and Search Fields"
chapter: "E-utilities Quick Start"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter1/#chapter1.Getting_Database_Statistics_and"
---
# Getting Database Statistics and Search Fields

    einfo.fcgi?db=<database>

Input: Entrez database (&db)

Output: XML containing database statistics

*Note: If no database parameter is supplied, einfo will return a list of all valid Entrez databases.*

*Example: Find database statistics for Entrez Protein.*

<https://eutils.ncbi.nlm.nih.gov/entrez/eutils/einfo.fcgi?db=protein>

## For More Information

Please see [EInfo In-Depth](https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter4/#chapter4.EInfo) for a full description of EInfo.

## Sample EInfo Output

    <?xml version="1.0"?>
    <!DOCTYPE eInfoResult PUBLIC "-//NLM//DTD eInfoResult, 11 May 2002//EN" 
    "https://www.ncbi.nlm.nih.gov/entrez/query/DTD/eInfo_020511.dtd">
    <eInfoResult>
    <DbInfo>
    <DbName>protein</DbName>
    <MenuName>Protein</MenuName>
    <Description>Protein sequence record</Description>
    <Count>26715092</Count>
    <LastUpdate>2009/05/12 04:39</LastUpdate>
    <FieldList>
    <Field>
    <Name>ALL</Name>
    <FullName>All Fields</FullName>
    <Description>All terms from all searchable fields</Description>
    <TermCount>133639432</TermCount>
    <IsDate>N</IsDate>
    <IsNumerical>N</IsNumerical>
    <SingleToken>N</SingleToken>
    <Hierarchy>N</Hierarchy>
    <IsHidden>N</IsHidden>
    </Field>
    ...
    <Field>
    <Name>PORG</Name>
    <FullName>Primary Organism</FullName>
    <Description>Scientific and common names 
    of primary organism, and all higher levels of taxonomy</Description>
    <TermCount>673555</TermCount>
    <IsDate>N</IsDate>
    <IsNumerical>N</IsNumerical>
    <SingleToken>Y</SingleToken>
    <Hierarchy>Y</Hierarchy>
    <IsHidden>N</IsHidden>
    </Field>
    </FieldList>
    <LinkList>
    <Link>
    <Name>protein_biosystems</Name>
    <Menu>BioSystem Links</Menu>
    <Description>BioSystems</Description>
    <DbTo>biosystems</DbTo>
    </Link>
    ...
    <Link>
    <Name>protein_unigene</Name>
    <Menu>UniGene Links</Menu>
    <Description>Related UniGene records</Description>
    <DbTo>unigene</DbTo>
    </Link>
    </LinkList>
    </DbInfo>
    </eInfoResult>
