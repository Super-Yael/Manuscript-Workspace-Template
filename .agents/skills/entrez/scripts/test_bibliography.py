"""Offline checks of BibTeX export, point discovery, and citation resolution."""
import base64
from contextlib import redirect_stdout
import io
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET

import bibtexparser
from bibtex_records import export_record, normalize_doi
from build_bibliography import build, cited_keys
from readme_queries import find_queries
from search_pubmed import parse_records
from test_search_pubmed import article


def entry(key, doi='10.1234/a', pmid='1', title='A study', abstract='Summary'):
    fields = dict(title=title, author='Family, Given', year='2024', abstract=abstract)
    if doi:
        fields['doi'] = doi
    if pmid:
        fields['pmid'] = pmid
    return '@article{' + key + ',\n' + ',\n'.join(k + '={' + v + '}' for k, v in fields.items()) + '\n}\n'


class BibliographyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.sources = self.root/'refs'
        self.sources.mkdir()
        self.main = self.root/'main.tex'
        self.output = self.sources/'reference.bib'

    def write(self, name, content):
        path = self.root/name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path

    def build(self):
        with redirect_stdout(io.StringIO()):
            build(self.main, self.sources, self.output, self.root)
        return bibtexparser.loads(self.output.read_text()).entries

    def test_used_only_duplicates_and_stable_output(self):
        self.write('main.tex', r'\input{section}' + '\n% \\cite{unused}\n')
        self.write('section.tex', r'\citep[see][p. 2]{10.1234/a}')
        self.write('refs/Introduction/P01.bib', entry('10.1234/a'))
        self.write('refs/OtherSection/P02.bib', entry('10.1234/a', abstract='A much longer complete summary') + entry('unused', '10.1234/other', '2'))
        rows = self.build()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['abstract'], 'A much longer complete summary')
        before = self.output.stat().st_mtime_ns
        self.build()
        self.assertEqual(before, self.output.stat().st_mtime_ns)

    def test_different_articles_same_key_stop_without_overwrite(self):
        self.write('main.tex', r'\cite{collision}')
        self.write('refs/one/a.bib', entry('collision'))
        self.write('refs/two/b.bib', entry('collision', '10.1234/different', '2', 'Different study'))
        self.output.write_text('previous good output')
        with self.assertRaisesRegex(ValueError, 'collision'):
            self.build()
        self.assertEqual(self.output.read_text(), 'previous good output')

    def test_same_doi_different_title_or_pmid_is_conflict(self):
        self.write('main.tex', r'\cite{10.1234/a}')
        self.write('refs/one.bib', entry('10.1234/a'))
        for title, pmid in [('Unrelated study', '1'), ('A study', '99')]:
            self.write('refs/two.bib', entry('10.1234/a', pmid=pmid, title=title))
            with self.assertRaisesRegex(ValueError, 'collision'):
                self.build()

    def test_missing_key_and_unconfirmed_duplicate_fail(self):
        self.write('main.tex', r'\cite{missing}')
        with self.assertRaisesRegex(ValueError, 'not found'):
            self.build()
        self.write('main.tex', r'\cite{same}')
        self.write('refs/a.bib', '@misc{same,note={a}}')
        self.write('refs/b.bib', '@misc{same,note={b}}')
        with self.assertRaisesRegex(ValueError, 'unverified duplicate'):
            self.build()

    def test_key_alias_and_crossref(self):
        self.write('main.tex', r'\cite{10.1234/a}')
        self.write('refs/a.bib', entry('old-key', doi='https://doi.org/10.1234/A').replace('abstract={Summary}', 'crossref={parent}'))
        self.write('refs/b.bib', '@proceedings{parent,title={Proceedings},year={2024}}')
        self.assertEqual({r['ID'] for r in self.build()}, {'10.1234/a', 'parent'})

    def test_multicite_comments_and_nocite_star(self):
        source = r'''% \cite{ignored}
\cites[see]{first}[also]{second}
\begin{verbatim}\cite{not-used}\end{verbatim}
\verb|\cite{not-used-either}|
'''
        self.write('main.tex', source)
        self.assertEqual(cited_keys(self.main, self.root), {'first', 'second'})
        self.write('main.tex', r'\nocite{*}')
        with self.assertRaisesRegex(ValueError, 'nocite'):
            self.build()

    def test_empty_skips_and_stale_generated_file_removed(self):
        self.write('main.tex', 'No citations.')
        self.output.write_text('stale')
        with redirect_stdout(io.StringIO()):
            build(self.main, self.sources, self.output, self.root)
        self.assertFalse(self.output.exists())

    def test_point_discovery_arbitrary_sections(self):
        self.write('refs/CustomSection/README.md', '## claim\n```pubmed P01\nA[Title] AND B[MeSH Terms]\n```\n')
        self.write('refs/README.md', '```pubmed EXAMPLE\nnot an actual query\n```')
        points = find_queries(self.sources)
        self.assertEqual([(p.parent.name, i, q) for p, i, q in points], [('refs', 'P01', 'A[Title] AND B[MeSH Terms]')])
        self.write('refs/CustomSection/README.md', '```pubmed P01\nx\n```\n```pubmed P01\ny\n```')
        with self.assertRaises(ValueError):
            find_queries(self.sources)

    def test_rich_bib_export_abstract_and_lossless_xml(self):
        record = ET.fromstring(article('123'))
        row = parse_records(ET.fromstring('<PubmedArticleSet>' + article('123') + '</PubmedArticleSet>'))[0]
        bib = export_record(record, row)
        parsed = bibtexparser.loads(bib).entries[0]
        self.assertEqual(parsed['ID'], '10.123/test')
        self.assertIn('Some results.', parsed['abstract'])
        self.assertIn('Study Group', parsed['author'])
        restored = ET.fromstring(base64.b64decode(parsed['ncbi_xml_base64']))
        self.assertEqual(ET.tostring(restored), ET.tostring(record))
        row.update(doi='', abstract='')
        parsed = bibtexparser.loads(export_record(record, row)).entries[0]
        self.assertEqual(parsed['ID'], 'pmid:123')
        self.assertEqual(parsed['abstract'], '')
        self.assertEqual(parsed['abstract_available'], 'false')
        self.assertEqual(normalize_doi('https://doi.org/10.123/ABC'), '10.123/abc')


if __name__ == '__main__':
    unittest.main()
