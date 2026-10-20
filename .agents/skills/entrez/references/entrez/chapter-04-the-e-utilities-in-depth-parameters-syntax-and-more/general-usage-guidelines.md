---
title: "General Usage Guidelines"
chapter: "The E-utilities In-Depth: Parameters, Syntax and More"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter4/#chapter4.General_Usage_Guidelines"
---
# General Usage Guidelines

Please see [Chapter 2](https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter2/) for a detailed discussion of E-utility usage policy. The following two parameters should be included in all E-utility requests.

## tool

Name of application making the E-utility call. Value must be a string with no internal spaces.

## email

E-mail address of the E-utility user. Value must be a string with no internal spaces, and should be a valid e-mail address.

If you expect to post more than 3 E-utility requests per second from a single IP address, consider including the following parameter:

## **api_key**

Value of the API key for sites that post more than 3 requests per second. Please see [Chapter 2](https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter2/) for a full discussion of this policy.
