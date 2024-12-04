"""
Doubley Connected Edge List (DCEL) data structure
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Vertex:
    x: int
    y: int
    edge: Edge
    
    def __str__(self):
        return f"Vertex({self.x:.2f}, {self.y:.2f})"

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, other: object) -> bool:
        return (isinstance(other, Vertex) and 
                self.x == other.x and self.y == other.y)
    
@dataclass
class Edge:
    origin: Vertex
    twin: Edge | None
    next: Edge | None
    prev: Edge | None

    def __str__(self) -> str:
        return f"Edge({self.origin}, {self.next.origin if self.next != None else "t:" + str(self.twin.origin) if self.twin != None else "None"})"

    def __eq__(self, other: object) -> bool:
        return (isinstance(other, Edge) and 
                self.origin == other.origin and (self.next.origin == other.next.origin if self.next != None else self.next == other.next))

    def __hash__(self) -> int:
        return hash((self.origin, 
                     self.next.origin if self.next != None else None,
                     self.twin.origin if self.twin != None else None))


    def set_next(self, next_edge: Edge) -> None:
        """
        Sets next of current edge and the previous of other edge accordingly
        """
        self.next = next_edge
        next_edge.prev = self
        

    def set_prev(self, prev_edge: Edge) -> None:
        """
        Sets next of current edge and the previous of other edge accordingly
        """
        self.prev = prev_edge
        prev_edge.next = self
        