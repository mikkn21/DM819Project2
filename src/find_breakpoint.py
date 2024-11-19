import math
import numpy as np
from point import Point
import sympy as sp
from point import Point

def define_circle(left: Point, middle: Point, right: Point):
    """
    Returns the center and radius of the circle passing the given 3 points.
    In case the 3 points form a line, returns (None, infinity).
    """
    print("Define circle of points: ", left, middle, right)
    p1, p2, p3 = [left.x, left.y], [middle.x, middle.y], [right.x, right.y] # TODO: Avoid redefining the points
    temp = p2[0] * p2[0] + p2[1] * p2[1]
    bc = (p1[0] * p1[0] + p1[1] * p1[1] - temp) / 2
    cd = (temp - p3[0] * p3[0] - p3[1] * p3[1]) / 2
    det = (p1[0] - p2[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p2[1])
    
    if abs(det) < 1.0e-6:
        return (None, np.inf)
    
    # Center of circle
    cx = (bc*(p2[1] - p3[1]) - cd*(p1[1] - p2[1])) / det
    cy = ((p1[0] - p2[0]) * cd - (p2[0] - p3[0]) * bc) / det
    
    radius = np.sqrt((cx - p1[0])**2 + (cy - p1[1])**2)
    return (Point(cx, cy), radius)

def find_breakpoint(site1: Point, site2: Point, sweep_line_y: float) -> list[Point]:
    x = sp.Symbol('x')
    # Define the coordinates for the sites and sweep line
    h1, k1 = site1
    h2, k2 = site2
    b = sweep_line_y
    
    
    # Relative tolerance for math.isclose()
    rel_tol = 1e-9

    # Both parabolas are vertical liens
    if math.isclose(k1, b, rel_tol=rel_tol) and math.isclose(k2, b, rel_tol=rel_tol):
        # Under general position, this should not occur
        raise ValueError("Both sites are on the sweep line simultaneously, which violates the general position assumption.")

    # Site1's parabola is a vertica line on the sweep line
    elif math.isclose(k1, b, rel_tol=rel_tol):
        if k2 - b <= 0:
            raise ValueError("Site2's parabola is below the sweep line") # TODO: Check if this can actually happen
        y_value = ((h1 - h2) ** 2) / (2 * (k2 - b)) + (k2 + b) / 2
        return [Point(h1, y_value)]
    # Site2's parabola is a vertical line on the sweep line 
    elif math.isclose(k2, b, rel_tol=rel_tol):
        if k1 - b <= 0:
            raise ValueError("Site 1's parabola does not exist above the sweep line") # TODO: Check if this can actually happen
        y_value = ((h2 - h1) ** 2) / (2 * (k1 - b)) + (k1 + b) / 2
        return [Point(h2, y_value)]
    # Both parabolas are valid
    else:
        if k1 - b <= 0 or k2 - b <= 0:
            raise ValueError("One of the parabolas does not exist above the sweep line") # TODO: check if this can actually happen

        
        y1 = ((x - h1) ** 2) / (2 * (k1 - b)) + (k1 + b) / 2
        y2 = ((x - h2) ** 2) / (2 * (k2 - b)) + (k2 + b) / 2
        intersection_points = sp.solve(y1 - y2, x)

        # Filter out complex solutions
        real_intersection_points = [
            point.evalf() for point in intersection_points if point.is_real
        ]
        # Calculate y-values for the real intersections and convert to Points
        intersections = [Point(float(point), float(sp.N(y1.subs(x, point)))) for point in real_intersection_points
        ]
        return intersections