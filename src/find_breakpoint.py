import math
from point import Point
import sympy as sp

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