# Validation notes

Checked on 2026-09-21.

- 28 offline Python tests passed. Provider transport is mocked; no paid model calls were made.
- The offline demonstration completed with synthetic inputs and clearly labeled illustrative thresholds.
- The article HTML was inspected in the in-app browser. The desktop layout fits the viewport, and the copy button reports a successful plain-text copy.
- The calculator displayed $1.28 and 68% lower cost at 20% fallback, then $4.28 and 7% higher cost at 70% fallback. Its separate 99%-per-step, 20-step thought experiment displayed 81.8%.
- The cover and four body figures were visually inspected. All numerical charts state their hypothetical inputs and limitations.
- Internal Markdown links resolve.
- Gitleaks found no secrets in the publication folder. Available local study credentials were also compared directly against packaged files without printing their values; no matches were found. No private absolute workspace paths were found.

These checks validate the examples and packaging. They do not validate Jev accuracy, calibrate thresholds, demonstrate production reliability, or verify the optional live API adapter against a current provider response. No earlier study results or customer data are included.
