"""
polyhedral/sets.py

Implements the concept of Sets of Named Integer Tuples (Chapter 2 of
'Presburger Formula and Polyhedral Compilation').

This module defines the IntegerSet class, which models integer points
satisfying a set of linear constraints (Presburger constraints).
"""

from __future__ import annotations

from typing import Dict, List

from presburger.constraint import LinearConstraint
from presburger.formula import PresburgerFormula


class IntegerSet:
    """
    Represents a set of named integer tuples, defined by a conjunction
    of linear constraints over integer variables.

    Example:
        S = IntegerSet([
            LinearConstraint.from_str("0 <= i <= 4"),
            LinearConstraint.from_str("0 <= j <= 4")
        ])
        s.contains({"i": 2, "j": 3})  # True
    """

    def __init__(
        self,
        constraints: List[LinearConstraint] | None = None,
        subsets: List["IntegerSet"] | None = None,
    ):
        self.constraints: List[LinearConstraint] = []
        self.subsets: List["IntegerSet"] = subsets or []

        if constraints:
            for c in constraints:
                if isinstance(c, list):
                    # Flatten chainned constraints like [LinearConstraint, LinearConstraint]
                    self.constraints.extend(c)
                else:
                    self.constraints.append(c)

    def contains(self, values: Dict[str, int]) -> bool:
        if self.subsets:
            return any(s.contains(values) for s in self.subsets)
        return all(c.evaluate(values) for c in self.constraints)

    def intersection(self, other: IntegerSet) -> IntegerSet:
        """Return a new IntegerSet representing the intersection of two sets."""
        return IntegerSet(constraints=self.constraints + other.constraints)

    def union(self, other: IntegerSet) -> IntegerSet:
        return IntegerSet(subsets=[self, other])

    def is_empty(self) -> bool:
        """
        Check whether the set could be empty.
        (Simple version: just detects direct contradictions like x <= 1 and x >= 2)
        """
        # This is a heuristic placeholder - in a full system, we'd use a solver
        vars_involved = {}
        for c in self.constraints:
            for v, coeff in c.coefficients.items():
                vars_involved.setdefault(v, []).append((coeff, c.constant, c.relation))

        # Simple consistency check: detect impossible bounds
        for v, bounds in vars_involved.items():
            lowers = [c for c in bounds if c[2] in (">=", ">")]
            uppers = [c for c in bounds if c[2] in ("<=", "<")]

            if lowers and uppers:
                max_lower = max(c[1] for c in lowers)
                min_upper = min(c[1] for c in uppers)
                if max_lower > min_upper:
                    return True
        return False

    def __str__(self) -> str:
        if self.subsets:
            return " u ".join([str(s) for s in self.subsets])
        joined = " ∧ ".join(str(c) for c in self.constraints)
        return f"{{ {joined} }}"

    @staticmethod
    def from_formula(formula: PresburgerFormula) -> IntegerSet:
        """
        Build an IntegerSet from a PresburgerFormula
        - atom(constraint)  -> a single-conjunct set
        - and(children)     -> intersection; if any child is a union, distribute
        - or(children)      -> union (flattened)
        """
        if formula.op == "atom":
            if getattr(formula, "constraint", None) is None:
                return IntegerSet([])
            return IntegerSet([formula.constraint])

        if formula.op == "or":
            subsets: list[IntegerSet] = []
            for ch in formula.children or []:
                s = IntegerSet.from_formula(ch)
                if s.subsets:
                    subsets.extend(s.subsets)
                else:
                    subsets.append(s)
            return IntegerSet(subsets=subsets)

        if formula.op == "and":
            parts: list[IntegerSet] = [
                IntegerSet.from_formula(ch) for ch in (formula.children or [])
            ]
            return IntegerSet._and_distribute(parts)

        return IntegerSet([])

    @staticmethod
    def _intersect_two(a: "IntegerSet", b: "IntegerSet") -> "IntegerSet":
        if not a.subsets and not b.subsets:
            return IntegerSet(a.constraints + b.constraints)

        # A∩(B1∪B2)=(A∩B1)∪(A∩B2)
        a_opts = a.subsets if a.subsets else [a]
        b_opts = b.subsets if b.subsets else [b]
        out_subsets: list[IntegerSet] = []
        for sa in a_opts:
            for sb in b_opts:
                out_subsets.append(IntegerSet(sa.constraints + sb.constraints))
        return IntegerSet(subsets=out_subsets)

    @staticmethod
    def _and_distribute(sets: list["IntegerSet"]) -> "IntegerSet":
        if not sets:
            return IntegerSet([])
        acc = sets[0]
        for s in sets[1:]:
            acc = IntegerSet._intersect_two(acc, s)
        return acc
