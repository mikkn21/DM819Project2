import math
from point import Point


def find_breakpoint(site1: Point, site2: Point, sweep_line_y: float) -> Point:
    """
    Returns the breakpoint between the two parabolas defined by site1 and site2
    at the current sweep line position.
    """
    print("Find breakpoint: ", site1, site2, sweep_line_y)
    x1, y1 = site1
    x2, y2 = site2
    l = sweep_line_y

    # Handle the special case when both sites are at the same y-coordinate
    if y1 == y2:
        x = (x1 + x2) / 2.0
        y = ( (x - x1)**2 ) / (2 * (y1 - l)) + (y1 + l) / 2.0
        return Point(x, y)

    # Compute coefficients for the quadratic equation
    # a*x^2 + b*x + c = 0
    d1 = 2.0 * (y1 - l)
    d2 = 2.0 * (y2 - l)

    # Avoid division by zero (sites below the sweep line)
    if d1 == 0 or d2 == 0:
        raise ValueError("Division by zero encountered; site(s) may be below the sweep line.")
    
    # Coefficients of the quadratic equation
    a = 1.0 / d1 - 1.0 / d2
    b = -2.0 * ( x1 / d1 - x2 / d2 )
    c = ( x1**2 + y1**2 - l**2 ) / d1 - ( x2**2 + y2**2 - l**2 ) / d2

    # Check if the equation is linear (a is zero)
    if abs(a) < 1e-10:
        # Linear equation: a is approximately zero
        x = -c / b
        raise ValueError("Linear equation: a is approximately zero")
    else:
        # Quadratic equation
        discriminant = b**2 - 4 * a * c
        if discriminant < 0:
            raise ValueError("No real intersection points (discriminant < 0).")

        sqrt_discriminant = math.sqrt(discriminant)

        # Calculate both possible x values
        x1_root = (-b + sqrt_discriminant) / (2 * a)
        x2_root = (-b - sqrt_discriminant) / (2 * a)

        # Select the correct root based on context
        # For Fortune's algorithm, the correct breakpoint depends on the relative positions
        # Here, we'll choose the breakpoint with the larger y-coordinate
        y1_root = ( (x1_root - x1)**2 ) / (2 * (y1 - l)) + (y1 + l) / 2.0
        y2_root = ( (x2_root - x1)**2 ) / (2 * (y1 - l)) + (y1 + l) / 2.0
        
        p1 = Point(x1_root, y1_root)
        p2 = Point(x2_root, y2_root)
        return (p1, p2) if p1.x < p2.x else (p2, p1)

        
        # if y1_root > y2_root:
        #     x, y = x1_root, y1_root
        # else:
        #     x, y = x2_root, y2_root

    # return Point(x, y)