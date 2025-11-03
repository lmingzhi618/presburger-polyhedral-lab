from __future__ import annotations

from typing import Dict, List

from polyhedral.sets import IntegerSet
from presburger.constraint import LinearConstraint


class Relation:
    """
    Represents a binary relation between two integer sets (domain -> range).
    Example:
        (i, j) -> (i + 1, j)
    """

    def __init__(
        self,
        domain: IntegerSet,
        range_: IntegerSet,
        mapping: Dict[str, str] | None = None,
    ):
        self.domain = domain
        self.range = range_
        self.mapping = mapping or {}

    def apply(self, point: Dict[str, int]) -> Dict[str, int] | None:
        """Apply relation maping of point ∈ domain."""
        if not self.domain.contains(point):
            return None
        return {k: eval(expr, {}, point) for k, expr in self.mapping.items()}

    def inverse(self) -> "Relation":
        """Return the inverse relation (swap domain and range)."""
        inverse_map = {v: k for k, v in self.mapping.items()}
        return Relation(self.range, self.domain, inverse_map)

    def __str__(self) -> str:
        mapping_str = ", ".join(f"{k} -> {v}" for k, v in self.mapping.items())
        return (
            f"Relation(domain={self.domain}, range={self.range}, map={{mapping_str}})"
        )
