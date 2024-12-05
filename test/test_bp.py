import math
import pytest
from geometry import find_breakpoint
from point import Point


def test_both_sites_on_sweep_line():
    """Test when both sites are on the sweep line."""
    p1 = Point(60, 30)
    p2 = Point(90, 30)
    sweep_y = 30
    with pytest.raises(
        ValueError, match="Both sites are on the sweep line simultaneously"
    ):
        find_breakpoint(p1, p2, sweep_y)


def test_site1_on_sweep_line_site2_above():
    """Test when site1 is on the sweep line and site2 is above."""
    p1 = Point(60, 30)
    p2 = Point(90, 40)
    sweep_y = 30
    breakpoints = find_breakpoint(p1, p2, sweep_y)
    assert len(breakpoints) == 1, "Expected 1 breakpoint"
    assert isinstance(breakpoints[0], Point), "Breakpoint should be of type Point"
    assert breakpoints[0].is_close_to(Point(60.02, 79.93)), "Unexpected breakpoint"


def test_site2_on_sweep_line_site1_above():
    """Test when site2 is on the sweep line and site1 is above."""
    p1 = Point(60, 40)
    p2 = Point(90, 30)
    sweep_y = 30
    breakpoints = find_breakpoint(p1, p2, sweep_y)
    assert len(breakpoints) == 1, "Expected 1 breakpoint"
    assert isinstance(breakpoints[0], Point), "Breakpoint should be of type Point"
    assert breakpoints[0].is_close_to(Point(89.98, 79.93)), "Unexpected breakpoint"


def test_both_sites_above_sweep_line():
    """Test when both sites are above the sweep line."""
    p1 = Point(60, 50)
    p2 = Point(90, 40)
    sweep_y = 30
    breakpoints = find_breakpoint(p1, p2, sweep_y)
    assert len(breakpoints) == 2, "Expected 2 breakpoints"
    assert all(
        isinstance(bp, Point) for bp in breakpoints
    ), "All breakpoints should be of type Point"
    assert breakpoints[0].is_close_to(Point(75.27, 48.83)), "Unexpected breakpoint"
    assert breakpoints[1].is_close_to(Point(164.72, 314.16)), "Unexpected breakpoint"
