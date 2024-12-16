from fortunes import fortunes
import visualization.dcel_plot as dcel_plot
from dcel import *
import re
import sys 

from point import Point

if __name__ == "__main__":    
    point_pattern = re.compile(r"[-+]?\d*\.?\d+")

    points : list[Point] = []
    query_point_count = 0
    for line_number, line in enumerate(sys.stdin):
        point = point_pattern.findall(line)
        if len(point) == 0:
            continue # Skip empty lines:
        if len(point) == 2:
            x, y = point
            points.append(Point(float(x), float(y)))
        else:
            print(f"Warning: Incorrect format on line {line_number}: '{line.strip()}'.")
            print("Expected format: 'x1 y1 \\n' ")
            print("where x and y are numbers seperate by any delimiter.")
            sys.exit(1) 

    output = fortunes(points)
    # print("Done")
    dcel_plot.dcel_plot(output, points)