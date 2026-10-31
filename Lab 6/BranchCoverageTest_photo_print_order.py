"""Lab 6 - Branch coverage tests for photo_print_order.py
Every decision is exercised in both its True and False direction."""
import pytest
from photo_print_order import extra_print_charge, order_valid, dispatch_status


# ---------- extra_print_charge ----------
# print_size validation
def test_unknown_print_size_raises():
    with pytest.raises(ValueError):
        extra_print_charge("A4", 10, "matte", False)


def test_known_print_size_ok():
    assert extra_print_charge("5x7", 10, "matte", False) == 0


# copies validation
def test_negative_copies_raises():
    with pytest.raises(ValueError):
        extra_print_charge("4x6", -1, "matte", False)


def test_zero_copies():
    assert extra_print_charge("4x6", 0, "matte", False) == 0


# is_member and print_size != "8x10"
def test_non_member_no_bonus():
    # included 20, 30 copies -> 10 extra * 4
    assert extra_print_charge("4x6", 30, "matte", False) == 40


def test_member_gets_bonus():
    # included 25, 30 copies -> 5 extra * 4
    assert extra_print_charge("4x6", 30, "matte", True) == 20


def test_member_8x10_no_bonus():
    # included stays 10, 20 copies -> 10 extra * 4
    assert extra_print_charge("8x10", 20, "matte", True) == 40


# extra <= 0
def test_exactly_included_copies():
    assert extra_print_charge("4x6", 20, "matte", False) == 0


def test_one_extra_copy():
    assert extra_print_charge("4x6", 21, "matte", False) == 4


# finish == "matte"
def test_matte_rate():
    assert extra_print_charge("4x6", 30, "matte", False) == 40


def test_glossy_rate():
    assert extra_print_charge("4x6", 30, "glossy", False) == 70


# extra > 50 (boundary) and finish == "canvas"
def test_extra_exactly_50_no_surcharge():
    # 50 extra * 4
    assert extra_print_charge("4x6", 70, "matte", False) == 200


def test_extra_51_surcharge():
    # 51 extra * (4 + 2)
    assert extra_print_charge("4x6", 71, "matte", False) == 306


def test_bulk_glossy_no_canvas_surcharge():
    # 60 extra * (7 + 2)
    assert extra_print_charge("4x6", 80, "glossy", False) == 540


def test_bulk_canvas_surcharge():
    # 60 extra * (7 + 2 + 5)
    assert extra_print_charge("4x6", 80, "canvas", False) == 840


def test_canvas_without_bulk():
    # canvas but extra <= 50 -> plain rate 7
    assert extra_print_charge("4x6", 30, "canvas", False) == 70


# ---------- order_valid ----------
def test_rush_within_limit():
    assert order_valid(10, 50, True) is True


def test_rush_over_limit():
    assert order_valid(10, 51, True) is False


def test_rush_ignores_file_size():
    assert order_valid(100, 10, True) is True


def test_file_too_large():
    assert order_valid(25.1, 100, False) is False


def test_file_exactly_25_ok():
    assert order_valid(25, 100, False) is True


def test_normal_copies_at_limit():
    assert order_valid(10, 500, False) is True


def test_normal_copies_over_limit():
    assert order_valid(10, 501, False) is False


# ---------- dispatch_status ----------
# is_framed True/False x is_international True/False
def test_plain_on_time():
    assert dispatch_status(12, False, False) == "on_time"


def test_plain_tight_upper():
    assert dispatch_status(11, False, False) == "tight"


def test_plain_tight_lower():
    assert dispatch_status(6, False, False) == "tight"


def test_plain_missed():
    assert dispatch_status(5, False, False) == "missed"


def test_framed_on_time():
    assert dispatch_status(24, True, False) == "on_time"


def test_framed_tight():
    assert dispatch_status(18, True, False) == "tight"


def test_framed_missed():
    assert dispatch_status(17, True, False) == "missed"


def test_international_on_time():
    assert dispatch_status(36, False, True) == "on_time"


def test_international_tight():
    assert dispatch_status(30, False, True) == "tight"


def test_international_missed():
    assert dispatch_status(29, False, True) == "missed"


def test_framed_international_on_time():
    assert dispatch_status(48, True, True) == "on_time"
