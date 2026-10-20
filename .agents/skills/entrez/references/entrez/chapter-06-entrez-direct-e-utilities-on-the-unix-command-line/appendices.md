---
title: "Appendices"
chapter: "Entrez Direct: E-utilities on the Unix Command Line"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter6/#chapter6.Appendices"
---
# Appendices

Each EDirect program has a **‑help** command that prints detailed information about available command-line arguments. These include ‑**sort** values for esearch, **‑format** and **‑mode** choices for efetch, and **‑cmd** options for elink.

## Einfo Data

Einfo field data contains status flags for several term list index properties:

      <Field>
        <Name>ALL</Name>
        <FullName>All Fields</FullName>
        <Description>All terms from all searchable fields</Description>
        <TermCount>280005319</TermCount>
        <IsDate>N</IsDate>
        <IsNumerical>N</IsNumerical>
        <SingleToken>N</SingleToken>
        <Hierarchy>N</Hierarchy>
        <IsHidden>N</IsHidden>
        <IsTruncatable>Y</IsTruncatable>
        <IsRangable>N</IsRangable>
      </Field>

## Additional Elink Options

Elink has several additional modes that can be specified with the ‑cmd argument. When not using the default "neighbor" command ("neighbor_history" has been retired), elink will return an eLinkResult XML object, with the links for each UID presented in separate blocks. For example, the "neighbor" command:

      esearch -db pubmed -query "Hoffmann PC [AUTH] AND dopamine [MAJR]" |
      elink -related -cmd neighbor |
      xtract -pattern LinkSetDb -element Id

will show the original PMID in the first column and related article PMIDs in subsequent columns:

      1504781    11754494    3815119    1684029    14614914    12128255    …
      1684029    3815119     1504781    8097798    17161385    14755628    …
      2572612    2903614     6152036    2905789    9483560     1352865     …
      …

The "acheck" command returns all available link names for each record:

      esearch -db pubmed -query "Federhen S [AUTH]" |
      elink -cmd acheck |
      xtract -pattern LinkSet -tab "\n" -element IdLinkSet/Id \
        -block LinkInfo -tab "\n" -element LinkName

printing each on its own line:

      25510495
      pubmed_images
      pubmed_pmc
      pubmed_pmc_local
      pubmed_pmc_refs
      pubmed_pubmed
      pubmed_pubmed_citedin
      …

The "prlinks" command can obtain the URL reference to the publisher web page for an article. The Unix "xargs" command calls elink separately for each identifier:

      epost -db pubmed -id 22966225,19880848 |
      efetch -format uid |
      xargs -n 1 elink -db pubmed -cmd prlinks -id |
      xtract -pattern LinkSet -first Id -element ObjUrl/Url

## Nquire Arguments

The nquire program uses command-line arguments to obtain data from RESTful, CGI, or FTP servers. Queries are built up from command-line arguments. Paths can be separated into components, which are combined with slashes. Remaining arguments (starting with a dash) are tag/value pairs, with multiple values between tags combined with commas.

For example, a POST request (using ‑url):

      nquire -url https://eutils.ncbi.nlm.nih.gov/entrez/eutils/ espell.fcgi \
        -db pubmed -term "vitamen" |
      xtract -pattern eSpellResult -element CorrectedQuery

returns the corrected spelling of "vitamen":

      vitamin

while a GET query:

      nquire -get https://eutils.ncbi.nlm.nih.gov/entrez/eutils/ einfo.fcgi -db pubmed |
      xtract -pattern DbInfo -block Field -element Name FullName -deq "\n"

returns information about the fields indexed for the PubMed database:

      ALL     All Fields
      UID     UID
      FILT    Filter
      TITL    Title
      MESH    MeSH Terms
      MAJR    MeSH Major Topic
      …

and an FTP request:

      nquire -ftp ftp.ncbi.nlm.nih.gov pub/gdp ideogram_9606_GCF_000001305.14_850_V1 |
      grep acen | cut -f 1,2,6,7 | awk '/^X\t/'

returns data with the (estimated) sequence coordinates of the human X chromosome centromere (here showing where the p and q arms meet):

      X    p    58100001    61000000
      X    q    61000001    63800000

Nquire can also produce a list of files in an FTP server directory:

      nquire -lst ftp://nlmpubs.nlm.nih.gov online/mesh/MESH_FILES/xmlmesh

or a list of FTP file names preceded by a column with the file sizes:

      nquire -dir ftp.ncbi.nlm.nih.gov gene/DATA

Finally, nquire can download FTP files to the local disk:

      nquire -dwn ftp.nlm.nih.gov online/mesh/MESH_FILES/xmlmesh desc2026.zip

If Aspera Connect is installed, the nquire ‑asp command will provide faster retrieval from NCBI servers:

      nquire -asp ftp.ncbi.nlm.nih.gov pubmed baseline pubmed26n0001.xml.gz

Without Aspera Connect, nquire ‑asp defaults to using the ‑dwn logic.
