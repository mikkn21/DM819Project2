"""
Doubley Connected Edge List (DCEL) data structure
"""
from __future__ import annotations



class Vertex:
    def __init__(self, x : int , y : int, edge: Edge):
        self.x = x
        self.y = y
        self.edge = edge

    
    def __str__(self):
        return f"Vertex({self.x}, {self.y})"

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, other: object) -> bool:
        return (isinstance(other, Vertex) and 
                self.x == other.x and self.y == other.y)
    

class Edge:
    def __init__(self, origin : Vertex, twin: Edge, face: Face, next: Edge, prev: Edge):
        self.origin = origin
        self.twin = twin
        self.face = face 
        self.next = next
        self.prev = prev

    def __str__(self) -> str:
        return f"Edge({self.origin}, {self.next.origin})"

    def __eq__(self, other: object) -> bool:
        return (isinstance(other, Edge) and 
                self.origin == other.origin and self.next.origin == other.next.origin)

    def __hash__(self) -> int:
        return hash((self.origin, self.next.origin))

    def find_edge(self, edge: Edge) -> Edge | None:
        if self == edge:
            return self

        cur = self.next
        while cur != edge and cur != self:
            cur = cur.next

        return cur if cur == edge else None
    
    # def copy(self) -> Edge:
    #     return Edge(self.origin, self.twin, self.face, self.next, self.prev)
    

class Face:
    def __init__(self, component: Edge):
        self.component = component

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Face):
            return False

        first = self.component
        first_other = other.component.find_edge(first)
        if first_other == None:
            return False
        
        cur = first.next
        cur_other = first_other.next
        while cur == cur_other and cur != first:
            cur = cur.next
            cur_other = cur_other.next
        
        return cur == first and cur_other == first_other
    
    def _create_superficial_twin_edge(edge: Edge) -> Edge:
        twin_next = Edge(edge.origin, None, None, None, None)
        return Edge(edge.next.origin, edge, None, twin_next, None)
    
    def new_from_vertices(vertices: list[Vertex], all_edges: set[Edge]) -> Face:
        """
        Precondition: len(vertices) >= 2
        """
        face = Face(None)
        i = 0
        edges: list[Edge] = []
        last_edge: Edge | None = None
        while i < len(vertices):
            edge = Edge(vertices[i], None, face, None, last_edge)
            edges.append(edge)
            if last_edge != None:
                last_edge.next = edge

            vertices[i].edge = edge
            i += 1
            last_edge = edge

        vertices[0].edge.prev = last_edge
        last_edge.next = vertices[0].edge

        # Twins
        for edge in edges:
            twin = all_edges.pop(Face._create_superficial_twin_edge(edge))
            if twin != None:
                twin.twin = edge
                edge.twin = twin
                all_edges.add(twin)
        
        for edge in edges:
            all_edges.add(edge)

        face.component = last_edge.next
        return face
