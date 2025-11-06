from __future__ import annotations

from typing import Dict, List

from sympy import sympify

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
        result: dict[str, int] = {}
        for k, expr in self.mapping.items():
            try:
                symbolic_expr = sympify(expr)
                value = symbolic_expr.subs(point)
                result[k] = int(value)
            except Exception as e:
                print(f"exception: {e}")
                raise ValueError(f"Invalid mapping expression '{expr}': {e}")
        return result

    def inverse(self) -> "Relation":
        """Return the inverse relation (swap domain and range)."""
        if len(set(self.mapping.values())) != len(self.mapping):
            raise ValueError("Mapping not invertible")
        inverse_map = {v: k for k, v in self.mapping.items()}
        return Relation(self.range, self.domain, inverse_map)

    def compose(self, other: "Relation") -> "Relation":
        """
        Return the composed relations (self ∘ other).
        other: A -> B
        self: B -> C
        result: A -> C
        """
        if not isinstance(other, Relation):
            raise TypeError("compose expects another Relation")

        if not self.domain.is_compatible_with(other.range):
            raise ValueError("Cannot compose: incompatible dimensions")

        subs_map = {k: sympify(v) for k, v in other.mapping.items()}
        composed_mapping: dict[str, str] = {}
        for out_var, expr in self.mapping.items():
            sym_expr = sympify(expr)
            composed_expr = sym_expr.subs(subs_map)
            composed_mapping[out_var] = str(composed_expr)

        return Relation(
            domain=other.domain,  # A
            range_=self.range,  # C
            mapping=composed_mapping,
        )

    @staticmethod
    def from_str(expr: str) -> "Relation":
        """
        Parse a string like:
            "{ (i,j) -> (i+1, j+2) }"
            "{ (i,j) -> (i', j') | i >= 0, j < 10 }"
        """
        # Clean input
        expr = expr.strip().removeprefix("{").removesuffix("}").strip()

        mapping_part, _, cond_part = expr.partition("|")
        if "->" not in mapping_part:
            raise ValueError(f"Invalid relation: {expr}")
        lhs, rhs = [
            x.strip().removeprefix("(").removesuffix(")")
            for x in mapping_part.split("->")
        ]

        lhs_vars = [v.strip() for v in lhs.split(",") if v.strip()]
        rhs_exprs = [str(sympify(v.strip())) for v in rhs.split(",") if v.strip()]

        min_len = min(len(lhs_vars), len(rhs_exprs))
        if min_len == 0:
            raise ValueError("No valid mapping variables found.")

        mapping = dict(zip(lhs_vars[:min_len], rhs_exprs[:min_len]))

        # Simplified - no real constraints parsing
        domain = IntegerSet([])
        range_ = IntegerSet([])
        return Relation(domain, range_, mapping)

    def __eq__(self, other):
        return (
            isinstance(other, Relation)
            and self.domain == other.domain
            and self.range == other.range
            and self.mapping == other.mapping
        )

    def __str__(self) -> str:
        return "{ " + ", ".join(f"{k} -> {v}" for k, v in self.mapping.items()) + " }"
