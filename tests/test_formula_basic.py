import pytest

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
