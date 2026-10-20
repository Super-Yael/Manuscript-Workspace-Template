---
title: "Demonstration Programs"
chapter: "E-utilities Quick Start"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter1/#chapter1.Demonstration_Programs"
---
# Demonstration Programs

## EBot

[EBot](https://www.ncbi.nlm.nih.gov/Class/PowerTools/eutils/ebot/ebot.cgi) is an interactive web tool that first allows users to construct an arbitrary E-utility analysis pipeline and then generates a Perl script to execute the pipeline. The Perl script can be downloaded and executed on any computer with a Perl installation. For more details, see the EBot page linked above.

## Sample Perl Scripts

The two sample Perl scripts below demonstrate basic E-utility functions. Both scripts should be copied and saved as plain text files and can be executed on any computer with a Perl installation.

ESearch-EFetch demonstrates basic search and retrieval functions.

    #!/usr/local/bin/perl -w
    # =======================================================================
    #
    #                            PUBLIC DOMAIN NOTICE
    #               National Center for Biotechnology Information
    #
    #  This software/database is a "United States Government Work" under the
    #  terms of the United States Copyright Act.  It was written as part of
    #  the author's official duties as a United States Government employee and
    #  thus cannot be copyrighted.  This software/database is freely available
    #  to the public for use. The National Library of Medicine and the U.S.
    #  Government have not placed any restriction on its use or reproduction.
    #
    #  Although all reasonable efforts have been taken to ensure the accuracy
    #  and reliability of the software and data, the NLM and the U.S.
    #  Government do not and cannot warrant the performance or results that
    #  may be obtained by using this software or data. The NLM and the U.S.
    #  Government disclaim all warranties, express or implied, including
    #  warranties of performance, merchantability or fitness for any particular
    #  purpose.
    #
    #  Please cite the author in any work or product based on this material.
    #
    # =======================================================================
    #
    # Author:  Oleg Khovayko
    #
    # File Description: eSearch/eFetch calling example
    #  
    # ---------------------------------------------------------------------
    # Subroutine to prompt user for variables in the next section

    sub ask_user {
      print "$_[0] [$_[1]]: ";
      my $rc = <>;
      chomp $rc;
      if($rc eq "") { $rc = $_[1]; }
      return $rc;
    }

    # ---------------------------------------------------------------------
    # Define library for the 'get' function used in the next section.
    # $utils contains route for the utilities.
    # $db, $query, and $report may be supplied by the user when prompted; 
    # if not answered, default values, will be assigned as shown below.

    use LWP::Simple;

    my $utils = "https://www.ncbi.nlm.nih.gov/entrez/eutils";

    my $db     = ask_user("Database", "Pubmed");
    my $query  = ask_user("Query",    "zanzibar");
    my $report = ask_user("Report",   "abstract");

    # ---------------------------------------------------------------------
    # $esearch cont?ins the PATH & parameters for the ESearch call
    # $esearch_result containts the result of the ESearch call
    # the results are displayed ?nd parsed into variables 
    # $Count, $QueryKey, and $WebEnv for later use and then displayed.

    my $esearch = "$utils/esearch.fcgi?" .
                  "db=$db&retmax=1&usehistory=y&term=";

    my $esearch_result = get($esearch . $query);

    print "\nESEARCH RESULT: $esearch_result\n";

    $esearch_result =~ 
      m|<Count>(\d+)</Count>.*<QueryKey>(\d+)</QueryKey>.*<WebEnv>(\S+)</WebEnv>|s;

    my $Count    = $1;
    my $QueryKey = $2;
    my $WebEnv   = $3;

    print "Count = $Count; QueryKey = $QueryKey; WebEnv = $WebEnv\n";

    # ---------------------------------------------------------------------
    # this area defines a loop which will display $retmax citation results from 
    # Efetch each time the the Enter Key is pressed, after a prompt.

    my $retstart;
    my $retmax=3;

    for($retstart = 0; $retstart < $Count; $retstart += $retmax) {
      my $efetch = "$utils/efetch.fcgi?" .
                   "rettype=$report&retmode=text&retstart=$retstart&retmax=$retmax&" .
                   "db=$db&query_key=$QueryKey&WebEnv=$WebEnv";
        
      print "\nEF_QUERY=$efetch\n";     

      my $efetch_result = get($efetch);
      
      print "---------\nEFETCH RESULT(". 
             ($retstart + 1) . ".." . ($retstart + $retmax) . "): ".
            "[$efetch_result]\n-----PRESS ENTER!!!-------\n";
      <>;
    }

EPost-ESummary demonstrates basic uploading and document summary retrieval.

    #!/usr/local/bin/perl -w
    # =======================================================================
    #
    #                            PUBLIC DOMAIN NOTICE
    #               National Center for Biotechnology Information
    #
    #  This software/database is a "United States Government Work" under the
    #  terms of the United States Copyright Act.  It was written as part of
    #  the author's official duties as a United States Government employee and
    #  thus cannot be copyrighted.  This software/database is freely available
    #  to the public for use. The National Library of Medicine and the U.S.
    #  Government have not placed any restriction on its use or reproduction.
    #
    #  Although all reasonable efforts have been taken to ensure the accuracy
    #  and reliability of the software and data, the NLM and the U.S.
    #  Government do not and cannot warrant the performance or results that
    #  may be obtained by using this software or data. The NLM and the U.S.
    #  Government disclaim all warranties, express or implied, including
    #  warranties of performance, merchantability or fitness for any particular
    #  purpose.
    #
    #  Please cite the author in any work or product based on this material.
    #
    # =======================================================================
    #
    # Author:  Oleg Khovayko
    #
    # File Description: ePost/eSummary calling example
    #  

    # ---------------------------------------------------------------------
    my $eutils_root  = "https://www.ncbi.nlm.nih.gov/entrez/eutils";
    my $ePost_url    = "$eutils_root/epost.fcgi";
    my $eSummary_url = "$eutils_root/esummary.fcgi";

    my $db_name = "PubMed";

    # ---------------------------------------------------------------------
    use strict;

    use LWP::UserAgent;
    use LWP::Simple;
    use HTTP::Request;
    use HTTP::Headers;
    use CGI;

    # ---------------------------------------------------------------------
    # Read input file into variable $file
    # File name - forst argument $ARGV[0]

    undef $/;  #for load whole file

    open IF, $ARGV[0] || die "Can't open for read: $!\n";
    my $file = <IF>;
    close IF;
    print "Loaded file: [$file]\n";

    # Prepare file - substitute all separators to comma

    $file =~ s/\s+/,/gs;
    print "Prepared file: [$file]\n";

    #Create CGI param line

    my $form_data = "db=$db_name&id=$file";

    # ---------------------------------------------------------------------
    # Create HTTP request

    my $headers = new HTTP::Headers(
        Accept      => "text/html, text/plain",
        Content_Type    => "application/x-www-form-urlencoded"
    );

    my $request = new HTTP::Request("POST", $ePost_url, $headers );

    $request->content($form_data);

    # Create the user agent object

    my $ua = new LWP::UserAgent;
    $ua->agent("ePost/example");

    # ---------------------------------------------------------------------
    # send file to ePost by HTTP

    my $response = $ua->request($request);

    # ---------------------------------------------------------------------

    print "Responce status message: [" . $response->message . "]\n";
    print "Responce content: [" .        $response->content . "]\n";

    # ---------------------------------------------------------------------
    # Parse response->content and extract QueryKey & WebEnv
    $response->content =~ 
      m|<QueryKey>(\d+)</QueryKey>.*<WebEnv>(\S+)</WebEnv>|s;

    my $QueryKey = $1;
    my $WebEnv   = $2;

    print "\nEXTRACTED:\nQueryKey = $QueryKey;\nWebEnv = $WebEnv\n\n";

    # ---------------------------------------------------------------------
    # Retrieve DocSum from eSummary by simple::get method and print it
    #
    print "eSummary result: [" . 
      get("$eSummary_url?db=$db_name&query_key=$QueryKey&WebEnv=$WebEnv") . 
      "]\n";
