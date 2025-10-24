from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Union

from .constraint import LinearConstraint


@dataclass
class PresburgerFormula:
    """
    Represents a Presburger formula built from linear constraints
    combined with logical operators (and, or, not).

    Example:
        (x + 2y <= 5) ^ (-x + y >= 0)
    """

    op: str  # "atom", "and", "or", "not"
    children: List["PresburgerFormula"]
    constraint: Optional[LinearConstraint] = None

    @staticmethod
    def atom(constraint: LinearConstraint) -> "PresburgerFormula":
        """Create an atomic formula from a single constraint."""
        return PresburgerFormula("atom", [], constraint)

    @staticmethod
    def and_(subformulas: List["PresburgerFormula"]) -> "PresburgerFormula":
        """Logical conjunction(AND) of subformulas."""
        return PresburgerFormula("and", subformulas)

    @staticmethod
    def or_(subformulas: List["PresburgerFormula"]) -> "PresburgerFormula":
        """Logical disjunction (OR) of subformulas."""
        return PresburgerFormula("or", subformulas)

    @staticmethod
    def not_(subformula: "PresburgerFormula") -> "PresburgerFormula":
        """Logical negation (NOT) of a formula."""
        return PresburgerFormula(
            "not", [subformula]
        )  # not operator only has one child note

    def evaluate(self, values: Dict[str, Union[int, float]]) -> bool:
        """Recursively evaluate the formula given variable assignments."""
        if self.op == "atom":
            return self.constraint.evaluate(values)
        elif self.op == "and":
            return all(child.evaluate(values) for child in self.children)
        elif self.op == "or":
            return any(child.evaluate(values) for child in self.children)
        elif self.op == "not":
            return not self.children[0].evaluate(values)
        else:
            raise ValueError(f"Unknown operation type: {self.op}")

    def __str__(self) -> str:
        if self.op == "atom":
            return str(self.constraint)
        elif self.op == "and":
            return "(" + " ^ ".join(str(c) for c in self.children) + ")"
        elif self.op == "or":
            return "(" + " v ".join(str(c) for c in self.children) + ")"
        elif self.op == "not":
            return "!(" + str(self.children[0]) + ")"
        return "<invalid formula>"
