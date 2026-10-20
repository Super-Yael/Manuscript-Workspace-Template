---
title: "Shell Scripting"
chapter: "Entrez Direct: E-utilities on the Unix Command Line"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter6/#chapter6.Shell_Scripting"
---
# Shell Scripting

The Unix "shell" is a command interpreter that supports user-defined variables, conditional statements, and repetitive execution loops. Shell scripts are saved in files, and are referenced by file name.

Comments start with a pound sign ("**\#**") and are ignored. Quotation marks within quoted strings are entered by "escaping" with a backslash ("**\\**"). Subroutines (functions) can be used to collect common code or simplify the organization of the script.

Given a tab-delimited file of feature keys and values, where each gene is followed by its coding regions:

      gene    matK
      CDS     maturase K
      gene    ATP2B1
      CDS     ATPase 1 isoform 2
      CDS     ATPase 1 isoform 7

the **cat** command can pipe the file contents to a shell script that reads the data one line at a time.

Dissecting the code, the first line selects the Bash shell for executing the script on the user's machine:

      #!/bin/bash

The latest gene name is stored in the "gene" variable, which is first initialized to an empty string:

      gene=""

The **while** command sequentially reads each line of the input file, **IFS** indicates tab-delimited fields, and **read** saves the first field in the "feature" variable and the remaining text in the "product" variable. The statements between the **do** and **done** commands are then executed separately for each input line:

      while IFS=$'\t' read feature product
      do

The **if** command retrieves the current value stored in the feature variable (indicated by placing a dollar sign in front of the variable name) and compares it to the word "gene":

        if [ "$feature" = "gene" ]

If the feature key was "gene", it runs the **then** section, which copies the contents of the current line's "product" value into the persistent "gene" variable. Otherwise, the **else** section prints the saved gene name and the current coding region product name, separated by a tab character. The conditional block is terminated with a **fi** instruction ("if" in reverse):

        then
          gene="$product"
        else
          echo -e "$gene\t$product"
        fi
      done

(Prior to **else**, a series of **elif / then** commands can encode multiple conditional blocks.)

The resulting output has paired gene and CDS product names in separate columns on individual rows:

      matK      maturase K
      ATP2B1    ATPase 1 isoform 2
      ATP2B1    ATPase 1 isoform 7
