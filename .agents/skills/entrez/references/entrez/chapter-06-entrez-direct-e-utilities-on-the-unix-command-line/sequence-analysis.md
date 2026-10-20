---
title: "Sequence Analysis"
chapter: "Entrez Direct: E-utilities on the Unix Command Line"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter6/#chapter6.Sequence_Analysis"
---
# Sequence Analysis

EDirect sequence processing functions are provided by the transmute program. They can handle huge sequences as normal strings, without requiring any special coding techniques or custom data structures.

## Reverse Complementation

A GenBank sequence can be converted to FASTA, reverse-complemented, and printed as FASTA with:

      efetch -db nuccore -id U00096 -format gb |
      gbf2fsa | transmute -revcomp | transmute -fasta -width 50

## Sequence Editing

The pBR322 cloning vector is a circular plasmid with unique restriction sites in two antibiotic resistance genes. The transmute **‑replace** function introduces a second BamHI restriction enzyme recognition site (based on a site-directed mutagenesis experiment) by modifying two bases in the *rop* gene:

      efetch -db nuccore -id J01749 -format fasta |
      transmute -replace -offset 1907 -delete GG -insert TC |
      …

## Pattern Searching

The modified sequence from above is then passed to transmute **‑search**, which takes a list of sequence patterns (with optional labels) and uses a finite-state algorithm to simultaneously search for all patterns:

      …
      transmute -search -circular GGATCC:BamHI GAATTC:EcoRI CTGCAG:PstI |
      align-columns -g 4 -a rl

The (0‑based) starting positions and restriction enzyme names for each match are printed in a table:

       374    BamHI
      1904    BamHI
      3606    PstI
      4358    EcoRI

The **disambiguate‑nucleotides** and **systematic‑mutations** scripts can generate all possible single-base substitutions in a pattern for use in a relaxed-stringency search.

## Six-Frame Translation

Protein translation uses a finite-state machine to slide a triplet-codon window along the sequence. State values are offsets into an amino acid lookup table. The next-state and reverse-complement transition tables, and an amino acid table for every genetic code, are all precomputed. A nucleotide sequence can then be translated in all six possible reading frames by an extremely fast loop of indexed lookups:

      efetch -db nuccore -id U54469.1 -format fasta |
      transmute -cds2prot -gcode 1 -all |

This produces regions of translated protein separated by asterisks representing stop codons:

      >U54469.1-1+
      RLLGFYNISQ*QAFPELPCSTIDSCLWPPKSQT*LKN*IIRIIIKPSNLR …
      >U54469.1-2+
      GCLGFITSVSDRHFQSCPVQQSIAAFGHQNPKLN*RIK*FE**LSPVTYA …
      …

The FASTAs are then converted to XML, and xtract **‑pept** splits the translated frames at each stop codon (asterisk), sequence gap (hyphen), or ambiguous translation ("X") character:

      fsa2xml |
      xtract -rec FASTA -pattern FASTA \
        -group "FASTA/*" -element "*" \
        -group FASTA -wrp FRAG -pept Seq

That appends individual peptide fragments to the original fields and creates 6 new XML records:

      …
      <FRAG>rllgfynisq</FRAG>
      <FRAG>qafpelpcstidsclwppksqt</FRAG>
      <FRAG>lkn</FRAG>
      …

## Feature Locations

A table of coding region locations and gene names can be saved directly as XML with xtract **‑insdx**:

      efetch -db nuccore -id NC_000011 -format gb -style master |
      xtract -insdx CDS gene feat_location > cds_loc.xml

The human β‑globin coding region location is then retrieved and stored in a Unix shell variable with:

      loc=$( xtract -input cds_loc.xml -pattern Rec \
               -if gene -equals HBB -element feat_location )

Location intervals are shown in biological order, where start is greater than stop on the minus strand:

      5227021..5226930,5226799..5226577,5225726..5225598

## Sequence Transformations

The cascading effects of a genomic SNP can be reproduced with transmute functions: **‑replace** applies the substitution, **‑extract** uses the location intervals from above to isolate the altered coding sequence, and **‑cds2prot** translates the modified CDS into protein with the designated genetic code:

      efetch -db nuccore -id NC_000011 -format fasta |
      transmute -replace -offset 5226773 -delete G -insert A |
      transmute -extract -1-based "$loc" |
      transmute -cds2prot -gcode 1 -frame 0 -every -trim

The genomic G to A transition on human chromosome 11 corresponds to the C to T substitution on the minus-strand-encoded β‑globin mRNA in the earlier SNP example:

      MVHLTPEEKSAVTALWGKVNVDEVGGEALGRLLVVYPWT*R …

## Gene Positions

An understanding of sequence coordinate conventions is necessary in order to use gene positions to retrieve the corresponding chromosome subregion with efetch or with the UCSC browser.

Sequence records displayed in GenBank or GenPept formats use a "**one‑based**" coordinate system, with sequence position numbers starting at "1":

        1 catgccattc gttgagttgg aaacaaactt gccggctagc cgcatacccg cggggctgga
       61 gaaccggctg tgtgcggcca cagccaccat cctggacaaa cccgaagacg tgagtgaggg
      121 tcggcgagaa cttgtgggct agggtcggac ctcccaatga cccgttccca tccccaggga
      181 ccccactccc ctggtaacct ctgaccttcc gtgtcctatc ctcccttcct agatcccttc
      …

Under this convention, positions refer to the sequence letters themselves:

      C   A   T   G   C   C   A   T   T   C
      1   2   3   4   5   6   7   8   9  10

and the position of the last base or residue is equal to the length of the sequence. The ATG initiation codon above is at positions 2 through 4, inclusive.

For computer programs, however, using "**zero‑based**" coordinates can simplify the arithmetic used for calculations on sequence positions. The ATG codon in the 0‑based representation is at positions 1 through 3. (The UCSC browser uses a hybrid, half-open representation, where the start position is 0‑based and the stop position is 1‑based.)

Software at NCBI will typically convert positions to 0‑based coordinates upon input, perform whatever calculations are desired, and then convert the results to a 1‑based representation for display. These transformations are done by simply subtracting 1 from the 1‑based value or adding 1 to the 0‑based value.

## Coordinate Conversions

Retrieving the docsum for a particular gene:

      esearch -db gene -query "BRCA2 [GENE] AND human [ORGN]" |
      efetch -format docsum |

returns the chromosomal position of that gene in "0‑based" coordinates:

      …
      <GenomicInfoType>
        <ChrLoc>13</ChrLoc>
        <ChrAccVer>NC_000013.11</ChrAccVer>
        <ChrStart>32315479</ChrStart>
        <ChrStop>32399671</ChrStop>
        <ExonCount>27</ExonCount>
      </GenomicInfoType>
      …

Piping the document summary to an xtract command using ‑element:

      xtract -pattern GenomicInfoType -element ChrAccVer ChrStart ChrStop

obtains the accession and 0‑based coordinate values:

      NC_000013.11    32315479    32399671

Efetch has **‑seq_start** and **‑seq_stop** arguments to retrieve a gene segment, but these expect the sequence subrange to be in 1‑based coordinates.

To address this problem, two additional efetch arguments, **‑chr_start** and **‑chr_stop**, were created to allow direct use of the 0‑based coordinates:

      efetch -db nuccore -format gb -id NC_000013.11 \
        -chr_start 32315479 -chr_stop 32399671

Xtract numeric extraction commands can also assist with coordinate conversion. Using xtract ‑inc:

      xtract -pattern GenomicInfoType -element ChrAccVer -inc ChrStart ChrStop

obtains the accession and 0‑based coordinates, then increments the positions to produce 1‑based values:

      NC_000013.11    32315480    32399672

EDirect knows the policies for sequence positions in all relevant Entrez databases (e.g., gene, snp, dbvar), and provides additional shortcuts for converting these to other conventions. For example:

      xtract -pattern GenomicInfoType -element ChrAccVer -1-based ChrStart ChrStop

understands that gene docsum ChrStart and ChrStop fields are 0‑based, sees that the desired output is 1‑based, and translates the command to convert coordinates internally using the ‑inc logic. Similarly:

      -element ChrAccVer -ucsc-based ChrStart ChrStop

leaves the 0‑based start value unchanged but increments the original stop value to produce the half-open form that can be passed to the UCSC browser:

      NC_000013.11    32315479    32399672

## Gene Sequence

Genes encoded on the minus strand of a sequence:

      esearch -db gene -query "DDT [GENE] AND mouse [ORGN]" |
      efetch -format docsum |
      xtract -pattern GenomicInfoType -element ChrAccVer ChrStart ChrStop |

have coordinates ("0‑based" in docsums) where the start position is greater than the stop:

      NC_000076.6    75773373    75771232

These values can be read into Unix variables by a "while" loop:

      while IFS=$'\t' read acn str stp
      do
        efetch -db nuccore -format gb \
          -id "$acn" -chr_start "$str" -chr_stop "$stp"
      done

The variables can then be used to obtain the reverse-complemented subregion in GenBank format:

      LOCUS       NC_000076               2142 bp    DNA     linear   CON 08-AUG-2019
      DEFINITION  Mus musculus strain C57BL/6J chromosome 10, GRCm38.p6 C57BL/6J.
      ACCESSION   NC_000076 REGION: complement(75771233..75773374)
      …
           gene            1..2142
                           /gene="Ddt"
           mRNA            join(1..159,462..637,1869..2142)
                           /gene="Ddt"
                           /product="D-dopachrome tautomerase"
                           /transcript_id="NM_010027.1"
           CDS             join(52..159,462..637,1869..1941)
                           /gene="Ddt"
                           /codon_start=1
                           /product="D-dopachrome decarboxylase"
                           /protein_id="NP_034157.1"
                           /translation="MPFVELETNLPASRIPAGLENRLCAATATILDKPEDRVSVTIRP
                           GMTLLMNKSTEPCAHLLVSSIGVVGTAEQNRTHSASFFKFLTEELSLDQDRIVIRFFP
                           …

The reverse complement of a plus-strand sequence range can be selected with efetch **‑revcomp**.
