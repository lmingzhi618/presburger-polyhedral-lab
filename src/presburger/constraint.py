# constraint.py
from dataclasses import dataclass
from typing import Dict
import re


@dataclass
class LinearConstraint:
    coefficients: Dict[str, int]    # variables and coefficients, e.g. {"x": 1, "y": 2}
    constant: int                   # constant b
    relation: str                   # "<=", "<", ">=", "=", "!="

    def evaluate(self, values: Dict[str, int]) -> bool:
        """Check if the constraint holds for given variable assignments."""
        lhs = sum(v * values.get(k, 0) for k, v in self.coefficients.items())
        if self.relation == "<=":
            return lhs <= self.constant 
        elif self.relation == "<":
            return lhs < self.constant
        elif self.relation == ">=":
            return lhs >= self.constant 
        elif self.relation == "=":
            return lhs == self.constant
        elif self.relation == "!=":
            return lhs != self.constant 
        else:
            raise ValueError(f"Unsupported relation {self.relation}")

    @staticmethod
    def from_str(expr: str) -> "LinearConstraint":
        """
        Parse a simple linear constraint string such as:
            "x + 2y <= 5"
            "3x - y = 7"
            "-x + 4z >= 10"
        Supported relations: <=, >=, =, !=, <, >
        Variables must be simple identifiers (letters, numbers, underscors).
        Coefficients default to 1 or -1 if omitted.
        """
        # Normalize whitespace
        expr = expr.strip().replace(" ", "")

        # Find the relational operator
        match = re.search(r"(<=|>=|!=|=|<|>)", expr)
        if not match:
            raise ValueError(f"No valid relational operator found in '{expr}'")
        relation = match.group(1)

        lhs, rhs = expr.split(relation)
        try:
            constant = int(rhs)
        except ValueError:
            raise ValueError(f"Right-hand side must be an integer: '{rhs}'")

        # Extract terms fro mlhs (like 3x, -y, +2z)
        # Regex: optional sign, optional digits, then variable name
        term_pattern = re.compile(r"([+-]?)(\d*)([A-Za-z_]\w*)")
        coefficients: Dict[str, int] = {}

        for sign, num, var in term_pattern.findall(lhs):
            coeff = int(num) if num else 1
            if sign == "-":
                coeff = -coeff
            coefficients[var] = coefficients.get(var, 0) + coeff

        if not coefficients:
            raise ValueError(f"No variables found in expression '{expr}'")

        # Make sure to return the new instance
        return LinearConstraint(coefficients, constant, relation)


    def __str__(self) -> str:
        """Return a human readable representation like 'x + 2y <= 5'."""
        terms = []
        for var, coef in self.coefficients.items():
            if coef == 1:
                terms.append(f"{var}")
            elif coef == -1:
                terms.append(f"-{var}")
            else:
                terms.append(f"{coef}{var}")
        lhs = " + ".join(terms).replace("+ -", "- ")
        return f"{lhs} {self.relation} {self.constant}"


