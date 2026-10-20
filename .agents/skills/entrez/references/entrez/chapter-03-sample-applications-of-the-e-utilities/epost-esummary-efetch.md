---
title: "EPost – ESummary/EFetch"
chapter: "Sample Applications of the E-utilities"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter3/#chapter3.EPost__ESummaryEFetch"
---
# EPost – ESummary/EFetch

**Input:** List of Entrez UIDs (integer identifiers, e.g. PMID, GI, Gene ID)

**ESummary Output:** XML Document Summaries

**EFetch Output:** Formatted data records (e.g. abstracts, FASTA)

    use LWP::Simple;

    # Download protein records corresponding to a list of GI numbers.

    $db = 'protein';
    $id_list = '194680922,50978626,28558982,9507199,6678417';

    #assemble the epost URL
    $base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/';
    $url = $base . "epost.fcgi?db=$db&id=$id_list";

    #post the epost URL
    $output = get($url);

    #parse WebEnv and QueryKey
    $web = $1 if ($output =~ /<WebEnv>(\S+)<\/WebEnv>/);
    $key = $1 if ($output =~ /<QueryKey>(\d+)<\/QueryKey>/);

    ### include this code for EPost-ESummary
    #assemble the esummary URL
    $url = $base . "esummary.fcgi?db=$db&query_key=$key&WebEnv=$web";

    #post the esummary URL
    $docsums = get($url);
    print "$docsums";

    ### include this code for EPost-EFetch
    #assemble the efetch URL
    $url = $base . "efetch.fcgi?db=$db&query_key=$key&WebEnv=$web";
    $url .= "&rettype=fasta&retmode=text";

    #post the efetch URL
    $data = get($url);
    print "$data";

***Note:*** *To post a large number (more than a few hundred) UIDs in a single URL, please use the HTTP POST method for the EPost call (see* [*Application 4*](application-4-finding-unique-sets-of-linked-records-for-each-member-of-a-large-dataset.md)*).*
