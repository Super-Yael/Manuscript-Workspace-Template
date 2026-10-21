#!/usr/bin/env python3
"""Search PubMed using the Python standard library; no project paths are embedded."""
import argparse
from bibtex_records import export_record
import csv
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import re
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

BASE = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
FIELDS = ['pmid', 'doi', 'title', 'authors', 'journal', 'year', 'abstract', 'url']


def load_env(path):
    """Read literal KEY=value; never execute shell code or expand variables."""
    values = {}
    if not path.is_file():
        return values
    for number, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        key, sep, value = line.partition('=')
        if not sep or not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', key.strip()):
            raise ValueError(f'Invalid config assignment at line {number}')
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        values[key.strip()] = value
    return values


def positive(config, key, default, integer=False, minimum=0):
    value = (int if integer else float)(config.get(key, default))
    if not math.isfinite(value) or value < minimum:
        raise ValueError(f'Invalid {key}')
    return value


class Client:
    def __init__(self, config):
        self.email = config.get('NCBI_EMAIL', '').strip()
        self.key = config.get('NCBI_API_KEY', '').strip()
        self.tool = config.get('NCBI_TOOL', 'entrez-literature-search').strip()
        if not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', self.email):
            raise ValueError('Set NCBI_EMAIL to a real contact email')
        if not self.tool or any(c.isspace() for c in self.tool):
            raise ValueError('NCBI_TOOL must be non-empty and contain no whitespace')
        ceiling = 10 if self.key else 3
        rate = config.get('NCBI_REQUESTS_PER_SECOND', 'auto')
        self.rate = ceiling if rate == 'auto' else float(rate)
        if not math.isfinite(self.rate) or not 0 < self.rate <= ceiling:
            raise ValueError(f'NCBI_REQUESTS_PER_SECOND must be >0 and <={ceiling}')
        self.timeout = positive(config, 'NCBI_TIMEOUT_SECONDS', '30', minimum=0.1)
        self.retries = positive(config, 'NCBI_MAX_RETRIES', '3', integer=True)
        if self.retries > 10:
            raise ValueError('NCBI_MAX_RETRIES must be <=10')
        self.next_request = 0.0

    def request(self, endpoint, parameters):
        params = dict(parameters, email=self.email, tool=self.tool)
        if self.key:
            params['api_key'] = self.key
        request = Request(BASE + endpoint, data=urlencode(params).encode(),
                          headers={'User-Agent': self.tool})
        for attempt in range(self.retries + 1):
            time.sleep(max(0, self.next_request - time.monotonic()))
            self.next_request = time.monotonic() + 1.02 / self.rate
            try:
                with urlopen(request, timeout=self.timeout) as response:
                    payload = response.read()
                root = ET.fromstring(payload)
                if root.find('.//ERROR') is not None or root.find('.//ErrorList') is not None:
                    raise ValueError('NCBI returned an error; check query and configuration')
                return payload, root
            except HTTPError as error:
                if error.code not in (429, 500, 502, 503, 504) or attempt == self.retries:
                    raise RuntimeError(f'NCBI HTTP {error.code}; credentials and response omitted') from None
                retry_after = error.headers.get('Retry-After', '')
                delay = min(60, float(retry_after)) if retry_after.isdigit() else min(60, 2 ** attempt)
            except (URLError, TimeoutError, OSError, ET.ParseError):
                if attempt == self.retries:
                    raise RuntimeError('NCBI transport/XML failure after bounded retries') from None
                delay = min(60, 2 ** attempt)
            time.sleep(delay)


def text(node):
    return ' '.join(''.join(node.itertext()).split()) if node is not None else ''


def parse_records(root):
    if root.tag != 'PubmedArticleSet':
        raise ValueError('Unexpected EFetch document type')
    rows = []
    for record in root:
        if record.tag not in ('PubmedArticle', 'PubmedBookArticle'):
            raise ValueError('Unsupported PubMed record type')
        book = record.tag == 'PubmedBookArticle'
        article = record.find('BookDocument' if book else 'MedlineCitation/Article')
        if article is None:
            raise ValueError('Missing article body')
        pmid = text(record.find('BookDocument/PMID' if book else 'MedlineCitation/PMID'))
        authors = []
        for author in article.findall('AuthorList/Author'):
            authors.append(text(author.find('CollectiveName')) or ' '.join(filter(None, [
                text(author.find('LastName')), text(author.find('ForeName')) or text(author.find('Initials'))])))
        ids = record.findall('PubmedBookData/ArticleIdList/ArticleId' if book else 'PubmedData/ArticleIdList/ArticleId')
        doi = next((text(i) for i in ids if i.get('IdType') == 'doi'), '')
        if not doi:
            doi = next((text(i) for i in article.findall('ELocationID') if i.get('EIdType') == 'doi'), '')
        date = article.find('Book/PubDate' if book else 'Journal/JournalIssue/PubDate')
        year = text(date.find('Year')) if date is not None else ''
        if not year and date is not None:
            match = re.search(r'\b\d{4}\b', text(date))
            year = match.group() if match else ''
        if not pmid.isdigit():
            raise ValueError('Missing/invalid PMID')
        abstract = ' '.join((part.get('Label', '') + ': ' if part.get('Label') else '') + text(part)
                            for part in article.findall('Abstract/AbstractText'))
        rows.append(dict(zip(FIELDS, [pmid, doi, text(article.find('ArticleTitle')),
            '; '.join(authors), text(article.find('Book/BookTitle' if book else 'Journal/Title')),
            year, abstract, f'https://pubmed.ncbi.nlm.nih.gov/{pmid}/'])))
    return rows


def search(config, query, output, client=None):
    if config.get('ENTREZ_DATABASE', 'pubmed') != 'pubmed':
        raise ValueError('This literature script supports PubMed only')
    maximum = positive(config, 'ENTREZ_MAX_RECORDS', '0', integer=True)
    batch = positive(config, 'ENTREZ_BATCH_SIZE', '100', integer=True, minimum=1)
    if batch > 1000:
        raise ValueError('ENTREZ_BATCH_SIZE must be <=1000')
    client = client or Client(config)
    params = dict(db='pubmed', term=query, retmode='xml', retmax=min(maximum or 10000, 10000),
                  sort=config.get('ENTREZ_SORT', 'relevance'), usehistory='y')
    raw, found = client.request('esearch.fcgi', params)
    if found.tag != 'eSearchResult' or found.find('Count') is None:
        raise ValueError('Unexpected ESearch document')
    count = int(found.findtext('Count'))
    target = min(count, maximum) if maximum else count
    if target > 10000:
        raise ValueError('PubMed ESearch cannot retrieve >10000 hits; split the query or use EDirect')
    ids = [text(i) for i in found.findall('IdList/Id')]
    if len(ids) != target or len(set(ids)) != target or any(not i.isdigit() for i in ids):
        raise ValueError('ESearch identifier count mismatch')
    output.mkdir(parents=True, exist_ok=True)
    run = output / datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S-%fZ')
    run.mkdir()
    (run / 'query.txt').write_text(query + '\n', encoding='utf-8')
    (run / 'esearch.xml').write_bytes(raw)
    (run / 'ids.txt').write_text(''.join(i + '\n' for i in ids), encoding='utf-8')
    metadata = dict(status='running', database='pubmed', timestamp_utc=datetime.now(timezone.utc).isoformat(),
                    endpoint=BASE, search_parameters=params, api_key_present=bool(client.key),
                    requests_per_second=client.rate, total_hits=count, selected_count=target,
                    retrieved_count=0, all_hits_retrieved=False, batches=[],
                    query_translation=found.findtext('QueryTranslation', ''))
    rows = []
    bibliography = []
    try:
        for offset in range(0, target, batch):
            selected = ids[offset:offset + batch]
            payload, records = client.request('efetch.fcgi', dict(db='pubmed', id=','.join(selected), retmode='xml'))
            name = f'records-{offset // batch + 1:03d}.xml'
            (run / name).write_bytes(payload)
            parsed = parse_records(records)
            if len(parsed) != len(selected) or {r['pmid'] for r in parsed} != set(selected):
                raise ValueError('EFetch identifier/count mismatch; raw batch preserved')
            by_pmid = {r['pmid']: r for r in parsed}
            for record in records:
                pmid_path = 'BookDocument/PMID' if record.tag == 'PubmedBookArticle' else 'MedlineCitation/PMID'
                bibliography.append(export_record(record, by_pmid[text(record.find(pmid_path))]))
            rows.extend(parsed)
            metadata['batches'].append(dict(file=name, count=len(parsed)))
            metadata['retrieved_count'] = len(rows)
        with (run / 'records.tsv').open('w', encoding='utf-8', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=FIELDS, delimiter='\t')
            writer.writeheader()
            writer.writerows(rows)
        (run / 'records.bib').write_text('\n'.join(bibliography), encoding='utf-8')
        metadata.update(status='complete', all_hits_retrieved=(len(rows) == count))
    except Exception:
        metadata.update(status='failed', error='Retrieval incomplete; inspect preserved batches and rerun')
        raise
    finally:
        (run / 'search.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return run, metadata


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--env-file', type=Path, default=Path('.env'))
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--query')
    group.add_argument('--query-file', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--bib', type=Path, help='Publish successful results as this per-query BibTeX file')
    args = parser.parse_args(argv)
    config = {}
    try:
        # Relative paths refer to the caller's working directory, not the skill.
        config = load_env(Path('.env.example'))
        config.update(load_env(args.env_file))
        config.update(os.environ)
        query = args.query if args.query is not None else config.get('ENTREZ_QUERY', '')
        query_file = args.query_file
        if args.query is None and query_file is None and not query.strip():
            query_file = Path(config['ENTREZ_QUERY_FILE']) if config.get('ENTREZ_QUERY_FILE') else None
        if query_file is not None:
            query = query_file.read_text(encoding='utf-8')
        query = query.strip()
        if not query:
            print('SKIP: no PubMed query configured')
            return 0
        output = args.output or config.get('ENTREZ_OUTPUT_DIR')
        if not output:
            raise ValueError('Set --output or ENTREZ_OUTPUT_DIR')
        run, result = search(config, query, Path(output))
        if args.bib is not None:
            from readme_queries import publish_bib
            publish_bib(run / 'records.bib', args.bib)
        print(f"Saved {result['retrieved_count']}/{result['total_hits']} hits: {run}")
        return 0
    except (ValueError, OSError, RuntimeError) as error:
        # Never echo remote payloads, request URLs, email, API keys, or query errors.
        if isinstance(error, (ValueError, RuntimeError)):
            message = str(error)
            for key in ('NCBI_API_KEY', 'NCBI_EMAIL'):
                secret = config.get(key, '')
                if secret:
                    message = message.replace(secret, '[redacted]')
        else:
            message = 'Local file access failed; check query and output paths'
        print('ERROR: ' + message, file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
