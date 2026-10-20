---
title: "Downloading Document Summaries"
chapter: "E-utilities Quick Start"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter1/#chapter1.Downloading_Document_Summaries"
---
# Downloading Document Summaries

## Basic Downloading

    esummary.fcgi?db=<database>&id=<uid_list>

Input: List of UIDs (&id); Entrez database (&db)

Output: XML DocSums

*Example: Download DocSums for these protein GIs: 6678417,9507199,28558982,28558984,28558988,28558990*

<https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=protein&id=6678417,9507199,28558982,28558984,28558988,28558990>

## Downloading Data From a Previous Search

    esearch.fcgi?db=<database>&term=<query>&usehistory=y

    # esearch produces WebEnv value ($web1) and QueryKey value ($key1)

    esummary.fcgi?db=<database>&query_key=$key1&WebEnv=$web1

Input: Web environment (&WebEnv) and query key (&query_key) representing a set of Entrez UIDs on the Entrez history server

Output: XML DocSums

## Sample ESummary Output

The output of ESummary is a series of XML “DocSums” (Document Summaries), the format of which depends on the database. Below is an example DocSum for Entrez Protein.

    <?xml version="1.0"?>
    <!DOCTYPE eSummaryResult PUBLIC "-//NLM//DTD eSummaryResult, 29 October
     2004//EN" "https://www.ncbi.nlm.nih.gov/entrez/query/DTD/eSummary_
    041029.dtd">
    <eSummaryResult>
    <DocSum>
    <Id>15718680</Id>
    <Item Name="Caption" Type="String">NP_005537</Item>
    <Item Name="Title" Type="String">IL2-inducible T-cell kinase [Homo
     sapiens]</Item>
    <Item Name="Extra" 
    Type="String">gi|15718680|ref|NP_005537.3|[15718680]</Item>
    <Item Name="Gi" Type="Integer">15718680</Item>
    <Item Name="CreateDate" Type="String">1999/06/09</Item>
    <Item Name="UpdateDate" Type="String">2009/04/05</Item>
    <Item Name="Flags" Type="Integer">512</Item>
    <Item Name="TaxId" Type="Integer">9606</Item>
    <Item Name="Length" Type="Integer">620</Item>
    <Item Name="Status" Type="String">live</Item>
    <Item Name="ReplacedBy" Type="String"></Item>
    <Item Name="Comment" Type="String"><![CDATA[  ]]></Item>
    </DocSum>
    </eSummaryResult>

## Sample ESummary version 2.0 Output

Version 2.0 of ESummary is an alternate XML presentation of Entrez DocSums. To retrieve version 2.0 DocSums, the URL should contain the &version parameter with an assigned value of ‘2.0’. Each Entrez database provides its own unique DTD for version 2.0 DocSums, and a link to the relevant DTD is provided in the header of the version 2.0 XML.

    esummary.fcgi?db=<database>&id=<uid_list>&version=2.0

Below is an example version 2.0 DocSum from Entrez Protein (the same record as shown above in the default DocSum XML).

    <?xml version="1.0"?>
    <!DOCTYPE eSummaryResult PUBLIC "-//NLM//DTD eSummaryResult//EN" "https://www.ncbi.nlm.nih.gov/entrez/query/DTD/eSummaryDTD/eSummary_protein.dtd">
    <eSummaryResult>
        <DocumentSummarySet status="OK">
            <DocumentSummary uid="15718680">
                <Caption>NP_005537</Caption>
                <Title>tyrosine-protein kinase ITK/TSK [Homo sapiens]</Title>
                <Extra>gi|15718680|ref|NP_005537.3|</Extra>
                <Gi>15718680</Gi>

                <CreateDate>1999/06/09</CreateDate>
                <UpdateDate>2011/10/09</UpdateDate>
                <Flags>512</Flags>
                <TaxId>9606</TaxId>
                <Slen>620</Slen>

                <Biomol/>

                <MolType>aa</MolType>
                <Topology>linear</Topology>
                <SourceDb>refseq</SourceDb>
                <SegSetSize>0</SegSetSize>
                <ProjectId>0</ProjectId>
                <Genome>genomic</Genome>

                <SubType>chromosome|map</SubType>
                <SubName>5|5q31-q32</SubName>
                <AssemblyGi>399658</AssemblyGi>
                <AssemblyAcc>D13720.1</AssemblyAcc>
                <Tech/>
                <Completeness/>
                <GeneticCode>1</GeneticCode>

                <Strand/>
                <Organism>Homo sapiens</Organism>
                <Statistics>
                    <Stat type="all" count="8"/>
                    <Stat type="blob_size" count="16154"/>
                    <Stat type="cdregion" count="1"/>
                    <Stat type="cdregion" subtype="CDS" count="1"/>
                    <Stat type="gene" count="1"/>
                    <Stat type="gene" subtype="Gene" count="1"/>
                    <Stat type="org" count="1"/>
                    <Stat type="prot" count="1"/>
                    <Stat type="prot" subtype="Prot" count="1"/>
                    <Stat type="pub" count="14"/>
                    <Stat type="pub" subtype="PubMed" count="10"/>
                    <Stat type="pub" subtype="PubMed/Gene-rif" count="4"/>
                    <Stat type="site" count="4"/>
                    <Stat type="site" subtype="Site" count="4"/>
                    <Stat source="CDD" type="all" count="15"/>
                    <Stat source="CDD" type="region" count="6"/>
                    <Stat source="CDD" type="region" subtype="Region" count="6"/>
                    <Stat source="CDD" type="site" count="9"/>
                    <Stat source="CDD" type="site" subtype="Site" count="9"/>
                    <Stat source="HPRD" type="all" count="3"/>
                    <Stat source="HPRD" type="site" count="3"/>
                    <Stat source="HPRD" type="site" subtype="Site" count="3"/>
                    <Stat source="SNP" type="all" count="31"/>
                    <Stat source="SNP" type="imp" count="31"/>
                    <Stat source="SNP" type="imp" subtype="variation" count="31"/>
                    <Stat source="all" type="all" count="57"/>
                    <Stat source="all" type="blob_size" count="16154"/>
                    <Stat source="all" type="cdregion" count="1"/>
                    <Stat source="all" type="gene" count="1"/>
                    <Stat source="all" type="imp" count="31"/>
                    <Stat source="all" type="org" count="1"/>
                    <Stat source="all" type="prot" count="1"/>
                    <Stat source="all" type="pub" count="14"/>
                    <Stat source="all" type="region" count="6"/>
                    <Stat source="all" type="site" count="16"/>
                </Statistics>
                <AccessionVersion>NP_005537.3</AccessionVersion>
                <Properties aa="2">2</Properties>
                <Comment/>
                <OSLT indexed="yes">NP_005537.3</OSLT>
                <IdGiClass mol="3" repr="2" gi_state="10" sat="4" sat_key="58760802" owner="20"
                    sat_name="NCBI" owner_name="NCBI-Genomes" defdiv="GNM" length="620" extfeatmask="41"
                />
            </DocumentSummary>

        </DocumentSummarySet>
    </eSummaryResult>
