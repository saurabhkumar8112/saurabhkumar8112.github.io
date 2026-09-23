# When AI Does the Work, What Will Infosys and TCS Sell?

By Saurabh Kumar · [@drummatick](https://x.com/drummatick)

*Agents can make implementation cheaper. Verification, recovery, and accountability could determine who captures the savings.*

If an AI agent completes a software change in twenty minutes, what should an IT services company charge for it?

The engineer hours it replaced? The compute it consumed? Or the result it delivered?

For companies such as Infosys and TCS, the answer matters beyond pricing. It changes what they must measure, which risks they absorb, and what customers are actually buying.

Recent research from frontier labs makes that question more urgent. Agents are taking on longer tasks, but even the benchmarks used to judge their work are proving difficult to trust.

The twenty-minute change is a hypothetical example. The commercial problem is real: implementation can get cheaper while verification, integration, and responsibility for failures remain substantial costs. To understand what these companies can sell next, you have to follow the work beyond code generation, through acceptance and into production.

## The hourly model is under pressure, but the industry has already moved beyond it

There is an appealing version of this story: IT firms sell engineers by the hour, agents replace the engineers, and the business model collapses.

The actual industry is more complicated. Infosys reported that fixed-price contracts accounted for 54% of revenue in both fiscal 2026 and 2025. Its filings also describe time-and-material, unit-of-work, and outcome-based arrangements. The same filing warns that misjudging automation gains and delivery costs can damage profitability. [Infosys FY2026 Form 20-F, printed pages 22 and 77](https://www.infosys.com/investors/documents/exchange-filings/2026/form20f-2026.pdf)

That distinction changes the argument.

Under an hourly contract, fewer billable hours can reduce revenue. Under a fixed-price contract, a genuine productivity improvement can increase the supplier's margin, at least until competition and renegotiation pass some of the savings to the customer. Under an outcome contract, the supplier must also understand how often work is accepted, reopened, escalated, or repaired.

Agents therefore affect different contracts differently. There is no reason to assume that every project should immediately become a pay-per-completion service.

A well-specified dependency upgrade is a plausible candidate. Discovering what a business actually needs from a new platform is much harder to package into a fixed unit. Customers change their minds. Requirements conflict. Sometimes the valuable work is discovering that the requested feature should not be built.

Time-based consulting still has a role where the problem itself is uncertain. The pressure will be strongest where the work is repeatable and the customer can independently recognize a good result.

Lower delivery costs could also make previously uneconomic projects worth doing. That may expand demand even as prices fall. Whether a particular firm's revenue grows will depend on the extra work it wins, the savings it retains, and the business its customers bring in-house.

## Their earnings calls show the transition is already happening

The July 2026 earnings calls make the headline's question more precise. These companies already sell several forms of delivery commitment. What is changing is the productivity customers expect within those arrangements.

On TCS's July 9 call, Aarthi Subramanian described outcome commitments, fixed-price capacity, and time-and-material engagements operating alongside one another, with increased outcome commitments in agentic global business services. The company also said headcount had increased that quarter. Its CFO attributed a 170-basis-point margin impact to wage increases, partly offset by currency and operating efficiencies. Those statements do not support a simple story of agents replacing payroll and immediately expanding margins. [TCS Q1 FY2027 call, pages 4 and 21–24](https://www.tcs.com/content/dam/tcs/investor-relations/financial-statements/2026-27/q1/Management%20Commentary/Transcript%20of%20the%20Q1%202026-27%20Earnings%20Conference%20Call%20held%20on%20Jul%209,%202026.pdf)

Infosys's July 23 call was particularly explicit about the negotiation. Management said clients seek AI productivity benefits at renewal and sometimes mid-contract. Pricing still rose, but less than expected amid competition and productivity demands. It reported AI revenue at 8.2% of total revenue, distinguishing this category from AI incorporated into existing work. It did not publicly quantify the associated revenue compression. The CFO also said the company would decline deals requiring uneconomic productivity assumptions. [Infosys Q1 FY2027 call, PDF pages 12, 15–17 and 23](https://www.infosys.com/investors/reports-filings/quarterly-results/2026-2027/q1/documents/transcripts/earningscall.pdf)

Read those statements together and a more useful business-model picture emerges:

| Commercial arrangement | What the customer buys | How automation changes the economics |
|---|---|---|
| Time and material | Agreed skills and billable effort | Fewer hours can reduce the bill; rates, scope, and demand can also change |
| Fixed-price project | Delivery of an agreed scope | Lower delivery cost can improve margin, while estimation errors and rework remain the supplier's problem |
| Fixed-capacity service | Reserved delivery capacity | Productivity can expand throughput; the agreement must say what capacity and service levels mean |
| Transaction or outcome pricing | An agreed unit or accepted result | Fewer human interventions can improve unit economics, provided verification and recovery costs stay controlled |

This table describes contractual mechanics, not each company's revenue mix. In particular, a fixed-price project is not automatically payment for a verified business outcome, and a claim of “outcome accountability” does not establish a pay-only-on-success contract.

TCS separately reported a $2.6 billion annualized AI revenue figure for Q1 FY2027. That is a run-rate measure, not $2.6 billion earned in the quarter. Neither company's AI revenue label tells you how much work completed autonomously, what fraction used outcome pricing, or whether delivery savings exceeded customer discounts. The figures should not be treated as a like-for-like ranking without reconciling their definitions. [TCS Q1 results](https://www.tcs.com/who-we-are/newsroom/press-release/tcs-financial-results-q1-fy-2027)

The engineering strategy is also more concrete than a generic promise to use AI. Infosys described selecting among 15 models in Topaz Fabric according to task and cost. That makes evaluation and routing part of the service itself. It remains a management description, not an independently tested performance claim. [Infosys call, PDF page 20](https://www.infosys.com/investors/reports-filings/quarterly-results/2026-2027/q1/documents/transcripts/earningscall.pdf)

For a supplier, the unresolved question is how much productivity it can deliver after paying for integration, verification, exceptions, and recovery. For a buyer, it is how much of that benefit reaches the contract without degrading service. Public earnings commentary does not provide the task-level failure rates, intervention costs, or acceptance criteria needed to settle that question.

That is the opportunity examined here: making delivery commitments measurable enough to price and operate responsibly. Outcome pricing is already part of the industry; stronger evidence can make those commitments more credible.

## Adoption is not the same as dependable delivery

It is tempting to explain the opportunity by saying that only 5–10% of businesses use AI. That is too broad a claim.

McKinsey's August 2026 survey reports regular AI use in at least one business function among nearly nine in ten respondents. Scaling agents is a different measure: 40% of respondents from organizations with more than $1 billion in annual revenue reported scaling agents in one or more functions, compared with 22% at smaller organizations. These are survey responses, not a census of businesses or a measurement of autonomous task success. [McKinsey, The state of AI in 2026](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai)

For a buyer, the useful question is more specific: can this provider run this workflow, against your systems, with an acceptable rate of failure and a predictable cost?

An agent can produce a plausible patch without establishing that the patch preserves a billing invariant. It can call an API successfully while updating the wrong customer. It can close a support ticket while leaving the underlying issue unresolved.

Conventional engineering already has checks for many of these problems: tests, type systems, access controls, deployment gates, observability, and rollback procedures. Agent evaluations add another source of evidence. Anthropic's evaluation guidance, for example, combines code, model, and human graders and distinguishes occasional success from consistent performance across repeated trials. [Anthropic, Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)

The gap is whether those checks cover the promise being sold. A unit test can verify a calculation. A load test can expose a bottleneck. Neither, by itself, establishes that an autonomous support workflow consistently applies the correct policy to the correct account.

## What the frontier labs are actually showing

The evidence available in September 2026 makes the question more interesting than “can agents write code?” Capabilities are improving, specialized training is changing costs, and the machinery used to measure progress is itself being challenged.

Anthropic's August internal snapshot reports that Claude leads 26% of its AI R&D work under a weighted automation index. “Leads” still includes human supervision; no measured subset was rated fully autonomous. This is a company-reported, partly model-judged assessment, not an independently measured production completion rate. [Anthropic's R&D automation measurements](https://www.anthropic.com/institute/measuring-pace-of-ai-development)

That distinction matters for an IT supplier. A team can delegate much more implementation while retaining responsibility for what ships. Measuring engineer hours saved, autonomous completions, and customer outcomes answers three different questions.

Several recent results show why the architecture around the model belongs in the commercial discussion:

| Research | What was reported | What a buyer should infer |
|---|---|---|
| OpenAI, July 2026 benchmark audit | Estimated roughly 30% of SWE-Bench Pro tasks were broken; withdrew its earlier recommendation to adopt the benchmark | Audit acceptance tests before turning their scores into procurement criteria |
| Cognition, July 2026 SWE-1.7 release | Reported 42.3% on FrontierCode 1.1 Main, versus 30.1% for its Kimi K2.7 Code base in the same published table | Specialized post-training can materially change task performance; this is a vendor comparison, not a customer SLA |
| UIUC and Bridgewater AIA Labs researchers collaborating with Thinking Machines, August 2026 | Reported specialized SQL performance exceeding a cited 92.96% human proxy with 16-sample selection, at $0.56 per task | Domain expertise and verification can alter the cost-quality frontier; the sampling budget and evaluation population matter |

Sources: [OpenAI audit](https://openai.com/index/separating-signal-from-noise-coding-evaluations/), [Cognition SWE-1.7](https://cognition.com/blog/swe-1-7), [Thinking Machines collaboration](https://thinkingmachines.ai/news/putting-task-expertise-into-rl/). These are authors' reported findings, not a common evaluation performed for this article. The rows cannot be ranked against one another.

The SQL result deserves a closer look. ReViSQL-K2.6 uses reinforcement learning with verifiable rewards, expert-cleaned training data, and reward design aimed at specific SQL errors. Its reported evaluation uses Arcwise-Plat-SQL; the cited human reference comes from BIRD. The headline therefore needs that cross-benchmark qualification. Its 16 candidates are grouped by execution results and a query is selected from the largest group. This is not single-attempt accuracy, and matching output on one database does not establish semantic correctness on every possible database. [Methods and evaluation scope](https://thinkingmachines.ai/news/putting-task-expertise-into-rl/)

For an IT company with permission to use domain-specific examples, this suggests a concrete strategy: improve the task specification, training signal, and acceptance process together. Buying more inference is only one way to improve delivery. Building a complicated multi-agent workflow is another option, with its own latency and failure modes. Neither should be the default before measuring a simpler system.

Cognition's training account offers a related lesson. It describes isolated grading, restricted training sandboxes, removal of reference artifacts, and checks against reward hacking. Those details belong to its training setup, not proof that every deployed action is safe. They show why the verifier and environment are engineering work in their own right. [Cognition's training methodology](https://cognition.com/blog/swe-1-7)

The commercial inference is that competition increasingly includes the model, its training, the execution environment, and the verification process. A services firm needs to decide which of those it can improve and which it should buy. A new lab's funding or launch announcement cannot answer that question; a reproducible result on relevant work can help.

## Longer task horizons are not reliability guarantees

A common shortcut is to translate “the model can do hours of work” into “the model can operate unattended for hours.” That is not what a task-horizon evaluation measures.

METR's methodology relates success to the time humans require for benchmark tasks. A 50% horizon describes a fitted success probability, not a safe delegation limit. Its January 2026 limitations note explicitly warns against interpreting that figure as unattended working time and says that estimating 99%+ reliability requires much larger, higher-quality benchmarks. [METR's explanation](https://metr.org/notes/2026-01-22-time-horizon-limitations/)

Even the estimates depend on methodology. In March, METR reported that correcting a modeling mistake reduced recent models' estimated 50% horizons by up to 20%. That does not erase capability progress. It demonstrates why a contract should identify the evaluation version and uncertainty behind a number. [METR's methodology update](https://metr.org/notes/2026-03-20-impact-of-modelling-assumptions-on-time-horizon-results/)

For a maintenance contract, the useful target is narrower: which upgrades can this system complete within budget, with acceptable regressions and intervention, on the repositories the customer actually owns? Longer-horizon capability expands the candidate workload. Evaluation and operational controls determine how much of it you can responsibly sell.

## Define the unit of work before measuring the model

A production agent is a stateful system. It observes a business state, chooses an action, calls a tool, and receives a new observation. An evaluation needs to inspect those state transitions as well as the final response.

Consider a dependency-maintenance service. Its input is a repository revision, an upgrade request, and a policy specifying permitted changes. Its output is a particular patch and deployment, not the sentence “upgrade completed.” Acceptance might require compatibility tests, security checks, approved rollout results, and no attributable regression during an agreed observation window.

For eligible task `i`, define a binary acceptance indicator:

```text
A_i = functional requirements satisfied
      AND required policy constraints satisfied
      AND delivery deadline satisfied
      AND observation window complete without a disqualifying defect
```

An independent acceptance process supplies these labels. The agent cannot award itself a billable completion. A task still inside its observation window is pending, not a confirmed success. For reporting, use cohorts whose deadlines and observation windows have elapsed; keep timed-out, abandoned, and rejected tasks in the denominator.

Then separate four quantities:

| Metric | Definition on the same matured cohort |
|---|---|
| Eligibility coverage | Eligible arrivals / all arrivals |
| Service completion rate | Accepted outcomes / eligible arrivals |
| Autonomous completion rate | Accepted outcomes with no human intervention / eligible arrivals |
| Escaped-defect rate | Provisionally released outcomes later adjudicated defective / provisionally released outcomes |

A provider could have a high completion rate because humans rescue difficult cases. That may be a good service, but its staffing and cost cannot be inferred from the autonomous agent's score. A provider covering only an easy subset should report that restriction next to its success rate.

## You cannot put a supervisor behind every decision

Having an engineer watch an agent is useful during development and for sensitive operations. Making that the default for every action can erase the economics of automation.

Consider a hypothetical service processing one million cases a month. If 5% require ten minutes of human attention, that creates roughly 8,333 hours of monthly work. At 160 hours per person, that is about 52 full-time equivalents before allowing for leave, training, management, or uneven demand.

The number of agents is a poor staffing metric. What matters is the volume of exceptions, the time needed to resolve them, and how sharply they arrive together. A change to one shared API can overwhelm a review queue even when its average monthly workload looks manageable.

The queue also has to be stable. Let `λ` be eligible arrivals per hour, `r` the fraction requiring human handling, `t_h` the mean handling time in hours, and `c` the number of concurrent reviewers. Ignoring additional audit work for this first estimate:

```text
Human utilization ρ = λ × r × t_h / c
```

With 1,000 arrivals per hour, 5% escalation, ten-minute handling, and ten reviewers, utilization is about 83%. If escalation doubles, it becomes about 167%. The backlog grows even though the models and APIs may remain healthy. Keeping utilization below 100% is only a necessary long-run capacity condition; it does not guarantee a waiting-time target. Staffing must account for bursts, handling-time variation, audits, and shift coverage.

A more practical design gives different actions different levels of autonomy. A read-only search can run freely within access controls. A proposed patch can go through automated tests. A production deployment can require a release gate. A destructive operation can require explicit approval or remain outside the agent's permissions entirely.

Human attention then goes toward ambiguous cases, consequential decisions, audits, and improving the controls. A random sample of apparently successful cases still needs review, because the escalation mechanism can miss errors too.

There is a concrete example of layered oversight at much greater scale. Anthropic reports roughly 30,000 concurrent agents on its most-used internal platform in August, with online checks before execution and offline monitoring afterward. Its report separates monitoring coverage, review latency, and escalation. These are self-reported oversight measures; monitoring every action does not establish that every harmful action is detected. [Anthropic's oversight measurements](https://www.anthropic.com/institute/measuring-pace-of-ai-development)

Adding another agent as a reviewer may help, but its mistakes must also be measured. Two agents using similar context can agree on the same false assumption. Agreement becomes useful evidence only when you know what it predicts.

This suggests a viable service offering: operating the workflow with a defined boundary of autonomy, staffed exception handling, and evidence that the controls work.

## Before charging for completion, define what completion means

Outcome pricing becomes much less straightforward when a customer asks for the invoice to be justified.

Does a generated pull request count? A merged one? A deployed one? What happens if the defect appears a week later?

For a support case, does silence mean resolution? What if the customer returns through another channel? For a data migration, does a successful job status count when records have been silently dropped?

Here are examples of acceptance criteria a buyer and supplier could agree on. They are proposed contract units, not claims about any vendor's current performance.

| Service | A result worth paying for | Evidence needed |
|---|---|---|
| Dependency maintenance | An eligible upgrade accepted and deployed within the agreed window | Compatibility checks, security checks, rollout results, and an agreed defect-observation period |
| Customer support | An eligible issue resolved under policy without a related reopening during the agreed window | Account state, action records, policy compliance, and audited resolution labels |
| Data migration | A defined batch reconciled against the source and accepted | Record counts, integrity checks, business invariants, and recoverability |
| Incident operations | An eligible incident restored within the agreed target | User-facing recovery measurements, change records, and recurrence tracking |
| Enterprise search | Answers meeting an agreed evidence and access-control standard on a defined query mix | Task-level evaluation, source checks, permission enforcement, and sampled review |

Each unit needs rules for customer-caused delays, unsupported cases, duplicate requests, retries, and reopened work. Eligibility should be recorded when work enters the system. Otherwise, a provider can make its success rate look excellent by excluding difficult cases after seeing the outcome.

There is already a commercial precedent. Sierra describes pricing against agreed customer-service outcomes, while also acknowledging that some interactions fit consumption-based or blended pricing better. That demonstrates a pricing approach, not independent proof of its reliability. [Sierra, Outcome-based pricing for AI agents](https://sierra.ai/blog/outcome-based-pricing-for-ai-agents)

For many IT services, a sensible starting point could combine an integration fee, a recurring fee for reserved support capacity, and a charge for accepted outcomes. Uncertain discovery work can remain separately priced. Customers still need to understand the total bill and which risks remain theirs.

## Enforce the workflow outside the model

For that dependency-maintenance service, a plausible execution path is:

```text
Intake and eligibility check
  → isolated agent workspace
  → independently controlled acceptance tests
  → authorized release gate
  → limited rollout and observation
  → final acceptance and billing record

A failed check routes to repair, escalation, or rejection.
An uncertain side effect routes to reconciliation before retry.
```

The model can propose changes. The surrounding application controls credentials, permitted tools, spending limits, deployment authority, and durable task state. A prompt saying “do not deploy without approval” is weaker than an executor that rejects deployments without a valid approval tied to the specific artifact.

Retries deserve particular attention. A timeout does not establish that a write failed. If an action succeeded but its response was lost, blindly repeating it can create a duplicate operation. Use idempotency keys where the API supports them, bind the key to the intended operation, and reconcile unknown outcomes against the system of record. AWS's Builders' Library describes this distinction between retrying requests and preserving their intended effect. [AWS, Making retries safe with idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)

Not every effect can be rolled back. A database update may support a compensating transaction; a notification already sent cannot be unsent. The evaluation should distinguish detected failure, contained failure, and successful recovery. Those are different capabilities with different commercial consequences.

## The cheapest agent can produce the most expensive service

Suppose two proposed systems each handle 10,000 incoming cases. The following numbers are entirely hypothetical, chosen to show how fallback costs can change the comparison.

| Cost or result for the same incoming workload | System A | System B |
|---|---:|---:|
| Agent execution, including retries | $2,000 | $8,000 |
| Human fallback and review, at $15 per case | $30,000 for 2,000 cases | $7,500 for 500 cases |
| Allocated infrastructure, integration, and evaluation | $5,000 | $5,000 |
| Separate allowance for subsequent rework and incidents | $10,000 | $2,000 |
| Total service cost | $47,000 | $22,500 |
| Accepted outcomes, including human-assisted completions | 9,500 | 9,900 |
| Cost per accepted outcome | $4.95 | $2.27 |

System A spends less on agents and more on delivering the service. Its failures and rejected work still cost money, even though they do not contribute to the accepted-outcome denominator.

This is the comparison that outcome pricing requires:

**Cost per accepted outcome = all delivery costs, including failed work, divided by accepted outcomes.**

For forecasting, let `q` be the probability of an accepted outcome per eligible arrival, `c_a` the expected automation cost per arrival including retries and machine checks, `r` the human-intervention probability, `c_h` the mean cost conditional on intervention, `ℓ` the expected additional provider loss per arrival, and `F` the fixed delivery cost allocated to a period with `N` eligible arrivals. These cost buckets must not overlap.

```text
Expected delivery cost per eligible arrival = c_a + r × c_h + ℓ + F/N
Break-even price per accepted outcome = (c_a + r × c_h + ℓ + F/N) / q
```

For a target margin `m` on outcome revenue, the corresponding price is the break-even price divided by `(1 − m)`, assuming no separate fees. This is a planning ratio based on expected volumes, not a promise about any particular month's realized margin. When `q = 0`, there is no finite outcome price that makes the service viable.

Measure `c_h` on the cases actually escalated. Their complexity can differ substantially from the average incoming case. Similarly, the fallback model's accuracy must be measured on the routed subset, not borrowed from its overall benchmark score.

The incident allowance is an assumption, not a magic way to make risk predictable. A supplier must test how the economics change when escalation rates rise, fallback cases take longer, or a shared dependency fails. A rare incident can cost far more than an average-case estimate suggests.

There is also a distinction between the provider's cost and the customer's loss. Service credits may compensate a customer for a missed target without covering the full consequence of a bad decision. Both sides need to understand that difference before calling the arrangement a guarantee.

## A benchmark for IT providers should test the service they actually deliver

A shared evaluation protocol could help here, provided it includes a way to challenge its own tests.

SWE-bench evaluates systems on resolving software issues. That gives buyers useful information about a particular kind of technical capability. It does not certify a provider's deployment process, access controls, staffing capacity, or incident response. [SWE-bench](https://www.swebench.com/)

OpenAI's July audit is a warning against treating a benchmark name as a quality seal. It identified overly restrictive tests, missing requirements, inadequate test coverage, and misleading prompts. A supplier can be penalized for a valid implementation or rewarded for an incomplete one. [Audit findings](https://openai.com/index/separating-signal-from-noise-coding-evaluations/)

A procurement benchmark therefore needs a documented appeals process, independent adjudication, and versioned corrections. Preserve the original results when a defective task is discovered; publish the corrected comparison separately and apply changes consistently to every supplier. Keep reference solutions and hidden tests outside the agent's accessible environment. Refresh private cases without quietly changing the contractual acceptance standard.

Other research already moves closer to business workflows. The original τ-bench evaluates tool-using agents against policy constraints and checks the resulting database state. Its design is a useful precedent for looking beyond the agent's final message. Its historical scores should not be treated as measurements of today's systems. [τ-bench paper](https://arxiv.org/abs/2406.12045)

The next step for procurement could be a shared evaluation protocol for complete services, with separate tracks for software maintenance, support, migrations, and operations.

A buyer would compare providers on the same representative workload, with the same acceptance rules, access boundaries, and resource budgets. Each submission would identify the complete delivery configuration: models, prompts, tools, retrieval sources, validators, retry policy, and human assistance.

The report should answer these questions:

| Question | What the evaluation should disclose |
|---|---|
| How much of the workload is covered? | Eligible cases as a share of all arrivals, with exclusions declared in advance |
| How much work succeeds? | Accepted outcomes over all eligible cases, including failures and timeouts |
| How much succeeds autonomously? | Accepted outcomes without human intervention, reported separately |
| What escapes the checks? | Defects, policy violations, and unauthorized actions, broken down by consequence |
| How much human capacity is needed? | Intervention frequency, handling time, and peak queue demand |
| How long does delivery take? | End-to-end latency, including waits, retries, approvals, and recovery |
| What does it cost? | Total cost per accepted outcome under the agreed workload |
| What happens during disruption? | Behavior during timeouts, duplicate events, stale data, and partial outages |

This should produce a profile rather than one universal league table. A supplier that is excellent at low-risk maintenance may be unsuitable for a workflow with irreversible financial consequences.

Public test cases could help providers develop against the protocol. Procurement decisions should also use fresh, private cases from the buyer's environment, with access and retention controls. Keep tuning examples separate from held-out acceptance cases, and lock the criteria before the comparison.

The grading process needs scrutiny too. Where possible, inspect actual state changes and deterministic invariants. Use expert review for ambiguous outcomes. If a model judges quality, calibrate it against independent reviewers and measure its false approvals. The agent being evaluated should not control the acceptance tests or the billing record.

Include cases where retrieved documents contain malicious instructions, access crosses account boundaries, or a tool returns incomplete information. A task can finish successfully while violating a security constraint; those violations need their own acceptance gates.

For the comparison to remain credible, failed and escalated cases must stay in the report. Providers should disclose the assistance they receive and the work they decline. Tests need refreshing, and material changes to the delivery system need reevaluation.

A useful comparison also needs a risk-versus-coverage curve. Suppose a routing policy automatically releases cases only when its decision score exceeds threshold `τ`. On an independently labeled evaluation set, measure:

```text
Coverage(τ) = automatically released cases / eligible cases
Selective risk(τ) = incorrect automatically released cases / automatically released cases
```

If no cases are released, selective risk is undefined, not zero. A provider must show how much work it can automate at the buyer's allowed risk, alongside the resulting human workload, latency, and cost. A model's self-reported confidence is not sufficient evidence that its score is calibrated to these outcomes.

Choose the threshold on a tuning set, freeze it, and report the result on held-out cases. Keep related tasks together when splitting by customer, repository, or incident, so near-duplicates do not leak across the boundary. Show performance by task class and consequence, with uncertainty intervals. A global average can conceal a failing subgroup.

Repeated trials reveal nondeterminism, but they do not turn a small set of tasks into a large independent sample. Compute uncertainty at the appropriate task or cluster level. If a benchmark allows multiple attempts, report their full cost and how the system selects a valid result. Finding one successful candidate among several is useful only when the deployed verifier can identify it without access to the answer key.

The proposed benchmark would help a buyer shortlist firms. A customer-specific pilot would still be needed before making production commitments.

## Passing a benchmark does not establish an SLA

A service-level agreement cannot honestly promise certainty from a finite set of tests. It can define a measurable commitment, the conditions under which it applies, and what happens when the provider misses it.

Google's site reliability guidance offers a useful foundation: define service-level objectives, measure performance against them, and use an error budget to decide when reliability work should take priority over new changes. [Google SRE, Implementing SLOs](https://sre.google/workbook/implementing-slos/)

Agent services need similarly explicit measurements. API availability, correct task completion, harmful side effects, and recovery time should not be compressed into a single “accuracy” number. A service that answers every request but regularly acts on the wrong account is available and unacceptable.

For example, a hypothetical service might target acceptance of 99% of eligible cases within the agreed deadline, measured over a matured monthly cohort. For 10,000 eligible cases, that permits at most 100 missed outcomes under that definition. The target is illustrative; a real one must reflect consequence, customer tolerance, and evidence.

The error-budget policy should specify an operational response: reduce automatic-release coverage, restore a validated configuration, or pause a failing workflow while preserving a staffed fallback. It must not hide failures by redefining eligibility after the event. Track critical policy violations separately; good average completion cannot compensate for an unauthorized action.

Latency also needs an honest denominator. A low p95 among successful tasks can coexist with many timeouts. Report completion-by-deadline across all eligible cases and show latency conditional on completion as a separate distribution. Include tool waits, approval queues, retries, and recovery in elapsed time.

Evidence for rare failures also takes more work than a successful demonstration suggests. If zero failures occur in 3,000 independent, representative trials, the one-sided 95% upper confidence bound on the failure probability is still roughly 0.1%. That is a statistical bound under those assumptions, not proof that production will stay below it. Thousands of near-duplicate tests do not establish coverage of thousands of different failure modes.

Long workflows add another difficulty. Under the simplifying assumption that every step must succeed independently, twenty steps that each succeed 99% of the time produce only about an 82% chance that all twenty succeed. Real workflows can recover, and failures can be correlated, so this is an illustration rather than a production forecast.

A wrong early assumption can affect many later decisions. Conversely, a checkpoint that verifies the actual system state can stop an error from propagating. Both effects are reasons to evaluate the complete workflow and its recovery behavior.

A production pilot should therefore grow in stages: historical replay, shadow operation, restricted live actions, and wider deployment after explicit acceptance gates. Shadow tests cannot fully measure actions they never execute, so the restricted live phase matters. Include peak load, dependency failures, and rollback exercises before promising performance at scale.

Human fallback is part of that system. A target backed by an understaffed escalation queue may hold on an ordinary Tuesday and fail during an outage. Changing the model, permissions, retrieval corpus, or approval policy can change the result enough to require a new evaluation.

## Where IT services companies can still earn their place

If the premise is that agents make all engineering labor unnecessary, incumbents have little reason to exist. That premise overlooks much of what enterprise delivery involves.

Someone still has to resolve ambiguous requirements, integrate with old systems, define acceptable behavior, secure access, coordinate a release, and restore service when a dependency changes. Those responsibilities can become more valuable as automated execution becomes easier to obtain.

Existing providers may have advantages: domain knowledge, customer relationships, integration experience, and established support operations. Those advantages have to show up in better delivery economics and evidence the customer can inspect. Customer data and incident records cannot simply be pooled into a proprietary evaluation asset without permission.

Smaller firms have an opening too. A specialist can choose one narrow workflow, build strong checks around it, and offer a credible service before it can compete for an entire transformation program. Meanwhile, some buyers will bring more work in-house. No pricing redesign guarantees that today's providers keep tomorrow's contracts.

For an IT firm, the practical starting point is one repeatable workflow with a clear acceptance test. Measure the current service, including its human errors and hidden rework. Evaluate an agent-assisted alternative on the same task mix. Price the offer only after counting the exceptions and testing the recovery plan.

For a buyer, the question to put in the next request for proposals is simple:

**What result are you committing to, how will you prove it, and what happens when you fail to deliver?**

An agent can make the work cheaper. A services company earns its place by making the answer to that question credible.

---

The companion [evaluation protocol](TECHNICAL_PROTOCOL.md) defines the task records, holdout design, release gates, and reporting rules behind this proposal.

Research checked September 23, 2026. This article presents an argument and a proposed evaluation approach, not results from a new experiment. All worked examples are hypothetical. Research and drafting prepared with AI assistance.
