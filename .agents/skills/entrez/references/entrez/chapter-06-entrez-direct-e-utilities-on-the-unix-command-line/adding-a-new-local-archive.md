---
title: "Adding a New Local Archive"
chapter: "Entrez Direct: E-utilities on the Unix Command Line"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter6/#chapter6.Adding_a_New_Local_Archive"
---
# Adding a New Local Archive

New database domains can be added using records obtained from external public data resources, or with private information taken from a laboratory's research results or a hospital's clinical trial data.

## Archive Scripts

The first step is to create a one-line archive script that sends command-line arguments to **xbuild**. A sample database indexed by peptide sequence fragments is built with **archive‑peptide**, which runs:

      xbuild -db peptide -project peptide "$@"

A primary database has the same values for the **‑db** and **‑project** arguments. It may import structured records, optionally caching simpler derived records, or it may assemble records from tabular data.

Secondary projects add new indexed fields or links to primary databases. The **archive‑nihocc** script:

      xbuild -db pubmed -project nihocc "$@"

adds reciprocal citation reference links to the pubmed database, but does not create its own records.

## Project Directories

A new database or project next requires adding a project directory within the **edirect / extern** folder. The **edirect / extern / peptide** subfolder contains several helper scripts. By convention, their names are composed of a formal step in the build process, a hyphen, and the project name:

      download-peptide
      populate-peptide
      index-peptide

A single configuration file named for the project is also present:

      peptide.ini

Secondary project files go in an **edirect / extern / {database}-{project}** subfolder.

## Configuration Files

Project-specific configuration files guide the build process. The **peptide.ini** file provides sections for archiving and posting, as well as information used by xfetch to retrieve the derived records:

      [info]
      db=peptide
      project=peptide

      [archive]
      name=PeptInfo
      index=PeptInfo/UID

      [fetch]
      name=PeptInfo
      set=PeptInfoSet

In contrast, the **nihocc.ini** configuration file adds link flags in the merge and posting sections:

      [info]
      db=pubmed
      project=nihocc

      [merge]
      link=true

      [posting]
      fields="CITED CITES"
      link=true

while **pubmed.ini** has a links section with destination databases for xlink **‑target** arguments:

      …
      [links]
      CITED=pubmed
      CITES=pubmed
      PMCID=pmc

## "Download" Helper

The actual helper files needed for any given project depends on the source of the records, and on any accessory data files that must be retrieved separately. For each archive step, the helper file is "sourced" by an intermediate script, which executes it in the context of properly initialized variables.

An abridged version of the **download‑peptide** file is shown below:

      FilterByDivision() {

        dir="$1"

        if [ "$dir" = "archaea" ]
        then
          grep "wp_"
        elif [ "$dir" = "bacteria" ] || [ "$dir" = "plasmid" ]
        then
          grep "."
        else
          grep -v "wp_"
        fi
      }

      if [ -d "${sourceBase}" ]
      then
        cd "${sourceBase}"

        if [ -n "$custom" ]
        then
          nquire -lst ftp.ncbi.nih.gov/refseq/release "$custom" < /dev/null |
          grep gpff | FilterByDivision "$custom" | sort -V | skip-if-file-exists |
          while read fl
          do
            echo "$fl" | nquire -asp ftp.ncbi.nih.gov/refseq/release "$custom"
          done
        fi
      fi

For this example, a RefSeq division folder is passed by archive‑peptide using the **‑custom** argument:

      archive-peptide -custom "viral"

In the real download-peptide file, the custom variable contains one or more division abbreviations:

      archive-peptide -custom "ARC FUN PRO VRL"

Individual build steps can be executed with **‑step**, or bypassed with **‑skip**:

      archive-peptide -step IDX
      archive-peptide -index -skip "SET CHK DAT DWN GEN POP RES IDX COL MRG PST CLR"

For the full download‑peptide helper file, running just the download step without a ‑custom argument prints a table displaying the division abbreviation, actual subfolder name, number of files, and total number of bytes, for each taxonomic division (formatted by align‑columns **‑h 2 ‑g 4 ‑a llrm**):

      ARC    archaea                   9      1,956,632,000
      BCT    bacteria                825    181,043,837,778
      FUN    fungi                    36      4,029,672,534
      INV    invertebrate             93      6,206,662,948
      MAM    vertebrate_mammalian    121      5,892,072,442
      MIT    mitochondrion             1        113,495,942
      PLN    plant                    67      4,368,670,110
      PRO    protozoa                  7        786,600,954
      PSM    plasmid                   9      1,388,949,422
      PST    plastid                   3        512,697,988
      VRL    viral                     1        227,714,284
      VRT    vertebrate_other        178     10,748,398,867

The counts refer to data files run through the FilterByDivision function. This favors the non-redundant "WP" protein sequence files for archaea and bacteria, which were introduced for prokaryotes in 2013.

## "Populate" Helper

Unless the source records are perfect for your intended use, you can design a more convenient structure containing just the information you want.

The **populate‑peptide** script originally converted the downloaded GenPept flatfiles to INSDSeq XML. The current record number, which was obtained by using a **plus sign** ("**+**") as an xtract ‑element argument, then became the integer access key for caching the derived record:

      base=${fl%.gz}
      if [ ! -f "${sentinelsBase}/$base.snt" ] && [ -s "$fl" ]
      then

        gunzip -c "$fl" | gbf2xml |
        xtract -rec PeptInfo -pattern INSDSeq \
          -wrp UID -element "+" \
          …
          -wrp Sequence -element INSDSeq_sequence |
        transmute -format |
        rchive -gzip -archive -db "$dbase" -index UID -pattern PeptInfo

        touch "${sentinelsBase}/$base.snt"
      fi

Each protein record is converted into a simple PeptInfo structure with a unique identifier value:

      <PeptInfo>
        <UID>302720946</UID>
        <Accession>WP_003047541</Accession>
        <Organism div="BCT" taxid="271">Thermus aquaticus</Organism>
        <Product>type I DNA topoisomerase</Product>
        <Sequence>mpkkpktqgaahlgeggpkaearattlvvvespakarsiqkmlgp … </Sequence>
        …

(The current code calls a direct conversion function to bypass the INSDSeq intermediate. It also adds the previous maximum UID value, which allows separate divisions to be processed at different times.)

## "Index" Helper

Given a protein sequence, **‑element** will show it as a polypeptide, **‑letters** will split it into individual amino acids, and **‑pentamers** will create overlapping oligopeptides (residues 1‑5, 2‑6, 3‑7, etc.):

      -element      mpkkpktqgaahlgeggpkaearattlvvvespakarsiqk …
      -letters      m p k k p k t q g a a h l g e g g p k a e …
      -pentamers    mpkkp pkkpk kkpkt kpktq pktqg ktqga tqgaa …

The ‑letters option resembles words in a sentence, which is the starting point for building the positional indices that support phrase and proximity searches. But a standard phrase search will drop candidates that have even a single mismatch to the query sequence.

A better approach for finding the most similar sequences is to use xsearch **‑match** on the pentamers. Indexing short overlapping peptides would make more efficient use of the local archive's directory hierarchy. The choice of 5‑mers was based on results from NCBI's early SEQR indexed search experiment (10). For convenience, when peptide fragments are indexed using the PENT field, ‑match will internally split the protein query sequence into overlapping pentamers before running the search:

      xsearch -db peptide -match "rlgrdtadmiqlikefdaqgvavrfiddgistdgdmgqmv [PENT]"

The result is a set of record keys ranked by the number of unique overlapping fragments matched.

For primary databases, index helpers embed an xtract command in a Unix "HERE" document. This is then passed as an argument for execution within an incremental indexing function. (Secondary projects do not need this invalidated index repopulation mechanism.)

A simplified excerpt of the **index‑peptide** script:

      read -r -d '' idxtxt <<- EOS
      xtract -set IdxDocumentSet -rec IdxDocument \
        -pattern PeptInfo -UID PeptInfo/UID \
          -wrp IdxUid -element "&UID" -clr -rst -tab "" \
          -group PeptInfo -pkg IdxSearchFields \
            …
            -block Product -wrp PROD -indexer Product \
            -block Organism -wrp ORGN -element Organism -rst \
              -wrp DIV -element @div \
            -block Sequence  …  -wrp PENT -pentamers Sequence
      EOS

      IncrementalIndex "${idxtxt}"

will split the overlapping pentamers into separate terms for regular indexing:

      …
      <IdxDocument>
        <IdxUid>302720946</IdxUid>
        <IdxSearchFields>
          <UID>0302720946</UID>
          <ACCN-WP>003047541</ACCN-WP>
          <PROD pos="3">dna</PROD>
          <PROD pos="2">i</PROD>
          <PROD pos="4">topoisomerase</PROD>
          <PROD pos="1">type</PROD>
          <ORGN>Thermus aquaticus</ORGN>
          <DIV>BCT</DIV>
          <SLEN>833</SLEN>
          <MLWT>93298</MLWT>
          <PENT>mpkkp</PENT>
          <PENT>pkkpk</PENT>
          …

Text fields can use **‑indexer** to create positional indices, but it also removes stop words, which would discard valid pentapeptides like "apply", "every", and "never". Those attributes will likely be decoupled by adding new configuration options to allow finer adjustment of field-specific behavior.

Later build steps, starting with index inversion, are standardized, and do not need external helper files.

## Importing Data Tables

Large data tables are processed by programs written in the Go programming language. They are compiled and executed on-the-fly by helpers calling "**go run**". The central loop in **prep‑nihocc.go**, simplified for brevity, and without the usual reality checks and periodic output buffer flushing, is:

      var bldr strings.Builder

      wrtr := bufio.NewWriter(os.Stdout)
      scanr := bufio.NewScanner(os.Stdin)

      for scanr.Scan() {

          line := scanr.Text()
          if line == "citing,referenced" {
              continue
          }

          cols := strings.Split(line, ",")
          fst, scd := cols[0], cols[1]

          pdFst, pdScd := padNumericID(fst), padNumericID(scd)

          bldr.WriteString(fst + "\tCITED\t" + pdScd + "\n")
          bldr.WriteString(scd + "\tCITES\t" + pdFst + "\n")

          txt := bldr.String()
          wrtr.WriteString(txt[:])
          bldr.Reset()
      }

      wrtr.Flush()

## Archive Configuration File

More flexible drive management uses an environment variable that points to a configuration file:

      export EDIRECT_LOCAL_CONFIG="${HOME}/.edirectrc"

(For quick evaluation, you can instead place an **edirect.ini** configuration file into the edirect folder.)

The configuration file has one section per database, with entries pointing to solid-state drives:

      [pubmed]

An **ARCHIVE** entry is required, and defaults to having all folders in the absence of other entries, but it is primarily for the **Archive**, **Data**, and **Posting** folders needed for record retrieval and indexed queries:

      ARCHIVE=/Volumes/archive/

If set, a **WORKING** entry will move **Extras**, **Invert**, **Merged**, **Scratch**, and **Source** folders, used for building the archive and search indices but not for active queries, to another drive:

      WORKING=/Volumes/builder-pool-pm/

(**Scratch** prevents secondary projects from colliding with primary incremental inverted index files.)

Independently, **POSTING** and **SOURCES** can move their respective folders to other drives. The source file repository can even use a large, rotating hard disk, since it only needs sequential streaming access:

      POSTING=/Volumes/pm-posting/
      SOURCES=/Volumes/common-sources-1/

An optional **\[default\]** section applies to any databases that do not have their own named sections.

With this configuration mechanism, each separate database can point to its own set of unique drives.

## Solid-State Drive Preparation

To initialize a solid-state drive for hosting the local archive on a Mac, log into an admin account, run Disk Utility, choose View → Show All Devices, select the top-level external drive, and press the Erase icon. Set the Scheme popup to GUID Partition Map, and APFS will appear as a format choice. Set the Format popup to APFS, enter the desired name for the volume, and click the Erase button.

To finish the drive configuration, disable Spotlight indexing on the drive with:

      sudo mdutil -i off "${EDIRECT_LOCAL_ARCHIVE}"
      sudo mdutil -E "${EDIRECT_LOCAL_ARCHIVE}"

and disable FSEvents logging with:

      sudo touch "${EDIRECT_LOCAL_ARCHIVE}/.fseventsd/no_log"

Also exclude the drive from being backed up by Time Machine or scanned by a virus checker, and, in Apple → System Settings → Privacy & Security → Full Disk Access, turn on the Terminal slide switch.
