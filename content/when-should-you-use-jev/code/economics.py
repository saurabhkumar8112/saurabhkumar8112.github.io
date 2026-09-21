"""Hypothetical planning arithmetic and per-item classification replay."""
from dataclasses import dataclass
from math import isfinite
from routing import probability


def nonnegative(value: object) -> bool:
    return type(value) in (int, float) and isfinite(value) and value >= 0


def mean_cost(primary_cost: float, fallback_fraction: float,
              selected_fallback_cost: float, extra_cost: float = 0) -> float:
    """All prices must use the same units; extra_cost is per incoming request."""
    if (not all(nonnegative(v) for v in (primary_cost, selected_fallback_cost, extra_cost))
            or not probability(fallback_fraction)):
        raise ValueError('Costs must be finite/nonnegative and fraction in [0, 1]')
    return primary_cost + fallback_fraction * selected_fallback_cost + extra_cost


def all_steps_correct(step_probability: float, steps: int) -> float:
    """Toy assumption: independent equal-probability steps, every error fatal,
    no recovery. Not a forecast of an agent's completion probability.
    """
    if not probability(step_probability) or type(steps) is not int or steps < 1:
        raise ValueError('Provide a probability and a positive integer step count')
    return step_probability ** steps


@dataclass(frozen=True)
class Item:
    item_id: str
    gold: str
    primary_choice: str | None
    confidence: float | None
    fallback_choice: str | None
    primary_cost: float
    fallback_cost: float


def replay(items: list[Item], threshold: float) -> dict:
    """Replay a single-label classification rule on separately collected calls.

    Both models' actual billed costs must be recorded per item, including any
    failed attempts. Missing answers count as failures, not dropped examples.
    This is not an evaluation of the action policy in routing.py or live latency.
    """
    if not items or not probability(threshold):
        raise ValueError('Provide nonempty items and a threshold in [0, 1]')
    seen = set()
    kept = escalated = correct = retained_wrong = fallback_correct = 0
    total_cost = baseline_cost = 0.0
    unresolved = baseline_correct = 0
    for item in items:
        if (not item.item_id or item.item_id in seen or not item.gold
                or type(item.item_id) is not str or type(item.gold) is not str
                or any(value is not None and (type(value) is not str or not value)
                       for value in (item.primary_choice, item.fallback_choice))
                or not all(nonnegative(c) for c in (item.primary_cost, item.fallback_cost))
                or (item.confidence is not None and not probability(item.confidence))):
            raise ValueError('Invalid or duplicate evaluation item')
        seen.add(item.item_id)
        use_fallback = (item.primary_choice is None or item.confidence is None
                        or item.confidence < threshold)
        total_cost += item.primary_cost
        baseline_cost += item.fallback_cost
        baseline_correct += item.fallback_choice == item.gold
        if use_fallback:
            escalated += 1
            choice = item.fallback_choice
            total_cost += item.fallback_cost
            fallback_correct += choice == item.gold
        else:
            kept += 1
            choice = item.primary_choice
            retained_wrong += choice != item.gold
        correct += choice == item.gold
        unresolved += choice is None
    n = len(items)
    return {
        'n': n, 'correct': correct, 'accuracy': correct/n,
        'kept': kept, 'escalated': escalated, 'coverage': kept/n,
        'retained_error_rate': retained_wrong/kept if kept else None,
        'selected_fallback_accuracy': fallback_correct/escalated if escalated else None,
        'unresolved': unresolved, 'cascade_api_cost': total_cost,
        'baseline_correct': baseline_correct, 'baseline_api_cost': baseline_cost,
    }
