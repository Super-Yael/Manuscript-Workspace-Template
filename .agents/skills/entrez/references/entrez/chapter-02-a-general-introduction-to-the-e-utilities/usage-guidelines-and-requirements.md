---
title: "Usage Guidelines and Requirements"
chapter: "A General Introduction to the E-utilities"
source: "https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter2/#chapter2.Usage_Guidelines_and_Requiremen"
---
# Usage Guidelines and Requirements

## Use the E-utility URL

All E-utility requests should be made to URLs beginning with the following string:

<https://eutils.ncbi.nlm.nih.gov/entrez/eutils/>

These URLs direct requests to servers that are used only by the E-utilities and that are optimized to give users the best performance.

## Frequency, Timing and Registration of E-utility URL Requests

In order not to overload the E-utility servers, NCBI recommends that users post no more than three URL requests per second and limit large jobs to either weekends or between 9:00 PM and 5:00 AM Eastern time during weekdays. Failure to comply with this policy may result in an IP address being blocked from accessing NCBI. If NCBI blocks an IP address, service will not be restored unless the developers of the software accessing the E-utilities register values of the **tool** and **email** parameters with NCBI. The value of **tool** should be a string with no internal spaces that uniquely identifies the software producing the request. The value of **email** should be a complete and valid e-mail address of the software developer and not that of a third-party end user. The value of **email** will be used only to contact developers if NCBI observes requests that violate our policies, and we will attempt such contact prior to blocking access. In addition, developers may request that the value of **email** be added to the E-utility mailing list that provides announcements of software updates, known bugs and other policy changes affecting the E-utilities. To register **tool** and **email** values, simply send an e-mail to [vog.hin.mln.ibcn@seitilitue](mailto:dev@null) including the desired values along with the name of either a developer or the organization creating the software. Once NCBI establishes communication with a developer, receives values for **tool** and **email** and validates the e-mail address in **email**, the block will be lifted. Once **tool** and **email** values are registered, all subsequent E-utility requests from that software package should contain both values. Please be aware that merely providing values for **tool** and **email** in requests is not sufficient to comply with this policy; these values must be registered with NCBI. Requests from any IP that lack registered values for **tool** and **email** and that violate the above usage policies may be blocked. Software developers may register values of **tool** and **email** at any time, and are encouraged to do so.

## API Keys

Since December 1, 2018, NCBI has provided API keys that offer enhanced levels of supported access to the E-utilities. Without an API key, any site (IP address) posting more than 3 requests per second to the E-utilities will receive an error message. By including an API key, a site can post up to 10 requests per second by default. Higher rates are available by request ([vog.hin.mln.ibcn@seitilitue](mailto:dev@null)). Users can obtain an API key now from the Settings page of their NCBI account (to create an account, visit [http://www.ncbi.nlm.nih.gov/account/](https://www.ncbi.nlm.nih.gov/account/)). After creating the key, users should include it in each E-utility request by assigning it to the *api_key* parameter.

    Example request including an API key:
    esummary.fcgi?db=pubmed&id=123456&api_key=ABCDE12345

    Example error message if rates are exceeded:
    {"error":"API rate limit exceeded","count":"11"}

Only one API key is allowed per NCBI account; however, a user may request a new key at any time. Such a request will invalidate any existing API key associated with that NCBI account.

## Minimizing the Number of Requests

If a task requires searching for and/or downloading a large number of records, it is much more efficient to use the Entrez History to upload and/or retrieve these records in batches rather than using separate requests for each record. Please refer to [Application 3 in Chapter 3](https://www.ncbi.nlm.nih.gov/sites/books/n/helpeutils/chapter3/#chapter3.Application_3_Retrieving_large) for an example. Many thousands of IDs can be uploaded using a single EPost request, and several hundred records can be downloaded using one EFetch request.

## Disclaimer and Copyright Issues

If you use the E-utilities within software, NCBI's Disclaimer and Copyright notice (<https://www.ncbi.nlm.nih.gov/About/disclaimer.html>) must be evident to users of your product. Please note that abstracts in PubMed may incorporate material that may be protected by U.S. and foreign copyright laws. All persons reproducing, redistributing, or making commercial use of this information are expected to adhere to the terms and conditions asserted by the copyright holder. Transmission or reproduction of protected items beyond that allowed by fair use (PDF) as defined in the copyright laws requires the written permission of the copyright owners. NLM provides no legal advice concerning distribution of copyrighted materials. Please consult your legal counsel. If you wish to do a large data mining project on PubMed data, you can download a local copy of the database at <https://www.nlm.nih.gov/databases/download/pubmed_medline.html>.

## Handling Special Characters Within URLs

When constructing URLs for the E-utilities, please use lowercase characters for all parameters except &WebEnv. There is no required order for the URL parameters in an E-utility URL, and null values or inappropriate parameters are generally ignored. Avoid placing spaces in the URLs, particularly in queries. If a space is required, use a plus sign (+) instead of a space:

    Incorrect: &id=352, 25125, 234
    Correct:   &id=352,25125,234

    Incorrect: &term=biomol mrna[properties] AND mouse[organism]
    Correct:   &term=biomol+mrna[properties]+AND+mouse[organism]

Other special characters, such as quotation marks (“) or the \# symbol used in referring to a query key on the History server, should be represented by their URL encodings (%22 for “; %23 for \#).

    Incorrect: &term=#2+AND+"gene in genomic"[properties]
    Correct:   &term=%232+AND+%22gene+in+genomic%22[properties]
