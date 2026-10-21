"""Offline behavioral checks; no real credentials or network calls."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.parse import parse_qs
import xml.etree.ElementTree as ET
import search_pubmed as s

CONFIG = {'NCBI_EMAIL': 'contact@example.org', 'NCBI_API_KEY': 'private-test-key'}


def article(pmid):
    return f'''<PubmedArticle><MedlineCitation><PMID>{pmid}</PMID><Article>
    <ArticleTitle>Title <i>with markup</i></ArticleTitle>
    <Journal><Title>Journal</Title><JournalIssue><PubDate><MedlineDate>2020 Jan-Feb</MedlineDate></PubDate></JournalIssue></Journal>
    <AuthorList><Author><CollectiveName>Study Group</CollectiveName></Author></AuthorList>
    <Abstract><AbstractText Label="RESULTS">Some\n results.</AbstractText></Abstract>
    </Article></MedlineCitation><PubmedData><ArticleIdList>
    <ArticleId IdType="doi">10.123/test</ArticleId></ArticleIdList></PubmedData></PubmedArticle>'''


def response(xml):
    data = xml.encode()
    return data, ET.fromstring(data)


class SearchTests(unittest.TestCase):
    def test_key_rates_and_validation(self):
        self.assertEqual(s.Client({'NCBI_EMAIL': CONFIG['NCBI_EMAIL']}).rate, 3)
        self.assertEqual(s.Client(CONFIG).rate, 10)
        self.assertEqual(s.Client(dict(CONFIG, NCBI_REQUESTS_PER_SECOND='2')).rate, 2)
        for value in ['11', 'nan', '-1', '0']:
            with self.assertRaises(ValueError):
                s.Client(dict(CONFIG, NCBI_REQUESTS_PER_SECOND=value))
        with self.assertRaises(ValueError):
            s.Client({'NCBI_EMAIL': CONFIG['NCBI_EMAIL'], 'NCBI_REQUESTS_PER_SECOND': '4'})

    def test_literal_config(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td)/'.env'
            path.write_text('NCBI_API_KEY="$(do-not-execute)"\n# comment\nENTREZ_QUERY=a=b\n')
            values = s.load_env(path)
            self.assertEqual(values['NCBI_API_KEY'], '$(do-not-execute)')
            self.assertEqual(values['ENTREZ_QUERY'], 'a=b')

    def test_batches_counts_and_secret_exclusion(self):
        seen = []
        def request(client, endpoint, params):
            seen.append(endpoint)
            if endpoint.startswith('esearch'):
                return response('<eSearchResult><Count>3</Count><IdList><Id>1</Id><Id>2</Id><Id>3</Id></IdList></eSearchResult>')
            return response('<PubmedArticleSet>' + ''.join(article(i) for i in params['id'].split(',')) + '</PubmedArticleSet>')
        with tempfile.TemporaryDirectory() as td, patch.object(s.Client, 'request', request):
            run, report = s.search(dict(CONFIG, ENTREZ_BATCH_SIZE='2'), 'test query', Path(td))
            self.assertEqual(seen, ['esearch.fcgi', 'efetch.fcgi', 'efetch.fcgi'])
            self.assertEqual(report['retrieved_count'], 3)
            self.assertTrue(report['all_hits_retrieved'])
            self.assertEqual(len(list(run.glob('records-*.xml'))), 2)
            tsv = (run/'records.tsv').read_text()
            self.assertIn('Title with markup', tsv)
            self.assertIn('2020', tsv)
            self.assertIn('Study Group', tsv)
            self.assertNotIn(CONFIG['NCBI_API_KEY'], (run/'search.json').read_text())
            self.assertNotIn(CONFIG['NCBI_EMAIL'], (run/'search.json').read_text())

    def test_limit_zero_hits_and_too_large(self):
        with tempfile.TemporaryDirectory() as td:
            with patch.object(s.Client, 'request', return_value=response('<eSearchResult><Count>0</Count><IdList/></eSearchResult>')):
                run, meta = s.search(CONFIG, 'query', Path(td))
                self.assertEqual((run/'records.tsv').read_text().strip().split('\t'), s.FIELDS)
                self.assertEqual(meta['retrieved_count'], 0)
            with patch.object(s.Client, 'request', return_value=response('<eSearchResult><Count>10001</Count><IdList/></eSearchResult>')):
                with self.assertRaisesRegex(ValueError, '10000'):
                    s.search(dict(CONFIG, ENTREZ_MAX_RECORDS='0'), 'query', Path(td))

    def test_partial_selection_is_not_all_hits(self):
        replies = [response('<eSearchResult><Count>200</Count><IdList><Id>1</Id></IdList></eSearchResult>'),
                   response('<PubmedArticleSet>' + article('1') + '</PubmedArticleSet>')]
        with tempfile.TemporaryDirectory() as td, patch.object(s.Client, 'request', side_effect=replies):
            _, report = s.search(dict(CONFIG, ENTREZ_MAX_RECORDS='1'), 'query', Path(td))
            self.assertEqual(report['retrieved_count'], 1)
            self.assertEqual(report['total_hits'], 200)
            self.assertFalse(report['all_hits_retrieved'])

    def test_failed_fetch_preserves_failed_report(self):
        replies = [response('<eSearchResult><Count>1</Count><IdList><Id>1</Id></IdList></eSearchResult>'),
                   response('<PubmedArticleSet>' + article('2') + '</PubmedArticleSet>')]
        with tempfile.TemporaryDirectory() as td, patch.object(s.Client, 'request', side_effect=replies):
            with self.assertRaises(ValueError):
                s.search(CONFIG, 'query', Path(td))
            run = next(Path(td).iterdir())
            self.assertEqual(json.loads((run/'search.json').read_text())['status'], 'failed')
            self.assertTrue((run/'records-001.xml').exists())
            self.assertFalse((run/'records.tsv').exists())

    def test_post_credentials_retry_and_throttle(self):
        reply = unittest.mock.MagicMock()
        reply.__enter__.return_value.read.return_value = b'<eSearchResult><Count>0</Count></eSearchResult>'
        error = HTTPError('https://example.org', 429, 'rate limit', {'Retry-After': '2'}, None)
        with patch.object(s, 'urlopen', side_effect=[error, reply]) as send, patch.object(s.time, 'sleep') as sleep:
            s.Client(CONFIG).request('esearch.fcgi', {'term': 'a & b'})
            params = parse_qs(send.call_args.args[0].data.decode())
            self.assertEqual(params['api_key'], [CONFIG['NCBI_API_KEY']])
            self.assertEqual(params['term'], ['a & b'])
            self.assertIn(unittest.mock.call(2.0), sleep.call_args_list)
        client = s.Client(CONFIG)
        with patch.object(s, 'urlopen', return_value=reply), patch.object(s.time, 'monotonic', return_value=100), patch.object(s.time, 'sleep') as sleep:
            client.request('esearch.fcgi', {})
            client.request('esearch.fcgi', {})
            self.assertGreaterEqual(sleep.call_args_list[-1].args[0], 0.10)

    def test_empty_query_and_invalid_config_do_not_network(self):
        with tempfile.TemporaryDirectory() as td, patch.object(s, 'load_env', return_value={}), patch.dict(s.os.environ, {}, clear=True), patch.object(s, 'urlopen') as send, contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(s.main(['--output', td]), 0)
            send.assert_not_called()
            self.assertEqual(list(Path(td).iterdir()), [])
        with patch.object(s, 'load_env', side_effect=ValueError('Invalid config')), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(s.main([]), 1)


if __name__ == '__main__':
    unittest.main()
