import math

import pytest
from hypothesis import example, given, settings, strategies as st
from gym_membership import parse_plan, calculate_bmi, average_workout

@given(st.text() | st.none())
@settings(max_examples=500, derandomize=True)
@example("GOLD-12")
@example(" gold - 12 ")
@example("GOLD-" + "9" * 5000)
def test_parse_plan_no_crash(s):
    result = parse_plan(s)
    if result is not None:
        plan, months = result
        assert plan and plan.isascii() and plan.isalpha()
        assert plan == plan.upper()
        assert isinstance(months, int) and months > 0

@given(st.text() | st.none())
@settings(max_examples=500, derandomize=True)
@example("70,1.75")
@example("70,0")
@example("70,1e-300")
@example("70,1e200")
@example("nan,1.75")
@example("1e308,1e-100")
def test_calculate_bmi_no_crash(s):
    result = calculate_bmi(s)
    if result is not None:
        assert isinstance(result, float)
        assert math.isfinite(result) and result >= 0

@given(st.text() | st.none())
@settings(max_examples=500, derandomize=True)
@example("45 60 30")
@example(" ")
@example("9" * 5000)
def test_average_workout_no_crash(s):
    result = average_workout(s)
    if result is not None:
        assert isinstance(result, int) and result >= 0


@given(
    st.text(alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", min_size=1, max_size=30),
    st.integers(min_value=1, max_value=10000),
)
@settings(max_examples=300, derandomize=True)
def test_valid_plans(plan, months):
    assert parse_plan(f" {plan} - {months} ") == (plan.upper(), months)


@given(
    st.integers(min_value=1, max_value=1000),
    st.integers(min_value=10, max_value=300),
)
@settings(max_examples=300, derandomize=True)
def test_valid_bmi(weight, height_cm):
    height_m = height_cm / 100
    assert calculate_bmi(f"{weight},{height_m}") == round(weight / (height_m ** 2), 1)


@given(st.lists(st.integers(min_value=0, max_value=1000000), min_size=1, max_size=100))
@settings(max_examples=300, derandomize=True)
def test_valid_workouts(values):
    result = average_workout(" \t".join(map(str, values)))
    assert result == sum(values) // len(values)
    assert min(values) <= result <= max(values)


@given(st.floats(), st.floats())
@settings(max_examples=500, derandomize=True)
def test_numeric_bmi_extremes(weight, height):
    result = calculate_bmi(f"{weight},{height}")
    if not (math.isfinite(weight) and math.isfinite(height) and weight > 0 and height > 0):
        assert result is None
    if result is not None:
        assert math.isfinite(result) and result >= 0


@pytest.mark.parametrize("code", [
    None, "", "-", "GOLD", "GOLD-x", "GOLD-0", "GOLD--1", "-12", "GOLD-1-2", "G0LD-12",
])
def test_invalid_plans(code):
    assert parse_plan(code) is None


@pytest.mark.parametrize("data", [
    None, "", ",", "70", "70,1,2", "x,1.75", "70,0", "-70,1.75", "70,-1.75",
    "0,1.75", "nan,1.75", "70,inf", "70,1e-300", "70,1e200", "1e308,1e-100",
])
def test_invalid_bmi(data):
    assert calculate_bmi(data) is None


@pytest.mark.parametrize("minutes", [None, "", ":", " \t\n", "45 abc", "-10 20", "1.5 2"])
def test_invalid_workouts(minutes):
    assert average_workout(minutes) is None


@pytest.mark.parametrize("value", [0, 1.5, [], {}, b"GOLD-12"])
def test_non_text_inputs(value):
    assert parse_plan(value) is None
    assert calculate_bmi(value) is None
    assert average_workout(value) is None


def test_known_results():
    assert parse_plan("GOLD-12") == ("GOLD", 12)
    assert calculate_bmi("70,1.75") == 22.9
    assert average_workout("45 60 30") == 45
    assert average_workout("1 2") == 1
    assert average_workout("0 0") == 0
