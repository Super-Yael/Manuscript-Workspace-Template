---
title: "Application 4: Finding unique sets of linked records for each member of a large dataset"
chapter: "Sample Applications of the E-utilities"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter3/#chapter3.Application_4_Finding_unique_se"
---
# Application 4: Finding unique sets of linked records for each member of a large dataset

**Goal:** Download separately the SNP rs numbers (identifiers) for each current gene on human chromosome 20.

**Solution:** First use ESearch to retrieve the Gene IDs for the genes, and then assemble an ELink URL where each Gene ID is submitted as a separate &id parameter.

**Input:** \$query – human\[orgn\]+AND+20\[chr\]+AND+alive\[prop\]

**Output:** A file named "snp_table" containing on each line the gene id followed by a colon (":") followed by a comma-delimited list of the linked SNP rs numbers.

    use LWP::Simple;
    use LWP::UserAgent;
    $query = 'human[orgn]+AND+20[chr]+AND+alive[prop]';
    $db1 = 'gene';
    $db2 = 'snp';
    $linkname = 'gene_snp';

    #assemble the esearch URL
    $base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/';
    $url = $base . "esearch.fcgi?db=$db1&term=$query&usehistory=y&retmax=5000";

    #post the esearch URL
    $output = get($url);

    #parse IDs retrieved
    while ($output =~ /<Id>(\d+?)<\/Id>/sg) {
       push(@ids, $1);
    }

    #assemble  the elink URL as an HTTP POST call
    $url = $base . "elink.fcgi";

    $url_params = "dbfrom=$db1&db=$db2&linkname=$linkname";
    foreach $id (@ids) {      
       $url_params .= "&id=$id";
    }

    #create HTTP user agent
    $ua = new LWP::UserAgent;
    $ua->agent("elink/1.0 " . $ua->agent);

    #create HTTP request object
    $req = new HTTP::Request POST => "$url";
    $req->content_type('application/x-www-form-urlencoded');
    $req->content("$url_params");

    #post the HTTP request
    $response = $ua->request($req); 
    $output = $response->content;

    open (OUT, ">snp_table") || die "Can't open file!\n";

    while ($output =~ /<LinkSet>(.*?)<\/LinkSet>/sg) {

       $linkset = $1;
       if ($linkset =~ /<IdList>(.*?)<\/IdList>/sg) {
          $input = $1;
          $input_id = $1 if ($input =~ /<Id>(\d+)<\/Id>/sg); 
       }

       while ($linkset =~ /<Link>(.*?)<\/Link>/sg) {
          $link = $1;
          push (@output, $1) if ($link =~ /<Id>(\d+)<\/Id>/);
       }
          
       print OUT "$input_id:" . join(',', @output) . "\n";
      
    }

    close OUT;

***Notes:*** *This example uses an HTTP POST request for the elink call, as the number of Gene IDs is over 500. The &retmax parameter in the ESearch call is set to 5000, as this is a reasonable limit to the number of IDs to send to ELink in one request (if you send 5000 IDs, you are effectively performing 5000 ELink operations). If you need to link more than 5000 records, add &retstart to the ESearch call and repeat the entire procedure for each batch of 5000 IDs, incrementing &retstart for each batch.*
