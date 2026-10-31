"""Lab 6 - Line (code) coverage tests for photo_print_order.py"""
import pytest
from photo_print_order import extra_print_charge, order_valid, dispatch_status


# ---------- extra_print_charge ----------
def test_within_included_prints():
    assert extra_print_charge("4x6", 15, "matte", False) == 0


def test_unknown_print_size_raises():
    with pytest.raises(ValueError):
        extra_print_charge("A4", 10, "matte", False)


def test_negative_copies_raises():
    with pytest.raises(ValueError):
        extra_print_charge("4x6", -1, "matte", False)


def test_member_bonus_prints():
    # member 4x6: 20 + 5 = 25 included, 30 copies -> 5 extra * 4
    assert extra_print_charge("4x6", 30, "matte", True) == 20


def test_matte_rate():
    # 10 extra * 4
    assert extra_print_charge("4x6", 30, "matte", False) == 40


def test_glossy_rate():
    # 10 extra * 7
    assert extra_print_charge("4x6", 30, "glossy", False) == 70


def test_bulk_extra_surcharge_matte():
    # 60 extra * (4 + 2)
    assert extra_print_charge("4x6", 80, "matte", False) == 360


def test_bulk_extra_surcharge_canvas():
    # 60 extra * (7 + 2 + 5)
    assert extra_print_charge("4x6", 80, "canvas", False) == 840


# ---------- order_valid ----------
def test_order_valid():
    assert order_valid(10, 100, False) is True


def test_rush_order_valid():
    assert order_valid(10, 50, True) is True


def test_file_too_large():
    assert order_valid(30, 100, False) is False


# ---------- dispatch_status ----------
def test_dispatch_on_time():
    assert dispatch_status(12, False, False) == "on_time"


def test_dispatch_tight():
    assert dispatch_status(8, False, False) == "tight"


def test_dispatch_missed():
    assert dispatch_status(2, False, False) == "missed"


def test_dispatch_framed_international():
    # cutoff = 24 + 24 = 48
    assert dispatch_status(48, True, True) == "on_time"
