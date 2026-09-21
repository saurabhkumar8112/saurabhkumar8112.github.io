"""Build a small static publication from site.json and approved article folders.

Uses only the Python standard library. No provider calls or external assets.
GitHub Pages serves only the generated docs/ directory.
"""
from datetime import date, datetime
from email.utils import format_datetime
from html import escape, unescape
from pathlib import Path
import json
import re
import shutil
import struct
import subprocess
import sys
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent
SITE = json.loads((ROOT / 'site.json').read_text())
BASE = SITE['base_url'].rstrip('/')
REPO = SITE['repository'].rstrip('/')
POSTS = sorted(SITE['articles'], key=lambda post: post['date'], reverse=True)
OUT = ROOT / 'docs'
assert BASE.startswith('https://') and REPO.startswith('https://github.com/')
assert len({p['slug'] for p in POSTS}) == len(POSTS), 'Duplicate article slug'
for post in POSTS:
    assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', post['slug']), 'Invalid slug'
    date.fromisoformat(post['date'])
    assert date.fromisoformat(post.get('updated',post['date'])) >= date.fromisoformat(post['date'])
    for field, day in [('published_at','date'),('updated_at','updated')]:
        timestamp=datetime.fromisoformat(post[field])
        assert timestamp.utcoffset() is not None, f'{field} must include a timezone'
        assert timestamp.date().isoformat()==post.get(day,post['date']), f'{field} must match {day}'
    assert datetime.fromisoformat(post['updated_at']) >= datetime.fromisoformat(post['published_at'])
    assert (ROOT / 'content' / post['slug'] / post['image']).is_file()
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir()
(OUT / '.nojekyll').touch()
for verification in (ROOT / 'verification').glob('google*.html'):
    assert re.fullmatch(r'google[a-f0-9]+\.html', verification.name)
    assert verification.read_text().strip() == 'google-site-verification: '+verification.name
    shutil.copyfile(verification, OUT / verification.name)

CSS = '''
:root{--ink:#101d33;--muted:#536075;--paper:#faf8f2;--line:#dedfdc;--accent:#dce978}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:95px}body{margin:0;background:var(--paper);color:var(--ink);font:17px/1.65 system-ui,sans-serif}a{color:inherit;text-underline-offset:4px}a:focus-visible,button:focus-visible{outline:3px solid #7563c5;outline-offset:5px}
header{position:sticky;top:0;background:rgba(250,248,242,.97);border-bottom:1px solid var(--line);z-index:5;font:14px/1.4 system-ui,sans-serif}nav{max-width:1120px;margin:auto;padding:20px 24px;display:flex;align-items:center;justify-content:space-between;gap:20px}.brand{font:750 19px/1.2 system-ui,sans-serif;letter-spacing:-.025em;text-decoration:none}.controls{display:flex;gap:22px;align-items:center}.nav-link{padding:0;border:0;background:transparent;font:500 14px/1.4 system-ui,sans-serif;border-radius:0;text-decoration:none}.nav-link:hover{text-decoration:underline}button.copy{border:1px solid #bcc2ca;background:transparent;color:var(--ink);border-radius:5px;padding:7px 10px;font:500 12px system-ui;cursor:pointer}.status{max-width:1120px;margin:auto;padding:0 24px;font:12px/1.5 system-ui}.status:not(:empty){padding-bottom:10px}
.home{max-width:1120px;margin:auto;padding:0 24px}.hero{padding:90px 0 68px;max-width:870px}.eyebrow{font:600 12px/1.5 system-ui,sans-serif;text-transform:uppercase;letter-spacing:.12em;color:var(--muted)}.hero h1{font-size:clamp(42px,7vw,76px);line-height:1.06;letter-spacing:-.055em;margin:20px 0 24px;max-width:900px}.intro{font-size:20px;line-height:1.6;color:var(--muted);max-width:650px}.section-title{font-size:16px;letter-spacing:-.02em;margin:0 0 22px;display:flex;justify-content:space-between;align-items:center}.section-title a{font-size:13px;font-weight:450;color:var(--muted)}.cards{display:grid;gap:28px}.card{display:grid;grid-template-columns:1.1fr 1fr;border:1px solid var(--line);border-radius:12px;overflow:hidden;background:#fffefa;text-decoration:none}.card img{width:100%;height:100%;object-fit:contain;background:var(--ink);min-height:265px}.card-copy{padding:32px}.card h2{font-size:29px;line-height:1.2;letter-spacing:-.04em;margin:16px 0}.card p{font-size:15px;color:var(--muted);margin:0 0 22px}.card .read{font-size:14px;font-weight:650}.card:hover h2{text-decoration:underline;text-underline-offset:5px}.about{border-top:1px solid var(--line);padding:44px 0;margin-top:70px;display:grid;grid-template-columns:1fr 2fr;gap:35px}.about h2{font-size:24px;letter-spacing:-.03em;margin:0}.about p{margin:0 0 16px;max-width:650px;color:var(--muted)}.socials{display:flex;gap:22px;font-size:14px}.site-footer{max-width:1120px;margin:30px auto 0;padding:24px;border-top:1px solid var(--line);font:12px/1.7 system-ui,sans-serif;color:var(--muted);display:flex;gap:24px;justify-content:space-between;flex-wrap:wrap}.site-footer p{margin:0;max-width:700px}.article-page{font:19px/1.75 Georgia,serif}.publication-date{font:13px/1.5 system-ui,sans-serif;color:var(--muted);margin:-18px 0 26px}.publication-note{font:13px/1.7 system-ui,sans-serif;color:var(--muted);padding-top:22px;border-top:1px solid var(--line)}.skip{position:absolute;top:-100px;left:15px;background:var(--paper);padding:10px;z-index:10}.skip:focus{top:10px}
@media(max-width:700px){nav{padding:16px 20px;gap:14px;flex-wrap:wrap}.brand{display:block}.controls{gap:16px}.nav-link{display:inline}.copy{display:none}.home{padding:0 20px}.hero{padding:54px 0 44px}.hero h1{font-size:46px}.intro{font-size:18px}.card{grid-template-columns:1fr}.card img{min-height:0;height:auto}.card-copy{padding:24px}.card h2{font-size:27px}.about{grid-template-columns:1fr;gap:20px;margin-top:48px}.site-footer{padding:22px 20px}.publication-date{margin-top:-16px}}
.breadcrumbs{font:12px/1.6 system-ui,sans-serif;color:var(--muted);padding:0;margin:22px 0 12px;display:block}.breadcrumbs ol{list-style:none;display:flex;flex-wrap:wrap;gap:8px;padding:0;margin:0}.breadcrumbs li{margin:0;padding:0}.breadcrumbs li+li:before{content:'/';padding-right:8px}.author-copy{max-width:760px;padding-bottom:30px}.author-copy h2{font-size:25px;letter-spacing:-.025em;margin-top:38px}.author-copy p{color:var(--muted)}.profile-hero{padding-bottom:30px}.profile-hero h1{font-size:clamp(38px,6vw,62px)}.resource-link{font-weight:600}
'''


def stamp(post):
    return date.fromisoformat(post['date']).strftime('%B %d, %Y').replace(' 0', ' ')


def header(copy=False):
    button = '<button id="copy" class="copy">Copy article</button>' if copy else ''
    return ('<a class="skip" href="#main">Skip to content</a><header><nav>'
            '<a class="brand" href="/">Saurabh Kumar</a><div class="controls">'
            '<a class="nav-link" href="/#articles">Articles</a>'
            '<a class="nav-link" href="/about/">About</a>'
            '<a class="nav-link" href="/feed.xml">RSS</a>' + button +
            '</div></nav><div id="status" class="status" role="status" aria-live="polite"></div></header>')


def footer():
    return ('<footer class="site-footer"><p>© 2026 Saurabh Kumar. '
            'Articles: CC BY 4.0. Code: MIT.<br>No advertising or analytics scripts. '
            'Hosted on GitHub Pages.</p><div class="socials">'
            '<a href="https://x.com/drummatick">X / @drummatick</a>'
            '<a href="https://github.com/saurabhkumar8112">GitHub</a></div></footer>')


def json_ld(data):
    return '<script type="application/ld+json">'+json.dumps(data,ensure_ascii=False).replace('<','\\u003c')+'</script>'


def person():
    return {'@type':'Person','@id':BASE+'/about/#person','name':SITE['name'],
            'url':BASE+'/about/','sameAs':[SITE['social_url'],'https://github.com/saurabhkumar8112']}


def image_dimensions(path):
    data=path.read_bytes()
    assert data[:8] == b'\x89PNG\r\n\x1a\n', 'Expected original PNG'
    return struct.unpack('>II',data[16:24])


def optimize_html_images(html, source, card=False):
    def replace(match):
        attrs={key:unescape(value) for key,value in re.findall(r'([\w:-]+)="([^"]*)"',match[1])}
        src=attrs.get('src','')
        original=source/'assets'/Path(src).name
        if not original.is_file() or original.suffix!='.png':
            return match[0]
        width,height=image_dimensions(original)
        attrs.update(width=str(width),height=str(height),decoding='async')
        cover=original.stem=='cover'
        attrs['loading']='eager' if cover else 'lazy'
        if cover:
            attrs['fetchpriority']='high'
        if original.with_suffix('.webp').is_file():
            prefix=src.rsplit('/',1)[0]+'/'
            attrs['src']=prefix+original.with_suffix('.webp').name
            variants=[]
            for smaller in (640,1280):
                variant=original.with_name(f'{original.stem}-{smaller}.webp')
                if variant.is_file() and smaller<width:
                    variants.append(f'{prefix}{variant.name} {smaller}w')
            variants.append(f'{attrs["src"]} {width}w')
            attrs['srcset']=', '.join(variants)
            attrs['sizes']='(max-width: 700px) calc(100vw - 40px), 560px' if card else ('(max-width: 1150px) 100vw, 1102px' if cover else '(max-width: 900px) calc(100vw - 40px), 812px')
        return '<img '+ ' '.join(f'{key}="{escape(value,quote=True)}"' for key,value in attrs.items())+'>'
    return re.sub(r'<img\s+([^>]+)>',replace,html)


def metadata(title, description, path='/', image=None, article=None, noindex=False):
    url = BASE + path
    image_object=None
    values = {'og:title': title, 'og:description': description,
              'og:type': 'article' if article else 'website', 'og:url': url,
              'og:site_name': SITE['name'], 'twitter:card': 'summary_large_image' if image else 'summary',
              'twitter:creator': '@drummatick'}
    if image:
        values['og:image'] = BASE + image
        values['og:image:alt'] = title
        image_object={'@type':'ImageObject','url':BASE+image}
        original=ROOT/'content'/image.removeprefix('/articles/')
        if original.is_file() and original.suffix=='.png':
            width,height=image_dimensions(original)
            image_object.update(width=width,height=height)
            values.update({'og:image:width':str(width),'og:image:height':str(height),'og:image:type':'image/png'})
    if article:
        values['article:published_time'] = article['published_at']
        values['article:modified_time'] = article['updated_at']
        values['article:author'] = BASE+'/about/'
    tags = ''.join(f'<meta {"name" if k.startswith("twitter:") else "property"}="{escape(k)}" content="{escape(v, quote=True)}">' for k, v in values.items())
    if not noindex:
        tags += f'<link rel="canonical" href="{escape(url)}">'
    tags += '<link rel="alternate" type="application/rss+xml" title="Saurabh Kumar" href="/feed.xml">'
    tags += '<link rel="icon" type="image/svg+xml" sizes="any" href="/favicon.svg">'
    tags += '<meta name="robots" content="'+('noindex, follow' if noindex else 'index, follow, max-image-preview:large')+'">'
    if SITE.get('google_site_verification'):
        tags += '<meta name="google-site-verification" content="'+escape(SITE['google_site_verification'],quote=True)+'">'
    if article:
        data = {'@type':'BlogPosting','@id':url+'#article','url':url,'headline':title,
                'description':description,'datePublished':values['article:published_time'],
                'dateModified':values['article:modified_time'],'inLanguage':'en',
                'articleSection':article['category'],'author':person(),'publisher':person(),
                'isPartOf':{'@id':BASE+'/#website'},'mainEntityOfPage':{'@type':'WebPage','@id':url},
                'image':image_object}
        breadcrumbs={'@type':'BreadcrumbList','itemListElement':[
            {'@type':'ListItem','position':1,'name':'Home','item':BASE+'/'},
            {'@type':'ListItem','position':2,'name':title,'item':url}]}
        tags += json_ld({'@context':'https://schema.org','@graph':[data,breadcrumbs]})
    elif path=='/':
        website={'@type':'WebSite','@id':BASE+'/#website','url':BASE+'/',
                 'name':SITE['name'],'description':SITE['description'],'inLanguage':'en','publisher':person()}
        tags += json_ld({'@context':'https://schema.org','@graph':[website,person()]})
    elif path=='/about/':
        tags += json_ld({'@context':'https://schema.org','@type':'ProfilePage','@id':url,
                         'url':url,'name':'About Saurabh Kumar','mainEntity':person(),
                         'dateModified':SITE['profile_updated'],'inLanguage':'en'})
    return tags


def page(title, description, body, path='/', image=None, noindex=False):
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{escape(title)}</title><meta name="description" content="{escape(description, quote=True)}">'
            '<meta name="author" content="Saurabh Kumar">' + metadata(title,description,path,image,noindex=noindex) +
            '<style>'+CSS+'</style></head><body>'+header()+body+footer()+'</body></html>')


def public_links(html, slug):
    def replace(match):
        target = match[1]
        if target == 'article.html':
            return 'href="./"'
        if target.split('#')[0].endswith(('.md', '.py')):
            return 'href="'+REPO+'/blob/main/content/'+slug+'/'+target+'"'
        return match[0]
    return re.sub(r'href="([^\"]+)"', replace, html)


cards = []
for post in POSTS:
    slug = post['slug']
    source = ROOT / 'content' / slug
    target = OUT / 'articles' / slug
    target.mkdir(parents=True)
    subprocess.run([sys.executable, str(source / 'build_article.py')], check=True)
    for p in (source / 'assets').iterdir():
        assert p.is_file() and not p.is_symlink() and p.suffix in ('.png','.svg','.webp')
    shutil.copytree(source / 'assets', target / 'assets')
    shutil.copyfile(source / 'ARTICLE.txt', target / 'ARTICLE.txt')
    html = (source / 'article.html').read_text()
    html = re.sub(r'<title>.*?</title>','<title>'+escape(post.get('seo_title',post['title']+' | '+SITE['name']))+'</title>',html,count=1)
    html = re.sub(r'<meta name="description" content="[^"]*">','<meta name="description" content="'+escape(post['description'],quote=True)+'">',html,count=1)
    html = re.sub(r'<header>.*?</header>',header(copy=True),html,count=1,flags=re.S)
    html = html.replace('<main>', '<main id="main">',1)
    html = html.replace('<body>', '<body class="article-page">',1)
    html = html.replace('</head>', metadata(post['title'],post['description'],f'/articles/{slug}/',f'/articles/{slug}/'+post['image'],post)+'<style>'+CSS+'</style></head>',1)
    html = re.sub(r'(<p class="byline">.*?</p>)',r'\1<p class="publication-date"><time datetime="'+post['date']+'">'+stamp(post)+'</time></p>',html,count=1)
    if post.get('updated',post['date']) != post['date']:
        updated=date.fromisoformat(post['updated']).strftime('%B %d, %Y').replace(' 0',' ')
        html=html.replace('</time></p>','</time> · Updated <time datetime="'+post['updated']+'">'+updated+'</time></p>',1)
    html = html.replace('By Saurabh Kumar ·','By <a href="/about/" rel="author">Saurabh Kumar</a> ·',1)
    breadcrumb='<nav class="breadcrumbs" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li><li aria-current="page">'+escape(post['title'])+'</li></ol></nav>'
    html = html.replace('<article>',breadcrumb+'<article>',1)
    note = '<p class="publication-note">Writing and illustrations prepared with AI assistance. The cover is AI-generated; the diagrams are generated from code. See the <a href="SOURCES.md">sources and illustration notes</a>.</p>'
    html = html.replace('</article>',note+'</article>',1).replace('</body>',footer()+'</body>')
    html = public_links(html,slug)
    html = optimize_html_images(html,source)
    (target / 'index.html').write_text(html)
    if (source/'calculator.html').exists():
        calculator = public_links((source/'calculator.html').read_text(),slug)
        calc_title='LLM Cascade Cost Calculator | Saurabh Kumar'
        calc_description='Estimate LLM routing costs from your first-stage cost, fallback rate, and selected fallback workload. Explore explicit assumptions without sending data to a server.'
        calculator = re.sub(r'<title>.*?</title>','<title>'+calc_title+'</title>',calculator,count=1)
        calculator = calculator.replace('</head>','<meta name="author" content="Saurabh Kumar"><meta name="description" content="'+calc_description+'">'+metadata(calc_title,calc_description,f'/articles/{slug}/calculator.html')+'</head>',1)
        (target / 'calculator.html').write_text(calculator)
    card=f'<a class="card" href="/articles/{slug}/"><img src="/articles/{slug}/{post["image"]}" alt="{escape(post["title"])}"><div class="card-copy"><div class="eyebrow">{escape(post["category"])} · <time datetime="{post["date"]}">{stamp(post)}</time></div><h2>{escape(post["title"])}</h2><p>{escape(post["description"])}</p><span class="read">Read the article →</span></div></a>'
    cards.append(optimize_html_images(card,source,card=True))

home = '<main class="home" id="main"><section class="hero"><div class="eyebrow">Technical writing by Saurabh Kumar</div><h1>AI, systems, and<br>engineering decisions.</h1><p class="intro">What does it cost? Where does it fail? When should you use it? Articles that work through the decisions behind the technology.</p></section><section id="articles" aria-labelledby="articles-title"><h2 class="section-title" id="articles-title">Articles <a href="/feed.xml">Follow via RSS ↗</a></h2><div class="cards">'+''.join(cards)+'</div></section><section class="about" id="about"><h2>About this space</h2><div><p>A collection of technical articles by Saurabh Kumar, exploring AI systems, cost, reliability, and practical engineering choices.</p><p>Each article brings its references and supporting material with it. Follow along as the collection grows.</p><div class="socials"><a href="https://x.com/drummatick">Follow @drummatick on X ↗</a><a href="https://github.com/saurabhkumar8112">Find the code on GitHub ↗</a></div></div></section></main>'
cover='/articles/'+POSTS[0]['slug']+'/'+POSTS[0]['image'] if POSTS else None
(OUT/'index.html').write_text(page('Saurabh Kumar | AI, systems, and engineering',SITE['description'],home,image=cover))
(OUT/'404.html').write_text(page('Page not found | Saurabh Kumar','This page could not be found.','<main class="home" id="main"><section class="hero"><div class="eyebrow">404</div><h1>This page is missing.</h1><p class="intro">You can find the published articles on the homepage.</p><a href="/">Browse the articles →</a></section></main>',path='/404.html',noindex=True))
(OUT/'about').mkdir()
article_links=''.join('<li><a href="/articles/'+post['slug']+'/">'+escape(post['title'])+'</a></li>' for post in POSTS)
about='<main class="home" id="main"><section class="hero profile-hero"><div class="eyebrow">About the author</div><h1>Saurabh Kumar</h1><p class="intro">Technical writing about AI systems, reliability, and the cost of engineering decisions.</p></section><div class="author-copy"><p>Saurabh Kumar writes practical articles that work through when to use a technology, how to evaluate it, and what can go wrong after a decision is made.</p><h2>What you can read here</h2><p>The collection covers AI agents, model choices, search, coding workflows, and the trade-off between cost and reliability.</p><ul>'+article_links+'</ul><h2>Sources and supporting work</h2><p>References, assumptions, and companion code are linked from each article. Hypothetical examples are labeled, and experimental findings are distinguished from general guidance. AI assistance is disclosed where it is used.</p><p>The <a href="https://github.com/saurabhkumar8112/jev-gpt5-routing-study">separate Jev and GPT-5 routing study</a> includes its code, results, and limitations on GitHub.</p><h2>Find me elsewhere</h2><p><a href="https://x.com/drummatick">@drummatick on X</a> · <a href="https://github.com/saurabhkumar8112">saurabhkumar8112 on GitHub</a></p><p><a class="resource-link" href="/feed.xml">Follow new articles via RSS →</a></p></div></main>'
(OUT/'about/index.html').write_text(page('About Saurabh Kumar | AI Engineering Articles','Saurabh Kumar writes about AI agents, model evaluation, cost, and reliability. Read the articles, explore supporting code, and find his public profiles.',about,path='/about/'))
(OUT/'favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#101d33"/><text x="32" y="41" text-anchor="middle" fill="#faf8f2" font-family="system-ui,sans-serif" font-size="27" font-weight="700">SK</text></svg>')

rss=ET.Element('rss',{'version':'2.0'})
channel=ET.SubElement(rss,'channel')
for tag,value in [('title',SITE['name']),('link',BASE+'/'),('description',SITE['description']),('language','en')]:
    ET.SubElement(channel,tag).text=value
for post in POSTS:
    item=ET.SubElement(channel,'item')
    url=BASE+'/articles/'+post['slug']+'/'
    for tag,value in [('title',post['title']),('link',url),('guid',url),('description',post['description']),('pubDate',format_datetime(datetime.fromisoformat(post['published_at'])))]:
        ET.SubElement(item,tag).text=value
ET.indent(rss)
ET.ElementTree(rss).write(OUT/'feed.xml',encoding='utf-8',xml_declaration=True)
sitemap=ET.Element('urlset',{'xmlns':'http://www.sitemaps.org/schemas/sitemap/0.9'})
urls=[('/',max([SITE['profile_updated']]+[p.get('updated',p['date']) for p in POSTS])),('/about/',SITE['profile_updated'])]
urls += [('/articles/'+p['slug']+'/',p.get('updated',p['date'])) for p in POSTS]
urls += [('/articles/'+p['slug']+'/calculator.html',p.get('updated',p['date'])) for p in POSTS if (OUT/'articles'/p['slug']/'calculator.html').exists()]
for path,updated in urls:
    url=ET.SubElement(sitemap,'url')
    ET.SubElement(url,'loc').text=BASE+path
    ET.SubElement(url,'lastmod').text=updated
ET.indent(sitemap)
ET.ElementTree(sitemap).write(OUT/'sitemap.xml',encoding='utf-8',xml_declaration=True)
(OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+BASE+'/sitemap.xml\n')
print(f'Built {len(POSTS)} article(s), homepage, feed, sitemap, and 404 page in docs/.')
