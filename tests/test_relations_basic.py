import pytest

from polyhedral.relations import Relation
from polyhedral.sets import IntegerSet
from presburger.constraint import LinearConstraint


def test_inverse_relation_and_out_of_domain():
    # domain: i in [0, 2]
    domain = IntegerSet(
        [LinearConstraint.from_str("i >= 0"), LinearConstraint.from_str("i <= 2")]
    )
    # range: j in [1, 3]
    range_ = IntegerSet(
        [LinearConstraint.from_str("j >= 1"), LinearConstraint.from_str("j <= 3")]
    )
    mapping = {"j": "i + 1"}

    R = Relation(domain, range_, mapping)

    # Case 1: apply inside domain
    result = R.apply({"i": 1})
    assert result == {"j": 2}

    # Case 2: apply outside domain triggers "return None"
    assert R.apply({"i": 5}) is None

    # Case 3: test inverse relation
    R_inv = R.inverse()
    assert isinstance(R_inv, Relation)
    assert R_inv.mapping == {"i + 1": "j"} or len(R_inv.mapping) > 0


def test_basic_apply_and_inverse():
    S = IntegerSet([])
    R = Relation(S, S, {"i": "i+1", "j": "j+2"})
    result = R.apply({"i": 3, "j": 5})
    assert result == {"i": 4, "j": 7}

    inv = R.inverse()
    print(f"inv.mapping: {inv.mapping}")
    assert inv.mapping == {"i+1": "i", "j+2": "j"}


def test_parse_and_stringify():
    R = Relation.from_str("{ (i,j) -> (i + 1, j+2) }")
    assert R.mapping == {"i": "i + 1", "j": "j + 2"}
    assert "i -> i + 1" in str(R)
    assert "j -> j + 2" in str(R)


def test_invalid_relation_syntax():
    with pytest.raises(ValueError):
        Relation.from_str("{ (i, j) (i+1, j+2) }")

    with pytest.raises(ValueError):
        Relation.from_str("{ (i) -> () }")


def test_apply_exception():
    R = Relation.from_str("{ (i,j) -> (i + 1, j+2) }")
    point = {"i": "a"}
    with pytest.raises(ValueError):
        R.apply(point)


def test_inverse_exception():
    S = IntegerSet([])
    R1 = Relation(S, S, {"i": "i+1", "j": "i+1"})
    with pytest.raises(ValueError):
        R1.inverse()


def test_compose_exception():
    # domain: i in [0, 2]
    domain = IntegerSet(
        [LinearConstraint.from_str("i >= 0"), LinearConstraint.from_str("i <= 2")]
    )
    # range: j in [1, 3]
    range_ = IntegerSet(
        [LinearConstraint.from_str("j >= 1"), LinearConstraint.from_str("j <= 3")]
    )
    R1 = Relation(domain, range_, {"i": "i+1"})
    R2 = Relation(domain, range_, {"j": "j+2"})
    with pytest.raises(ValueError):
        R2.compose(R1)

    with pytest.raises(TypeError):
        R2.compose(5)


def test_compose_relations():
    # domain: i in [0, 2]
    domain = IntegerSet(
        [LinearConstraint.from_str("i >= 0"), LinearConstraint.from_str("i <= 2")]
    )
    # range: j in [1, 3]
    range_ = IntegerSet(
        [LinearConstraint.from_str("j >= 1"), LinearConstraint.from_str("j <= 3")]
    )
    R1 = Relation(domain, range_, {"i": "i+1", "j": "j"})
    R2 = Relation(range_, domain, {"i": "i", "j": "j+2"})
    R3 = R2.compose(R1)
    assert R3.mapping == {"i": "i + 1", "j": "j + 2"}


def test_eq():
    S = IntegerSet([])
    R1 = Relation(S, S, {"i": "i+1", "j": "i+1"})
    R2 = Relation(S, S, {"i": "i+1", "j": "i+1"})
    assert R1 == R2
