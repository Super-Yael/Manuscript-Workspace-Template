---
title: "XML Data Extraction"
chapter: "Entrez Direct: E-utilities on the Unix Command Line"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter6/#chapter6.XML_Data_Extraction"
---
# XML Data Extraction

The ability to obtain Entrez records in structured format, and to easily extract the underlying data, allows the user to ask novel questions that are not addressed by existing analysis software.

The xtract program uses command-line arguments to direct the conversion of data in eXtensible Markup Language (XML) format. It allows record detection, path exploration, conditional processing, element selection, substring isolation, and report formatting to be controlled independently.

The advantage of XML is that information is in specific locations in a well-defined data hierarchy. Accessing individual units of data that are fielded by name, such as:

      <PubDate>2013</PubDate>
      <Source>PLoS One</Source>
      <Volume>8</Volume>
      <Issue>3</Issue>
      <Pages>e58144</Pages>

requires matching the same general pattern, differing only by the element name. This is much simpler than parsing the units from a long, complex string:

      1. PLoS One. 2013;8(3):e58144 …

The disadvantage of XML is that data extraction usually requires custom programming. But EDirect relies on the common pattern of XML value representation to provide a simplified approach to interpreting XML data.

The **‑pattern** (or **‑record**) command partitions an XML stream by object name into individual records that are processed separately. Within each record, the **‑element** command does an exhaustive, depth-first search to find data content by field name. For example:

      xtract -pattern ENTREZ_DIRECT -element Count

Neither explicit object paths nor complicated path formulas are needed for element identification.

## Format Customization

By default, the ‑pattern argument divides the results into rows, while placement of data into columns is controlled by ‑element, to create a tab-delimited table.

Formatting commands allow extensive customization of the output. The line break between ‑pattern rows is changed with **‑ret**, while the tab character between ‑element columns is modified by **‑tab**.

Multiple instances of the same element are distinguished using **‑sep**, which controls their separation independently of the ‑tab command. The following query:

      efetch -db pubmed -id 6271474,24178092 -format docsum |
      xtract -pattern DocumentSummary -sep "|" -element Id PubDate Name

returns a tab-delimited table with individual author names separated by vertical bars:

      6271474     1981        Casadaban MJ|Chou J|Lemaux P|Tu CP|Cohen SN
      24178092    1994 Dec    Garber ED|Ruddat M

The ‑sep value also applies to distinct ‑element arguments that are grouped with **commas**. This can be used to keep data from multiple related fields in the same column:

      -sep " " -element Initials,LastName

Groups of fields are preceded by the **‑pfx** value and followed by the **‑sfx** value, both of which are initially empty.

The **‑def** command sets a default placeholder to be printed when none of the comma-separated fields in an ‑element clause are present:

      -def "-" -sep " " -element Year,Month,MedlineDate

## Limit by Parent

An ‑element argument can use the **parent / child** construct to limit selection when items can only be disambiguated by position, not by name. In this case, it prevents the display of additional PMIDs that might be present inside CommentsCorrections objects deeper within the MedlineCitation container:

      xtract -pattern PubmedArticle -element MedlineCitation/PMID

## Element Variants

Derivatives of ‑element were initially created to avoid having to write post-processing scripts just to perform trivial modifications or integer calculations on extracted data. Other variants were added for content normalization, report formatting, or index generation. The commands are in several categories:

      Positional:       -first, -last, -even, -odd, -backward

      Numeric:          -num, -len, -inc, -dec, -mod, -bin, -hex, -bit

      Statistics:       -sum, -acc, -min, -max, -dev, -med

      Averages:         -avg, -geo, -hrm, -rms

      Logarithms:       -sqt, -lge, -lg2, -log

      Character:        -encode, -upper, -title, -mirror, -alpha, -alnum

      String:           -basic, -plain, -simple, -prose

      Text:             -words, -pairs, -letters, -split, -order, -reverse, -pentamers

      Citation:         -year, -month, -date, -auth, -initials, -page, -author, -journal

      Sequence:         -revcomp, -fasta, -ncbi2na, -molwt, -pept, -nucleic

      Translation:      -cds2prot, -gcode, -frame

      Coordinate:       -0-based, -1-based, -ucsc-based

      Variation:        -hgvs

      Frequency:        -histogram

      Expression:       -reg, -exp, -replace

      Substitution:     -transform, -translate

      Indexing:         -indexer, -aliases, -classify

      Miscellaneous:    -doi, -wct, -trim, -pad, -mask, -accession, -numeric

The original ‑element prefix shortcuts, "**\#**" and "**%**", are redirected to **‑num** and **‑len**, respectively.

See xtract **‑help** for a brief description of each command.

## Substring Extraction

Following an element name with square brackets allows subset selection by numeric range (with a colon between the character start and stop positions), or permits removal of leading and trailing text (with a vertical bar \[or caret\] separating the required \[or optional\] interior prefix and suffix endpoints):

      -author Initials[1:1] -numeric "ArticleId[PMC|]" -upper "Accession[^.]"

## XML Repackaging

Repackaging commands (**‑wrp**, **‑enc**, and **‑pkg**) wrap extracted data values with bracketed XML tags given only the object name. For example, "‑wrp Word" issues the following formatting instructions:

      -pfx "<Word>" -sep "</Word><Word>" -sfx "</Word>"

It also sets an internal flag to ensure that data values containing encoded symbols (ampersands, angle brackets, apostrophes, and quotation marks) remain properly encoded inside the new XML.

Combining **‑**wrp commands and **‑**element variants can break up complex tasks into a series of simpler operations. No custom reading or writing code is needed, since the data remains in XML format.

## Generating Attributes

Additional commands (**‑tag**, **‑att**, **‑atr**, **‑cls**, **‑slf**, and **‑end**) allow generation of XML tags with attributes. The following will produce regular and self-closing XML objects, respectively:

      -tag Item -att type journal -cls -element Source -end Item

      <Item type="journal">J Bacteriol</Item>

      -tag Item -att type journal -atr name Source -slf

      <Item type="journal" name="J Bacteriol" />

## Exploration Control

Exploration commands control the order in which XML record contents are examined, by separately presenting each instance of the chosen subregion. This limits what subsequent commands "see" at any one time, and can allow related fields in an object to be kept together in the output.

Unlike the simpler DocumentSummary format, records retrieved as PubmedArticle XML:

      efetch -db pubmed -id 1413997 -format xml |

have authors with separate fields for last name and initials:

      <Author>
        <LastName>Mortimer</LastName>
        <Initials>RK</Initials>
      </Author>

Without being given any guidance about context, an ‑element command on initials and last names:

      xtract -pattern PubmedArticle -element Initials LastName

will explore the current record for each argument in turn, printing all initials followed by all last names:

      RK    CR    JS    Mortimer    Contopoulou    King

Inserting a **‑block** command adds a new exploration layer between ‑pattern and ‑element , which redirects data exploration to present the authors one at a time:

      xtract -pattern PubmedArticle -block Author -element Initials LastName

Each time through the loop, the ‑element command only sees the current author's values. This restores the correct association of initials and last names in the output:

      RK    Mortimer    CR    Contopoulou    JS    King

Grouping the two author subfields with a comma, and adjusting the ‑sep and ‑tab values:

      xtract -pattern PubmedArticle -block Author \
        -sep " " -tab ", " -element Initials,LastName

produces a more traditional formatting of author names:

      RK Mortimer, CR Contopoulou, JS King

## Sequential Exploration

Multiple ‑block statements can be used in a single xtract to explore different areas of the XML. This limits element extraction to the desired subregions, and allows disambiguation of fields with identical names but with different parents. For example:

      efetch -db pubmed -id 6092233,4640931,4296474 -format xml |
      xtract -pattern PubmedArticle -element MedlineCitation/PMID \
        -block PubDate -sep " " -element Year,Month,MedlineDate \
        -block AuthorList -num Author -sep "/" -element LastName |
      sort-table -k 3,3n -k 4,4f

generates a table that allows easy parsing of author last names, and sorts the results by author count:

      4296474    1968 Apr        1    Friedmann
      4640931    1972 Dec        2    Tager/Steiner
      6092233    1984 Jul-Aug    3    Calderon/Contopoulou/Mortimer

Like ‑element arguments, the individual ‑block statements are executed sequentially, in order of appearance.

Note also that the PubDate object can exist either in a structured form:

      <PubDate>
        <Year>1968</Year>
        <Month>Apr</Month>
        <Day>25</Day>
      </PubDate>

(with the Day field frequently absent), or in a string form:

      <PubDate>
        <MedlineDate>1984 Jul-Aug</MedlineDate>
      </PubDate>

but would not contain a mixture of both types, so the directive:

      -sep " " -element Year,Month,MedlineDate

will only contribute a single column to the output.

## Nested Exploration

Exploration command names (**‑group**, **‑block**, and **‑subset**) are assigned to a precedence hierarchy:

      -pattern > -group > -block > -subset > -element

and are combined in ranked order to control object iteration at progressively deeper levels in the XML data structure. Each command argument acts as a nested " for loop" control variable, retaining information about the context, or state of exploration, at its level.

(Hypothetical) census data would need several nested loops to visit each unique address in context:

      -pattern State -group City -block Street -subset Number -element Resident

A nucleotide or protein sequence record can have multiple features. Each feature can have multiple qualifiers. And every qualifier has separate name and value nodes. Exploring this natural data hierarchy, with **‑pattern** for the sequence record, **‑group** for the feature, and **‑block** for the qualifier:

      efetch -db nuccore -id NM_021486.4 -format gbc |
      xtract -pattern INSDSeq -element INSDSeq_accession-version \
        -group INSDFeature -deq "\n\t" -element INSDFeature_key \
          -block INSDQualifier -deq "\n\t\t" \
            -element INSDQualifier_name INSDQualifier_value

keeps qualifiers, such as gene and product, associated with their parent features, and keeps qualifier names and values together on the same line:

      NM_021486.4
          source
                    organism       Mus musculus
                    mol_type       mRNA
          gene
                    gene           Bco1
          CDS
                    gene           Bco1
                    product        beta,beta-carotene 15,15'-dioxygenase isoform 1
                    protein_id     NP_067461.2
                    translation    MEIIFGQNKKEQLEPVQAKVTGSIPAWLQGTLLRNGPGM … 
                    …

## Saving Data in Variables

A value can be recorded in a variable and used wherever needed. Variables are created by a hyphen followed by a name consisting of a string of capital letters or digits (e.g., **‑KEY**). Variable values are retrieved by placing an ampersand before the variable name (e.g., "**&KEY**") in an ‑element statement:

      efetch -db nuccore -id NM_021486.4 -format gbc |
      xtract -pattern INSDSeq -element INSDSeq_accession-version \
        -group INSDFeature -KEY INSDFeature_key \
          -block INSDQualifier -deq "\n\t" \
            -element "&KEY" INSDQualifier_name INSDQualifier_value

This prints the feature key on each line before the qualifier name and value, even though the feature key is now outside of the visibility scope (which is the current qualifier):

      NM_021486.4
          source    organism       Mus musculus
          source    mol_type       mRNA
          gene      gene           Bco1
          CDS       gene           Bco1
          CDS       product        beta,beta-carotene 15,15'-dioxygenase isoform 1
          CDS       protein_id     NP_067461.2
          CDS       translation    MEIIFGQNKKEQLEPVQAKVTGSIPAWLQGTLLRNGPGM … 
          …

Variables can be (re)initialized with an explicit literal value inside parentheses:

      -block Author -sep " " -tab "" -element "&COM" Initials,LastName -COM "(, )"

They can also be used as the first argument in a conditional statement:

      -CHR Chromosome -block GenomicInfoType -if "&CHR" -differs-from ChrLoc

A double-hyphen (e.g., **‑‑KYWDS**) appends a value to the variable.

A variable can also save the modified data resulting from an ‑element variant operation. This can allow multiple sequential transitions within a single xtract command:

      -END -sum "Start,Length" -MID -avg "Start,&END"

All variables are reset when the next record is processed.

## Conditional Execution

Conditional processing commands (**‑if** and **‑ unless**) restrict object exploration by data content. They check to see if the named field is within the scope, and may be used in conjunction with string, numeric, or object constraints to require an additional match by value. Use **‑and** and **‑or** to build compound tests. Streaming input through **‑select** removes records that do not satisfy the condition:

      esearch -db pubmed -query "Havran W [AUTH]" |
      efetch -format xml |
      xtract -pattern PubmedArticle -select Language -equals eng |
      xtract -pattern PubmedArticle -block Author -if LastName -is-not Havran \
        -sep ", " -tab "\n" -author LastName,Initials[1:1] |
      sort-uniq-count-rank

This limits the results to papers written in English and prints a table of the most frequent collaborators, using a range to keep only the first initial so that variants like "Berg, C" and "Berg, CM" are combined:

      35    Witherden, D
      15    Boismenu, R
      12    Jameson, J
      10    Allison, J
      10    Fitch, F
      …

Numeric constraints can compare the integer values of two fields. This can be used to find genes that are encoded on the minus strand of a particular chromosome:

      -if ChrLoc -equals X -and ChrStart -gt ChrStop

Object constraints will compare the string values of two named fields, and can look for internal inconsistencies between fields whose contents should (in most cases) be identical:

      -if Chromosome -differs-from ChrLoc

The **‑position** command restricts presentation of objects by relative location or index number:

      -block Author -position last -sep ", " -element LastName,Initials

The **‑else** command can run alternative ‑element or **‑lbl** instructions if the condition is not satisfied:

      -if Strand -contains "-" -lbl "minus strand" -else -lbl "plus strand"

Parallel ‑if and ‑unless statements can be used to provide a more complex response to alternative conditions that include nested explorations.

## Copying XML Objects

The **‑element** **"\*"** construct prints the entirety of the current XML container, including all XML tags. (A period or a percent sign writes ASN.1 or JSON, respectively. Tag names with leading, trailing, or internal underscores control item-specific formats, such as unquoted values or unnamed brackets.)

## Automatic Format Conversion

Xtract can now detect and convert input data in JSON, text ASN.1, and GenBank/GenPept flatfile formats, into XML. Explicit transmute or shortcut commands are only needed to view the intermediate XML's field names or override the default conversion settings.
