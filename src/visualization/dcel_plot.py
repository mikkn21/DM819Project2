import sys
import matplotlib.pyplot as plt
from dcel import *
from point import Point
from dataclasses import dataclass

@dataclass
class Box:
    min_x: float
    max_x: float
    min_y: float
    max_y: float

    def __str__(self) -> str:
        return f"Box({self.min_x}, {self.max_x}, {self.min_y}, {self.max_y})"

def plot_edges(edges: set[Edge]) -> None:
    for edge in edges:
        point_to = edge.next.origin if edge.next != None else edge.twin.origin
        color = "black"
        plt.annotate(
            "",
            xytext=(edge.origin.x, edge.origin.y),
            xy=(point_to.x, point_to.y),
            arrowprops=dict(arrowstyle="-", lw=1.5, color=color),
        )


def plot_vertices(vertices: set[Vertex]) -> None:
    for vertex in vertices:
        if isinstance(vertex, Vertex):
            plt.plot(vertex.x, vertex.y, "bo" if isinstance(vertex, Point) else "ko")

def bind_to_box(edges: set[Edge], box: Box) -> None:
    for edge in edges:
        if isinstance(edge.twin.origin, Point):
            intersections = find_edge_intersections(edge, box)
            intersection = min(intersections, key=lambda p: euclidean_dist(p, edge.origin))
            edge.twin.origin = intersection

def find_edge_intersections(edge: Edge, box: Box) -> list[Point]:
    a,b = calculate_edge_line(edge) 
        
    direction = edge.twin.origin - edge.origin

    intersections = []

    if direction.x > 0:
        intersections.append(Point(box.max_x, a * box.max_x + b))
    elif direction.x < 0:
        intersections.append(Point(box.min_x, a * box.min_x + b))

    if direction.y > 0:
        intersections.append(Point((box.max_y - b) / a, box.max_y))
    elif direction.y < 0:
        intersections.append(Point((box.min_y - b) / a, box.min_y))
        
    return intersections

         
def calculate_edge_line(edge: Edge) -> tuple[float, float]:
    x1 = edge.origin.x
    y1 = edge.origin.y
    x2 = edge.twin.origin.x
    y2 = edge.twin.origin.y
    
    a = (y2 - y1) / (x2 - x1)
    b = y1 - a * x1
    return a, b

def euclidean_dist(a: Point, b: Vertex) -> float:
    return ((a.x - b.x) ** 2 + (a.y - b.y) ** 2) ** 0.5


def dcel_plot(init_edge: Edge, sites: list[Point]) -> None:
    plt.figure()

    edges = get_all_edges(init_edge)
    vertices = get_all_vertices(edges)

    for site in sites:
        plt.plot(site.x, site.y, "ro")

    print("Edges:")
    for edge in edges:
        print(f"({edge.origin.x:2f}, {edge.origin.y:2f}), {"inf" if isinstance(edge.twin.origin, Point) else ""}({edge.twin.origin.x:2f}, {edge.twin.origin.y:2f})")
    print()
    print("Vertices:")
    for vertex in vertices:
        if isinstance(vertex, Vertex):
            print(f"({vertex.x:2f}, {vertex.y:.2f})")

    coordinates = [(v.x, v.y) for v in vertices if isinstance(v, Vertex)] + [(v.x, v.y) for v in sites]
    max_x = max([v[0] for v in coordinates])
    min_x = min([v[0] for v in coordinates])
    x_dist = max_x - min_x
    max_x += x_dist * 0.1
    min_x -= x_dist * 0.1
    max_y = max([v[1] for v in coordinates])
    min_y = min([v[1] for v in coordinates])
    y_dist = max_y - min_y
    max_y += y_dist * 0.1
    min_y -= y_dist * 0.1

    box = Box(min_x, max_x, min_y, max_y)

    bind_to_box(edges, box)
    plot_edges(edges)
    plot_vertices(vertices)
    
    plt.xlim(min_x, max_x)
    plt.ylim(min_y, max_y)
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title("Result")
    plt.grid()
    plt.axhline(0, color="black", linewidth=0.5, ls="--")
    plt.axvline(0, color="black", linewidth=0.5, ls="--")

    plt.savefig("result.pdf", format="pdf")
    plt.close()


def get_all_edges(edge: Edge, visited: set[Edge] = None) -> list[Edge]:
    if visited is None:
        visited = set()
    if edge in visited:
        return []
    visited.add(edge)
    edges = [edge]
    if edge.twin:
        edges.extend(get_all_edges(edge.twin, visited))
    if edge.next:
        edges.extend(get_all_edges(edge.next, visited))
    if edge.prev:
        edges.extend(get_all_edges(edge.prev, visited))
    return edges


def get_all_vertices(edges: list[Edge]) -> set[Vertex]:
    vertices = set()
    for edge in edges:
        vertices.add(edge.origin)
    return vertices

