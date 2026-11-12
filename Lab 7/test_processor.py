"""Hypothesis fuzz tests for the Lab 7 photo print order processor."""

import math

import pytest
from hypothesis import given, settings, strategies as st

from processor import dispatch_status, extra_print_charge, order_valid


@settings(max_examples=250, deadline=None)
@given(
    print_size=st.one_of(st.none(), st.booleans(), st.integers(), st.text()),
    copies=st.one_of(st.none(), st.booleans(), st.integers(),
                     st.floats(allow_nan=True, allow_infinity=True), st.text()),
    finish=st.one_of(st.none(), st.booleans(), st.integers(), st.text()),
    is_member=st.one_of(st.none(), st.booleans(), st.integers(), st.text()),
)
def test_extra_print_charge_rejects_invalid_inputs(print_size, copies, finish, is_member):
    valid = (
        isinstance(print_size, str)
        and print_size in {"4x6", "5x7", "8x10"}
        and type(copies) is int and copies >= 0
        and isinstance(finish, str)
        and finish in {"matte", "glossy", "canvas"}
        and type(is_member) is bool
    )
    if not valid:
        with pytest.raises(ValueError):
            extra_print_charge(print_size, copies, finish, is_member)
        return

    included = {"4x6": 20, "5x7": 15, "8x10": 10}[print_size]
    if is_member and print_size != "8x10":
        included += 5
    extra = max(0, copies - included)
    rate = 4 if finish == "matte" else 7
    if extra > 50:
        rate += 2 + (5 if finish == "canvas" else 0)
    assert extra_print_charge(print_size, copies, finish, is_member) == (extra * rate if extra else 0)


@settings(max_examples=100, deadline=None)
@given(copies=st.one_of(st.booleans(), st.floats(allow_nan=True, allow_infinity=True), st.text(), st.none()))
def test_extra_print_charge_rejects_non_integer_copies(copies):
    with pytest.raises(ValueError):
        extra_print_charge("4x6", copies, "matte", False)


def _valid_number(value):
    return (not isinstance(value, bool)
            and isinstance(value, (int, float))
            and (not isinstance(value, float) or math.isfinite(value))
            and value >= 0)


@settings(max_examples=250, deadline=None)
@given(
    file_mb=st.one_of(st.none(), st.booleans(), st.integers(),
                      st.floats(allow_nan=True, allow_infinity=True), st.text()),
    copies=st.one_of(st.none(), st.booleans(), st.integers(),
                     st.floats(allow_nan=True, allow_infinity=True), st.text()),
    is_rush=st.one_of(st.none(), st.booleans(), st.integers(), st.text()),
)
def test_order_valid_rejects_invalid_inputs(file_mb, copies, is_rush):
    valid = _valid_number(file_mb) and type(copies) is int and copies >= 0 and type(is_rush) is bool
    if not valid:
        with pytest.raises(ValueError):
            order_valid(file_mb, copies, is_rush)
        return
    expected = copies <= (50 if is_rush else 500) and (is_rush or file_mb <= 25)
    assert order_valid(file_mb, copies, is_rush) is expected


@settings(max_examples=250, deadline=None)
@given(
    hours=st.one_of(st.none(), st.booleans(), st.integers(),
                    st.floats(allow_nan=True, allow_infinity=True), st.text()),
    is_framed=st.one_of(st.none(), st.booleans(), st.integers(), st.text()),
    is_international=st.one_of(st.none(), st.booleans(), st.integers(), st.text()),
)
def test_dispatch_status_rejects_invalid_inputs(hours, is_framed, is_international):
    valid = _valid_number(hours) and type(is_framed) is bool and type(is_international) is bool
    if not valid:
        with pytest.raises(ValueError):
            dispatch_status(hours, is_framed, is_international)
        return
    cutoff = (24 if is_framed else 12) + (24 if is_international else 0)
    expected = "on_time" if hours >= cutoff else "tight" if hours >= cutoff - 6 else "missed"
    assert dispatch_status(hours, is_framed, is_international) == expected


@pytest.mark.parametrize("args,expected", [
    (("4x6", 20, "matte", False), 0),
    (("4x6", 21, "matte", False), 4),
    (("4x6", 70, "matte", False), 200),
    (("4x6", 71, "matte", False), 306),
    (("4x6", 80, "canvas", False), 840),
    (("8x10", 15, "glossy", True), 35),
])
def test_extra_print_charge_business_boundaries(args, expected):
    assert extra_print_charge(*args) == expected


@pytest.mark.parametrize("args,expected", [
    ((25, 500, False), True),
    ((25.01, 500, False), False),
    ((1000, 50, True), True),
    ((10, 51, True), False),
])
def test_order_valid_business_boundaries(args, expected):
    assert order_valid(*args) is expected


@pytest.mark.parametrize("args,expected", [
    ((12, False, False), "on_time"),
    ((11, False, False), "tight"),
    ((6, False, False), "tight"),
    ((5.99, False, False), "missed"),
    ((48, True, True), "on_time"),
])
def test_dispatch_status_business_boundaries(args, expected):
    assert dispatch_status(*args) == expected
