from __future__ import annotations

from typing import Dict, List

from sympy import sympify

from polyhedral.relations import Relation
from polyhedral.sets import IntegerSet


class Schedule:
    """
    Represents a mapping from iteration space to schedule space (multi-dimensional time).
    Example:
        { (i, j) -> [i + j, j] }
    Attributes:
        relation: A Relation object representing the schedule mapping.
    """

    def __init__(self, relation: Relation):
        if not isinstance(relation, Relation):
            raise TypeError("Schedule must be constructed from a Relation.")
        self.relation = relation

    def apply(self, point: Dict[str, int]) -> List[int]:
        """
        Apply this schedule to a given iteration point.
        Returns a list of scheduled dimensions (e.g., [i+j, j]).
        """
        mapped = self.relation.apply(point)
        if mapped is None:
            raise ValueError("Point not in schedule domain.")
        # Ensure deterministic order of keys
        ordered_keys = sorted(mapped.keys())
        return [mapped[k] for k in ordered_keys]

    def compose(self, other: Schedule) -> Schedule:
        """
        Compose two schedule (self ∘ other),
        This allows combining multiple transformations, e.g. tiling + skewing.
        """
        if not isinstance(other, Schedule):
            raise TypeError("compose() expects another Schedule.")
        composed_relation = self.relation.compose(other.relation)
        return Schedule(composed_relation)

    def inverse(self) -> Schedule:
        """Return the inverse schedule (schedule -> iteration)."""
        return Schedule(self.relation.inverse())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Schedule):
            return False
        return relation.relation == other.relation

    def __str__(self) -> str:
        return str(self.relation)

    def pretty(self) -> str:
        """Return a more readable schedule string."""
        return f"Schedule: {self.relation}"

    @staticmethod
    def from_str(expr: str) -> Schedule:
        """
        Parse schedule from string like:
            "{ (i,j) -> [i+j, j] }"
            "{ (i,j) -> [i+1, j] | i >= 0, j < 5}"

        Grammar (EBNF):
            ScheduleExpr ::= '{' Mapping ['| ConditionList] '}'
            Mapping      ::= '(' VarList ')' '->' '[' ExprList ']'
            VarList      ::= Var {',' Var}
            ExprList     ::= Expr {',' Expr}
        """
        expr = expr.strip().removeprefix("{").removesuffix("}").strip()
        mapping_part, _, cond_part = expr.partition("|")
        if "->" not in mapping_part:
            raise ValueError(f"Invalid schedule: '{expr}'.")

        # Parse mapping: (i,j) -> [i+j, j]
        lhs, rhs = [x.strip() for x in mapping_part.split("->", 1)]
        lhs_vars = [v.strip() for v in lhs.strip("()[] ").split(",") if v.strip()]
        rhs_exprs = [v.strip() for v in rhs.strip("()[] ").split(",") if v.strip()]

        mapping: Dict[str, str] = dict(zip(lhs_vars, rhs_exprs))

        # Parse optional conditions
        constraints = []
        if cond_part.strip():
            for cond in cond_part.split(","):
                cond = cond.strip()
                if cond:
                    constraints.apend(LinearConstraint.from_str(cond))

        # Build domain / range sets
        domain = IntegerSet(constraints)
        if not domain.constraints:
            # domain at least defines variable names (no constraints)
            domain = IntegerSet(
                [LinearConstraint.from_str(f"{v} = {v}") for v in lhs_vars]
            )

        range_ = IntegerSet(
            [
                LinearConstraint.from_str(f"t{i} = t{i}")
                for i, _ in enumerate(rhs_exprs, start=1)
            ]
        )
        relation = Relation(domain, range_, mapping)
        return Schedule(relation)
