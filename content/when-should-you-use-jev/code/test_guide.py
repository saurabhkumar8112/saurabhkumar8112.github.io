"""Offline tests of control flow, API failure handling and accounting."""
import json
import os
import unittest
import urllib.error
from unittest.mock import patch, Mock
from routing import Decision, DecisionError, Policy, recommend
from jev_http import JevClassifier, NoRedirect, MODEL, MAX_RESPONSE_BYTES, parse_response
from economics import Item, replay, mean_cost, all_steps_correct

CRITERIA = {'search': 'Read-only search', 'write': 'A consequential write', 'unknown': 'Insufficient context'}
POLICY = Policy(frozenset(CRITERIA), frozenset({'search'}), {'search': .90})


def response():
    return {'model': MODEL, 'answers': {'route': {'type': 'choice', 'choice': 'search',
            'confidence': .95, 'probabilities': {'search': .95, 'write': .03, 'unknown': .02}}},
            'usage': {'input_tokens': 123}}


class RoutingTests(unittest.TestCase):
    def test_high_confidence_avoids_fallback(self):
        fallback = Mock(return_value='write')
        result = recommend('x', lambda _: Decision('search', .9), fallback, POLICY)
        self.assertEqual((result.source, result.disposition), ('primary', 'automatic'))
        fallback.assert_not_called()

    def test_low_confidence_uses_fallback(self):
        result = recommend('x', lambda _: Decision('search', .89), lambda _: 'search', POLICY)
        self.assertEqual(result.source, 'fallback')

    def test_review_action_cannot_be_promoted(self):
        fallback = Mock(return_value='search')
        result = recommend('x', lambda _: Decision('write', 1.0), fallback, POLICY)
        self.assertEqual(result.disposition, 'review')
        fallback.assert_not_called()

    def test_fallback_cannot_bypass_review(self):
        result = recommend('x', lambda _: Decision('search', .1), lambda _: 'write', POLICY)
        self.assertEqual((result.source, result.disposition), ('fallback', 'review'))

    def test_unknown_requests_information(self):
        fallback = Mock(return_value='search')
        result = recommend('x', lambda _: Decision('unknown', 1), fallback, POLICY)
        self.assertEqual(result.disposition, 'clarify')
        fallback.assert_not_called()

    def test_malformed_primary_escalates(self):
        for decision in [Decision('unlisted', .99), Decision('search', float('nan')),
                         Decision('search', True), Decision('search', -1), {'choice': 'search'}]:
            with self.subTest(decision=decision):
                result = recommend('x', lambda _: decision, lambda _: 'search', POLICY)
                self.assertEqual(result.source, 'fallback')

    def test_both_providers_unavailable_requires_review(self):
        def fail(_): raise DecisionError('unavailable')
        self.assertEqual(recommend('x', fail, fail, POLICY).disposition, 'review')

    def test_invalid_fallback_requires_review(self):
        result = recommend('x', lambda _: Decision('search', .1), lambda _: 'invented', POLICY)
        self.assertIsNone(result.choice)
        self.assertEqual(result.disposition, 'review')

    def test_programming_errors_are_not_silenced(self):
        def broken(_): raise RuntimeError('programming bug')
        with self.assertRaises(RuntimeError): recommend('x', broken, lambda _: 'search', POLICY)

    def test_policy_requires_explicit_thresholds(self):
        with self.assertRaises(ValueError): Policy(frozenset(CRITERIA), frozenset({'search'}), {})

    def test_policy_cannot_automate_unknown(self):
        with self.assertRaises(ValueError): Policy(frozenset(CRITERIA), frozenset({'unknown'}), {'unknown': .9})

    def test_policy_copies_caller_configuration(self):
        thresholds = {'search': .9}
        policy = Policy(frozenset(CRITERIA), frozenset({'search'}), thresholds)
        thresholds['search'] = 0
        self.assertEqual(policy.thresholds['search'], .9)


class AdapterTests(unittest.TestCase):
    def test_parses_documented_contract(self):
        self.assertEqual(parse_response(json.dumps(response()).encode(), CRITERIA), Decision('search', .95, 123))

    def test_rejects_wrong_model(self):
        body = response(); body['model'] = 'unexpected-snapshot'
        with self.assertRaises(DecisionError): parse_response(json.dumps(body).encode(), CRITERIA)

    def test_rejects_missing_or_invalid_contract_fields(self):
        variants = [b'not-json', b'null', b'[]', b'{}']
        body = response(); body['answers']['route']['confidence'] = True
        variants.append(json.dumps(body).encode())
        body = response(); body['usage']['input_tokens'] = -1
        variants.append(json.dumps(body).encode())
        body = response(); body['answers']['route']['probabilities']['search'] = float('nan')
        variants.append(json.dumps(body).encode())
        for data in variants:
            with self.subTest(data=data):
                with self.assertRaises(DecisionError): parse_response(data, CRITERIA)

    def test_redirect_is_refused(self):
        with self.assertRaises(DecisionError):
            NoRedirect().redirect_request(None, None, 302, '', {}, 'https://example.invalid')

    def test_missing_key_makes_no_network_call(self):
        client = JevClassifier(CRITERIA, 'Choose.')
        client.opener = Mock()
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(DecisionError): client('x')
        client.opener.open.assert_not_called()

    def test_transport_failure_is_redacted(self):
        client = JevClassifier(CRITERIA, 'Choose.')
        client.opener = Mock()
        client.opener.open.side_effect = urllib.error.URLError('private debug context')
        with patch.dict(os.environ, {'TYPESAFE_API_KEY': 'synthetic-test-value'}):
            with self.assertRaisesRegex(DecisionError, '^provider_unavailable$'): client('x')

    def test_live_request_contract_via_mock(self):
        client = JevClassifier(CRITERIA, 'Choose.')
        handle = Mock(status=200)
        handle.read.return_value = json.dumps(response()).encode()
        context = Mock(); context.__enter__ = Mock(return_value=handle); context.__exit__ = Mock(return_value=False)
        client.opener = Mock(); client.opener.open.return_value = context
        with patch.dict(os.environ, {'TYPESAFE_API_KEY': 'synthetic-test-value'}):
            self.assertEqual(client('synthetic state').choice, 'search')
        request = client.opener.open.call_args.args[0]
        self.assertEqual(request.full_url, 'https://api.typesafe.ai/v1/systemone')
        self.assertEqual(json.loads(request.data)['model'], MODEL)
        handle.read.assert_called_once_with(MAX_RESPONSE_BYTES + 1)

    def test_large_response_is_rejected(self):
        client = JevClassifier(CRITERIA, 'Choose.')
        handle = Mock(status=200); handle.read.return_value = b'x' * (MAX_RESPONSE_BYTES+1)
        context = Mock(); context.__enter__ = Mock(return_value=handle); context.__exit__ = Mock(return_value=False)
        client.opener = Mock(); client.opener.open.return_value = context
        with patch.dict(os.environ, {'TYPESAFE_API_KEY': 'synthetic-test-value'}):
            with self.assertRaisesRegex(DecisionError, 'application_budget'): client('x')


class EconomicsTests(unittest.TestCase):
    def test_per_item_cost_and_failed_case_are_preserved(self):
        items = [Item('1', 'a', 'a', .95, 'a', 1, 10),
                 Item('2', 'b', 'a', .2, 'b', 2, 100),
                 Item('3', 'a', None, None, None, 3, 50)]
        r = replay(items, .9)
        self.assertEqual(r['cascade_api_cost'], 1+2+3+100+50)
        self.assertEqual(r['correct'], 2)
        self.assertEqual(r['n'], 3)
        self.assertEqual(r['unresolved'], 1)
        self.assertEqual(r['selected_fallback_accuracy'], .5)

    def test_equality_is_retained(self):
        r = replay([Item('1', 'a', 'a', .9, 'b', 1, 100)], .9)
        self.assertEqual((r['kept'], r['cascade_api_cost']), (1, 1))

    def test_empty_conditional_subset_is_null(self):
        r = replay([Item('1', 'a', 'b', .1, 'a', 1, 3)], .9)
        self.assertIsNone(r['retained_error_rate'])

    def test_duplicates_rejected(self):
        row = Item('1', 'a', 'a', .9, 'a', 1, 1)
        with self.assertRaises(ValueError): replay([row, row], .9)

    def test_nonfinite_or_negative_cost_rejected(self):
        for value in [float('nan'), float('inf'), -1, True]:
            with self.assertRaises(ValueError): mean_cost(value, .2, 6)

    def test_article_planning_examples(self):
        for fraction, expected in [(.2, 1.28), (.6, 3.68), (.7, 4.28)]:
            self.assertAlmostEqual(mean_cost(.08, fraction, 6), expected)

    def test_extra_cost_is_per_incoming_request(self):
        self.assertAlmostEqual(mean_cost(.08, .2, 6, .5), 1.78)

    def test_horizon_assumption_math(self):
        self.assertAlmostEqual(all_steps_correct(.99, 20), .8179069376)
        self.assertEqual(all_steps_correct(1, 20), 1)
        self.assertEqual(all_steps_correct(0, 20), 0)
        with self.assertRaises(ValueError): all_steps_correct(.99, True)


if __name__ == '__main__':
    unittest.main()
