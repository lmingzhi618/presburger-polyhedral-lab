import pytest

from polyhedral.sets import IntegerSet
from presburger.constraint import LinearConstraint


def test_basic_membership():
    S = IntegerSet(
        [
            LinearConstraint.from_str("0 <= i <= 4"),
            LinearConstraint.from_str("0 <= j <= 4"),
        ]
    )

    assert S.contains({"i": 0, "j": 0})
    assert S.contains({"i": 4, "j": 3})
    assert not S.contains({"i": 5, "j": 2})
    assert not S.contains({"i": 1, "j": 6})


def test_union_and_intersection():
    S1 = IntegerSet([LinearConstraint.from_str("i <= 2")])
    S2 = IntegerSet([LinearConstraint.from_str("i >= 1")])

    inter = S1.intersection(S2)
    assert inter.contains({"i": 1})
    assert inter.contains({"i": 2})
    assert not inter.contains({"i": 0})
    assert not inter.contains({"i": 3})

    union = S1.union(S2)
    assert union.contains({"i": 0})
    assert union.contains({"i": 3})


def test_empty_detection():
    # Contradictory constraints: i <= 1 and i >= 3
    S = IntegerSet(
        [
            LinearConstraint.from_str("i <= 1"),
            LinearConstraint.from_str("i >= 3"),
        ]
    )
    assert S.is_empty()


def test_string_representation():
    S = IntegerSet(
        [
            LinearConstraint.from_str("0 <= i <= 1"),
            LinearConstraint.from_str("j >= 0"),
        ]
    )
    assert S.is_empty() is False
    s = str(S)
    assert "i" in s and "j" in s
    assert "0" in s and "1" in s
    assert "{" in s and "}" in s


def test_str_with_subsets():
    S1 = IntegerSet([LinearConstraint.from_str("i <= 1")])
    S2 = IntegerSet([LinearConstraint.from_str("i >= 3")])
    S_union = IntegerSet(subsets=[S1, S2])

    s = str(S_union)

    assert "u" in s or "{" in s
    assert "i" in s
    assert isinstance(s, str)


def test_eq():
    S1 = IntegerSet(
        [LinearConstraint.from_str("i >= 0"), LinearConstraint.from_str("j >= 0")]
    )
    S2 = IntegerSet(
        [LinearConstraint.from_str("j >= 0"), LinearConstraint.from_str("i >= 0")]
    )
    assert S1 != 123
    assert S1 == S2

    S1 = IntegerSet(
        subsets=[
            IntegerSet([LinearConstraint.from_str("i >= 0")]),
            IntegerSet([LinearConstraint.from_str("j >= 0")]),
        ]
    )
    S2 = IntegerSet(
        subsets=[
            IntegerSet([LinearConstraint.from_str("j >= 0")]),
            IntegerSet([LinearConstraint.from_str("i >= 0")]),
        ]
    )
    S3 = IntegerSet(subsets=[IntegerSet([LinearConstraint.from_str("j >= 1")])])
    assert S1 == S2
    assert S2 != S3

    S5 = IntegerSet(
        [
            LinearConstraint.from_str("i >= 0"),
        ]
    )
    assert S1 != S5  # ✅ structure mismatch
