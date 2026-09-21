"""Optional live adapter. Standard library only; no API calls on import."""
import json
import os
import urllib.error
import urllib.request
from math import isfinite
from routing import Decision, DecisionError, probability

MODEL = 'jev-1.13.0'
ENDPOINT = 'https://api.typesafe.ai/v1/systemone'
MAX_REQUEST_BYTES = 256_000  # Application budget, not the provider's limit.
MAX_RESPONSE_BYTES = 2_000_000


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # Never forward the Authorization header to a redirected endpoint.
        raise DecisionError('provider_redirect_refused')


def parse_response(body: bytes, criteria: dict[str, str]) -> Decision:
    try:
        result = json.loads(body)
        if not isinstance(result, dict) or result.get('model') != MODEL:
            raise DecisionError('unexpected_model')
        answer = result['answers']['route']
        probabilities = answer['probabilities']
        if (answer['type'] != 'choice'
                or type(answer['choice']) is not str
                or answer['choice'] not in criteria
                or not probability(answer['confidence'])
                or not isinstance(probabilities, dict)
                or set(probabilities) != set(criteria)
                or not all(probability(p) for p in probabilities.values())
                or sum(probabilities.values()) == 0):
            raise DecisionError('invalid_choice_response')
        usage = result['usage']['input_tokens']
        if type(usage) is not int or usage < 0:
            raise DecisionError('invalid_usage')
        # Policy uses the returned confidence. It neither derives confidence
        # from these probabilities nor changes their serialized rounding.
        return Decision(answer['choice'], answer['confidence'], usage)
    except (KeyError, TypeError, ValueError, UnicodeDecodeError):
        raise DecisionError('invalid_response_contract') from None


class JevClassifier:
    def __init__(self, criteria: dict[str, str], instructions: str, timeout=10.0):
        if (not isinstance(criteria, dict) or not 2 <= len(criteria) <= 255
                or 'unknown' not in criteria
                or not all(type(k) is str and k and type(v) is str and v
                           for k, v in criteria.items())):
            raise ValueError('Provide 2 to 255 described options, including unknown')
        if not isinstance(instructions, str) or not instructions:
            raise ValueError('Instructions are required')
        if type(timeout) not in (int, float) or not isfinite(timeout) or timeout <= 0:
            raise ValueError('Timeout must be finite and positive')
        self.criteria = dict(criteria)
        self.instructions = instructions
        self.timeout = timeout
        self.opener = urllib.request.build_opener(NoRedirect())

    def __call__(self, state: str) -> Decision:
        if not isinstance(state, str) or not state:
            raise ValueError('State must be a nonempty string')
        key = os.environ.get('TYPESAFE_API_KEY', '')
        if not key:
            raise DecisionError('missing_api_key')
        payload = {'model': MODEL, 'state': state, 'questions': {'route': {
            'type': 'choice', 'instructions': self.instructions,
            'criteria': self.criteria,
        }}}
        encoded = json.dumps(payload, ensure_ascii=False, allow_nan=False).encode()
        if len(encoded) > MAX_REQUEST_BYTES:
            raise DecisionError('request_exceeds_application_budget')
        request = urllib.request.Request(ENDPOINT, data=encoded, method='POST',
            headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'})
        try:
            with self.opener.open(request, timeout=self.timeout) as response:
                if response.status != 200:
                    raise DecisionError('provider_request_failed')
                body = response.read(MAX_RESPONSE_BYTES + 1)
                if len(body) > MAX_RESPONSE_BYTES:
                    raise DecisionError('response_exceeds_application_budget')
        except (urllib.error.URLError, TimeoutError, OSError):
            # No request headers, input text or response body in error messages.
            raise DecisionError('provider_unavailable') from None
        return parse_response(body, self.criteria)
