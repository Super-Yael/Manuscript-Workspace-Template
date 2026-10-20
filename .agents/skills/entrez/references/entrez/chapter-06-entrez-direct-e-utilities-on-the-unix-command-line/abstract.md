---
title: "Abstract"
chapter: "Entrez Direct: E-utilities on the Unix Command Line"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter6/#chapter6.Abstract"
---
# Abstract

Entrez Direct was designed to make it easy for biologists to automate Entrez queries and analyze structured data results without requiring extensive computer programming experience.

EDirect supports both online network queries and local record archives by providing parallel search, link, filter, and fetch scripts. The same structured message format is used for communication between steps, allowing query pipelines to seamlessly operate on a mixture of local and remote data sources.

Central to EDirect's success is a utility that uses command-line arguments to control data extraction from XML, JSON, and ASN.1 text records. It deliberately avoids explicit object paths and complicated path formulas. Instead, the input stream is first partitioned into separate records by parent object name. Then, within each record, data items are found by element name, using a depth-first recursive search.

Exploration commands allow data context to be taken into account by redirecting the search order to separately present each instance of a named container. They are equivalent to nested "for loops", and can keep related fields together in the output. For example, exploration by Author restricts the subsequent searches for Initials and LastName elements to child nodes of the current author object. Conditional processing tests that examine data content are also applied at this level.

Element extraction variants perform simple text modifications or integer calculations on the raw data values. Formatting commands control record, field, and instance separators. A wrapping shortcut places the extracted information inside a new XML object. Combining these features can reduce a complex structured record analysis to an elegant sequence of simpler transformations. No custom reading or writing code is needed, since the data in each step remains in parsable XML format.

EDirect's data extraction and network access tools simplify the construction of local archives. Users can add new public datasets by writing custom helper scripts for the download, generate, populate, and index steps of the build process. Similar processing of tables that associate biological concepts with existing record identifiers can incorporate new indexed search fields. Contributing the helper scripts to a public repository would allow other users to install local copies of any desired datasets.

Researchers or coding agents could then create experimental discovery pipelines that use EDirect's simple query interface to access the new local data domains. The same indexed search mechanism can apply biological reality checks to filter the results of intermediate steps.
