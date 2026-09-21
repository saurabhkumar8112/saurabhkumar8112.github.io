# Runnable companion

Python 3.10 or newer. The runtime examples and tests use only the standard library.

## Offline demo

```bash
python3 code/demo.py
python3 -m unittest discover -s code -p 'test_*.py' -v
```

The demo uses synthetic decisions and prices. Its numbers are not Jev measurements. It illustrates acceptance, fallback, clarification, review-only actions, per-item billing and a failed case that remains in the denominator.

## Files

- [routing.py](routing.py): immutable per-action policy, confidence gating, typed recommendations and fallback validation.
- [jev_http.py](jev_http.py): optional HTTP adapter with a pinned model, contract checks, time and payload bounds, and no redirects or automatic retries.
- [economics.py](economics.py): conditional fallback-cost arithmetic, classification replay and explicitly hypothetical horizon arithmetic.
- [demo.py](demo.py): offline fixtures and an explicit opt-in live mode.
- [test_guide.py](test_guide.py): offline behavior tests. All HTTP is mocked.

## Optional live request

With `TYPESAFE_API_KEY` already available in the process environment, `python3 code/demo.py --live` sends one hard-coded synthetic search-routing question to the official TypeSafe endpoint. This incurs an API charge. It never reads a local environment file and does not send private workspace files. No live request was run when validating this guide.

Live mode has no stronger-model integration. When fallback is needed, it returns review. The offline fallback is a fixed fixture, not a call to another LLM. To build a real cascade, supply your own evaluated fallback classifier returning one of the allowed labels, and report its selected-subset quality and actual cost.

`automatic` means eligible for the configured recommendation route. It does not authorize an external action. No included code executes tools or writes to an account. Even the fallback cannot promote a review-only action to automatic execution.

The example thresholds are synthetic. They are not calibrated production defaults. Keep permissions, trusted configuration, idempotency, action-specific validators, total task budgets and human approval rules in the host application. Catch `DecisionError` for expected provider failures; programming errors are intentionally not silently swallowed.

The adapter suppresses provider error bodies and does not log input text, credentials or headers. Instrument production usage and failures through an appropriately redacted, access-controlled logging path rather than printing raw requests.
