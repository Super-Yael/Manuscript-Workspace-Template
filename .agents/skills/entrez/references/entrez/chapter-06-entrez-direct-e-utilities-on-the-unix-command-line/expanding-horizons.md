---
title: "Expanding Horizons"
chapter: "Entrez Direct: E-utilities on the Unix Command Line"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter6/#chapter6.Expanding_Horizons"
---
# Expanding Horizons

The nquire program uses command-line arguments to obtain data from external RESTful, CGI, or FTP servers. (Xtract can read JSON, ASN.1, and GenBank formats directly, but previously-required conversion commands - now for inspecting XML or overriding defaults - are shown below in light text.)

## JSON Arrays

Human β‑globin information from a Scripps Research data integration project (4):

      nquire -get https://mygene.info/v3 gene 3043 | json2xml |

contains a multi-dimensional JavaScript Object Notation array of exon coordinates:

      "position": [
        [ 5225463, 5225726 ],
        [ 5226576, 5226799 ],
        [ 5226929, 5227071 ]
      ],
      "strand": -1,

Conversion to XML assigns distinct tag names to each level with the json2xml **‑nest element** default:

      <position>
        <position_E>5225463</position_E>
        <position_E>5225726</position_E>
      </position>
      …

## Heterogeneous Data

A query for the human green-sensitive opsin gene:

      nquire -get https://mygene.info/v3/gene/2652 | json2xml |

returns data containing a heterogeneous mixture of objects in the pathway section:

      <pathway>
        <reactome>
          <id>R-HSA-162582</id>
          <name>Signal Transduction</name>
        </reactome>
        …
        <wikipathways>
          <id>WP455</id>
          <name>GPCRs, Class A Rhodopsin-like</name>
        </wikipathways>
      </pathway>

The **parent / star** construct is used to visit the individual components of a parent object without needing to explicitly specify their names. For printing, the name of a child object is indicated by a **question mark** ("**?**"), while a **tilde** ("**~**") would return the anonymous object's value:

      xtract -pattern opt -group "pathway/*" \
        -pfc "\n" -element "?,name,id"

This displays a table of pathway database references:

      reactome        Signal Transduction                R-HSA-162582
      reactome        Disease                            R-HSA-1643685
      …
      reactome        Diseases of the neuronal system    R-HSA-9675143
      wikipathways    GPCRs, Class A Rhodopsin-like      WP455

## Exhaustive Exploration

PubMed Central full-text records consist of recursive "sec" objects that contain section title and paragraph text elements. A record obtained in XML format:

      esearch -db pmc -query "Kitts PA [AUTH] AND type strains [TITL]" |
      efetch -format xml |

is first processed by xtract **‑mask**, to remove complex formula and table mark-up instructions:

      xtract -mixed -pattern article -mask "table-wrap,alternatives,inline-formula,\
      disp-formula,pub-history,related-article,list-item,fig" -element "*" |

Extracting the title and abstract fields near the front of the document is straightforward:

      xtract -mixed -rec PMCData -pattern article \
        -division front \
          -wrp Title -prose title-group/article-title \
          -wrp Abstract -prose abstract/p \

The full text is obtained by exhaustive exploration using the **parent / double star** construct:

        -division "body/**" \

Multiple **‑if** clauses use a **question mark** to test the child object's name and select only paragraph and title elements. A **caret** returns the nesting depth of the element:

          -if "?" -equals "p" -pkg Paragraph \
            -wrp Level -element "^" -wrp Text -prose p \
          -if "?" -equals "title" -pkg Section \
            -wrp Level -element "^" -wrp Title -prose sec/title

Like **‑else**, the multiple **‑if** convention can only be used for element extraction operations. Multiple explorations below the double star would require the use of individual **‑group "\*"** commands.

      <PMCData>
        <Title>Collection and curation of prokaryotic genome assemblies … </Title>
        <Abstract>The public sequence databases are entrusted with the … </Abstract>
        …
        <Section>
          <Level>5</Level>
          <Title>Assemblies not used as types</Title>
        </Section>
        <Paragraph>
          <Level>5</Level>
          <Text>NCBI evaluates all assemblies, including type assemblies … </Text>
        </Paragraph>
        …

## GenBank Filtering

The most recent GenBank virus release file can be downloaded from NCBI servers:

      nquire -lst ftp.ncbi.nlm.nih.gov genbank |
      grep "^gbvrl" | grep ".seq.gz" | sort -V |
      tail -n 1 | skip-if-file-exists |
      nquire -dwn ftp.ncbi.nlm.nih.gov genbank

GenBank flatfile records can be selected by organism name or taxon identifier, or by presence or absence of an arbitrary text string, with **filter-genbank**:

      gunzip -c *.seq.gz | filter-genbank -taxid 11292 |

The full set of filter‑genbank arguments are **‑accession**, **‑accessions**, **‑taxid**, **‑taxids**, **‑organism**, **‑truncate**, **‑exclude**, **‑require**, **‑min**, and **‑max**.

While GenBank format can be read directly by xtract, explicit conversion to INSDSeq XML with **gbf2xml** may be up to three times faster for large sets of records:

      gbf2xml |

Feature location intervals and underlying sequences of individual coding regions are then obtained by:

      xtract -insd CDS gene product feat_location sub_sequence

## Table Operations

Tab-delimited tables can be piped through **filter‑columns** for numeric and substring matching:

      filter-columns '10 <= $2 && $2 <= 30 && $5 ~ peptide'

and sent to **print‑columns** for flexible modification of text and numbers in the final output:

      print-columns '$1, $2+1, $3+$4-1, "\042" $5 "\042", tolower($6), total += $2'

Both scripts are front-ends to the **awk** data manipulation utility. In awk, a **dollar sign** ("**\$**") followed by a digit indicates an input data column, not a Unix command-line argument position.

In order to prevent misinterpretation of awk dollar signs by the Unix shell interpreter, both scripts require their argument to be inside apostrophes instead of double quotation marks. The standard NF and NR awk variables can be used, as can YR (for year) and DT (for date in YYYY‑MM‑DD format).

Along with **sort‑table**, these scripts allow novice users to do useful things on tabular data without first having to know arcane setup details (such as how to specify the tab character as the column separator).

The **align‑columns** script has several arguments to reformat tables and make them easier to interpret.

The **intersect‑uids**, **combine‑uids**, and **exclude‑uids** scripts merge unique identifier files with Boolean operations (AND, OR, and NOT, respectively). Use **compare‑uids** to see UID differences.
