---
title: "EPost – ESearch"
chapter: "Sample Applications of the E-utilities"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter3/#chapter3.EPost__ESearch"
---
# EPost – ESearch

**Input:** List of Entrez UIDs (integer identifiers, e.g. PMID, GI, Gene ID)

**Output:** History set consisting of the subset of posted UIDs that match an Entrez text query

    use LWP::Simple;

    # Given an input set of protein GI numbers, this script creates 
    # a history set containing the members of the input set that 
    # correspond to human proteins. 
    #(Which of these proteins are from human?)

    $db = 'protein';
    $query = 'human[orgn]';
    $id_list = '194680922,50978626,28558982,9507199,6678417';

    #assemble the epost URL
    $base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/';
    $url = $base . "epost.fcgi?db=$db&id=$id_list";

    #post the epost URL
    $output = get($url);

    #parse WebEnv and QueryKey
    $web = $1 if ($output =~ /<WebEnv>(\S+)<\/WebEnv>/);
    $key = $1 if ($output =~ /<QueryKey>(\d+)<\/QueryKey>/);

    #assemble the esearch URL
    $term = "%23$key+AND+$query";  
    # %23 places a '#' before the query key
    $url = $base . "esearch.fcgi?db=$db&term=$term";
    $url .= "&WebEnv=$web&usehistory=y";

    #post esearch URL
    $limited = get($url);

    print "$limited\n";

    # Output remains on the history server (&query_key, &WebEnv)
    # Use ESummary or EFetch as above to retrieve them

***Note:*** *To post a large number (more than a few hundred) UIDs in a single URL, please use the HTTP POST method for the EPost call (see* [*Application 4*](application-4-finding-unique-sets-of-linked-records-for-each-member-of-a-large-dataset.md)*).*
