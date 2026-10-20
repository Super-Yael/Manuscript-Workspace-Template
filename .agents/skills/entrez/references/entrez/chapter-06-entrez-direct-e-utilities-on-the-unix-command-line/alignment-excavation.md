---
title: "Alignment Excavation"
chapter: "Entrez Direct: E-utilities on the Unix Command Line"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter6/#chapter6.Alignment_Excavation"
---
# Alignment Excavation

NHGRI's experimental GeneMachine program could run several gene prediction algorithms and BLAST searches, gathering the results to assemble a richly-annotated sequence record.

NCBI's Sequin program could read the record and display the combined ranges of separate alignments in a "smear" that made it possible to see an emerging image of the underlying gene structures:

![Image chapter6-Image003.jpg](https://www.ncbi.nlm.nih.gov/sites/books/NBK179288/bin/chapter6-Image003.jpg)

While interesting patterns (e.g., potential antisense regulation transcripts) might occasionally be noticed by visual inspection, examination by eye is tedious, error-prone, and does not scale to chromosome size. However, the process of converting raw BLAST alignment data in ASN.1 format to a computable, tab-delimited data table, is easily automated with a chain of simple xtract commands.

The first xtract reads the ASN.1 sequence record, converts it internally to XML, and uses **‑select** to conditionally filter out everything but the BLASTN‑mRNA annotation:

      xtract -pattern annot_E -select label/str -equals "BLASTN - mrna" |

For each alignment, the segment start positions (and strands) are implicitly paired - one for the genomic sequence followed by one for the mRNA sequence. One particular alignment has three segments (here showing the original ASN.1 on the right, and the automatically-derived XML on the left):

      <starts>                                                                     starts {
        <starts_E>5613</starts_E>                                                    5613,
        <starts_E>842</starts_E>                                                     842,
        <starts_E>-1</starts_E>                                                      -1,
        <starts_E>961</starts_E>                                                     961,
        <starts_E>5599</starts_E>                                                    5599,
        <starts_E>962</starts_E>                                                     962
      </starts>

The "-1" start position indicates an internal gap in the genomic assembly relative to the cloned mRNA sequence, and the length of "1" (below) says that it is a single base deletion. The "underscore‑E" suffix indicates that the object was derived from an unlabeled element within a named ASN.1 sequence or set.

A second xtract explores each alignment, using **‑odd** to get the first (genomic) value in each start pair:

      … -pattern align_E -block starts -wrp Start -odd starts_E … |

Each element is wrapped with a descriptive name, and the fields are packed into a novel structure:

      <Start>5613</Start>
      <Start>-1</Start>
      <Start>5599</Start>
      <Length>119</Length>
      <Length>1</Length>
      <Length>14</Length>

The range of an alignment can be calculated from the first and last start positions, and either the first or the last segment length value, depending upon the strand. Those values are obtained using **‑first** and **‑last** positional arguments:

      … -wrp FirstPos -first Start -wrp LastPos -last Start … |

and the new fields are packaged in a different ad hoc XML structure:

      <FirstPos>5613</FirstPos>
      <LastPos>5599</LastPos>
      <FirstLen>119</FirstLen>
      <LastLen>14</LastLen>
      <Strand>minus</Strand>

A final xtract command performs two parallel explorations, one for each strand:

      …
      -block Rec -if Strand -equals plus -def "-" \
        -element Accn Score FirstPos LastPos LastLen Strand \
      -block Rec -if Strand -equals minus -def "-" \
        -element Accn Score LastPos FirstPos FirstLen Strand |

producing a tab-delimited intermediate table:

      AY046051.1    126    5599    5613    119    minus

A print‑columns command calculates the end position and total length of each alignment, and the results are sorted by strand and genomic location. The "0‑based" position fields are then incremented to produce "1‑based" final values:

      print-columns '$1, $2, $3, $4 + $5 - 1, $4 + $5 - $3, $6' |
      sort-table -k 6,6fr -k 3,3n -k 4,4nr -k 1,1f |
      print-columns '$1, $2, $3 + 1, $4 + 1, $5, $6'

The adjusted table values, which are suitable for further computation:

      AY046051.1    126    5600    5732    133    minus

now match the coordinates in the standard BLAST report:

      5600  AACTTAATACATAA-GTTGGTAGCCCACAATGTGAAAGATTAAATTAAAACTCATCCATT  5658
            |||||||||||||| |||||||||||||||||||||||||||||||||||||||||||||
      976   AACTTAATACATAATGTTGGTAGCCCACAATGTGAAAGATTAAATTAAAACTCATCCATT  917
                                          …
