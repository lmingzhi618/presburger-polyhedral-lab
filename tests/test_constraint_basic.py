import pytest

from src.presburger.constraint import LinearConstraint


def test_constraint_parsing_and_evaluation():
    c1 = LinearConstraint.from_str("x + 2y <= 5")
    assert str(c1) == "x + 2y <= 5"
    assert c1.evaluate({"x": 1, "y": 2})  # 1 + 4 <= 5 -> True
    assert not c1.evaluate({"x": 3, "y": 2})  # 3 + 4 <= 5 -> False


def test_negative_and_multiple_terms():
    c2 = LinearConstraint.from_str("-x + 2y >= 4")
    assert not c2.evaluate({"x": 1, "y": 2})  # -1 + 4 >= 3 -> False
    assert c2.evaluate({"x": 1, "y": 3})  # 1 + 6 >= 4 -> True


def test_all_relations():
    # Equality and inequality operators
    assert LinearConstraint.from_str("x = 5").evaluate({"x": 5})
    assert not LinearConstraint.from_str("x != 5").evaluate({"x": 5})
    assert LinearConstraint.from_str("x < 5").evaluate({"x": 4})
    assert LinearConstraint.from_str("x > 5").evaluate({"x": 6})


def test_whitespace_and_formatting():
    c = LinearConstraint.from_str("  x +   2  y <=     5   ")
    assert str(c) == "x + 2y <= 5"


def test_default_coefficients():
    c = LinearConstraint.from_str("x + y <= 3")
    assert c.coefficients == {"x": 1, "y": 1}


def test_negative_rhs_and_combined_terms():
    c = LinearConstraint.from_str("x - 2y <= -3")
    assert c.evaluate({"x:": 1, "y": 3})


def test_duplicate_variables_are_combined():
    c = LinearConstraint.from_str("x + 2x <= 3")
    assert c.coefficients == {"x": 3}


def test_invalid_expressions():
    with pytest.raises(ValueError):
        LinearConstraint.from_str("x + y 5")
    with pytest.raises(ValueError):
        LinearConstraint.from_str("x + y <= foo")


def test_missing_variable_in_eval_defaults_to_zero():
    c = LinearConstraint.from_str("x + y <= 3")
    assert c.evaluate({"x": 3})  # y defaults to 0
