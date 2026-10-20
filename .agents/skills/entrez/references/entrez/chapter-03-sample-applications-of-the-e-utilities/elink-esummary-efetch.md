---
title: "ELink – ESummary/Efetch"
chapter: "Sample Applications of the E-utilities"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter3/#chapter3.ELink__ESummaryEfetch"
---
# ELink – ESummary/Efetch

**Input:** List of Entrez UIDs in database A (integer identifiers, e.g. PMID, GI, Gene ID)

**ESummary Output:** Linked XML Document Summaries from database B

**EFetch Output:** Formatted data records (e.g. abstracts, FASTA) from database B

    use LWP::Simple;

    # Download gene records linked to a set of proteins corresponding to a list
    # of GI numbers.

    $db1 = 'protein';  # &dbfrom
    $db2 = 'gene';     # &db
    $linkname = 'protein_gene'; # desired link &linkname
    #input UIDs in $db1 (protein GIs)
    $id_list = '194680922,50978626,28558982,9507199,6678417';

    #assemble the elink URL
    $base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/';
    $url = $base . "elink.fcgi?dbfrom=$db1&db=$db2&id=$id_list";
    $url .= "&linkname=$linkname&cmd=neighbor_history";

    #post the elink URL
    $output = get($url);

    #parse WebEnv and QueryKey
    $web = $1 if ($output =~ /<WebEnv>(\S+)<\/WebEnv>/);
    $key = $1 if ($output =~ /<QueryKey>(\d+)<\/QueryKey>/);

    ### include this code for ELink-ESummary
    #assemble the esummary URL
    $url = $base . "esummary.fcgi?db=$db&query_key=$key&WebEnv=$web";

    #post the esummary URL
    $docsums = get($url);
    print "$docsums";

    ### include this code for ELink-EFetch
    #assemble the efetch URL
    $url = $base . "efetch.fcgi?db=$db2&query_key=$key&WebEnv=$web";
    $url .= "&rettype=xml&retmode=xml";

    #post the efetch URL
    $data = get($url);
    print "$data";

***Notes:*** *To submit a large number (more than a few hundred) UIDs to ELink in one URL, please use the HTTP POST method for the Elink call (see Application 4). The &linkname parameter is used to force ELink to return only one set of links (one &query_key) to simplify parsing. If more than one link is desired, the above code must be altered to parse the multiple &query_key values from the ELink XML output. This code uses ELink in "batch" mode, in that only one set of gene IDs is returned and the one-to-one correspondence between protein GIs and gene IDs is lost. To preserve this one-to-one correspondence, please see* [*Application 4*](application-4-finding-unique-sets-of-linked-records-for-each-member-of-a-large-dataset.md) *below.*
