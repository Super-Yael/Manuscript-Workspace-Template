"""Lossless PubMed-to-BibTeX export and shared identifier normalization."""
import base64
import re
import xml.etree.ElementTree as ET


def node_text(node):
    return ' '.join(''.join(node.itertext()).split()) if node is not None else ''


def normalize_doi(value):
    value = value.strip()
    value = re.sub(r'^https?://(?:dx\.)?doi\.org/|^doi:\s*', '', value, flags=re.I)
    value = re.sub(r'\\([_&#%{}$])', r'\1', value)
    return value.strip().lower()


def doi_key(value):
    # Preserve readable DOIs, encoding characters unsafe in TeX/BibTeX keys.
    return re.sub(r'[\s,{}%#\\]', lambda m: '-u%04x-' % ord(m.group()), normalize_doi(value))


def escape(value):
    replacements = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$',
                    '#': r'\#', '_': r'\_', '{': r'\{', '}': r'\}',
                    '~': r'\textasciitilde{}', '^': r'\textasciicircum{}'}
    return ''.join(replacements.get(c, c) for c in value)


def export_record(record, row):
    book = record.tag == 'PubmedBookArticle'
    article = record.find('BookDocument' if book else 'MedlineCitation/Article')
    data = record.find('PubmedBookData' if book else 'PubmedData')
    fields = {name: row[name] for name in ('title', 'journal', 'year', 'abstract', 'url')}
    doi = normalize_doi(row['doi'])
    if doi:
        if not doi.startswith('10.') or '/' not in doi:
            raise ValueError('Malformed DOI in PubMed record')
        fields['doi'] = doi
    fields['pmid'] = row['pmid']
    fields['abstract_available'] = 'true' if row['abstract'] else 'false'
    for field, path in {'volume': 'Journal/JournalIssue/Volume', 'number': 'Journal/JournalIssue/Issue',
                        'pages': 'Pagination/StartPage', 'eid': 'ELocationID',
                        'issn': 'Journal/ISSN', 'journal_abbreviation': 'Journal/ISOAbbreviation'}.items():
        value = node_text(article.find(path))
        if value:
            fields[field] = value
    pages = node_text(article.find('Pagination/MedlinePgn'))
    if pages:
        fields['pages'] = pages
    for field, path in {'language': './/Language', 'keywords': './/KeywordList/Keyword',
                        'mesh': './/MeshHeadingList/MeshHeading', 'affiliation': './/Affiliation',
                        'publication_type': './/PublicationTypeList/PublicationType',
                        'grants': './/GrantList/Grant'}.items():
        values = list(dict.fromkeys(node_text(n) for n in record.findall(path) if node_text(n)))
        if values:
            fields[field] = '; '.join(values)
    if data is not None:
        for identifier in data.findall('ArticleIdList/ArticleId'):
            kind = identifier.get('IdType', '')
            if kind and kind != 'doi':
                fields['ncbi_id_' + re.sub(r'\W', '_', kind)] = node_text(identifier)
    date = article.find('Book/PubDate' if book else 'Journal/JournalIssue/PubDate')
    if date is not None:
        fields['publication_date'] = ' '.join(node_text(n) for n in date if node_text(n))
    authors = []
    for author in article.findall('AuthorList/Author'):
        collective = node_text(author.find('CollectiveName'))
        if collective:
            authors.append('{' + escape(collective) + '}')
        else:
            family = node_text(author.find('LastName'))
            given = node_text(author.find('ForeName')) or node_text(author.find('Initials'))
            suffix = node_text(author.find('Suffix'))
            parts = [family] + ([suffix] if suffix else []) + ([given] if given else [])
            authors.append(', '.join(escape(part) for part in parts))
    # All non-mapped metadata survives in this reversible custom field.
    fields['ncbi_xml_base64'] = base64.b64encode(ET.tostring(record, encoding='utf-8')).decode('ascii')
    key = doi_key(doi) if doi else 'pmid:' + row['pmid']
    lines = ['@' + ('incollection' if book else 'article') + '{' + key + ',']
    if authors:
        lines.append('  author = {' + ' and '.join(authors) + '},')
    for name, value in fields.items():
        lines.append('  ' + name + ' = {' + escape(value) + '},')
    lines.append('}')
    return '\n'.join(lines) + '\n'
