"""Bounded recommendations, not tool execution or an authorization service."""
from dataclasses import dataclass
from math import isfinite
from types import MappingProxyType
from typing import Callable, Mapping


class DecisionError(Exception):
    """Expected provider or response-contract failure. Do not include raw bodies."""


def probability(value: object) -> bool:
    return (type(value) in (int, float) and isfinite(value)
            and 0 <= value <= 1)


@dataclass(frozen=True)
class Decision:
    choice: str
    confidence: float
    input_tokens: int | None = None


@dataclass(frozen=True)
class Policy:
    choices: frozenset[str]
    automatic_actions: frozenset[str]
    thresholds: Mapping[str, float]

    def __post_init__(self):
        choices = frozenset(self.choices)
        automatic = frozenset(self.automatic_actions)
        thresholds = dict(self.thresholds)
        if ('unknown' not in choices or not all(type(c) is str and c for c in choices)
                or 'unknown' in automatic or not automatic <= choices
                or set(thresholds) != automatic
                or not all(probability(t) for t in thresholds.values())):
            raise ValueError('Invalid policy; every automatic action needs a threshold')
        object.__setattr__(self, 'choices', choices)
        object.__setattr__(self, 'automatic_actions', automatic)
        object.__setattr__(self, 'thresholds', MappingProxyType(thresholds))


@dataclass(frozen=True)
class Recommendation:
    choice: str | None
    disposition: str  # automatic, review, or clarify
    source: str       # primary, fallback, or policy
    reason: str


def finish(choice: str, source: str, policy: Policy) -> Recommendation:
    if choice == 'unknown':
        return Recommendation(None, 'clarify', source, 'more_information_needed')
    if choice not in policy.automatic_actions:
        return Recommendation(choice, 'review', source, 'review_only_action')
    return Recommendation(choice, 'automatic', source, 'within_evaluated_policy')


def recommend(
    state: str,
    primary: Callable[[str], Decision],
    fallback: Callable[[str], str],
    policy: Policy,
) -> Recommendation:
    """Fallback must itself be an evaluated classifier, never an action executor.

    'automatic' means eligible under this routing policy, not permission to
    access data or perform a side effect. Your application still checks both.
    """
    try:
        decision = primary(state)
        if (not isinstance(decision, Decision)
                or type(decision.choice) is not str
                or decision.choice not in policy.choices
                or not probability(decision.confidence)):
            raise DecisionError('invalid_primary_response')
    except DecisionError:
        decision = None

    if decision is not None:
        # An explicit rejection or review-only action never gets promoted by
        # a second model. Confidence cannot override the action policy.
        if (decision.choice == 'unknown'
                or decision.choice not in policy.automatic_actions):
            return finish(decision.choice, 'primary', policy)
        if decision.confidence >= policy.thresholds[decision.choice]:
            return finish(decision.choice, 'primary', policy)

    try:
        choice = fallback(state)
        if type(choice) is not str or choice not in policy.choices:
            raise DecisionError('invalid_fallback_response')
    except DecisionError:
        return Recommendation(None, 'review', 'policy', 'no_usable_model_answer')
    return finish(choice, 'fallback', policy)
