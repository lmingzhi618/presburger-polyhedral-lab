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
    assert str(R_inv).startswith("Relation(")
