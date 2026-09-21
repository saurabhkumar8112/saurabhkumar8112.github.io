"""Synthetic examples. Default mode is entirely offline."""
import argparse
import json
from dataclasses import asdict
from economics import Item, replay, mean_cost, all_steps_correct
from routing import Decision, DecisionError, Policy, recommend

CRITERIA = {
    'billing': 'Invoices, refunds, charges and payment policies',
    'product': 'Product behavior, features and setup instructions',
    'account_change': 'A request to change account data or settings',
    'unknown': 'Missing context or no clear matching collection',
}
# Synthetic demonstration only. These thresholds have not been calibrated.
DEMO_POLICY = Policy(frozenset(CRITERIA), frozenset({'billing', 'product'}),
                     {'billing': 0.90, 'product': 0.90})


def unavailable_fallback(state):
    raise DecisionError('no_fallback_configured')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--live', action='store_true',
                        help='Send one synthetic prompt to Jev; requires TYPESAFE_API_KEY')
    args = parser.parse_args()
    if args.live:
        from jev_http import JevClassifier
        classifier = JevClassifier(CRITERIA, 'Choose the relevant search route.')
        result = recommend('Where is the refund policy for a canceled annual plan?',
                           classifier, unavailable_fallback, DEMO_POLICY)
        print(json.dumps({'mode': 'live_primary_only_demo_policy',
                          'recommendation': asdict(result)}, indent=2))
        return

    print('SYNTHETIC DEMONSTRATION. No model accuracy is measured.')
    for label, decision, fallback in [
        ('accepted', Decision('billing', .97), lambda _: 'product'),
        ('escalated', Decision('billing', .55), lambda _: 'product'),
        ('review_only', Decision('account_change', 1.0), lambda _: 'billing'),
        ('needs_context', Decision('unknown', .99), lambda _: 'billing'),
    ]:
        result = recommend('Synthetic example', lambda _, d=decision: d, fallback, DEMO_POLICY)
        print(label + ': ' + json.dumps(asdict(result)))

    fixtures = [
        Item('synthetic-1', 'billing', 'billing', .97, 'billing', .00008, .002),
        Item('synthetic-2', 'product', 'billing', .55, 'product', .00008, .009),
        Item('synthetic-3', 'product', 'product', .92, 'product', .00008, .001),
        Item('synthetic-4', 'billing', None, None, None, .00008, .012),
    ]
    print('Replay fixture (not a benchmark): ' + json.dumps(replay(fixtures, .90)))
    print('Hypothetical cost per 1,000: ' + str(mean_cost(.08, .20, 6)))
    print('Toy probability, all 20 independent steps correct: ' + str(all_steps_correct(.99, 20)))


if __name__ == '__main__':
    main()
