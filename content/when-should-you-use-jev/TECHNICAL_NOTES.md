# Implementation and evaluation notes

These notes support the practical guide. They contain formulas, definitions and a worksheet for a new evaluation, not findings about Jev's accuracy, latency or cost advantage.

## Cost follows actual routes

For a batch of N inputs, let J_i be the complete first-stage model cost on item i, E_i indicate escalation, and F_i be the actual fallback cost for that item. Then:

```text
C_cascade = sum(J_i + E_i × F_i) / N
         = mean(J_i) + P(escalate) × E[F_i | escalate]
```

The second identity does not assume that escalation and fallback cost are independent. It is precisely why substituting an unconditional fallback average is unsafe. Costs must include the attempts actually made, including charged failures and retries. Avoid double-counting reasoning or cached tokens already included in a provider's usage fields.

If O is additional per-input cost for verification, retrieval, recovery or operations, compare C_cascade + O with the appropriate baseline. Costs shared by both designs can cancel only if they really remain unchanged. Human review can dominate both model bills.

For constant planning inputs J, conditional fallback price F > 0, baseline B and overhead O:

```text
Cost break-even escalation fraction = (B - J - O) / F
```

A value below zero means the proposed cascade is already more expensive without escalation. A value above one means no crossing occurs within a 0-to-100% escalation range. Neither case says anything about quality. Annual break-even volume for fixed additional operating cost M and positive per-input saving S is M / S. Do not choose M without a real budget assumption.

The article's fictional per-1,000 prices are B = $4, J = $0.08 and F = $6, with O = 0. The cost crossing is 65.33% escalation. These figures are teaching inputs, not provider prices.

## Classification replay and live execution answer different questions

`code/economics.py` selects the recorded primary or fallback answer on each item. It pays for the primary on every item and the fallback only where selected. A missing final answer is an unresolved failure in the original denominator. Conditional metrics return null when their subset is empty.

The replay assumes you already have independent model responses and actual costs for the same inputs. It does not infer fallback quality from an overall average. It does not reproduce an agent trajectory, changing tool state, queueing, concurrency, cache state or live failure timing.

Replaying alternative agent actions from a single recorded trace can be invalid: a different action changes the state and the future observations. Evaluate the actual alternative policy through complete episodes or a validated environment that can reproduce those transitions.

## Long-horizon arithmetic

Let S_t denote correctness of step t. The chain rule is:

```text
P(S_1 and ... and S_n)
  = P(S_1) × P(S_2 | S_1) × ... × P(S_n | S_1 ... S_(n-1))
```

This identity does not require independence. The article's p^n illustration assumes equal independent per-step correctness probabilities. Treating all-steps-correct as task success additionally assumes every error is fatal and no recovery is possible. A marginal accuracy measured on unrelated classification examples supplies neither those conditional probabilities nor that success definition.

In a real agent, measure terminal task success, serious action errors, interventions, retries, number of steps, total spend and latency. Report cost per success together with completion and failure rates. Zero successes makes that ratio undefined; it is not zero cost.

## Confidence and rejection

Coverage is the fraction accepted by the automated path. Retained risk is its measured error rate. More stringent thresholds may change both the number and composition of retained cases; they do not guarantee monotonic improvement on every finite sample.

Use held-out data to evaluate a selected policy. Confidence calibration, option probabilities, selective risk and task success are different objects. Agreement between two models is not a correctness certificate. Evaluate the fallback on the actual escalated subset, including cases where both models make the same mistake.

For consequential choices, policy can require review regardless of score. `code/routing.py` makes this explicit. It is only a recommendation layer: external authorization, data access, action-specific invariants and side-effect execution belong to the host application. User or document text must not define those permissions.

## An evaluation worksheet

| Decision to record before testing | What to write down |
|---|---|
| Outcome | The label, evidence selection, resolved ticket or complete task that counts as success |
| Consequential errors | Specific mistakes whose cost is too high to average away |
| Baselines | Rules, retrieval/ranking, a small trained classifier, or an LLM where applicable |
| Available evidence | The same intended task information, plus explicit differences in context or output requirements |
| Split unit | Independent users, documents, incidents or full task episodes, as appropriate |
| Frozen configuration | Model versions, taxonomy, prompts, tools, budgets, thresholds and stop conditions |
| Acceptance criteria | Maximum allowed error by action, coverage, reliability, latency and budget constraints |
| Uncertainty | Counts and intervals by segment; sufficient sample size for rare errors |
| Billing | Actual per-item usage, retries, cached inputs, tool/retrieval calls and review time |
| Operations | Model/API failures, fallbacks, review queues, deployment monitoring and rollback limits |

## Case-specific quality measurements

| Application | Measure before calling it cheaper |
|---|---|
| Search/RAG | Candidate recall, ranking metrics at the served cutoff, evidence retained, grounded final answers and access-control correctness |
| Coding | Issue resolution, missed failing tests, regression escape, repair cycles and end-to-end developer waiting time |
| Tool-using agents | Full-task success, erroneous side effects, unnecessary steps, recovery cost and budget exhaustion |
| Support | Queue accuracy, reroutes, resolution time and unauthorized account actions |
| Document extraction | Exact values, field semantics, source-span validity and business-rule violations |
| Moderation | Per-category false positives/negatives, relevant language/domain slices, escalation burden and appeal outcomes |
| Batch classification | Macro and per-label quality, unknown detection, accepted-case audits and drift |

## Implementation boundary

The optional HTTP adapter is documentation-backed and tested with mocked responses. No live provider call was made to validate this guide. It uses `jev-1.13.0`, checks the returned model, limits payload sizes and timeouts, and refuses redirects. It deliberately makes one attempt; a deployment may add bounded retries with a deadline and account for their costs.

The adapter validates the choice, confidence, option probabilities and required usage field. It does not derive confidence or enforce exact equality of serialized probabilities to one. If your application uses the probabilities in arithmetic, define and evaluate a documented precision policy.

The example threshold values and mock answers are synthetic. The offline tests establish software behavior on those cases, not calibration, provider availability or model quality.
