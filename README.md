# Saurabh Kumar

Technical articles on AI, systems, and engineering decisions.

**Read the publication: https://saurabhkumar8112.github.io/**

## Articles

- [When AI Does the Work, What Will Infosys and TCS Sell?](https://saurabhkumar8112.github.io/articles/future-of-it-services/)
  - [Article source](content/future-of-it-services/ARTICLE.md)
  - [Evaluation protocol](content/future-of-it-services/TECHNICAL_PROTOCOL.md)
  - [Sources](content/future-of-it-services/SOURCES.md)

- [When should you use JEV? A practical guide](https://saurabhkumar8112.github.io/articles/when-should-you-use-jev/) · September 22, 2026
  - [Article source](content/when-should-you-use-jev/ARTICLE.md)
  - [Optional code examples](content/when-should-you-use-jev/code/README.md)
  - [Sources and limitations](content/when-should-you-use-jev/SOURCES.md)

## Publishing another article

This repository is the home for an ongoing collection of articles. Each post has a stable `/articles/<slug>/` address. GitHub Pages serves `docs/` from the `main` branch.

1. Add an article folder under `content/<slug>/`, following the first article's structure: Markdown, local images, a `build_article.py` renderer, and any companions. The current renderer supports the Markdown constructs used by this article, not arbitrary Markdown. Calculator companions are optional.
2. Add its title, description, publication date, category, cover path, and slug to `site.json`. Include `published_at` and `updated_at` as ISO 8601 timestamps with a timezone, matching the `date` and `updated` calendar dates.
3. Run `python3 build_site.py`. The build uses the Python standard library and makes no external requests. It recreates only `docs/` and updates the article's generated reader and plain text.
4. Review the article and the generated homepage, check links and sensitive content, then commit the source and `docs/` together. Pushing `main` triggers GitHub Pages publication.

The homepage, RSS feed, sitemap, social previews, and article metadata are generated from `site.json`. No external fonts, analytics scripts, or JavaScript framework are required. Only local calculator arithmetic and the article copy button use JavaScript. The site contains no forms or application backend.

## Search and image metadata

`site.json` is the source of truth for search descriptions, optional `seo_title` values, and publication dates. The article heading remains the visible editorial title. Set `updated` and `updated_at` only when the article actually changes, never on every build. The author page uses the explicit `profile_updated` timestamp. The first article's publication timestamp comes from its first successful Pages deployment, and its modification timestamp comes from the source revision. Metadata-only corrections do not reset these dates.

The build creates self-canonical pages, an author profile, article and breadcrumb structured data, website identity, RSS, and a sitemap containing the homepage, profile, articles, and available calculators. The custom 404 page is marked `noindex`. Large search-image previews are permitted. Structured data and sitemaps make content understandable and discoverable; they do not guarantee indexing or ranking.

Original PNGs remain unchanged. Browser copies are compressed WebP images with responsive sizes, intrinsic dimensions, and lazy loading for body figures. Run `python3 optimize_images.py` after changing PNGs; this optional step requires `cwebp`. Commit the resulting derivatives, then run the standard-library site build. Social previews retain the original full-resolution PNG.

To verify Google Search Console, the build supports an optional `google_site_verification` field containing Google's public HTML-tag verification value. Add only a value actually issued for this site in the owner's Google account. Do not add credentials or OAuth tokens. Then verify ownership and submit `https://saurabhkumar8112.github.io/sitemap.xml` through Search Console. Publishing a sitemap by itself is not the same as submitting it in the owner's account.

Google's downloaded HTML verification file is preserved in `verification/` and copied to the site root on every build. Keep the verification file and tag after ownership is verified. These are public ownership proofs, not sign-in credentials.

## Future domain

The GitHub Pages address works now. To connect an owned domain later, verify and configure it in GitHub Pages, update `base_url` in `site.json`, and rebuild so canonical URLs, RSS, sitemap, and social images use the new address. Set the domain in GitHub Pages only after ownership and DNS are ready.

## Source and publication boundaries

Only the approved article package is included. No API credentials, environment files, provider logs, private study data, or earlier repository history were copied. The Jev guide uses hypothetical arithmetic; it does not report the earlier routing experiment's results. Live examples require an explicit opt-in and an environment variable on the reader's own machine. They are never run by this site's build.

Original writing and figures are CC BY 4.0, subject to the article's [content license](content/when-should-you-use-jev/CONTENT_LICENSE.md). Code is MIT licensed. AI assistance and image provenance are disclosed in the article and its source notes.
