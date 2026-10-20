---
title: "Discovery by Navigation"
chapter: "Entrez Direct: E-utilities on the Unix Command Line"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter6/#chapter6.Discovery_by_Navigation"
---
# Discovery by Navigation

PubMed related articles are identified by a statistical text retrieval algorithm (3) that examines the title, abstract, and medical subject headings (MeSH terms). The connections between papers can be used to help make discoveries. An example of this is finding the last enzymatic step in the vitamin A biosynthetic pathway.

Lycopene cyclase in plants converts lycopene into β‑carotene, the immediate biochemical precursor of vitamin A. β‑Carotene is an essential nutrient, required in the diet of herbivores. This indicates that lycopene cyclase is not present in animals (with a few exceptions caused by horizontal gene transfer from fungi to insects), and that the enzyme responsible for converting β‑carotene into vitamin A is not present in plants:

![Image chapter6-Image001.jpg](https://www.ncbi.nlm.nih.gov/sites/books/NBK179288/bin/chapter6-Image001.jpg)

An initial literature search on the lycopene cyclase enzyme:

      esearch -db pubmed -query "lycopene cyclase" |

finds 334 articles. Looking up their precomputed neighbors:

      elink -related |

returns 20,407 papers, some of which might be expected to discuss other enzymes in the pathway.

We cannot reliably limit the results to animals within PubMed, but we can for sequence records, which are indexed by the NCBI taxonomy. Linking the publication neighbors to their associated protein records:

      elink -target protein -complete -log |

finds 2,319,795 sequences. (Using elink **‑complete** will bypass the default input sampling. Otherwise it returns a fraction of that number.) Restricting those results to mice, and limiting to curated Reference Sequence records:

      efilter -organism mouse -source refseq |

excludes plants, fungi, and bacteria, thus eliminating enzymes catalyzing the earlier intermediate reactions.

This matches only 15 sequences, which is small enough to examine by retrieving the individual records:

      efetch -format fasta

As expected, the results include the enzyme that splits β‑carotene into two molecules of retinal:

      …
      >NP_067461.2 beta,beta-carotene 15,15'-dioxygenase isoform 1 [Mus musculus]
      MEIIFGQNKKEQLEPVQAKVTGSIPAWLQGTLLRNGPGMHTVGESKYNHWFDGLALLHSFSIRDGEVFYR
      SKYLQSDTYIANIEANRIVVSEFGTMAYPDPCKNIFSKAFSYLSHTIPDFTDNCLINIMKCGEDFYATTE
      …

A better example used Entrez protein neighbors to instantly rediscover the similarity between a human colon cancer gene and microbial DNA repair genes. Unfortunately, precomputed BLAST links were discontinued due to the exponential growth of the sequence databases.
