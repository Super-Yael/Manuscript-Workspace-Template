---
title: "Advanced Operations"
chapter: "Entrez Direct: E-utilities on the Unix Command Line"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter6/#chapter6.Advanced_Operations"
---
# Advanced Operations

## Text Modification

For custom editing, target and replacement strings are set with **‑reg** and **‑exp**, respectively. Regular expression text matching and substitution is then performed on an element with a **‑replace** command:

      xtract  …  -reg "-" -exp "." -replace Phone

## Value Substitution

External values can be loaded by reading a two-column precomputed file or ad hoc conversion table with **‑transform**. Lookup is then requested by applying **‑translate** to an element:

      xtract -transform accn-to-uid.txt  …  -translate Accession

      xtract -transform <( echo -e "Genomic\t1\nCoding\t2\nProtein\t3\n" )  …

## Multi-Step Transformations

Although xtract provides ‑element derivatives to do simple data manipulation, more complex tasks may be broken up into a series of simpler transformations, or "processing chains".

BioSample document summaries:

      efetch -db biosample -id SAMN38051082 -format docsum |

store preferred qualifier names in a "harmonized_name" XML attribute:

      <Attribute harmonized_name="strain">BALB/c</Attribute>
      <Attribute harmonized_name="isolate">Mtb infected Spleen MZB-2</Attribute>
      <Attribute harmonized_name="geo_loc_name">Singapore</Attribute>

Piping the data to a first xtract command, and using the "**@**" sign to select the attribute:

      xtract -rec BioSampleInfo -pattern DocumentSummary \
        -wrp Accession -element Accession \
        -group Attribute -if @harmonized_name \
          -TAG -lower @harmonized_name -wrp "&TAG" -element Attribute |

generates an intermediate form, with XML tag names taken from the original XML attributes:

      <BioSampleInfo>
        <Accession>SAMN38051082</Accession>
        <strain>BALB/c</strain>
        <isolate>Mtb infected Spleen MZB-2</isolate>
        <geo_loc_name>Singapore</geo_loc_name>
        …

Desired fields can then be selected by name in a second xtract command:

      xtract -pattern BioSampleInfo -def "-" -first Accession \
        geo_loc_name strain isolate

## Parsing XML Elements

GFF3 can be normalized with **gff‑sort**, and then converted to XML with **tbl2xml**, which gets field names from the remaining arguments (or, with **‑header**, from the first row of the input data):

      tbl2xml -rec Rec SeqID Source Type Start End Score Strand Phase Attributes |

The Attributes element consists of multiple clauses that are delimited by semicolons:

      <Attributes>ID=gene-XXXX_016554;Name=XXXX_016554; … </Attributes>

Piping to xtract creates a container, and uses **‑with** and **‑split** to parse the Attribute field:

      xtract -pattern Rec -pkg Context -wrp Item -with ";" -split Attributes |

into individual "**tag = value**" elements within the new package:

       <Context>
        <Item>ID=gene-XXXX_016554</Item>
        <Item>Name=XXXX_016554</Item>
        …

A second xtract can now use element suffix and prefix removal, respectively, to isolate the tag and value. The tag is saved in a variable to become the name of a new XML object in which the value is stored:

      xtract -pattern Context -pkg Fields -block Item \
        -TAG "Item[|=]" -wrp "&TAG" -element "Item[=|]" |

The final XML can be queried by field names that were extracted from the original Attributes clauses:

      <Fields>
        <ID>gene-XXXX_016554</ID>
        <Name>XXXX_016554</Name>
        …

## XML Namespaces

Namespace prefixes are followed by a colon, while a leading colon matches any prefix:

      nquire -url https://webservice.wikipathways.org getPathway -pwId WP455 |
      xtract -pattern "ns1:getPathwayResponse" -decode ":gpml" |

The embedded Graphical Pathway Markup Language object can then be processed:

      xtract -pattern Pathway -block Xref \
        -if @Database -equals "Entrez Gene" -tab "\n" -element @ID

## Record Filtering

The **filter‑records** script can extract an arbitrary range of text records using **‑min** and **‑max**:

      filter-records -pattern "<PubmedArticle>" -min 13 -max 24

It also has arguments to **‑require** or **‑exclude** specific text content.

## Sorting or Partitioning Sets of Records

To sort XML records by a particular field, pass the element name to xtract **‑sort‑fwd** or **‑sort‑rev**. Stable sorting, which preserves the relative order of records with identical sort key values, is provided by the **‑stable‑sort‑fwd** and **‑stable‑sort‑rev** commands:

      xtract -pattern PubmedArticle -sort-rev MedlineCitation/PMID

To partition XML records, give the number of records per output file to xtract **‑split‑by‑num**:

      xtract -set PubmedArticleSet -pattern PubmedArticle \
        -split-by-num 100 -prefix subset -suffix xml

or use the maximum byte size for each output file as the argument to xtract **‑split‑by‑len**:

      xtract -set PubmedArticleSet -pattern PubmedArticle \
        -split-by-len 1000000 -prefix subset -suffix xml

or make individual files by passing the record identifier's element name to xtract **‑split‑by‑id**:

      xtract -mixed -set pmc-articleset -pattern article \
        -split-by-id article-id -prefix PMC -suffix xml

Numbered output file names will be of the form "**subset001.xml**", "**subset002.xml**", etc.

To distribute text records into separate files, use **split‑records** with **‑by‑num** or **‑by‑len**.

## Viewing an XML Hierarchy

Piping a PubmedArticle XML object to xtract **‑outline**:

      esearch -db pubmed -query "Cozzarelli NR [AUTH] AND Casadaban MJ [AUTH]" |
      efetch -format xml | xtract -outline 3

will give an indented overview of the XML hierarchy, optionally limited to a specified object depth:

      PubmedArticle
        MedlineCitation
          PMID
          DateCompleted
          DateRevised
          Article
          MedlineJournalInfo
          ChemicalList
          CitationSubset
          MeshHeadingList
        PubmedData
        …

Using xtract **‑synopsis** or **‑contour** will show the full paths to all nodes or just the terminal (leaf) nodes, respectively. Piping those results to **sort‑uniq‑count** will produce a table of unique paths.

Use a **caret** ("**^**") as an element argument prefix to print its absolute depth in the XML hierarchy:

      xtract -pattern PubmedArticle -element "^PMID"

## Code Nesting Comparison

Sketching with indented pseudo code can clarify relative nesting levels. The extraction command:

      xtract -pattern PubmedArticle \
        -block Author -element Initials,LastName \
        -block MeshHeading \
          -if QualifierName \
            -element DescriptorName \
            -subset QualifierName -element QualifierName

where the rank of the argument name controls the nesting depth, could be represented as a computer program in pseudo code by:

      for pat = each PubmedArticle {
        for blk = each pat.Author {
          print blk.Initials blk.LastName
        }
        for blk = each pat.MeSHTerm {
          if blk.Qual is present {
            print blk.MeshName
            for sbs = each blk.Qual {
              print sbs.QualName
            }
          }
        }
      }

where the brace indentation count controls the nesting depth.

Extra arguments are held in reserve to provide additional levels of organization, should the need arise in the future for processing complex, deeply-nested XML data. The full set of exploration commands below ‑pattern, in order of rank, are:

      -path
        -division
          -group
            -branch
              -block
                -section
                  -subset
                    -unit

Starting xtract exploration with ‑block, and expanding with ‑group and ‑subset, leaves additional level names that can be used wherever needed without having to redesign the entire command.
