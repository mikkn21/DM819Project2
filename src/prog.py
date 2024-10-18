import visualization.dcel_plot as dcel_plot
from dcel import *
import re
import sys 

from point import Point

def main() -> None:
     
    f = Face(None)
    f2 = Face(None)

    # Create a DCEL
    v1 = Vertex(0, 0, None)
    v2 = Vertex(10, 0, None)
    v3 = Vertex(15, 20, None)
    v4 = Vertex(5, 15, None)

    v11 = Vertex(10, 0, None)
    v22 = Vertex(15, 0, None)
    v33 = Vertex(15, 20, None)

    e11 = Edge(v11, None, f2, None, None)
    e22 = Edge(v22, None, f2, None, None)
    e33 = Edge(v33, None, f2, None, None)

    v11.edge = e11
    v22.edge = e22
    v33.edge = e33
    e11.next = e22
    e11.prev = e33
    e22.next = e33
    e22.prev = e11
    e33.next = e11
    e33.prev = e22
    
    e1 = Edge(v1, None, f, None, None)   
    e2 = Edge(v2, None, f, None, None)
    e3 = Edge(v3, None, f, None, None)
    e4 = Edge(v4, None, f, None, None)

    e2.twin = e33
    e33.twin = e2

    v1.edge = e1
    v2.edge = e2
    v3.edge = e3
    v4.edge = e4

    e1.next = e2
    e1.prev = e4
    e2.next = e3
    e2.prev = e1
    e3.next = e4
    e3.prev = e2
    e4.next = e1
    e4.prev = e3

    f.component = e1
    f2.component = e11
    
    # Plot the DCEL
    print("asdasd")
    dcel_plot.dcel_plot(f)

def new_main() -> None:
    vertices: list[Vertex] = [
        Vertex(0, 0, None),
        Vertex(10, 0, None),
        Vertex(15, 20, None),
        Vertex(5, 15, None),
        Vertex(15, 0, None),
    ]

    edges: set[Edge] = set()

    f1 = Face.new_from_vertices(vertices[:4], edges)

    f2 = Face.new_from_vertices([   
        vertices[1],
        vertices[2],
        vertices[4]
        # Vertex(10, 0, None),
        # Vertex(15, 0, None),
        # Vertex(15, 20, None),
    ], edges)
    
    
    
    dcel_plot.dcel_plot(f1)



if __name__ == "__main__":
    # new_main()
    
    point_pattern = re.compile(r"[-+]?\d*\.?\d+")

    points : list[Point] = []
    query_point_count = 0
    for line_number, line in enumerate(sys.stdin):
        point = point_pattern.findall(line)
        print(point)
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

    output = fortunes_algorithm(points)