---
title: "Introduction"
chapter: "Entrez Direct: E-utilities on the Unix Command Line"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter6/#chapter6.Introduction"
---
# Introduction

Entrez Direct (EDirect) provides access to Entrez (1), the NCBI's suite of interconnected databases, from a Unix terminal window. Search terms are entered as command-line arguments. Individual operations are connected with Unix pipes to construct multi-step queries. Selected records can then be retrieved in a variety of formats. Each record in a database is assigned its own unique identifier (UID).

The **EDIRECT.pdf** reference document included in the edirect folder contains an abridged version of this document. It is intended to convey the most important points in the least amount of time for the new user, while still presenting the minimal essential details.

The full documentation here gives a more in-depth exploration of the underlying topics, especially in the Additional Examples web page, which is organized by Entrez database.

## Programmatic Access

EDirect connects to Entrez through the Entrez Programming Utilities (EUtils) interface. It supports searching by indexed terms, looking up precomputed neighbors or links, filtering results by date or category, and downloading record summaries or reports.

Navigation programs (**esearch**, **elink**, **efilter**, and **efetch**) communicate by means of a small structured message, which can be passed invisibly between operations with a Unix pipe. The message includes the current database, so it does not need to be given as an argument after the first step.

Accessory programs (**nquire**, **transmute**, and **xtract**) can help eliminate the need for writing custom software to answer ad hoc questions. Queries can move effortlessly between EDirect programs and Unix utilities or scripts to perform actions that cannot be accomplished entirely within Entrez.

EDirect programs are designed to work on large sets of data. They handle many technical details behind the scenes, thus avoiding the learning curve normally required for EUtils programming. There is no need to use a script to loop over records in small groups, or write code to retry a query after a transient network or server failure, or add a time delay between requests. All of those features are already built into the system.

Unix programs are run by typing the name of the program and then supplying any required or optional arguments on the command line. Argument names are letters or words that start with a dash ("**‑**") character.

Each program has a **‑help** command that prints detailed information about available arguments.

Running **xtract ‑unix** will print a reference sheet of useful Unix commands and constructs. Additional documentation can be obtained by typing "**man**" followed by a Unix command name.

## Navigation Functions

Esearch performs a new Entrez search using terms in indexed fields. It requires a **‑db** argument for the database name and uses **‑query** for the search terms. For PubMed, without field qualifiers, the server uses automatic term mapping to compose a search strategy by translating the supplied query:

      esearch -db pubmed -query "selective serotonin reuptake inhibitor"

Search terms can also be qualified with a bracketed field name to match within the specified index:

      esearch -db nuccore -query "insulin [PROT] AND rodents [ORGN]"

Elink looks up precomputed neighbors within a database:

      elink -related

or follows annotated links to records in other databases:

      elink -target gene

Elink also connects to the NIH Open Citation Collection service (2) to find publications that cite the selected PubMed articles:

      elink -cited

or to retrieve the reference lists of PubMed records:

      elink -cites

Efilter limits the results of a previous query, with shortcuts that can also be used in esearch:

      efilter -molecule genomic -location chloroplast -country sweden -mindate 1985

Efetch downloads selected records or reports in a style designated by **‑format**:

      efetch -format abstract

Einfo can report the fields and links that are indexed for each database:

      einfo -db protein -fields

This will return a table of field abbreviations and names indexed for proteins:

      ACCN    Accession
      ALL     All Fields
      ASSM    Assembly
      AUTH    Author
      BRD     Breed
      CULT    Cultivar
      DIV     Division
      ECNO    EC/RN Number
      FILT    Filter
      FKEY    Feature key
      …

## Constructing Multi-Line or Multi-Step Queries

A single command can be continued on the next line by typing the Unix backslash ("**\\**") escape character immediately before pressing the Return key. Pay careful attention to the exact spacing if the line break is within a quoted argument:

      esearch -db biosample -query "package mims metagenome/environmental, \
      water version 6 0 [PROP] AND ncbi [FILT] AND biosample sra [FILT]"

EDirect allows individual operations to be described separately, combining them into a multi-step query by using the Unix vertical bar ("**\|**") pipe symbol:

      esearch -db pubmed -query "tn3 transposition immunity" | efetch -format apa

The vertical bar also allows query steps to be placed on separate lines:

      esearch -db pubmed -query "raynaud disease AND fish oil" |
      efetch -format medline

In most modern versions of Unix the vertical bar pipe symbol also allows the query to continue on the next line, without the need for an additional backslash. That convention will be followed for the remainder of this document.

## Accessory Programs

Nquire retrieves data from remote servers with URLs constructed from command line arguments:

      nquire -get https://icite.od.nih.gov api/pubs -pmids 2539356 |

Transmute converts a concatenated stream of JSON objects or other structured formats into XML:

      transmute -j2x -nest depth |

Xtract uses waypoints to navigate complex XML hierarchies, and selects data values by field name:

      xtract -pattern data -element cited_by |

The resulting output can be post-processed by Unix utilities or scripts:

      fmt -w 1 | sort -V | uniq

## Mixed-Content Records

The **‑mixed** flag is needed when processing XML or HTML records that contain embedded markup instructions. Using this argument, transmute **‑format** can reformat the records for easier reading, and xtract **‑verify** can confirm that all opening and closing tags are properly balanced:

      efetch -db pmc -id 4305238 -format xml |
      transmute -mixed -format | xtract -mixed -verify
