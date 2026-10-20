---
title: "Summary"
chapter: "Entrez Direct: E-utilities on the Unix Command Line"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter6/#chapter6.Summary"
---
# Summary

Entrez Direct continues to grow in popularity for simplifying access to Entrez data. It generates over half a billion EUtils service requests per year, with a peak of 15.8 million network hits on its busiest day. Over 180,000 users (measured by unique IP addresses) made EDirect queries in 2025, and it is referenced by more than 360 links in Google Scholar and over 225 citations in PubMed Central.

Recent increases in computer speed, processor count, and memory size, along with the transition to solid-state storage drives and improved file systems, provide an opportunity to simplify data analysis pipelines and add new capabilities in ways that would not have been practical even a few years ago.

EDirect local archives keep derived records, search indices, and cross-domain link tables together in an integrated system. Self-contained native binary executables eliminate external library load delays and version conflicts. The software is modular and easy to maintain, and it has evolved gradually through careful, selective refactoring.

This design helps EDirect avoid tangled package dependencies and sensitivity to network latency that can occur with other architectures. Absence of a third-party database eliminates common system administration and hosted infrastructure costs. The mature archive build system removes the need for redundant infrastructure development by every group that wants a searchable Entrez-style database.

Postings files use variable-byte-length encoding of UIDs to efficiently reference trillions of records. This ensures the archive's long-term ability to keep pace with the expanding scale of biological databases.

An archive can be built on a single well-configured personal computer in a reasonable amount of time without exceeding available memory. The 423-million-record peptide database takes around 1 hour for archiving and 11 hours for indexing and inversion on a Mac Studio M4 Max computer with 16 CPUs, 128 GB of internal RAM, and an external 4 TB Thunderbolt 5 SSD.

A university could run **archive‑peptide ‑index** on an existing server to build a master copy of a searchable archive. Once finished, the **Archive**, **Data**, and **Posting** folders could be copied onto external solid-state drives (e.g., 2 TB Thunderbolt 3) provided by individual laboratories. By connecting an SSD to a lab's computer (and updating the configuration file), that lab will have unlimited use of the derived dataset, with the only expense being the purchase of one solid-state drive.

The ability to process a wide variety of scientific information (e.g., biochemical pathway components or mass spectrometry profiles) gives EDirect the potential to accelerate research through independent, cumulative data integration efforts. With these new local archives, pipelines can use **xsearch** queries to help look for unexpected but biologically relevant connections between records in different domains.

Additional search fields can be populated by importing curated references that map biological concepts (e.g., metabolic pathway classes) to an archive's source records. Using these in **xfilter** queries may help prevent combinatorial explosions when adapting multistep navigation protocols (11) for automated exploration tools that make discoveries by traversing a series of precomputed database links.

As EDirect begins to provide computable information from a growing set of public databases, scientists will be able to take those combined resources in directions that are limited only by their imaginations.
