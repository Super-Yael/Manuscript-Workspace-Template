---
title: "ELink – ESearch"
chapter: "Sample Applications of the E-utilities"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter3/#chapter3.ELink__ESearch"
---
# ELink – ESearch

**Input:** List of Entrez UIDs (integer identifiers, e.g. PMID, GI, Gene ID) in database A

**Output:** History set consisting of the subset of linked UIDs in database B that match an Entrez text query

    use LWP::Simple;

    # Given an input set of protein GI numbers, this script creates a 
    # history set containing the gene IDs linked to members of the input 
    # set that also are on human chromosome X. 
    #(Which of the input proteins are encoded by a gene on human 
    # chromosome X?)

    $db1 = 'protein';  # &dbfrom
    $db2 = 'gene';     # &db
    $linkname = 'protein_gene'; # desired link &linkname
    $query = 'human[orgn]+AND+x[chr]';
    #input UIDs in $db1 (protein GIs)
    $id_list = '148596974,42544182,187937179,4557377,6678417';

    #assemble the elink URL
    $base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/';
    $url = $base . "elink.fcgi?dbfrom=$db1&db=$db2&id=$id_list";
    $url .= "&linkname=$linkname&cmd=neighbor_history";

    #post the elink URL
    $output = get($url);

    #parse WebEnv and QueryKey
    $web = $1 if ($output =~ /<WebEnv>(\S+)<\/WebEnv>/);
    $key = $1 if ($output =~ /<QueryKey>(\d+)<\/QueryKey>/);

    #assemble the esearch URL
    $term = "%23$key+AND+$query";  # %23 places a '#' before the query key
    $url = $base . "esearch.fcgi?db=$db2&term=$term&WebEnv=$web&usehistory=y";

    #post esearch URL
    $limited = get($url);

    print "$limited\n";

    # Output remains on the history server (&query_key, &WebEnv)
    # Use ESummary or EFetch as in previous examples to retrieve them

***Note:*** *To submit a large number (more than a few hundred) UIDs to ELink in one URL, please use the HTTP POST method for the Elink call (see* [*Application 4*](application-4-finding-unique-sets-of-linked-records-for-each-member-of-a-large-dataset.md)*). The &linkname parameter is used to force ELink to return only one set of links (one &query_key) to simplify parsing. If more than one link is desired, the above code must be altered to parse the multiple &query_key values from the ELink XML output. This code uses ELink in "batch" mode, in that only one set of gene IDs is returned and the one-to-one correspondence between protein GIs and Gene IDs is lost. To preserve this one-to-one correspondence, please see* [*Application 4*](application-4-finding-unique-sets-of-linked-records-for-each-member-of-a-large-dataset.md) *below.*
