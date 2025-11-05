from __future__ import annotations

from typing import Dict, List

from sympy import simpify

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

        result = {}
        for k, expr in self.mapping.items():
            try:
                symbolic_expr = sympify(expr)
                value = symbolic_expr.subs(point)
                result[k] = int(value)
            except Exception as e:
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
        if self.domain != other.range:
            raise ValueError("Cannot compose: range/domain mismatch")

        subs_map = {var: sympify(e) for var, e in other.mapping.items()}
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

        # Split mapping and condition
        mapping_part, _, cond_part = expr.partition("|")
        # Split LHS -> RHS
        if "->" not in mapping_part:
            raise ValueError(f"Invalid relation: {expr}")
        lhs, rhs = [x.strip() for x in mapping_part.split("->")]

        # Remove parentheses
        lhs = lhs.removeprefix("(").removesuffix(")")
        rhs = rhs.removeprefix("(").removesuffix(")")

        lhs_vars = [v.strip() for v in lhs.split(",") if v.strip()]
        rhs_exprs = [v.strip() for v in rhs.split(",") if v.strip()]

        mapping = {
            lhs_vars[i]: rhs_exprs[i] for i in range(min(len(lhs_vars), len(rhs_exprs)))
        }

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
