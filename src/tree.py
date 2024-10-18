
from __future__ import annotations
from dataclasses import dataclass
from dcel import Edge
from point import Point
from events import CircleEvent

@dataclass
# Binary search tree
class Tree:
    root: Node | Leaf

    def add(self, leaf: Leaf) -> None:
        self.root._add(leaf)


@dataclass
class Node:
    left: Node | Leaf
    right: Node | Leaf
    parent: Node | None
    arc_points: tuple[Point]
    edge: Edge # Pointer in the doubley connected edge list 

    def _add(self, site: Point) -> None:
        # TODO: Don't base this on the x-coordinate of the first point
        #       But rather base it on the breakpoint between both the points in break_point
        if site.x < self.find_breakpoint().x:
            self.left._add(site)
        else:
            self.right._add(site)
    
    def find_breakpoint(self) -> Point:
        pass 

    def replace_child(self, cur_child, new_child) -> None:
        pass
 
 
@dataclass
class Leaf: 
    site: Point
    parent: Node | None
    circle_event: CircleEvent | None # Pointer in event queue 

    def _add(self, site: Point) -> None:

        # Remove circle event if it's there
        if self.circle_event != None:
            pass

        # Add subtree for which to replace leaf
        node_parent = Node(
            left = None,
            right= self,
            parent=self.parent,
            arc_points=(site, self.site),
            edge=None
        )

        # replace the leaf with the root of the subtree
        self.parent.replace_child(self, node_parent)
        self.parent = node_parent
            
        node_left = Node(
            left = None,
            right= None,
            parent= node_parent,
            arc_points=(self.site, site),
            edge=None
        )
        node_parent.left = node_left

        # Create new leaf
        site_leaf = Leaf(site, node_left, None)
        node_left.right = site_leaf
        
        # Copy old leaf as it is present twice in the tree
        copy_self = self.copy()
        node_left.left = copy_self
        copy_self.parent = node_left

        # Edges
        node_parent.edge = Edge(node_parent.find_breakpoint(), None, None, None, None)
        node_left.edge = Edge(node_left.find_breakpoint(), None, None, None, None)
        node_parent.edge.twin = node_left.edge
        node_left.edge.twin = node_parent.edge 

    def copy(self) -> Leaf:
        return Leaf(self.site, self.parent, self.circle_event)
        
        
        