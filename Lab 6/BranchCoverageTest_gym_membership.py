import pytest
from gym_membership import membership_cost, can_enter, bmi_category


# membership_cost
def test_monthly_plan():
    assert membership_cost("monthly", 30, False, False) == 1500

def test_unknown_plan():
    with pytest.raises(ValueError):
        membership_cost("weekly", 30, False, False)

def test_too_young():
    with pytest.raises(ValueError):
        membership_cost("monthly", 10, False, False)

def test_senior_discount():
    assert membership_cost("monthly", 65, False, False) == 1125

def test_student_discount():
    assert membership_cost("monthly", 20, True, False) == 1350

def test_yearly_with_trainer():
    assert membership_cost("yearly", 30, False, True) == 13500


# can_enter
def test_can_enter():
    assert can_enter(10, True, False, "M") is True

def test_plan_inactive():
    assert can_enter(10, False, False, "M") is False

def test_too_early():
    assert can_enter(3, True, False, "M") is False

def test_women_only_slot_female():
    assert can_enter(10, True, True, "F") is True


# bmi_category
def test_invalid_height():
    with pytest.raises(ValueError):
        bmi_category(70, 0)

def test_underweight():
    assert bmi_category(50, 1.75) == "underweight"

def test_normal():
    assert bmi_category(70, 1.75) == "normal"

def test_overweight():
    assert bmi_category(80, 1.75) == "overweight"

def test_obese():
    assert bmi_category(100, 1.75) == "obese"


# Extra cases for branch coverage (false branches and boundary values)
def test_monthly_with_trainer():
    assert membership_cost("monthly", 30, False, True) == 3500

def test_quarterly_student():
    assert membership_cost("quarterly", 20, True, False) == 3600

def test_senior_student_gets_senior_discount():
    assert membership_cost("monthly", 65, True, False) == 1125

def test_age_boundary_14():
    assert membership_cost("monthly", 14, False, False) == 1500

def test_age_boundary_60():
    assert membership_cost("monthly", 60, False, False) == 1125

def test_women_only_slot_male():
    assert can_enter(10, True, True, "M") is False

def test_too_late():
    assert can_enter(23, True, False, "M") is False

def test_hour_boundaries():
    assert can_enter(5, True, False, "M") is True
    assert can_enter(22, True, False, "M") is True

def test_bmi_boundaries():
    assert bmi_category(18.5, 1.0) == "normal"
    assert bmi_category(25, 1.0) == "overweight"
    assert bmi_category(30, 1.0) == "obese"
