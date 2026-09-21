"""Render the controlled Markdown draft to a reader and clean copy text.

Standard library only. Supports the constructs used by ARTICLE.md; this is
not a Markdown service and should not be exposed to untrusted input.
"""
from pathlib import Path
from html import escape
import json
import re

ROOT = Path(__file__).resolve().parent
source = (ROOT/'ARTICLE.md').read_text()
lines = source.splitlines()


def inline(text):
    text = escape(text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    return re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', text)


def plain_inline(text):
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)',
                  lambda m: m[1]+' ('+m[2]+')' if m[2].startswith('https://') else m[1], text)
    return re.sub(r'[*`]', '', text)


html=[]; plain=[]; toc=[];i=0
captions={
    'assets/decision-map.png':'Choose a component for the decision; retain application-level checks.',
    'assets/agent-checkpoints.png':'An observation checkpoint creates an opportunity to detect and recover from errors.',
    'assets/error-horizon.png':'Synthetic illustration. Independence, fatal errors and no recovery are assumptions, not measured behavior.',
    'assets/cascade-economics.png':'Fictional prices. The fallback workload has its own conditional cost.',
}
while i < len(lines):
    line=lines[i]
    if not line.strip():i+=1;continue
    if line.startswith('```'):
        language=line[3:].strip();i+=1;code=[]
        while i<len(lines) and not lines[i].startswith('```'):
            code.append(lines[i]);i+=1
        html.append('<pre><code class="language-'+escape(language)+'">'+escape('\n'.join(code))+'</code></pre>')
        plain.append('\n'.join(code));i+=1;continue
    match=re.match(r'^(#{1,3}) (.*)',line)
    if match:
        level=len(match[1]);text=match[2];slug=re.sub(r'[^a-z0-9 -]','',text.lower()).replace(' ','-')
        html.append(f'<h{level} id="{slug}">{inline(text)}</h{level}>');plain.append(plain_inline(text))
        if level==2:toc.append(f'<a href="#{slug}">{escape(text)}</a>')
        i+=1;continue
    match=re.fullmatch(r'!\[([^\]]*)\]\(([^)]+)\)',line)
    if match:
        alt,path=match.groups();caption=captions.get(path,alt)
        html.append(f'<figure><img loading="lazy" src="{escape(path)}" alt="{escape(alt)}"><figcaption>{escape(caption)}</figcaption></figure>')
        i+=1;continue
    if line.startswith('|'):
        rows=[]
        while i<len(lines) and lines[i].startswith('|'):
            row=[x.strip() for x in lines[i].strip('|').split('|')]
            if not all(re.fullmatch(r'[-: ]+',v) for v in row):rows.append(row)
            i+=1
        html.append('<div class="table-wrap"><table><thead><tr>'+''.join('<th>'+inline(c)+'</th>' for c in rows[0])+'</tr></thead><tbody>')
        for row in rows[1:]:
            html.append('<tr>'+''.join('<td>'+inline(c)+'</td>' for c in row)+'</tr>')
            plain.append(plain_inline(row[0])+'\n'+'\n'.join(plain_inline(k)+': '+plain_inline(v) for k,v in zip(rows[0][1:],row[1:])))
        html.append('</tbody></table></div>');continue
    if line.startswith('- '):
        entries=[]
        while i<len(lines) and lines[i].startswith('- '):entries.append(lines[i][2:]);i+=1
        html.append('<ul>'+''.join('<li>'+inline(v)+'</li>' for v in entries)+'</ul>')
        plain.append('\n'.join('• '+plain_inline(v) for v in entries));continue
    if line=='---':html.append('<hr>');i+=1;continue
    paragraph=[line];i+=1
    while i<len(lines) and lines[i].strip() and not re.match(r'^(#|```|!\[|\||- |---$)',lines[i]):
        paragraph.append(lines[i]);i+=1
    text=' '.join(paragraph)
    paragraph_class = ' class="byline"' if text.startswith('By Saurabh Kumar') else ''
    html.append('<p'+paragraph_class+'>'+inline(text)+'</p>')
    if not text.startswith('*Companion materials:'):plain.append(plain_inline(text))

plain_text='\n\n'.join(plain)+'\n'
(ROOT/'ARTICLE.txt').write_text(plain_text)
title=plain[0]
copy_body='\n\n'.join(plain[1:])
body='\n'.join(html)
css='''
:root{--ink:#101d33;--muted:#536075;--paper:#faf8f2;--line:#dedfdc;--accent:#dce978}*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:90px}body{margin:0;background:var(--paper);color:var(--ink);font:19px/1.75 Georgia,serif}a{color:#334e8c;text-underline-offset:3px}header{position:sticky;top:0;background:rgba(250,248,242,.97);z-index:5;border-bottom:1px solid var(--line);font:14px/1.4 system-ui,sans-serif}nav{max-width:1150px;margin:auto;display:flex;align-items:center;justify-content:space-between;gap:15px;padding:14px 24px}.brand{font-weight:750;font-size:18px;letter-spacing:-.02em}.byline{font:15px/1.6 system-ui,sans-serif;color:var(--muted);margin:-12px 0 32px}.byline a{color:inherit}button,.nav-link{font:600 13px system-ui,sans-serif;padding:10px 14px;border:1px solid #b4bdc9;border-radius:6px;cursor:pointer;background:white;color:var(--ink);text-decoration:none}button.primary{background:var(--ink);color:white}nav .controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap}.cover{max-width:1150px;margin:34px auto 0;padding:0 24px}.cover img{width:100%;height:auto;display:block;border-radius:10px}.meta{font:12px/1.6 system-ui,sans-serif;letter-spacing:.09em;text-transform:uppercase;color:var(--muted);max-width:760px;margin:32px auto 12px}main{max-width:760px;margin:auto;padding:0 24px 80px}h1,h2,h3{font-family:system-ui,sans-serif;line-height:1.2;letter-spacing:-.035em}h1{font-size:clamp(34px,4vw,48px);margin:16px 0 32px}h2{font-size:29px;margin:58px 0 24px}p{margin:0 0 22px}strong{font-weight:700}ul{padding-left:25px}li{padding-left:5px;margin:8px 0}figure{margin:36px -50px}figure img{display:block;width:100%;height:auto;border:1px solid var(--line);border-radius:8px}figcaption{font:13px/1.5 system-ui,sans-serif;color:var(--muted);margin-top:10px}pre{background:var(--ink);color:#f6f5eb;border-radius:9px;padding:24px;overflow:auto;font:13px/1.7 ui-monospace,SFMono-Regular,Menlo,monospace;margin:28px 0}code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.83em}p code{background:#eaece7;padding:2px 5px;border-radius:3px}pre code{font-size:inherit}.table-wrap{overflow:auto;margin:28px -40px;border:1px solid var(--line);border-radius:8px;background:white}table{border-collapse:collapse;width:100%;font:14px/1.55 system-ui,sans-serif;min-width:620px}td,th{padding:14px 16px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line)}th{background:#e8eadf;font-size:12px;text-transform:uppercase;letter-spacing:.035em}td:first-child{font-weight:650;width:23%}tr:last-child td{border-bottom:0}details{font:14px/1.6 system-ui,sans-serif;background:#eeeee6;padding:18px 22px;border-radius:8px;margin:34px 0}summary{font-weight:650;cursor:pointer}.toc{display:grid;gap:10px;margin-top:16px}.toc a{text-decoration:none}hr{border:0;border-top:1px solid var(--line);margin-top:45px}.status{max-width:1150px;margin:auto;padding:0 24px;font-size:12px;min-height:0}.status:not(:empty){padding-bottom:10px}dialog{width:min(800px,94vw);border:1px solid var(--line);border-radius:10px;padding:24px}dialog textarea{width:100%;height:60vh;font:16px/1.6 system-ui}dialog::backdrop{background:#101d3377}@media(max-width:900px){figure,.table-wrap{margin-left:0;margin-right:0}}@media(max-width:600px){nav{padding:12px 16px;flex-wrap:wrap}.brand{display:block}.cover{padding:0;margin-top:0}.cover img{border-radius:0}main{padding:0 20px 55px}body{font-size:18px}h2{font-size:25px}.meta{padding:0 20px}pre{padding:16px}figure{margin:26px 0}.nav-link{display:none}}@media print{header,.cover,details{display:none}main{max-width:none}body{font-size:12pt}h2{break-after:avoid}figure,pre,tr{break-inside:avoid}a{color:inherit}}
'''
page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="A practical guide to using Jev for bounded decisions in search, coding, agents and other workflows. Includes illustrative costs, code and evaluation advice."><meta name="author" content="Saurabh Kumar"><title>__TITLE__ | Saurabh Kumar</title><style>__CSS__</style></head><body><header><nav><span class="brand">Saurabh Kumar</span><div class="controls"><button id="copy" class="primary">Copy article text</button><a class="nav-link" href="ARTICLE.txt" download>Plain text</a><a class="nav-link" href="calculator.html">Planning calculator</a></div></nav><div id="status" class="status" role="status" aria-live="polite"></div></header><div class="cover"><img src="assets/cover.png" alt="When should you use JEV? A practical guide. Original cover showing a branching decision path."></div><div class="meta">AI engineering · Practical guide</div><main><details><summary>Inside the guide</summary><div class="toc">__TOC__</div></details><article>__BODY__</article></main><dialog id="copy-dialog"><p>Select and copy this plain text. It contains no Markdown markers or image placeholders.</p><textarea aria-label="Copy-ready article text"></textarea><p><button id="close">Close</button></p></dialog><script id="copy-text" type="application/json">__COPY__</script><script>
const copyText=JSON.parse(document.getElementById('copy-text').textContent);
document.getElementById('copy').onclick=async()=>{try{await navigator.clipboard.writeText(copyText);document.getElementById('status').textContent='Article body copied as plain text. Add the title and upload images separately.';}catch(error){const dialog=document.getElementById('copy-dialog');const area=dialog.querySelector('textarea');area.value=copyText;dialog.showModal();area.focus();area.select();}};
document.getElementById('close').onclick=()=>document.getElementById('copy-dialog').close();
</script></body></html>'''
page=page.replace('__TITLE__',escape(title)).replace('__CSS__',css).replace('__TOC__',''.join(toc)).replace('__BODY__',body).replace('__COPY__',json.dumps(copy_body).replace('<','\\u003c'))
(ROOT/'article.html').write_text(page)
print(f'Rendered article and clean copy text: {len(re.findall(r"\S+", plain_text))} whitespace-separated words including code, tables and reference URLs.')
