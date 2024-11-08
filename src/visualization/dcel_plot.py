
import sys
import matplotlib.pyplot as plt
from dcel import *
from point import Point

def plt_draw_new(edge: Edge, depth: int, target_depth: int) -> None:
    print(edge)
    if depth >= target_depth:
        return
    
    # Draw the vertex
    plt.plot(edge.origin.x, edge.origin.y, 'ko') 

    # Draw the edge
    point_to = edge.next.origin if edge.next != None else edge.twin.origin
    color = "black" if edge.next != None else "red"
    plt.annotate("",
                xytext=(edge.origin.x, edge.origin.y), xy=(point_to.x, point_to.y),
                arrowprops=dict(arrowstyle="->", lw=1.5, color=color))
    
    # Draw twin
    if edge.twin != None:
        plt_draw_new(edge.twin, depth + 1, target_depth)
    
    # Draw next edge
    if edge.next != None:
        plt_draw_new(edge.next, depth + 1, target_depth)

    # Draw prev edge
    if edge.prev != None:
        plt_draw_new(edge.prev, depth + 1, target_depth)

def plt_draw(edge: Edge, drawn_edges: set[Edge], drawn_vertices: set[Vertex]) -> None:
    print(edge)
    if edge in drawn_edges:
        return
    
    drawn_edges.add(edge)
    
    # Draw the vertex
    if edge.origin not in drawn_vertices:
        plt.plot(edge.origin.x, edge.origin.y, 'ko') 
        drawn_vertices.add(edge.origin)

    # Draw the edge
    point_to = edge.next.origin if edge.next != None else edge.twin.origin
    color = "black" if edge.next != None else "red"
    plt.annotate("",
                xytext=(edge.origin.x, edge.origin.y), xy=(point_to.x, point_to.y),
                arrowprops=dict(arrowstyle="->", lw=1.5, color=color))
    
    # Draw twin
    if edge.twin != None:
        plt_draw(edge.twin, drawn_edges, drawn_vertices)
    
    # Draw next edge
    if edge.next != None:
        plt_draw(edge.next, drawn_edges, drawn_vertices)

    # Draw prev edge
    if edge.prev != None:
        plt_draw(edge.prev, drawn_edges, drawn_vertices)

def plot_edges(edges: set[Edge]) -> None:
    for edge in edges:
        print("plt edge")
        point_to = edge.next.origin if edge.next != None else edge.twin.origin
        color = "black" if edge.next != None else "red"
        plt.annotate("",
                    xytext=(edge.origin.x, edge.origin.y), xy=(point_to.x, point_to.y),
                    arrowprops=dict(arrowstyle="->", lw=1.5, color=color))

def plot_vertices(vertices: set[Vertex]) -> None:
    for vertex in vertices:
        print("plt vertex")
        plt.plot(vertex.x, vertex.y, 'ko') 


def dcel_plot(init_edge: Edge, sites: list[Point]) -> None:
    plt.figure()

    edges = get_all_edges(init_edge)
    vertices = get_all_vertices(edges)
    plot_edges(edges)
    plot_vertices(vertices)

    for site in sites:
        plt.plot(site.x, site.y, 'ro')

    print()
    print("Drawing DCEL...")
    # plt_draw(init_edge, edges, vertices)
    # plt_draw_new(init_edge, 0, 5)
    print("Initial edge:")
    print(init_edge)
    print()
    print("Edges:")
    for edge in edges:
        print(edge)
    print()
    print("Vertices:")
    for vertex in vertices:
        print(vertex)
    
    coordinates = [(v.x, v.y) for v in vertices] + [(v.x, v.y) for v in sites]    
    max_x = max([v[0] for v in coordinates])
    min_x = min([v[0] for v in coordinates])
    max_y = max([v[1] for v in coordinates])
    min_y = min([v[1] for v in coordinates])
    padding = 5

    plt.xlim(min_x - padding, max_x + padding) 
    plt.ylim(min_y - padding, max_y + padding)
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Result')
    plt.grid()
    plt.axhline(0, color='black', linewidth=0.5, ls='--')
    plt.axvline(0, color='black', linewidth=0.5, ls='--')
    
    plt.savefig("result.pdf", format='pdf')
    plt.close()


def get_all_edges(edge: Edge, visited: set[Edge] = None) -> list[Edge]:
    if visited is None:
        visited = set()
    if edge in visited:
        print("Already visited", edge)
        return []
    print(edge)
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