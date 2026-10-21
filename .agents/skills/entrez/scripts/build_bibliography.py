#!/usr/bin/env python3
"""Collect cited BibTeX records; reject ambiguous citation keys before LaTeX runs."""
import argparse
from collections import defaultdict
from pathlib import Path
import re
import sys
import tempfile
import unicodedata

from bibtex_records import doi_key, normalize_doi


def tex_content(source):
    source = re.sub(r'\\begin\{(verbatim\*?|lstlisting|minted|comment)\}.*?\\end\{\1\}', '', source, flags=re.S)
    source = re.sub(r'\\verb\*?([^\w\s]).*?\1', '', source)
    return '\n'.join(strip_comment(line) for line in source.splitlines())


def strip_comment(line):
    for i, char in enumerate(line):
        if char == '%':
            slashes = len(line[:i]) - len(line[:i].rstrip('\\'))
            if slashes % 2 == 0:
                return line[:i]
    return line


def group_at(source, start, opening='{', closing='}'):
    if start >= len(source) or source[start] != opening:
        raise ValueError('Expected TeX group')
    depth, i = 1, start + 1
    while i < len(source):
        if source[i] == '\\':
            i += 2
            continue
        if source[i] == opening:
            depth += 1
        elif source[i] == closing:
            depth -= 1
            if depth == 0:
                return source[start + 1:i], i + 1
        i += 1
    raise ValueError('Unclosed TeX group')


def cited_keys(main, project_root):
    keys, visited = set(), set()
    def visit(path):
        path = path.resolve()
        if path in visited:
            return
        if not path.is_file():
            raise ValueError(f'Missing included TeX file: {path}')
        visited.add(path)
        source = tex_content(path.read_text(encoding='utf-8'))
        for command in re.finditer(r'\\([A-Za-z]+)\*?', source):
            name = command.group(1)
            if name not in ('input', 'include', 'subfile') and 'cite' not in name.lower():
                continue
            i = command.end()
            while i < len(source) and source[i].isspace():
                i += 1
            while i < len(source) and source[i] == '[':
                _, i = group_at(source, i, '[', ']')
                while i < len(source) and source[i].isspace():
                    i += 1
            if i >= len(source) or source[i] != '{':
                if name in ('input', 'include', 'subfile'):
                    match = re.match(r'[^\s%]+', source[i:])
                    value = match.group() if match else ''
                else:
                    raise ValueError(f'Citation requires literal keys in {path}')
            else:
                value, i = group_at(source, i)
            if name in ('input', 'include', 'subfile'):
                if '\\' in value or '#' in value or not value:
                    raise ValueError(f'Dynamic input path is unsupported: {path}')
                included = Path(value)
                if not included.suffix:
                    included = included.with_suffix('.tex')
                choices = [project_root / included, path.parent / included]
                visit(next((p for p in choices if p.is_file()), choices[0]))
            else:
                while True:
                    for key in value.split(','):
                        key = key.strip()
                        if not key or '\\' in key or '#' in key:
                            raise ValueError(f'Citation requires literal, non-empty keys in {path}')
                        keys.add(key)
                    if not name.lower().endswith('cites'):
                        break
                    while i < len(source) and source[i].isspace():
                        i += 1
                    while i < len(source) and source[i] == '[':
                        _, i = group_at(source, i, '[', ']')
                        while i < len(source) and source[i].isspace():
                            i += 1
                    if i >= len(source) or source[i] != '{':
                        break
                    value, i = group_at(source, i)
    visit(main)
    return keys


def normalized(value):
    value = re.sub(r'\\[A-Za-z]+', '', value)
    return ''.join(c for c in unicodedata.normalize('NFKD', value).casefold() if c.isalnum())


def same_work(left, right):
    ld, rd = normalize_doi(left.get('doi', '')), normalize_doi(right.get('doi', ''))
    lp, rp = left.get('pmid', '').strip(), right.get('pmid', '').strip()
    lt, rt = normalized(left.get('title', '')), normalized(right.get('title', ''))
    if (ld and rd and ld != rd) or (lp and rp and lp != rp):
        return False
    # A shared identifier does not excuse clearly different titles.
    if lt and rt and lt != rt:
        return False
    if (ld and rd and ld == rd) or (lp and rp and lp == rp):
        return True
    return bool(lt and lt == rt and left.get('year') and left.get('year') == right.get('year')
                and normalized(left.get('author', ''))
                and normalized(left.get('author', '')) == normalized(right.get('author', '')))


def build(main, sources, output, project_root=None):
    project_root = (project_root or Path.cwd()).resolve()
    if not main.is_file() or not main.stat().st_size:
        print('SKIP: no manuscript content')
        return
    keys = cited_keys(main, project_root)
    if '*' in keys:
        raise ValueError('\\nocite{*} conflicts with cited-only bibliography; list explicit keys')
    if not keys:
        output.unlink(missing_ok=True)
        print('SKIP: no citations in manuscript')
        return
    from bibtexparser.bparser import BibTexParser
    from bibtexparser.bwriter import BibTexWriter
    from bibtexparser.bibdatabase import BibDatabase
    index = defaultdict(list)
    files = sorted(p for p in sources.rglob('*')
                   if p.is_file() and p.suffix.lower() == '.bib' and p.resolve() != output.resolve() and not any(part.startswith('.') for part in p.relative_to(sources).parts))
    for path in files:
        parser = BibTexParser(common_strings=True)
        parser.ignore_nonstandard_types = False
        parser.homogenize_fields = False
        parser.interpolate_strings = True
        parser.add_missing_from_crossref = False
        try:
            db = parser.parse(path.read_text(encoding='utf-8'), partial=False)
        except Exception as error:
            raise ValueError(f'Invalid BibTeX in {path}: {type(error).__name__}') from None
        for entry in db.entries:
            aliases = {entry['ID']}
            if entry.get('doi'):
                aliases.add(doi_key(entry['doi']))
            if entry.get('pmid'):
                aliases.add('pmid:' + entry['pmid'].strip())
            for alias in aliases:
                index[alias].append((entry, path))
    selected, pending = {}, sorted(keys)
    while pending:
        key = pending.pop(0)
        if key in selected:
            continue
        hits = index.get(key, [])
        if not hits:
            raise ValueError(f'Cited key not found in source .bib files: {key}')
        # Compare every pair; missing identifiers cannot bridge distinct records.
        for i, (left, left_path) in enumerate(hits):
            for right, right_path in hits[i + 1:]:
                if not same_work(left, right):
                    raise ValueError(f'Citation key collision or unverified duplicate: {key}\n  {left_path}: {left.get("title", "[no title]")}\n  {right_path}: {right.get("title", "[no title]")}')
        merged = dict(hits[0][0])
        for entry, _ in hits[1:]:
            for field, value in entry.items():
                if field not in ('ID', 'ENTRYTYPE') and len(value) > len(merged.get(field, '')):
                    merged[field] = value
        merged['ID'] = key
        selected[key] = merged
        for field in ('crossref', 'xref', 'xdata'):
            pending.extend(k.strip() for k in merged.get(field, '').split(',') if k.strip() and k.strip() not in selected)
    db = BibDatabase()
    db.entries = [selected[k] for k in sorted(selected)]
    writer = BibTexWriter()
    content = '% Automatically generated from cited source records; do not edit.\n' + writer.write(db)
    if output.is_file() and output.read_text(encoding='utf-8') == content:
        print(f'Bibliography unchanged: {len(selected)} entries')
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=output.parent, mode='w', encoding='utf-8', delete=False) as stream:
        stream.write(content)
        temporary = Path(stream.name)
    try:
        temporary.replace(output)
    finally:
        temporary.unlink(missing_ok=True)
    print(f'Built {output}: {len(selected)} cited entries')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--main', type=Path, required=True)
    parser.add_argument('--sources', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        build(args.main, args.sources, args.output)
        return 0
    except (ValueError, OSError, ImportError) as error:
        print('ERROR: ' + str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
