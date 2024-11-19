
import math

import numpy as np
from find_breakpoint import define_circle
from point import Point
from find_breakpoint import define_circle

def test_center_on_circle():

    p1 = Point(4,4)
    p2 = Point(5, 5)
    p3 = Point(7, 4)
    p, r = define_circle(p1, p2, p3) 
    assert p == Point(5.5, 3.5), f"Center of circle is not as expected p = {p}"
    assert math.isclose(r, 1.5811388300841898), f"Radius is not as expected r = {r}"
    
    
def test_center_not_on_circle():
    p1 = Point(11, 2)
    p2 = Point(13, 2)
    p3 = Point(15, 2)
    p, r = define_circle(p1, p2, p3)
    assert p == None, f"Center of circle is not as expected p = {p}"
    assert r == np.inf, f"Radius is not as expected r = {r}"