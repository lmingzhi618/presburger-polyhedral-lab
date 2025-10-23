from src.presburger.constraint import LinearConstraint

def test_constraint_parsing_and_evaluation():
    c1 = LinearConstraint.from_str("x + 2y <= 5")
    assert str(c1) == "x + 2y <= 5"
    assert c1.evaluate({"x": 1, "y": 2})        # 1 + 4 <= 5 -> True
    assert not c1.evaluate({"x": 3, "y": 2})    # 3 + 4 <= 5 -> False


def test_negative_and_multiple_terms():
    c2 = LinearConstraint.from_str("-x + 2y >= 4")
    assert not c2.evaluate({"x": 1, "y": 2})        # -1 + 4 >= 3 -> False 
    assert c2.evaluate({"x": 1, "y": 3})            # 1 + 6 >= 4 -> True

