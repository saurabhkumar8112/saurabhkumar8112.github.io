# Research and editorial notes

Status: publication source. Checked September 23, 2026.

## Sources used in the article

1. [Infosys FY2026 Form 20-F](https://www.infosys.com/investors/documents/exchange-filings/2026/form20f-2026.pdf). Printed pp. 22 and 77: 54% fixed-price revenue in FY2026 and FY2025; mixed pricing arrangements; estimation and automation risks. One company's disclosure, not an industry-wide revenue estimate.
2. [McKinsey: The state of AI in 2026](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai). August 25, 2026. Self-reported adoption: nearly nine in ten use AI in at least one function; agent scaling in one or more functions is 40% among respondents at organizations above $1 billion revenue and 22% at smaller organizations. These are distinct measures, not autonomous-completion rates. The evergreen URL can change when the survey is updated.
3. [Anthropic: Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents). January 9, 2026. Technical discussion of graders and repeat-trial reliability. Vendor engineering guidance, not independent certification of any service.
4. [Sierra: Outcome-based pricing for AI agents](https://sierra.ai/blog/outcome-based-pricing-for-ai-agents). Commercial precedent for agreed outcomes and blended pricing. Vendor description, not audited customer performance or a universal price quotation.
5. [SWE-bench](https://www.swebench.com/). Primary benchmark site. Used for the task scope, not current model rankings or a production-readiness claim.
6. [Yao et al.: τ-bench](https://arxiv.org/abs/2406.12045). June 2024. Methodological precedent: tool interaction, policy constraints, and final database-state evaluation. Historical model scores intentionally omitted.
7. [Google SRE: Implementing SLOs](https://sre.google/workbook/implementing-slos/). Primary operational reference for objectives and error-budget decisions. The article's agent-specific procurement proposal is an extension, not a Google standard.
8. [AWS Builders' Library: Making retries safe with idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/). Primary engineering reference for ambiguous outcomes and idempotent retries. The maintenance workflow and evaluation protocol are proposed applications.

## Corrections to the starting premise

- Interpret “ID companies” as IT services companies and “SW bench” as SWE-bench.
- Do not say every firm bills only for engineer hours. Fixed-price and other models already exist.
- Do not use 5–10% as an unsupported figure for all B2B AI penetration.
- Do not claim agents have no checks or that production reliability is unknowable. Existing controls provide bounded evidence; universal guarantees are not justified.
- Outcome pricing is conditional on measurable acceptance and controllable scope. Hourly consulting and hybrid contracts can remain appropriate.
- Human oversight can scale through scoped authority, exception handling, and audits. It need not mean one observer per agent.
- A benchmark qualifies a specified delivery system for further evaluation. It does not certify a whole company or establish an SLA on its own.
- These are editorial inferences and a proposed protocol. No new benchmark, vendor ranking, production rollout, or customer experiment was performed.

## Arithmetic and assumptions

- Review workload: 1,000,000 × 0.05 × 10 / 60 = 8,333.33 hours. Dividing by 160 gives 52.08 monthly full-time equivalents before overhead and queueing effects.
- Cost example A: 2,000 + 30,000 + 5,000 + 10,000 = $47,000; / 9,500 accepted outcomes = $4.9474.
- Cost example B: 8,000 + 7,500 + 5,000 + 2,000 = $22,500; / 9,900 accepted outcomes = $2.2727.
- The two systems see the same 10,000 hypothetical arrivals. Accepted outcomes can include human-assisted completions; they do not measure autonomous success. Failed work remains in the numerator. Fallback/review costs and subsequent rework allowances are separate buckets. Dollar values are illustrative allocations, not vendor prices or measured losses. Real accounting must prevent double counting and include ongoing and amortized fixed costs.
- Under independent identical per-step success with every step required: 0.99^20 = 0.81790694. This does not model correlated errors, checkpoints, recovery, or real production success.
- Queue illustration: 1,000 × 0.05 × (10/60) / 10 = 0.833333 utilization. At 10% escalation it becomes 1.666667. This is an average workload ratio, not a waiting-time model. Audit work and staffing overhead must be added.
- Pricing model: expected per-arrival cost b = c_a + r*c_h + expected additional provider loss + F/N. Expected period cost divided by expected accepted volume is b/q. With outcome-only revenue and a target margin m, price is b/[q*(1-m)]. This assumes q>0, 0<=m<1, disjoint costs, specified volume, and no other fees. It is not the expectation of the realized random ratio of cost to accepted outcomes.
- Illustrative SLO: 99% completion across 10,000 eligible matured tasks permits 100 missed outcomes. Critical-violation policy and subgroup requirements are separate. This is not a recommended universal threshold.

## Technical revision

The expanded article adds matured-cohort metrics, an external authorization and verification architecture, retry semantics, review-queue capacity, outcome-pricing equations, selective risk and coverage, clustered evaluation, and explicit error-budget actions. [TECHNICAL_PROTOCOL.md](TECHNICAL_PROTOCOL.md) provides a proposed procurement/evaluation specification with an illustrative record. No new model calls, experiments, or production deployments were performed.
- For zero observed failures among n independent identically distributed Bernoulli trials, a one-sided exact 95% upper bound is 1 − 0.05^(1/n). At n=3,000 it is approximately 0.00099808, or 0.099808%. This is not a posterior probability, a production guarantee, or justification for replacing diverse testing with repeated identical cases.

## Approved title and framing

**When AI Does the Work, What Will Infosys and TCS Sell?**

Approved by the author. The company names provide the opening question; the article examines IT service delivery and accountability. It does not forecast either company's financial performance. The twenty-minute opening is explicitly hypothetical.

## Company context added

- [Infosys AI strategy, February 17, 2026](https://www.infosys.com/newsroom/press-releases/2026/unveils-ai-first-value-framework.html): company-described strategy, not independent validation of delivery performance.
- [TCS FY2026 report, printed page 90](https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2025-26/ar/annual-report-2025-2026.pdf): management outlook, not a quantified current outcome-contract revenue share.
- [TCS April 9, 2026 results announcement](https://www.tcs.com/who-we-are/newsroom/press-release/tcs-financial-results-q4-fy-2026): platform announcement, not audited workflow success.

## Publication notes

- Published article package is under `content/future-of-it-services/`.
- No Banking77 findings, keys, internal customer data, private logs, or employment claims are included.
- Verify date-sensitive adoption and filing references again if publication is delayed.
- Suitable future illustrations: a delivery-to-acceptance workflow with a verification gate and human escalation; the hypothetical cost table as a chart. No stock market predictions or unsupported company valuations are needed.

## Frontier research revision, September 23, 2026

These additions distinguish author-reported research, internal operational measurements, methodological audits, and this article's commercial inferences. They are not a unified leaderboard or independently replicated results.

- [Anthropic internal measurements](https://www.anthropic.com/institute/measuring-pace-of-ai-development): August snapshot, weighted automation categories and one internal platform. Not external customer outcomes.
- [OpenAI coding-evaluation audit, July 8](https://openai.com/index/separating-signal-from-noise-coding-evaluations/): supersedes its earlier recommendation of SWE-Bench Pro. Audit estimates are attributed, not universal benchmark failure rates.
- [Cognition SWE-1.7, July 8](https://cognition.com/blog/swe-1-7): vendor-authored comparison and training account. No inference-price or production-reliability equivalence inferred.
- [Thinking Machines collaboration, August 27](https://thinkingmachines.ai/news/putting-task-expertise-into-rl/): cross-benchmark human proxy and SC-16 qualification retained. No universal human-level SQL claim.
- [METR limitations, January 22](https://metr.org/notes/2026-01-22-time-horizon-limitations/): capability horizons are not unattended-runtime guarantees.
- [METR modeling correction, March 20](https://metr.org/notes/2026-03-20-impact-of-modelling-assumptions-on-time-horizon-results/): cited as methodological evidence, not a current ranking.

The newer-lab discussion uses a concrete Thinking Machines research collaboration and Cognition's specialized training results. It does not use fundraising, rumored capabilities, or unverified launch claims as performance evidence. Benchmark appeals, controlled corrections, and contamination controls are proposed procurement requirements.

## Earnings-call revision

Primary transcripts checked September 23, 2026:

- [TCS July 9, 2026](https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2026-27/q1/Management%20Commentary/Transcript%20of%20the%20Q1%202026-27%20Earnings%20Conference%20Call%20held%20on%20Jul%209,%202026.pdf), pages 4, 21–24. Management commentary, not independently verified workflow performance.
- [Infosys July 23, 2026](https://www.infosys.com/investors/reports-filings/quarterly-results/2026-2027/q1/documents/transcripts/earningscall.pdf), PDF pages 12, 15–17, 20, 23. Pricing, AI classification, and model-routing passages.
- [TCS quarterly release](https://www.tcs.com/who-we-are/newsroom/press-release/tcs-financial-results-q1-fy-2027). Annualized revenue is a run rate.

Editorial change: outcome pricing is already present. The proposal concerns verifiable commitments, not invention of a commercial model. The contract-mechanics table is analysis, not reported revenue segmentation. No causal attribution of company margins or staffing to AI alone. No comparable company-wide autonomous delivery metric established by these sources.
