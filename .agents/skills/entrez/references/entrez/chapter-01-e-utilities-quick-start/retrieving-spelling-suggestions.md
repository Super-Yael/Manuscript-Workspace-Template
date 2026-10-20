---
title: "Retrieving Spelling Suggestions"
chapter: "E-utilities Quick Start"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter1/#chapter1.Retrieving_Spelling_Suggestions"
---
# Retrieving Spelling Suggestions

    espell.fcgi?term=<query>&db=<database>

Input: Entrez text query (&term); Entrez database (&db)

Output: XML containing the original query and spelling suggestions.

*Example: Find spelling suggestions for the PubMed Central query ‘fiberblast cell grwth’.*

<https://eutils.ncbi.nlm.nih.gov/entrez/eutils/espell.fcgi?term=fiberblast+cell+grwth&db=pmc>

## For More Information

Please see [ESpell In-Depth](https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter4/#chapter4.ESpell) for a full description of EGQuery.

## Sample ESpell Output

    <?xml version="1.0"?>
    <!DOCTYPE eSpellResult PUBLIC "-//NLM//DTD eSpellResult, 23 November 
    2004//EN" "https://www.ncbi.nlm.nih.gov/entrez/query/DTD/eSpell.dtd">
    <eSpellResult>
    <Database>pmc</Database>
    <Query>fiberblast cell grwth</Query>
    <CorrectedQuery>fibroblast cell growth</CorrectedQuery>
    <SpelledQuery>
     <Replaced>fibroblast</Replaced>
     <Original> cell </Original>
     <Replaced>growth</Replaced>
    </SpelledQuery>
    <ERROR/>
    </eSpellResult>
