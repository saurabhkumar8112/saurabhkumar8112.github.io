# Evaluating an agent-operated IT service

Companion to [When AI Does the Work, What Will Infosys and TCS Sell?](ARTICLE.md). This is a proposed protocol, not a certification standard or a completed experiment. Example field names are illustrative. No provider APIs or production systems were exercised.

## 1. Specify the claim before collecting results

Define a workflow, customer population, task mix, delivery deadline, observation period, allowed actions, and human-support policy. Record eligibility at intake using rules independent of the eventual result. A request declined after admission remains an eligible unsuccessful task unless a predeclared rule legitimately assigns a different disposition.

Keep three questions separate:

- **Capability:** can the proposed agent perform the task in a controlled environment?
- **Service performance:** can the complete system, including humans, meet the acceptance criteria under the intended workload?
- **Economics:** can it do so at the offered price after accounting for unsuccessful work and recovery?

Register thresholds, reporting slices, statistical methods, resource limits, and stop conditions before the held-out evaluation. These thresholds belong to this proposed service evaluation; they do not modify the earlier Jev study.

## 2. Record the entire delivery configuration

Version the model and decoding settings, orchestration code, prompts, tool schemas, retrieval snapshot, policy, grader, deployment gate, and retry strategy. Include human access and intervention rules. Pin dependencies and record provider-returned model identifiers when available. Disclose any component that cannot be reproduced exactly.

Run competing services against equivalent environments and the same task cohort. Reset mutable state between independent trials. Declare limits for elapsed time, attempts, tokens, tools, and human minutes. Report both autonomous and assisted tracks; do not silently combine them.

An illustrative task record:

```json
{
  "task_id": "synthetic-upgrade-001",
  "cluster_id": "synthetic-repository-a",
  "eligible_at_intake": true,
  "task_class": "dependency_upgrade",
  "risk_class": "reversible_with_release_gate",
  "configuration_id": "candidate-v1",
  "acceptance_policy_version": "policy-v1",
  "attempt_count": 2,
  "human_intervention": true,
  "human_minutes": 12,
  "final_disposition": "pending_observation",
  "acceptance_label": null,
  "observation_complete": false,
  "evidence_record_id": "synthetic-evidence-001"
}
```

`null` means unknown or pending, not failure or success. Add durable timestamps, tool outcomes, provider usage, attributed cost records, and approval records in the actual implementation. Keep private content in controlled storage; public reports should contain authorized, redacted evidence and aggregates. Billing and acceptance records should be auditable and inaccessible to agent modification.

## 3. Separate development from acceptance testing

Use development cases for implementation, a tuning set for thresholds and policies, and a held-out set for final comparison. Split related cases together by repository, customer, incident family, or other relevant dependence unit. Use a later time period as an additional check on temporal generalization where appropriate.

Stratify by task class, difficulty, consequence, and dependency conditions. Publish the distribution and the relationship to expected production traffic. A stress-test suite deliberately oversampling rare attacks is useful, but its raw failure rate is not a production prevalence estimate.

Run multiple trials per task to expose variability. Keep all attempts and errors. For a provider comparison, use paired tasks and a cluster-aware interval for the difference. A bootstrap must resample the independent units while preserving trial and provider pairing. If independence assumptions are doubtful or the number of clusters is small, report that limitation rather than treating every tool call as a new sample.

## 4. Validate the verifier

Use independently controlled requirements and state assertions. Keep the acceptance grader outside the agent's writable workspace. Tests can be incomplete, so audit accepted and rejected outcomes against expert adjudication.

Two distinct error rates matter:

```text
Verifier false-approval rate = approved bad outcomes / all adjudicated bad outcomes
Defect rate among approvals = bad approved outcomes / all adjudicated approved outcomes
```

These have different denominators. A balanced test set for verifier capability does not directly estimate the defect rate under production prevalence. When auditing a stratified sample of live approvals, retain sampling probabilities and weight estimates appropriately. Unreviewed cases are not automatically correct.

For subjective labels, define the rubric, measure reviewer disagreement, and adjudicate disputes. A second model can contribute evidence but does not automatically supply independent ground truth.

### Benchmark integrity and appeals

Check prompts, reference solutions, and tests for consistency before freezing a benchmark. Independently adjudicate disputed failures and apparent successes. Preserve original results; issue versioned corrections applied uniformly across providers rather than silently dropping inconvenient tasks.

Record task provenance, publication dates, known training overlap, and access to reference artifacts. Near-duplicate detection and recent private cases reduce some contamination risks but do not prove absence of contamination. Isolate hidden graders and reference solutions from agent tools, retrieval, repository history, and logs.

Disclose candidate count and the deployed selection method. Oracle pass-at-k, where any successful attempt counts using answer-key knowledge, must not be reported as the deployed selector's completion rate. Charge every attempt and measure selection errors. Changes to tasks or graders require a new evaluation identifier and an explanation of comparability.

For monitoring, report action coverage, detection performance on labeled incidents, time to containment, review latency, and human escalation separately. A low block rate does not establish a low underlying violation rate.

## 5. Report outcome and cost at the task level

Use matured cohorts with completed deadlines and observation windows. Report pending cohorts separately. Link reopened cases to the original task and apply a declared acceptance-reversal or credit policy. Track late defects beyond the contractual window separately so the window does not conceal long-term quality.

For each eligible task, retain automation cost, conditional human cost, and subsequent rework cost, including failed tasks. Sum task costs before dividing by accepted outcomes. Allocate fixed costs transparently and distinguish measured costs from forecast loss allowances. Do not multiply an escalation count by a global average handling cost or fallback accuracy.

Report eligibility coverage, service completion, autonomous completion, intervention, escaped defects, critical violations, completion-by-deadline, latency distributions, and total cost per accepted outcome. Include sample counts and uncertainty. Show subgroup results and the risk-coverage-cost trade-off, not just the best threshold on the test set.

## 6. Exercise the failure paths

Test lost acknowledgements, duplicate requests, partial writes, stale reads, rate limits, unavailable dependencies, policy changes, malicious retrieved content, and attempts to cross tenant boundaries. Use isolated authorized environments and synthetic or appropriately protected data.

A retry is another attempt at the same business operation. Its identity must persist through restarts. Check the system of record before repeating an action with an unknown outcome. Measure compensation and recovery separately from initial success. Some side effects are irreversible and need stronger authorization before execution.

Evaluate the human queue under bursty arrivals and correlated incidents. Include audit load and nonproductive time. Stability at average load does not establish p95 or p99 waiting time; use workload traces and load tests to assess those targets.

## 7. Connect evidence to a release decision

Use staged deployment: replay, shadow, restricted live operation, then expansion. Define critical-violation stop conditions, error-budget actions, fallback capacity, rollback ownership, and incident response before the pilot. Shadow operation cannot establish the consequences of writes it never makes.

A release decision should identify the configuration, workload scope, evidence interval, measured uncertainty, unresolved failure modes, and owner accepting residual risk. Material changes trigger reevaluation. Periodic sampling of production outcomes checks whether task mix, calibration, human workload, or costs have drifted.

An SLA adds contractual measurement rules, exclusions, remedies, and obligations to operational targets. Its enforceability and commercial terms require appropriate review. This protocol supplies engineering evidence; it cannot guarantee zero failures or determine acceptable risk for every customer.

## References

- [Anthropic: Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- [Google SRE: Implementing SLOs](https://sre.google/workbook/implementing-slos/)
- [AWS Builders' Library: Making retries safe with idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)
- [τ-bench](https://arxiv.org/abs/2406.12045)

The evaluation design, record example, commercial metrics, and release protocol above are proposals developed for this article. The references supply relevant background, not endorsement of this protocol.
