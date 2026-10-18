"""Build the interactive reader and plain copy text for this article.

Standard library only. page.html holds the hand-built interactive page;
ARTICLE.md is the canonical text. This script writes ARTICLE.txt and
article.html (page.html with the copy-ready text embedded).
"""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent
lines = (ROOT / 'ARTICLE.md').read_text().splitlines()


def plain(text):
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)',
                  lambda m: m[1] + ' (' + m[2] + ')' if m[2].startswith('https://') else m[1], text)
    return re.sub(r'[*`]', '', text)


out = []
for line in lines[1:]:  # the title is added by whoever pastes the text
    if line.startswith('#'):
        line = line.lstrip('#').strip()
    if line.startswith('- '):
        line = '• ' + line[2:]
    out.append(plain(line))
text = re.sub(r'\n{3,}', '\n\n', '\n'.join(out)).strip() + '\n'
(ROOT / 'ARTICLE.txt').write_text(text)

page = (ROOT / 'page.html').read_text()
assert page.count('__COPY__') == 1
copy = json.dumps(text, ensure_ascii=True).replace('</', '<\\/')
(ROOT / 'article.html').write_text(page.replace('__COPY__', copy))
