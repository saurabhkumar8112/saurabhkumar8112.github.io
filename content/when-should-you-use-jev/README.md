# When should you use JEV? A practical guide

An independent practical guide to bounded decisions, fallback economics and errors across complete workflows. The article covers 14 use cases, with deeper treatment of search, coding and agents. All numerical scenarios are hypothetical. No experimental results or customer data are included.

## Read or copy

- [Illustrated reading version](article.html): self-contained local assets, with a plain-text copy button.
- [Clean copy-paste text](ARTICLE.txt): no Markdown headings, table syntax or image placeholders. Reformat it in the destination editor as needed.
- [Markdown source](ARTICLE.md): for GitHub and editors that support Markdown.
- [Interactive calculator](calculator.html): hypothetical fallback costs and an explicitly simplified long-horizon illustration. Runs locally without network calls.
- [Technical notes and evaluation worksheet](TECHNICAL_NOTES.md).
- [Runnable code](code/README.md) and [source/claim notes](SOURCES.md).

## Images and placement

Upload the PNGs individually when your article editor does not import local assets. The Markdown and HTML already place the four body figures.

| Asset | Placement |
|---|---|
| [Cover](assets/cover.png) | Article thumbnail/header |
| [Decision map](assets/decision-map.png) | After the three questions about answers, evidence and consequences |
| [Agent checkpoints](assets/agent-checkpoints.png) | In the agent section, after the recovery discussion |
| [Error horizon](assets/error-horizon.png) | After the hypothetical 20-step illustration |
| [Cascade economics](assets/cascade-economics.png) | After the fictional cost table |

The four body figures also have SVG versions with editable text. Their source is `visuals/build_figures.py`, using Matplotlib. The cover was made with built-in Image Gen; its exact prompt is saved in `visuals/cover-prompt.txt`.

## Rebuild and validate

The examples and tests need only Python 3.10+. Run the commands in [code/README.md] from this folder. The optional live example is explicitly gated by `--live`; it was not run for this guide.

`python3 build_article.py` regenerates the reading version and copy text from the Markdown. It uses only the standard library. Rebuilding the figures additionally requires Matplotlib and uses the same arithmetic functions as the code examples.

The calculator and plots do not predict accuracy or select deployment thresholds. They make assumptions visible. Their defaults must not be presented as vendor pricing or empirical measurements.

## Release boundary and license

This folder is a standalone publication package. It contains no credentials, environment files, raw provider logs, private Git history or desktop screenshots. The generated cover and diagrams are original article assets. Sources distinguish documented API capabilities from engineering recommendations.

Code is under the MIT license in [LICENSE](LICENSE). Original article prose and figures are licensed CC BY 4.0, attribution to saurabhkumar8112, under [CONTENT_LICENSE.md](CONTENT_LICENSE.md). Third-party services, documentation and trademarks retain their own rights. The API provider does not endorse this guide.
