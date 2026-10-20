---
title: "Searching and Filtering"
chapter: "Entrez Direct: E-utilities on the Unix Command Line"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter6/#chapter6.Searching_and_Filtering"
---
# Searching and Filtering

## Retrieving PubMed Reports

Piping PubMed query results to efetch and specifying the "abstract" format:

      esearch -db pubmed -query "lycopene cyclase" |
      efetch -format abstract

returns a set of reports that can be read by a person:

      …
      85. PLoS One. 2013;8(3):e58144. doi: 10.1371/journal.pone.0058144. Epub …

      Levels of lycopene β-cyclase 1 modulate carotenoid gene expression and
      accumulation in Daucus carota.

      Moreno JC(1), Pizarro L, Fuentes P, Handford M, Cifuentes V, Stange C.

      Author information:
      (1)Departamento de Biología, Facultad de Ciencias, Universidad de Chile,
      Santiago, Chile.

      Plant carotenoids are synthesized and accumulated in plastids through a
      highly regulated pathway. Lycopene β-cyclase (LCYB) is a key enzyme
      involved directly in the synthesis of α-carotene and β-carotene through
      …

If "medline" format is used instead:

      esearch -db pubmed -query "lycopene cyclase" |
      efetch -format medline

the output can be entered into common bibliographic management software packages:

      …
      PMID- 23555569
      OWN - NLM
      STAT- MEDLINE
      DA  - 20130404
      DCOM- 20130930
      LR  - 20131121
      IS  - 1932-6203 (Electronic)
      IS  - 1932-6203 (Linking)
      VI  - 8
      IP  - 3
      DP  - 2013
      TI  - Levels of lycopene beta-cyclase 1 modulate carotenoid gene expression
            and accumulation in Daucus carota.
      PG  - e58144
      LID - 10.1371/journal.pone.0058144 [doi]
      AB  - Plant carotenoids are synthesized and accumulated in plastids
            through a highly regulated pathway. Lycopene beta-cyclase (LCYB) is a
            key enzyme involved directly in the synthesis of alpha-carotene and
            …

## Retrieving Sequence Reports

Nucleotide and protein records can be downloaded in FASTA format:

      esearch -db protein -query "lycopene cyclase" |
      efetch -format fasta

which consists of a definition line followed by the sequence:

      …
      >gi|735882|gb|AAA81880.1| lycopene cyclase [Arabidopsis thaliana]
      MDTLLKTPNKLDFFIPQFHGFERLCSNNPYPSRVRLGVKKRAIKIVSSVVSGSAALLDLVPETKKENLDF
      ELPLYDTSKSQVVDLAIVGGGPAGLAVAQQVSEAGLSVCSIDPSPKLIWPNNYGVWVDEFEAMDLLDCLD
      TTWSGAVVYVDEGVKKDLSRPYGRVNRKQLKSKMLQKCITNGVKFHQSKVTNVVHEEANSTVVCSDGVKI
      QASVVLDATGFSRCLVQYDKPYNPGYQVAYGIIAEVDGHPFDVDKMVFMDWRDKHLDSYPELKERNSKIP
      TFLYAMPFSSNRIFLEETSLVARPGLRMEDIQERMAARLKHLGINVKRIEEDERCVIPMGGPLPVLPQRV
      VGIGGTAGMVHPSTGYMVARTLAAAPIVANAIVRYLGSPSSNSLRGDQLSAEVWRDLWPIERRRQREFFC
      FGMDILLKLDLDATRRFFDAFFDLQPHYWHGFLSSRLFLPELLVFGLSLFSHASNTSRLEIMTKGTVPLA
      KMINNLVQDRD
      …

Sequence records can also be obtained as GenBank or GenPept flatfiles:

      esearch -db protein -query "lycopene cyclase" |
      efetch -format gp

which have features annotating particular regions of the sequence:

      …
      LOCUS       AAA81880                 501 aa            linear   PLN …
      DEFINITION  lycopene cyclase [Arabidopsis thaliana].
      ACCESSION   AAA81880
      VERSION     AAA81880.1  GI:735882
      DBSOURCE    locus ATHLYC accession L40176.1
      KEYWORDS    .
      SOURCE      Arabidopsis thaliana (thale cress)
        ORGANISM  Arabidopsis thaliana
                  Eukaryota; Viridiplantae; Streptophyta; Embryophyta;
                  Tracheophyta; Spermatophyta; Magnoliophyta; eudicotyledons;
                  Brassicales; Brassicaceae; Camelineae; Arabidopsis.
      REFERENCE   1  (residues 1 to 501)
        AUTHORS   Scolnik,P.A. and Bartley,G.E.
        TITLE     Nucleotide sequence of lycopene cyclase (GenBank L40176) from
                  Arabidopsis (PGR95-019)
        JOURNAL   Plant Physiol. 108 (3), 1343 (1995)
        …
      FEATURES             Location/Qualifiers
           source          1..501
                           /organism="Arabidopsis thaliana"
                           /db_xref="taxon:3702"
           Protein         1..501
                           /product="lycopene cyclase"
           transit_peptide 1..80
           mat_peptide     81..501
                           /product="lycopene cyclase"
           CDS             1..501
                           /gene="LYC"
                           /coded_by="L40176.1:2..1507"
      ORIGIN
              1 mdtllktpnk ldffipqfhg ferlcsnnpy psrvrlgvkk raikivssvv sgsaalldlv
             61 petkkenldf elplydtsks qvvdlaivgg gpaglavaqq vseaglsvcs idpspkliwp
            121 nnygvwvdef eamdlldcld ttwsgavvyv degvkkdlsr pygrvnrkql kskmlqkcit
            181 ngvkfhqskv tnvvheeans tvvcsdgvki qasvvldatg fsrclvqydk pynpgyqvay
            241 giiaevdghp fdvdkmvfmd wrdkhldsyp elkernskip tflyampfss nrifleetsl
            301 varpglrmed iqermaarlk hlginvkrie edercvipmg gplpvlpqrv vgiggtagmv
            361 hpstgymvar tlaaapivan aivrylgsps snslrgdqls aevwrdlwpi errrqreffc
            421 fgmdillkld ldatrrffda ffdlqphywh gflssrlflp ellvfglslf shasntsrle
            481 imtkgtvpla kminnlvqdr d
      //
      …

## Restricting Query Results

The current results can be refined by further term searching in Entrez:

      esearch -db pubmed -query "opsin gene conversion" |
      elink -related |
      efilter -query "tetrachromacy"

## Limiting by Date

Results can also be filtered by date. For example, the following statements:

      efilter -days 60 -datetype PDAT

      efilter -mindate 2000

      efilter -maxdate 1985

      efilter -mindate 1990 -maxdate 1999

restrict results to articles published in the previous two months, since the beginning of 2000, through the end of 1985, or in the 1990s, respectively. YYYY/MM and YYYY/MM/DD date formats are also accepted.

## Fetch by Identifier

Efetch and elink can take a list of numeric identifiers or accessions in an **‑id** argument:

      efetch -db pubmed -id 7252148,1937004 -format xml

      efetch -db nuccore -id 1121073309 -format acc

      efetch -db protein -id 3OQZ_a -format fasta

      efetch -db bioproject -id PRJNA257197 -format docsum

      efetch -db pmc -id PMC209839 -format medline

      elink -db pubmed -id 2539356 -cites

without the need for a preceding esearch command.

Non-integer accessions will be looked up with an internal search, using the appropriate field for the database:

      esearch -db bioproject -query "PRJNA257197 [PRJA]" |
      efetch -format uid |
      …

Most databases use the \[ACCN\] field for identifier lookup, but there are a few exceptions:

      annotinfo      [ASAC]
      assembly       [ASAC]
      bioproject     [PRJA]
      books          [AID]
      clinvar        [VACC]
      gds            [ALL]
      genome         [PRJA]
      geoprofiles    [NAME]
      gtr            [GTRACC]
      mesh           [MHUI]
      nuccore        [ACCN] or [PACC]
      pcsubstance    [SRID]
      snp            [RS] or [SS]

(For ‑db pmc it merely removes any "PMC" prefix from the integer identifier.)

For backward compatibility, **esummary** is a shortcut for esearch ‑format docsum:

      esummary -db bioproject -id PRJNA257197

      esummary -db sra -id SRR5437876

## Reading Large Lists of Identifiers

Efetch and elink can also read a large list of identifiers or accessions piped in through stdin:

      cat "file_of_identifiers.txt" |
      efetch -db pubmed -format docsum

or from a file indicated by an **‑input** argument:

      efetch -input "file_of_identifiers.txt" -db pubmed -format docsum

As mentioned above, there is no need to use a script to split the identifiers into smaller groups or add a time delay between individual requests, since that functionality is already built into EDirect.

## Processing Groups of Terms

The **join‑into‑groups‑of** script combines text containing words, numbers, or identifiers into lines of comma-separated items:

      join-into-groups-of 20 |

Splitting text into one element per line is done by piping through **word‑at‑a‑time** for prose or **accn‑at‑a‑time** for accessions. These functions also lower-case the output:

      echo "$abstract_in_variable" |
      word-at-a-time |
      while read term
      do
        echo "$term"
      done |

The **sort‑uniq‑count‑rank** function then sorts the individual terms, counts the number of times each one appears in the list, and finally resorts the terms based on their frequency of occurrence:

      sort-uniq-count-rank

A faster version of **accn‑at‑a‑time** runs without lower-case transformation:

      tr -cs a-zA-Z0-9_. '\n' |

## Qualifying Queries by Indexed Field

Query terms in esearch or efilter can be qualified by entering an indexed field abbreviation in brackets. Boolean operators and parentheses can also be used in the query expression for more complex searches.

Commonly used fields for PubMed queries include:

      [AFFL]    Affiliation                 [LANG]    Language
      [ALL]     All Fields                  [MAJR]    MeSH Major Topic
      [AUTH]    Author                      [SUBH]    MeSH Subheading
      [FAUT]    Author - First              [MESH]    MeSH Terms
      [LAUT]    Author - Last               [PTYP]    Publication Type
      [CRDT]    Date - Create               [WORD]    Text Word
      [PDAT]    Date - Publication          [TITL]    Title
      [FILT]    Filter                      [TIAB]    Title/Abstract
      [JOUR]    Journal                     [UID]     UID

and a qualified query looks like:

      "Tager HS [AUTH] AND glucagon [TIAB]"

Filters that limit search results to subsets of PubMed include:

      humans [MESH]
      pharmacokinetics [MESH]
      chemically induced [SUBH]
      all child [FILT]
      english [FILT]
      freetext [FILT]
      has abstract [FILT]
      historical article [FILT]
      randomized controlled trial [FILT]
      clinical trial, phase ii [PTYP]
      review [PTYP]

Sequence databases are indexed with a different set of search fields, including:

      [ACCN]    Accession             [MLWT]    Molecular Weight
      [ALL]     All Fields            [ORGN]    Organism
      [AUTH]    Author                [PACC]    Primary Accession
      [GPRJ]    BioProject            [PROP]    Properties
      [BIOS]    BioSample             [PROT]    Protein Name
      [ECNO]    EC/RN Number          [SQID]    SeqID String
      [FKEY]    Feature key           [SLEN]    Sequence Length
      [FILT]    Filter                [SUBS]    Substance Name
      [GENE]    Gene Name             [WORD]    Text Word
      [JOUR]    Journal               [TITL]    Title
      [KYWD]    Keyword               [UID]     UID

and a sample query in the protein database is:

      "alcohol dehydrogenase [PROT] NOT (bacteria [ORGN] OR fungi [ORGN])"

Additional examples of subset filters in sequence databases are:

      mammalia [ORGN]
      mammalia [ORGN:noexp]
      txid40674 [ORGN]
      cds [FKEY]
      lacz [GENE]
      beta galactosidase [PROT]
      protein snp [FILT]
      reviewed [FILT]
      country united kingdom glasgow [TEXT]
      country united states [TEXT]
      biomol genomic [PROP]
      dbxref flybase [TEXT]
      gbdiv phg [PROP]
      phylogenetic study [PROP]
      sequence from mitochondrion [PROP]
      src cultivar [PROP]
      srcdb refseq validated [PROP]
      150:200 [SLEN]

(The calculated molecular weight (MLWT) field is only indexed for proteins and structures, not nucleotides.)

See **efilter ‑help** for a list of filter shortcuts available for several Entrez databases.

## Examining Intermediate Results

EDirect navigation functions produce a custom XML message with the relevant fields (database, web environment, query key, and record count) that can be read by the next command in the pipeline. EDirect may store intermediate results on the Entrez history server or instantiate them in the XML message.

The results of each step in a query can be examined to confirm expected behavior before adding the next step. The Count field in the ENTREZ_DIRECT object contains the number of records returned by the previous step. A good measure of query success is a reasonable (non‑zero) count value. For example:

      esearch -db protein -query "tryptophan synthase alpha chain [PROT]" |
      efilter -query "28000:30000 [MLWT]" | tee /dev/tty |
      elink -target structure -log |
      efilter -query "0:2 [RESO]"

produces:

      <ENTREZ_DIRECT>
        <Db>protein</Db>
        <WebEnv>MCID_6a56bdcecaf7c3511b0de8e1</WebEnv>
        <QueryKey>2</QueryKey>
        <Count>17617</Count>
        <Step>2</Step>
        <Elapsed>1</Elapsed>
      </ENTREZ_DIRECT>
      <ENTREZ_DIRECT>
        <Db>structure</Db>
        <Count>57</Count>
        <Step>4</Step>
        <Id>5822</Id>
        <Id>11701</Id>
        …
        <Id>211309</Id>
        <Id>255950</Id>
        <Elapsed>203</Elapsed>
      </ENTREZ_DIRECT>

The first message shows the molecular weight range filter returning 17,617 proteins. (Piping through **tee /dev/tty** prints the intermediate result on the terminal and also pipes it to the next step.) The second message shows the final result of 57 protein structures having the desired (X‑ray crystallographic) atomic position resolution.

(When saving to history, the QueryKey value may differ from Step because the elink command splits its query into smaller chunks to avoid server truncation limits and timeout errors.)

## Combining Independent Queries

Independent esearch/elink/efilter/efetch pipelines can be combined by passing the separate UID results to the **intersect‑uid‑lists** script. (The output of both pipelines must be in the same target database.)

(The history server's "**\#**" convention is no longer used for this example. Intermediate results are now saved in Unix shell script variables, which will be discussed in a later section of this document.)

For example, the query:

      amyl=$(
        esearch -db protein -query "amyloid* [PROT]" -log | tee /dev/tty |
        elink -target pubmed |
        efetch -format uid
      ) 

      apoe=$(
        esearch -db gene -query "apo* [GENE]" -log | tee /dev/tty |
        elink -target pubmed |
        efetch -format uid
      )

      both=$( intersect-uid-lists <( echo "$amyl" ) <( echo "$apoe" ) )

      echo "$both" |
      efetch -db pubmed -format docsum |
      xtract -mixed -pattern DocumentSummary -element Id Title |
      cat -v

uses truncation searching (entering the first few letters of a word followed by an asterisk) for the two main concepts, and return titles of papers with links to both amyloid protein sequences and apolipoprotein gene records:

      23962925    Genome analysis reveals insights into physiology and …
      23959870    Low levels of copper disrupt brain amyloid-β homeostasis …
      23371554    Genomic diversity and evolution of the head crest in the …
      23251661    Novel genetic loci identified for the pathophysiology of …
      …
