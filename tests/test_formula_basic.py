import pytest

from polyhedral.sets import IntegerSet
from presburger.constraint import LinearConstraint
from presburger.formula import PresburgerFormula


def test_and_formula():
    c1 = LinearConstraint.from_str("x <= 5")
    c2 = LinearConstraint.from_str("x >= 0")
    f = PresburgerFormula.and_(
        [
            PresburgerFormula.atom(c1),
            PresburgerFormula.atom(c2),
        ]
    )
    assert f.evaluate({"x": 3})
    assert not f.evaluate({"x": 7})
    assert str(f) == "(x <= 5 ^ x >= 0)"


def test_or_formula():
    c1 = LinearConstraint.from_str("x < 0")
    c2 = LinearConstraint.from_str("x > 5")
    f = PresburgerFormula.or_(
        [
            PresburgerFormula.atom(c1),
            PresburgerFormula.atom(c2),
        ]
    )
    assert f.evaluate({"x": -1})
    assert f.evaluate({"x": 6})
    assert not f.evaluate({"x": 2})
    assert str(f) == "(x < 0 v x > 5)"


def test_not_formula():
    c = LinearConstraint.from_str("x <= 5")
    f = PresburgerFormula.not_(PresburgerFormula.atom(c))
    assert not f.evaluate({"x": 3})
    assert f.evaluate({"x": 6})
    assert str(f) == "!(x <= 5)"


def test_nested_formula():
    # (x <= 5 AND x >= 0) OR (y > 0)
    f1 = PresburgerFormula.and_(
        [
            PresburgerFormula.atom(LinearConstraint.from_str("x <= 5")),
            PresburgerFormula.atom(LinearConstraint.from_str("x >= 0")),
        ]
    )
    f2 = PresburgerFormula.atom(LinearConstraint.from_str("y > 0"))
    f = PresburgerFormula.or_([f1, f2])

    assert f.evaluate({"x": 3, "y": -1})
    assert f.evaluate({"x": -2, "y": 1})
    assert not f.evaluate({"x": 7, "y": -1})


def test_invalid_operator():
    f = PresburgerFormula("invalid", [])
    with pytest.raises(ValueError):
        f.evaluate({})
    assert str(f) == "<invalid formula>"


def _atom(s: str) -> PresburgerFormula:
    return PresburgerFormula.atom(LinearConstraint.from_str(s))


def test_from_formula_or_union_flattened():
    # (i <= 1) OR (i >= 3)
    f = PresburgerFormula(op="or", children=[_atom("i <= 1"), _atom("i >= 3")])
    S = IntegerSet.from_formula(f)
    assert S.contains({"i": 0})
    assert S.contains({"i": 3})
    assert not S.contains({"i": 2})

    assert S.subsets and all(isinstance(x, IntegerSet) for x in S.subsets)


def test_from_formula_and_distribute_over_or():
    # (i >= 0) AND ((i <= 1) OR (i >= 3))
    f_or = PresburgerFormula(op="or", children=[_atom("i <= 1"), _atom("i >= 3")])
    f_and = PresburgerFormula(op="and", children=[_atom("i >= 0"), f_or])

    S = IntegerSet.from_formula(f_and)
    # {i >= 0 and i <= 1} U {i >= 0 and i >= 3}
    assert S.contains({"i": 0})
    assert S.contains({"i": 1})
    assert S.contains({"i": 3})
    assert not S.contains({"i": -1})
    assert not S.contains({"i": 2})
    assert S.subsets and len(S.subsets) == 2


def test_from_formula_and_all_single_conjunct():
    # (i <= 0) AND (i <= 2)
    f = PresburgerFormula(op="and", children=[_atom("i >= 0"), _atom("i <= 2")])
    S = IntegerSet.from_formula(f)
    assert S.contains({"i": 0})
    assert S.contains({"i": 2})
    assert not S.contains({"i": -1})
    assert not S.contains({"i": 3})
    assert not S.subsets


def test_from_formula_atom_no_constraint():
    f = PresburgerFormula.atom(None)
    S = IntegerSet.from_formula(f)
    assert len(S.constraints) == 0 and len(S.subsets) == 0


def test_from_formula_or_branch():
    # inner union (i <= 1 OR i >= 3)
    inner = PresburgerFormula(op="or", children=[_atom("i <= 1"), _atom("i >= 3")])
    outer = PresburgerFormula(
        op="or",
        children=[
            inner,  # this one returns IntegerSet with subsets
            _atom("i = 0"),  # this one returns without subsets
        ],
    )

    S = IntegerSet.from_formula(outer)
    assert isinstance(S, IntegerSet)
    assert len(S.subsets) >= 3  # {i <= 1}, {i >= 3}, {i == 0}
    # Verify the subset structure includes both single and nested unions
    assert any(not s.subsets for s in S.subsets)
    assert any(isinstance(s, IntegerSet) for s in S.subsets)
    # Behavioral check
    assert S.contains({"i": 0})
    assert S.contains({"i": 3})
    assert not S.contains({"i": 2})


def test_from_formula_op_not():
    f_not = PresburgerFormula(op="not", children=[_atom("i >= 0")])
    S = IntegerSet.from_formula(f_not)
    assert isinstance(S, IntegerSet)
    assert not S.constraints  # no constraints inside
    assert not S.subsets


def test_and_distribute_empty_list():
    result = IntegerSet._and_distribute([])
    assert isinstance(result, IntegerSet)
    assert not result.constraints
    assert not result.subsets
