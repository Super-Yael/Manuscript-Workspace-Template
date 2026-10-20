---
title: "Complex Objects"
chapter: "Entrez Direct: E-utilities on the Unix Command Line"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter6/#chapter6.Complex_Objects"
---
# Complex Objects

## Author Exploration

What's in a name? That which we call an author, by any other name, may be a consortium, investigator, or editor:

      <PubmedArticle>
        <MedlineCitation>
          <PMID>99999999</PMID>
          <Article>
            <AuthorList>
              <Author>
                <LastName>Tinker</LastName>
              </Author>
              <Author>
                <LastName>Evers</LastName>
              </Author>
              <Author>
                <LastName>Chance</LastName>
              </Author>
              <Author>
                <CollectiveName>FlyBase Consortium</CollectiveName>
              </Author>
            </AuthorList>
          </Article>
          <InvestigatorList>
            <Investigator>
              <LastName>Alpher</LastName>
            </Investigator>
            <Investigator>
              <LastName>Bethe</LastName>
            </Investigator>
            <Investigator>
              <LastName>Gamow</LastName>
            </Investigator>
          </InvestigatorList>
        </MedlineCitation>
      </PubmedArticle>

Within the record, ‑element exploration on last name:

      xtract -pattern PubmedArticle -element LastName

prints each last name, but does not match the consortium:

      Tinker    Evers    Chance    Alpher    Bethe    Gamow

Limiting to the author list:

      xtract -pattern PubmedArticle -block AuthorList -element LastName

excludes the investigators:

      Tinker    Evers    Chance

Using ‑num on each type of object:

      xtract -pattern PubmedArticle -num Author Investigator LastName CollectiveName

displays the various object counts:

      4    3    6    1

## Date Selection

Dates come in all shapes and sizes:

      <PubmedArticle>
        <MedlineCitation>
          <PMID>99999999</PMID>
          <DateCompleted>
            <Year>2011</Year>
          </DateCompleted>
          <DateRevised>
            <Year>2012</Year>
          </DateRevised>
          <Article>
            <Journal>
              <JournalIssue>
                <PubDate>
                  <Year>2013</Year>
                </PubDate>
              </JournalIssue>
            </Journal>
            <ArticleDate>
              <Year>2014</Year>
            </ArticleDate>
          </Article>
        </MedlineCitation>
        <PubmedData>
          <History>
            <PubMedPubDate PubStatus="received">
              <Year>2015</Year>
            </PubMedPubDate>
            <PubMedPubDate PubStatus="accepted">
              <Year>2016</Year>
            </PubMedPubDate>
            <PubMedPubDate PubStatus="entrez">
              <Year>2017</Year>
            </PubMedPubDate>
            <PubMedPubDate PubStatus="pubmed">
              <Year>2018</Year>
            </PubMedPubDate>
            <PubMedPubDate PubStatus="medline">
              <Year>2019</Year>
            </PubMedPubDate>
          </History>
        </PubmedData>
      </PubmedArticle>

Within the record, ‑element exploration on the year:

      xtract -pattern PubmedArticle -element Year

finds and prints all nine instances:

      2011    2012    2013    2014    2015    2016    2017    2018    2019

Using ‑block to limit the scope:

      xtract -pattern PubmedArticle -block History -element Year

prints only the five years within the History object:

      2015    2016    2017    2018    2019

**Surprisingly**, inserting a conditional statement to limit element selection to a date with a specific attribute:

      xtract -pattern PubmedArticle -block History \
        -if @PubStatus -equals "pubmed" -element Year

still prints all five years within History:

      2015    2016    2017    2018    2019

This is because the ‑if command uses the same exploration logic as ‑element, but is designed to declare success if it finds a match **anywhere** within the current scope. There is indeed a "pubmed" attribute within History, in one of its five PubMedPubDate child objects, so the test succeeds. Thus, ‑element is given free rein to do its own exploration within History, and prints all five years.

The solution is to explore the individual PubMedPubDate objects within History:

      xtract -pattern PubmedArticle -block History \
        -subset PubMedPubDate \
          -if @PubStatus -equals "pubmed" -element Year

This visits each PubMedPubDate separately, with the ‑if test matching only the indicated date type, thus returning only the desired year:

      2018

## PMID Extraction

Because of the presence of a CommentsCorrections object:

      <PubmedArticle>
        <MedlineCitation>
          <PMID>99999999</PMID>
          <CommentsCorrectionsList>
            <CommentsCorrections RefType="ErratumFor">
              <PMID>88888888</PMID>
            </CommentsCorrections>
          </CommentsCorrectionsList>
        </MedlineCitation>
      </PubmedArticle>

attempting to print the record's PubMed Identifier:

      xtract -pattern PubmedArticle -element PMID

also returns the PMID of the comment:

      99999999    88888888

Using an exploration command cannot exclude the second instance, because it would need a parent node unique to the first element, and the chain of parents to the first PMID:

      PubmedArticle/MedlineCitation

is a subset of the chain of parents to the second PMID:

      PubmedArticle/MedlineCitation/CommentsCorrectionList/CommentsCorrections

Although **‑first** PMID will work in this particular case, the more general solution is to limit by subpath with the parent / child construct:

      xtract -pattern PubmedArticle -element MedlineCitation/PMID

That would work even if the order of objects were reversed.
