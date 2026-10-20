---
title: "Python Integration"
chapter: "Entrez Direct: E-utilities on the Unix Command Line"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter6/#chapter6.Python_Integration"
---
# Python Integration

Controlling EDirect from Python scripts is easily done with assistance from the **edirect.py** library file, which is included in the EDirect archive.

At the beginning of your program, import the edirect module with the following commands:

      #!/usr/bin/env python3

      import sys
      import os
      import shutil

      sys.path.insert(1, os.path.dirname(shutil.which('xtract')))
      import edirect

The first argument to **edirect.execute** is the Unix command you wish to run. It can be a string:

      ("efetch -db nuccore -id NM_000518.5 -format fasta")

or a sequence of strings, which allows a variable's value to be substituted for a specific parameter:

      accession = "NM_000518.5"
      (('efetch', '-db', 'nuccore', '-id', accession, '-format', 'fasta'))

An optional second argument accepts data to be passed to the Unix command through stdin. Multiple steps are chained together by using the result of the previous command as the data argument in the next command:

      seq = edirect.execute("efetch -db nuccore -id NM_000518.5 -format fasta")
      sub = edirect.execute("transmute -extract -1-based -loc 51..494", seq)
      prt = edirect.execute(('transmute', '-cds2prot', '-every', '-trim'), sub)

Data piped to the script itself is relayed by using **sys.stdin.read()** as the second argument.

Alternatively, the **edirect.pipeline** function can execute a string containing several piped commands:

      edirect.pipeline('''efetch -db nuccore -id NM_000518.5 -format gb |
                          xtract -insd CDS gene product feat_location''')

or can accept a sequence of individual command strings to be piped together for execution:

      edirect.pipeline(('efetch -db protein -id NP_000509.1 -format gp',
                        'xtract -insd Protein mol_wt sub_sequence'))

Hiding details (e.g., isinstance, shlex.join, shlex.split, and subprocess.run) inside a common module means that biologists who are new to coding could control an entire analysis pipeline from their first Python program.

An **edirect.efetch** shortcut that uses named arguments is also available:

      edirect.efetch(db="nuccore", id="NM_000518.5", format="fasta")

To run a custom shell script, make sure the execute permission bit is set, supply the full execution path, and follow it with any command-line arguments:

      db = "pubmed"
      res = edirect.execute(("./datefields.sh", db), "")
