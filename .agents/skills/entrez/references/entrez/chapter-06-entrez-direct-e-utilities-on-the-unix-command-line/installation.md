---
title: "Installation"
chapter: "Entrez Direct: E-utilities on the Unix Command Line"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter6/#chapter6.Installation"
---
# Installation

EDirect consists of a set of scripts and programs that are downloaded to the user's computer. It will run on Unix and Macintosh computers, and under the Cygwin Unix-emulation environment on Windows PCs. To install the EDirect software, open a terminal window and execute one of the following two commands:

      sh -c "$(curl -fsSL https://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh)"

      sh -c "$(wget -q https://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh -O -)"

This will download a number of scripts and several precompiled programs into an "edirect" folder in the user's home directory. It may then print an additional command for updating the PATH environment variable in the user's configuration file. The editing instructions will look something like:

      echo "export PATH=\$HOME/edirect:\$PATH" >> $HOME/.bash_profile

As a convenience, the installation process ends by offering to run the PATH update command for you. Answer "y" and press the Return key if you want it run. If the PATH is already set correctly, or if you prefer to make any editing changes manually, just press Return.

Finally, quit the running terminal application. Windows in subsequent terminal sessions will be able to locate the edirect folder and execute EDirect commands.

For best performance of Entrez network service requests, obtain an API Key from NCBI, and place the following line in your .bash_profile and .zshrc configuration files:

      export NCBI_API_KEY=unique_api_key

For faster downloading of NCBI release files, install the free Aspera Connect file transfer utility on your computer. It is available from the IBM Aspera Connect link at:

      https://www.ibm.com/products/aspera/downloads#cds
