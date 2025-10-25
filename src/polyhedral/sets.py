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
        joined = ", ".join(str(c) for c in self.constraints)
        vars_str = sorted({v for c in self.constraints for v in c.coefficients.keys()})
        return f"{{ ({', '.join(vars_str)}) | {joined} }}"

    @staticmethod
    def from_formula(formula: PresburgerFormula) -> IntegerSet:
        """
        Convert a formula into a IntegerSet if it's a conjunction of constraints.
        For disjunctions, split branches (union of sets).
        """
        constraints: List[LinearConstraint] = []
        if formula.op == "and":
            for child in formula.children:
                if child.op == "atom" and child.constraint is not None:
                    constraints.append(child.constraint)
        elif formula.op == "or":
            # Simplified: return first branch for prototype
            if isinstance(formula.children[0], PresburgerFormula):
                return IntegerSet.from_formula(formula.children[0])
        return IntegerSet(constraints)
