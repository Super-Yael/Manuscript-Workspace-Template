---
title: "Compiled Go Programs"
chapter: "Entrez Direct: E-utilities on the Unix Command Line"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter6/#chapter6.Compiled_Go_Programs"
---
# Compiled Go Programs

A program written in a compiled language is translated into a computer's native machine instruction code, and will run much faster than an interpreted script. Piping FASTA data to the basecount binary executable (compiled from the basecount.go source code file, below):

      efetch -db nuccore -id J01749,U54469 -format fasta | basecount

will return rows containing an accession number followed by counts for each base:

      J01749.1    A 983    C 1210    G 1134    T 1034
      U54469.1    A 849    C 699     G 585     T 748

Google's Go language ("golang") has a straightforward build process that eliminates the complexity of typical package management systems. There are no complicated makefiles or separate header files. Circular dependencies between packages are not permitted.

Compilation of Go programs is fast, and error messages are clear and informative. For run-time failures (such as a nil pointer dereference, out-of-bounds array access, or thread deadlock), the error message includes the relevant stack traces with source code line numbers.

Programs in Go start with **package main** and then **import** additional software libraries (many included with Go, others residing in commercial repositories like github.com):

      package main

      import (
          "cmp"
          "eutils"
          "fmt"
          "maps"
          "os"
          "slices"
      )

Each compiled Go binary has a single **main** function, which is where program execution begins:

      func main() {

The fsta **variable** is assigned to a data **channel** that streams individual FASTA records one at a time:

          fsta := eutils.FASTAConverter(os.Stdin, false)

The countLetters **subroutine** will be called with the identifier and sequence of each FASTA record:

          countLetters := func(id, seq string) {

An empty counts **map** is created for each sequence, and its memory is freed when the subroutine exits:

              counts := make(map[rune]int)

A **for** loop on the **range** of the sequence string visits each sequence letter. The map keeps a running count for each base or residue, with "**++**" incrementing the current value of the letter's map entry:

              for _, base := range seq {
                  counts[base]++
              }

A sorted keys **array** is produced by calling **slices.SortedFunc**. The alphabetical sort order is determined by the second argument, which is is an **anonymous** function literal:

              keys := slices.SortedFunc(maps.Keys(counts),
                  func(i, j rune) int { return cmp.Compare(i, j) })

The sequence identifier is printed in the first column:

             fmt.Fprintf(os.Stdout, "%s", id)

Iterating over the array prints letters and base counts in alphabetical order, with tabs between columns:

              for _, base := range keys {
                  num := counts[base]
                  fmt.Fprintf(os.Stdout, "\t%c %d", base, num)
              }

A newline is printed at the end of the row, and then the subroutine exits, clearing the map and array:

              fmt.Fprintf(os.Stdout, "\n")
          }

The remainder of the main function uses a loop to **drain** the fsta channel, passing the identifier and sequence string of each successive FASTA record to the countLetters function. The main function then ends with a final closing brace:

          for fsa := range fsta {
              countLetters(fsa.SeqID, fsa.Sequence)
          }
      }

Save the following script to a file named **build.sh**, in the same directory as the **basecount.go** file. Adjust optional GOOS and GOARCH environment variables to cross-compile for a different platform:

      #!/bin/bash

      if [ ! -f "go.mod" ]
      then
        go mod init "$( basename $PWD )"
        echo "replace eutils => $HOME/edirect/eutils" >> go.mod
        go get eutils
      fi
      if [ ! -f "go.sum" ]
      then
        go mod tidy
      fi
      if [ ! -d "vendor" ]
      then
        go mod vendor -e
      fi

      for fl in *.go  do
        env GOOS=darwin GOARCH=arm64 go build -o "${fl%.go}" "$fl"
      done

Other build flags can show escape analysis decisions or strip debugging symbols from the executable.

The build script creates module files used to track dependencies and retrieve imported packages. It also computes the path for finding the local **eutils** helper library included with EDirect. Set the Unix execution permission bit for the build script and compile the program(s) by running:

      chmod +x build.sh
      ./build.sh

This produces a self-contained binary executable. With no reliance on local dynamic-link libraries, programs will not break when users update their development environments.
