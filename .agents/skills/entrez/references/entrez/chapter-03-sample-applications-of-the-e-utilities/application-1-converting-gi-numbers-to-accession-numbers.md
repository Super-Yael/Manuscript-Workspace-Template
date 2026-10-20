---
title: "Application 1: Converting GI numbers to accession numbers"
chapter: "Sample Applications of the E-utilities"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter3/#chapter3.Application_1_Converting_GI_num"
---
# Application 1: Converting GI numbers to accession numbers

**Goal:** Starting with a list of nucleotide GI numbers, prepare a set of corresponding accession numbers.

**Solution:** Use EFetch with &retttype=acc

**Input:** \$gi_list – comma-delimited list of GI numbers

**Output:** List of accession numbers.

    use LWP::Simple;
    $gi_list = '24475906,224465210,50978625,9507198';

    #assemble the URL
    $base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/';
    $url = $base . "efetch.fcgi?db=nucleotide&id=$gi_list&rettype=acc";

    #post the URL
    $output = get($url);
    print "$output";

***Notes:*** *The order of the accessions in the output will be the same order as the GI numbers in \$gi_list.*
