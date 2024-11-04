
import matplotlib.pyplot as plt
from dcel import *


def plt_draw(edge: Edge, drawn_edges: set[Edge], drawn_vertices: set[Vertex]) -> None:
    print(edge)
    if edge in drawn_edges:
        return
    
    drawn_edges.add(edge)
    
    # Draw the vertex
    if edge.origin not in drawn_vertices:
        plt.plot(edge.origin.x, edge.origin.y, 'ko') 
        drawn_vertices.add(edge.origin)

    point_to = edge.next.origin if edge.next != None else edge.twin.origin
        
    # Draw the edge
    plt.annotate("",
                xytext=(edge.origin.x, edge.origin.y), xy=(point_to.x, point_to.y),
                arrowprops=dict(arrowstyle="->", lw=1.5))
    
    # Draw twin
    if edge.twin != None:
        plt_draw(edge.twin, drawn_edges, drawn_vertices)
    
    # Draw next edge
    if edge.next != None:
        plt_draw(edge.next, drawn_edges, drawn_vertices)


def dcel_plot(init_edge: Edge) -> None:
    vertices = set()
    edges = set()

    plt.figure()
    plt_draw(init_edge, edges, vertices)
    
    
    max_x = max([v.x for v in vertices])
    min_x = min([v.x for v in vertices])
    max_y = max([v.y for v in vertices])
    min_y = min([v.y for v in vertices])
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
