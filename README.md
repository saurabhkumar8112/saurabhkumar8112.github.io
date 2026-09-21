# Saurabh Kumar

Technical articles on AI, systems, and engineering decisions.

**Read the publication: https://saurabhkumar8112.github.io/**

## Articles

- [When should you use JEV? A practical guide](https://saurabhkumar8112.github.io/articles/when-should-you-use-jev/) · September 22, 2026
  - [Article source](content/when-should-you-use-jev/ARTICLE.md)
  - [Optional code examples](content/when-should-you-use-jev/code/README.md)
  - [Sources and limitations](content/when-should-you-use-jev/SOURCES.md)

## Publishing another article

This repository is the home for an ongoing collection of articles. Each post has a stable `/articles/<slug>/` address. GitHub Pages serves `docs/` from the `main` branch.

1. Add an article folder under `content/<slug>/`, following the first article's structure: Markdown, local images, a `build_article.py` renderer, and any companions. The current renderer supports the Markdown constructs used by this article, not arbitrary Markdown. Calculator companions are optional.
2. Add its title, description, publication date, category, cover path, and slug to `site.json`.
3. Run `python3 build_site.py`. The build uses the Python standard library and makes no external requests. It recreates only `docs/` and updates the article's generated reader and plain text.
4. Review the article and the generated homepage, check links and sensitive content, then commit the source and `docs/` together. Pushing `main` triggers GitHub Pages publication.

The homepage, RSS feed, sitemap, social previews, and article metadata are generated from `site.json`. No external fonts, analytics scripts, or JavaScript framework are required. Only local calculator arithmetic and the article copy button use JavaScript. The site contains no forms or application backend.

## Future domain

The GitHub Pages address works now. To connect an owned domain later, verify and configure it in GitHub Pages, update `base_url` in `site.json`, and rebuild so canonical URLs, RSS, sitemap, and social images use the new address. Set the domain in GitHub Pages only after ownership and DNS are ready.

## Source and publication boundaries

Only the approved article package is included. No API credentials, environment files, provider logs, private study data, or earlier repository history were copied. The Jev guide uses hypothetical arithmetic; it does not report the earlier routing experiment's results. Live examples require an explicit opt-in and an environment variable on the reader's own machine. They are never run by this site's build.

Original writing and figures are CC BY 4.0, subject to the article's [content license](content/when-should-you-use-jev/CONTENT_LICENSE.md). Code is MIT licensed. AI assistance and image provenance are disclosed in the article and its source notes.
