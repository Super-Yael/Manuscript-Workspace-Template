---
title: "ESearch – ELink – ESummary/EFetch"
chapter: "Sample Applications of the E-utilities"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter3/#chapter3.ESearch__ELink__ESummaryEFetch"
---
# ESearch – ELink – ESummary/EFetch

**Input:** Entrez text query in database A

**ESummary Output:** Linked XML Document Summaries from database B

**EFetch Output:** Formatted data records (e.g. abstracts, FASTA) from database B

    use LWP::Simple;
    # Download protein FASTA records linked to abstracts published 
    # in 2009 that are indexed in MeSH for both asthma and 
    # leukotrienes.

    $db1 = 'pubmed';
    $db2 = 'protein';
    $linkname = 'pubmed_protein';
    $query = 'asthma[mesh]+AND+leukotrienes[mesh]+AND+2009[pdat]';

    #assemble the esearch URL
    $base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/';
    $url = $base . "esearch.fcgi?db=$db1&term=$query&usehistory=y";
    #post the esearch URL
    $output = get($url);

    #parse WebEnv and QueryKey
    $web1 = $1 if ($output =~ /<WebEnv>(\S+)<\/WebEnv>/);
    $key1 = $1 if ($output =~ /<QueryKey>(\d+)<\/QueryKey>/);

    #assemble the elink URL
    $base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/';
    $url = $base . "elink.fcgi?dbfrom=$db1&db=$db2";
    $url .= "&query_key=$key1&WebEnv=$web1";
    $url .= "&linkname=$linkname&cmd=neighbor_history";
    print "$url\n";

    #post the elink URL
    $output = get($url);
    print "$output\n";

    #parse WebEnv and QueryKey
    $web2 = $1 if ($output =~ /<WebEnv>(\S+)<\/WebEnv>/);
    $key2 = $1 if ($output =~ /<QueryKey>(\d+)<\/QueryKey>/);

    ### include this code for ESearch-ELink-ESummary
    #assemble the esummary URL
    $url = $base . "esummary.fcgi?db=$db2&query_key=$key2&WebEnv=$web2";
    #post the esummary URL
    $docsums = get($url);
    print "$docsums";

    ### include this code for ESearch-ELink-EFetch
    #assemble the efetch URL
    $url = $base . "efetch.fcgi?db=$db2&query_key=$key2&WebEnv=$web2";
    $url .= "&rettype=fasta&retmode=text";
    #post the efetch URL
    $data = get($url);
    print "$data";

***Notes:*** *The &linkname parameter is used to force ELink to return only one set of links (one &query_key) to simplify parsing. If more than one link is desired, the above code must be altered to parse the multiple &query_key values from the ELink XML output. This code uses ELink in "batch" mode, in that only one set of PubMed IDs is returned and the one-to-one correspondence between PubMed IDs and their related PubMed IDs is lost. To preserve this one-to-one correspondence, please see* [*Application 4*](application-4-finding-unique-sets-of-linked-records-for-each-member-of-a-large-dataset.md) *below.*
