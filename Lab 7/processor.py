"""Photo print order processor used for the Lab 7 fuzzing exercise."""

import math

INCLUDED_PRINTS = {"4x6": 20, "5x7": 15, "8x10": 10}
VALID_FINISHES = {"matte", "glossy", "canvas"}


def _is_valid_measurement(value):
    """Accept finite, non-negative int/float values, excluding bools."""
    return (
        not isinstance(value, bool)
        and isinstance(value, (int, float))
        and (not isinstance(value, float) or math.isfinite(value))
        and value >= 0
    )


def extra_print_charge(print_size, copies, finish, is_member):
    """Calculate the charge for copies beyond the included print allowance."""
    # Validate every input before doing arithmetic or set membership.
    if not isinstance(print_size, str) or print_size not in INCLUDED_PRINTS:
        raise ValueError("unknown print size")
    if type(copies) is not int or copies < 0:
        raise ValueError("invalid copies")
    if not isinstance(finish, str) or finish not in VALID_FINISHES:
        raise ValueError("unknown finish")
    if type(is_member) is not bool:
        raise ValueError("is_member must be a boolean")

    included = INCLUDED_PRINTS[print_size]
    if is_member and print_size != "8x10":
        included += 5

    extra = copies - included
    if extra <= 0:
        return 0

    rate = 4 if finish == "matte" else 7
    if extra > 50:
        rate += 2
        if finish == "canvas":
            rate += 5
    return extra * rate


def order_valid(file_mb, copies, is_rush):
    """Return whether an order fits the rush or standard-order limits."""
    if not _is_valid_measurement(file_mb):
        raise ValueError("invalid file size")
    if type(copies) is not int or copies < 0:
        raise ValueError("invalid copies")
    if type(is_rush) is not bool:
        raise ValueError("is_rush must be a boolean")

    if is_rush:
        return copies <= 50
    if file_mb > 25:
        return False
    return copies <= 500


def dispatch_status(hours_before_dispatch, is_framed, is_international):
    """Return the order's dispatch cutoff status."""
    if not _is_valid_measurement(hours_before_dispatch):
        raise ValueError("invalid hours before dispatch")
    if type(is_framed) is not bool:
        raise ValueError("is_framed must be a boolean")
    if type(is_international) is not bool:
        raise ValueError("is_international must be a boolean")

    cutoff = 24 if is_framed else 12
    if is_international:
        cutoff += 24
    if hours_before_dispatch >= cutoff:
        return "on_time"
    if hours_before_dispatch >= cutoff - 6:
        return "tight"
    return "missed"


if __name__ == "__main__":
    print("Photo print order processor")
    print("Sample charge:", extra_print_charge("4x6", 30, "matte", True))
    print("Sample standard order valid:", order_valid(10, 100, False))
    print("Sample dispatch status:", dispatch_status(12, False, False))
