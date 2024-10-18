
from fortunes import center_of_circle_from_three_points
from point import Point

def test_center():

    p1 = Point(-6, 3)
    p2 = Point(-3, 2)
    p3 = Point(0, 3)
    assert center_of_circle_from_three_points(p1, p2, p3).is_close_to(Point(-3, 6))
