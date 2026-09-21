# Sources and claim boundaries

Documentation checked 21 September 2026. API capabilities may change. The guide's recommendations are engineering judgments, and its use cases are proposed designs to evaluate. No prior experiment's results are included.

| Source | Supports | Does not establish |
|---|---|---|
| [TypeSafe primitives](https://docs.typesafe.ai/primitives) | Choice, Score and Noul are typed decision interfaces | Universal task accuracy or replacement of text/code generation |
| [TypeSafe HTTP API](https://docs.typesafe.ai/api) | Endpoint, bearer authentication, response model field, Choice schema and the 255-option limit | Successful live execution of this guide's adapter |
| [TypeSafe quick start](https://docs.typesafe.ai/introduction/quickstart) | Basic request/response structure and example pinned response version | A production-ready deployment |
| [TypeSafe confidence](https://docs.typesafe.ai/confidence) | Confidence derives from distribution shape; thresholds are application-dependent | A score is a calibrated correctness probability on a new workload |
| [TypeSafe reranking cookbook](https://docs.typesafe.ai/cookbooks/rerank_typesafe) | Retrieval-shortlist relevance judgment as a documented pattern | The guide's own search benchmark or a general retrieval advantage |
| [TypeSafe skill suggestion](https://docs.typesafe.ai/cookbooks/skill_suggestion) | Bounded selection from a supplied skill catalog | Reliability of a complete agent using that selection |
| [TypeSafe candidate extraction](https://docs.typesafe.ai/cookbooks/pre_parsed_value_extraction_cookbook) | Selecting among pre-parsed values and recovering source text in code | Arbitrary string generation or correctness of every extracted field |
| [Microsoft hybrid ranking documentation](https://learn.microsoft.com/azure/search/hybrid-search-ranking) | Combining separately retrieved result sets and distinguishing retrieval/ranking stages | A measured Jev comparison |
| [Anthropic, Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | Workflow/agent distinctions and the cost, latency and compounding-error concerns of autonomous loops | A Jev-specific long-horizon failure rate |
| [Geifman and El-Yaniv, SelectiveNet, ICML 2019](https://proceedings.mlr.press/v97/geifman19a.html) | Selective prediction and the risk–coverage framing | That Jev implements SelectiveNet or inherits its empirical results |

The article does not quote vendor speedups or use the numerical outcomes in vendor cookbooks. Cost curves, horizon curves and demo answers are original synthetic illustrations whose assumptions are stated beside them. The case matrix and deployment worksheet are proposals, not a published benchmark.

## Visual provenance

- Cover: generated with built-in Image Gen. Exact prompt: [visuals/cover-prompt.txt](visuals/cover-prompt.txt). No vendor logos or numerical performance claims.
- Four explanatory figures: original Matplotlib diagrams and synthetic plots. Source: [visuals/build_figures.py](visuals/build_figures.py). PNG exports and SVG versions with editable text are in `assets/`.
- No desktop screenshots, private logs, provider account data or customer records are included.
