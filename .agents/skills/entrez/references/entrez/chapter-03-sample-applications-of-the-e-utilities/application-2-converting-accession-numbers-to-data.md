---
title: "Application 2: Converting accession numbers to data"
chapter: "Sample Applications of the E-utilities"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter3/#chapter3.Application_2_Converting_access"
---
# Application 2: Converting accession numbers to data

**Goal:** Starting with a list of protein accession numbers, return the sequences in FASTA format.

**Solution:** Create a string consisting of items separated by 'OR', where each item is an accession number followed by '\[accn\]'.

Example: accn1\[accn\]+OR+accn2\[accn\]+OR+accn3\[accn\]+OR+…

Submit this string as a &term in ESearch, then use EFetch to retrieve the FASTA data.

**Input:** \$acc_list – comma-delimited list of accessions

**Output:** FASTA data

    use LWP::Simple;
    $acc_list = 'NM_009417,NM_000547,NM_001003009,NM_019353';
    @acc_array = split(/,/, $acc_list);

    #append [accn] field to each accession
    for ($i=0; $i < @acc_array; $i++) {
       $acc_array[$i] .= "[accn]";
    }

    #join the accessions with OR
    $query = join('+OR+',@acc_array);

    #assemble the esearch URL
    $base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/';
    $url = $base . "esearch.fcgi?db=nuccore&term=$query&usehistory=y";

    #post the esearch URL
    $output = get($url);

    #parse WebEnv and QueryKey
    $web = $1 if ($output =~ /<WebEnv>(\S+)<\/WebEnv>/);
    $key = $1 if ($output =~ /<QueryKey>(\d+)<\/QueryKey>/);

    #assemble the efetch URL
    $url = $base . "efetch.fcgi?db=nuccore&query_key=$key&WebEnv=$web";
    $url .= "&rettype=fasta&retmode=text";

    #post the efetch URL
    $fasta = get($url);
    print "$fasta";

***Notes:*** *For large numbers of accessions, use HTTP POST to submit the esearch request (see* [*Application 4*](application-4-finding-unique-sets-of-linked-records-for-each-member-of-a-large-dataset.md)*), and see* [*Application 3*](application-3-retrieving-large-datasets.md) *below for downloading the large set in batches.*
