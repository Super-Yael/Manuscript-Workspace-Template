#!/usr/bin/env python3
"""Run one PubMed query per labelled Markdown fence in section README files."""
import argparse
import os
from pathlib import Path
import re
import sys
import tempfile

from search_pubmed import Client, load_env, search


def publish_bib(source, destination):
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=destination.parent, delete=False) as stream:
        temporary = Path(stream.name)
        stream.write(source.read_bytes())
    try:
        temporary.replace(destination)
    finally:
        temporary.unlink(missing_ok=True)


def find_queries(root):
    points = []
    if not root.exists():
        return points
    for section in sorted(p for p in root.iterdir() if p.is_dir() and not p.name.startswith('.')):
        readme = section / 'README.md'
        if not readme.is_file():
            continue
        content = readme.read_text(encoding='utf-8')
        fences = re.findall(r'^```pubmed[^\n]*\n', content, re.M)
        blocks = list(re.finditer(r'^```pubmed[ \t]+([A-Za-z0-9][A-Za-z0-9_-]*)[ \t]*\n(.*?)^```[ \t]*$', content, re.M | re.S))
        if len(fences) != len(blocks):
            raise ValueError(f'Invalid pubmed fence or missing point ID in {readme}')
        seen = set()
        for block in blocks:
            point, query = block.group(1), block.group(2).strip()
            if point.casefold() in seen or not query:
                raise ValueError(f'Duplicate point ID or empty query: {readme}: {point}')
            seen.add(point.casefold())
            points.append((section, point, query))
    return points


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--env-file', type=Path, default=Path('.env'))
    args = parser.parse_args(argv)
    try:
        points = find_queries(args.root)
        if not points:
            print('SKIP: no section README PubMed queries')
            return 0
        config = load_env(Path('.env.example'))
        config.update(load_env(args.env_file))
        config.update(os.environ)
        client = Client(config)  # One rate limiter shared by all queries.
        for section, point, query in points:
            run, report = search(config, query, section / '.runs' / point, client=client)
            publish_bib(run / 'records.bib', section / (point + '.bib'))
            print(f"{section.name}/{point}.bib: {report['retrieved_count']}/{report['total_hits']} hits")
        return 0
    except (ValueError, RuntimeError, OSError) as error:
        # Remote errors are sanitized by the client; never print local configuration.
        message = str(error) if isinstance(error, (ValueError, RuntimeError)) else 'Local file access failed'
        config = locals().get('config', {})
        for name in ('NCBI_EMAIL', 'NCBI_API_KEY'):
            if config.get(name):
                message = message.replace(config[name], '[redacted]')
        print('ERROR: ' + message, file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
