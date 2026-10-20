---
title: "Biological Data in Entrez"
chapter: "Entrez Direct: E-utilities on the Unix Command Line"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter6/#chapter6.Biological_Data_in_Entrez"
---
# Biological Data in Entrez

EDirect provides additional functions, scripts, and exploration constructs to simplify the extraction of complex data obtained from the interconnected Entrez biological databases.

## Sequence Qualifiers

The NCBI data model for sequence records (5) is based on the central dogma of molecular biology. Sequences, including genomic DNA, messenger RNAs, and protein products, are "instantiated" with the actual sequence letters, and are assigned accession numbers for reference.

Features contain information about the biology of a region, including the transformations involved in gene expression. Qualifiers store specific details about a feature, such as the name of the gene, genetic code used for protein translation, or accession of the product sequence.

A **gene** feature indicates the location of a heritable region of nucleic acid that confers a measurable phenotype. An **mRNA** feature on genomic DNA represents the exonic and untranslated regions that remain after message transcription and intron splicing. A coding region (**CDS**) feature has a product reference to the translated protein sequence record:

![Image chapter6-Image002.jpg](https://www.ncbi.nlm.nih.gov/sites/books/NBK179288/bin/chapter6-Image002.jpg)

Since messenger RNA sequences are not always submitted with a genomic region, CDS features (which model the travel of ribosomes on transcript molecules) are traditionally annotated on the genomic sequence, with locations that encode the exonic intervals.

A qualifier can be dynamically generated from underlying data for the convenience of the user. Thus, the sequence of a mature peptide may be extracted from the mat_peptide feature's location on the precursor protein and displayed in a /peptide qualifier, even if a mature peptide is not instantiated.

As a convenience for exploring sequence records, the xtract **‑insd** helper function generates the appropriate nested extraction commands from feature and qualifier names on the command line. (The computed qualifiers **feat_location** (1-based), **feat_intervals** (0-based), and **sub_sequence** are also supported.)

## Snail Venom Peptide Sequences

A search for cone snail venom mature peptides:

      esearch -db protein -query "conotoxin" -feature mat_peptide |
      efetch -format gpc |
      xtract -insd complete mat_peptide "%peptide" product mol_wt peptide |

uses the xtract ‑insd function to print the accession number, mature peptide length, product name, calculated molecular weight, and amino acid sequence for a sample of neurotoxic peptides:

      AAD31916.1    24    O-superfamily conotoxin TxO3     2555    CYDGGTSCDSGIQCCSGWCIFVCF
      AIC77084.1    17    conotoxin Bt14.7                 1802    CAHSVPGMHPCKCNNTC
      AAD31921.1    24    omega conotoxin SVIA mutant 2    2419    CRPSGSPCGVTSICCGRCSRGKCT
      ADB43131.1    15    conotoxin Cal 1b                 1708    LCCKRHHGCHPCGRT
      ABE27008.1    25    conotoxin p114.2                 2773    GPGSAICNMACRLEHGHLYPFCHCR
      ABE27011.1    25    conotoxin fe14.2                 2697    SSGSTVCKMMCRLGYGHLYPSCGCR
      ABW16858.1    15    marmophin                        1915    DWEYHAHPKPNSFWT
      AIC77085.1    21    conotoxin Bt14.8                 2574    NECDNCMRSFCSMIYEKCRLK
      …

Piping the results to a series of Unix commands and EDirect scripts:

      grep -i conotoxin |
      filter-columns '10 <= $2 && $2 <= 30' |
      sort-table -u -k 2,2n |
      align-columns -

filters by product name, limits the results to a specified range of peptide lengths, sorts the table by peptide length, chooses one example for each length, and aligns the columns for cleaner printing:

      ADB43131.1    15    conotoxin Cal 1b      1708    LCCKRHHGCHPCGRT
      ADB43128.1    16    conotoxin Cal 5.1     1829    DPAPCCQHPIETCCRR
      AIC77105.1    17    conotoxin Lt1.4       1705    GCCSHPACDVNNPDICG
      ADB43129.1    18    conotoxin Cal 5.2     2008    MIQRSQCCAVKKNCCHVG
      ADD97803.1    20    conotoxin Cal 1.2     2206    AGCCPTIMYKTGACRTNRCR
      AIC77085.1    21    conotoxin Bt14.8      2574    NECDNCMRSFCSMIYEKCRLK
      ADB43125.1    22    conotoxin Cal 14.2    2157    GCPADCPNTCDSSNKCSPGFPG
      AIC77154.1    23    conotoxin Bt14.19     2578    VREKDCPPHPVPGMHKCVCLKTC
      …

The xtract **‑insdx** variant:

      esearch -db protein -query "conotoxin" | efilter -query "mat_peptide [FKEY]" |
      efetch -format gpc |
      xtract -insdx complete mat_peptide "%peptide" product mol_wt peptide |
      xtract -pattern Rec -select product -contains conotoxin |
      xtract -pattern Rec -sort mol_wt

saves the output table directly as XML, with the XML tag names taken from the original qualifier names:

      … 
      <Rec>
        <accession>AAO33169.1</accession>
        <feature_key>mat_peptide</feature_key>
        <peptide_Len>16</peptide_Len>
        <product>alpha-conotoxin GIC</product>
        <mol_wt>1615</mol_wt>
        <peptide>GCCSHPACAGNNQHIC</peptide>
      </Rec>
      <Rec>
        <accession>AIC77099.1</accession>
        <feature_key>mat_peptide</feature_key>
        <peptide_Len>16</peptide_Len>
        <product>conotoxin Im1.2</product>
        <mol_wt>1669</mol_wt>
        <peptide>GCCSHPACNVNNPHIC</peptide>
      </Rec>
      …

Qualifier names with prefix shortcuts "**\#**" and "**%**" are modified to use "\_Num" and "\_Len" suffixes, respectively.

## Missing Qualifiers

For records where a particular qualifier is missing:

      esearch -db protein -query "RAG1 [GENE] AND Mus musculus [ORGN]" |
      efetch -format gpc |
      xtract -insd source organism strain |
      sort-table -u -k 2,3

a dash is inserted as a placeholder:

      P15919.2       Mus musculus               -
      AAO61776.1     Mus musculus               129/Sv
      NP_033045.2    Mus musculus               C57BL/6
      EDL27655.1     Mus musculus               mixed
      BAD69530.1     Mus musculus castaneus     -
      BAD69531.1     Mus musculus domesticus    BALB/c
      BAD69532.1     Mus musculus molossinus    MOA

## Recursive Taxonomy Data

Certain XML objects returned by efetch are recursively defined, including Taxon in ‑db taxonomy and Gene-commentary in ‑db gene. Thus, they can contain nested objects with the same XML tag.

Retrieving a set of taxonomy records:

      efetch -db taxonomy -id 9615,9606 -format xml

produces XML with nested Taxon objects (marked below with line references) for each rank in the taxonomic lineage:

        <TaxaSet>
    1     <Taxon>
            <TaxId>9606</TaxId>
            <ScientificName>Homo sapiens</ScientificName>
            …
            <LineageEx>
    2         <Taxon>
                <TaxId>131567</TaxId>
                <ScientificName>cellular organisms</ScientificName>
                <Rank>no rank</Rank>
    3         </Taxon>
    4         <Taxon>
                <TaxId>2759</TaxId>
                <ScientificName>Eukaryota</ScientificName>
                <Rank>superkingdom</Rank>
    5         </Taxon>
              …
            </LineageEx>
            …
    6     </Taxon>
    7     <Taxon>
            <TaxId>9615</TaxId>
            <ScientificName>Canis lupus familiaris</ScientificName>
            …
    8     </Taxon>
        </TaxaSet>

Xtract tracks XML object nesting to determine that the \<Taxon\> start tag on line 1 is closed by the \</Taxon\> stop tag on line 6, and not by the first \</Taxon\> encountered on line 3.

To accommodate recursively-defined data, entry (by ‑element) to an internal object is blocked when its name matches the current exploration container.

The **star / child** construct bypasses the search constraint:

      efetch -db taxonomy -id 9606,7227 -format xml |
      xtract -pattern Taxon -block "*/Taxon" \
        -tab "\n" -element TaxId,ScientificName

to allow controlled descent to the next level:

      131567    cellular organisms
      2759      Eukaryota

Using **double star / child** recursively visits every object regardless of depth, and can flatten a complex structure into a linear set of elements in a single step:

      efetch -db taxonomy -id 9606 -format xml |
      xtract -pattern Taxon \
        -first TaxId -tab "\n" -element ScientificName \
        -block "**/Taxon" -if Rank -is-not "no rank" -and Rank -excludes "root" \
          -tab "\n" -element Rank,ScientificName

This prints all of the individual internal lineage nodes:

      9606          Homo sapiens
      domain        Eukaryota
      clade         Opisthokonta
      kingdom       Metazoa
      clade         Eumetazoa
      clade         Bilateria
      clade         Deuterostomia
      phylum        Chordata
      subphylum     Craniata
      clade         Vertebrata
      clade         Gnathostomata
      clade         Teleostomi
      clade         Euteleostomi
      superclass    Sarcopterygii
      clade         Dipnotetrapodomorpha
      clade         Tetrapoda
      clade         Amniota
      class         Mammalia
      …

## Genes in a Region

Records for protein-coding genes on the human X chromosome are retrieved by running:

      esearch -db gene -query "Homo sapiens [ORGN] AND X [CHR]" |
      efilter -status alive -type coding | efetch -format docsum |

Gene names and chromosomal positions are extracted by piping the records to:

      xtract -pattern DocumentSummary -NAME Name -DESC Description \
        -block GenomicInfoType -if ChrLoc -equals X \
          -min ChrStart,ChrStop -element "&NAME" "&DESC" |

Exploring each GenomicInfoType is needed because of pseudoautosomal regions at the ends of the X and Y chromosomes:

      …
      <GenomicInfo>
        <GenomicInfoType>
          <ChrLoc>X</ChrLoc>
          <ChrAccVer>NC_000023.11</ChrAccVer>
          <ChrStart>155997630</ChrStart>
          <ChrStop>156013016</ChrStop>
          <ExonCount>14</ExonCount>
        </GenomicInfoType>
        <GenomicInfoType>
          <ChrLoc>Y</ChrLoc>
          <ChrAccVer>NC_000024.10</ChrAccVer>
          <ChrStart>57184150</ChrStart>
          <ChrStop>57199536</ChrStop>
          <ExonCount>14</ExonCount>
        </GenomicInfoType>
      </GenomicInfo>
      …

Without limiting to chromosome X, the copy of IL9R near the "q" telomere of chromosome Y would be erroneously placed with genes that are near the X chromosome centromere, shown here in between SPIN2A and ZXDB:

      …
      57121860    FAAH2     fatty acid amide hydrolase 2
      57133042    SPIN2A    spindlin family member 2A
      57184150    IL9R      interleukin 9 receptor
      57592010    ZXDB      zinc finger X-linked duplicated B
      …

The ‑if statement eliminates coordinates from pseudoautosomal gene copies present on Y chromosome telomeres. Results can now be sorted by position, and then filtered and partitioned:

      sort-table -k 1,1n | cut -f 2- |
      grep -v pseudogene | grep -v uncharacterized | grep -v hypothetical |
      between-two-genes AMER1 FAAH2

to produce an ordered table of known genes located between two markers flanking the centromere:

      FAAH2      fatty acid amide hydrolase 2
      SPIN2A     spindlin family member 2A
      ZXDB       zinc finger X-linked duplicated B
      NLRP2B     NLR family pyrin domain containing 2B
      ZXDA       zinc finger X-linked duplicated A
      SPIN4      spindlin family member 4
      ARHGEF9    Cdc42 guanine nucleotide exchange factor 9
      AMER1      APC membrane recruitment protein 1

## SNP-Modified Product Pairs

Single nucleotide polymorphisms can represent different substitutions at the same position:

      efetch -db snp -id 11549407 -format docsum |

but variation records do not explicitly match a specific CDS modification to its altered protein product.

The hgvs2spdi script converts 1‑based HGVS (6) data ("**[NM_000518.5](https://www.ncbi.nlm.nih.gov/nuccore/1401724401):c.118C\>T**") into 0‑based SPDI (7) format ("**[NM_000518.5](https://www.ncbi.nlm.nih.gov/nuccore/1401724401):167:C:T**"). For SNPs on cDNA transcripts the position is CDS-relative, and the script retrieves the GenBank record in order to calculate the absolute sequence offset:

      snp2hgvs | hgvs2spdi | spdi2tbl | tbl2prod

The tbl2prod step translates the coding region locations (after nucleotide substitution), and sorts them with protein sequences (after residue replacement) to produce adjacent matching CDS/protein pairs:

      rs11549407    NM_000518.5:167:C:T    MVHLTPEEKSAVTALWGKVNVDEVGGEALGRLLVVYPWT*R …
      rs11549407    NP_000509.1:39:Q:*     MVHLTPEEKSAVTALWGKVNVDEVGGEALGRLLVVYPWT*R …
      rs11549407    NM_000518.5:167:C:G    MVHLTPEEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTER …
      rs11549407    NP_000509.1:39:Q:E     MVHLTPEEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTER …
      rs11549407    NM_000518.5:167:C:A    MVHLTPEEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTKR …
      rs11549407    NP_000509.1:39:Q:K     MVHLTPEEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTKR …
      …
