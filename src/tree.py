
from __future__ import annotations
from dataclasses import dataclass
from dcel import Edge
from point import Point
from events import CircleEvent, EventQueue
from find_breakpoint import find_breakpoint

# Binary search tree
@dataclass
class Tree:
    root: Node | Leaf | None
    event_queue: EventQueue

    def add(self, site: Point, sweep_line_y: float) -> None:
        if self.root == None:
            self.root = Leaf(site, None, None) # P: HandleSiteEvent step 1
        else:
            self.root._add(site, sweep_line_y, self.event_queue)

    def print_tree(self):
        if self.root is not None:
            self.root.print_subtree(level=0)
        else:
            print("Tree is empty.")


@dataclass
class Node:
    left: Node | Leaf
    right: Node | Leaf
    parent: Node | None
    arc_points: tuple[Point]
    edge: Edge # Pointer in the doubley connected edge list 

    def _add(self, site: Point, sweep_line_y: float, event_queue: EventQueue) -> None:
        # TODO: Don't base this on the x-coordinate of the first point
        #       But rather base it on the breakpoint between both the points in break_point
        if site.x < self.find_breakpoint(sweep_line_y).x:
            self.left._add(site, sweep_line_y, event_queue)
        else:
            self.right._add(site, sweep_line_y, event_queue)
    
    def find_breakpoint(self, sweep_line_y: float, update_edge_origin: bool = True) -> Point:
        # Note: If one site is a vertical line on the sweep line, there is only one breakpoint (bp)
        bps = find_breakpoint(self.arc_points[0], self.arc_points[1], sweep_line_y)
        if len(bps) == 1:
            bp = bps[0]
        else:
            bp = bps[1] if self.arc_points[0].y < self.arc_points[1].y else bps[0]

        if update_edge_origin:
            self.edge.origin.x = bp.x # TODO: Maybe not necessary
            self.edge.origin.y = bp.y # TODO: Maybe not necessary

        return bp 


    def replace_child(self, cur_child, new_child) -> None:
        """
        Precondition: cur_child is either self.left or self.right
        """
        if self.left == cur_child:
            self.left = new_child
        else:
            self.right = new_child
    

    
    def print_subtree(self, level):
        indent = "  " * level
        print(f"{indent}Node: arc_points={self.arc_points}")
        if self.left is not None:
            self.left.print_subtree(level + 1)
        if self.right is not None:
            self.right.print_subtree(level + 1)

 
 
@dataclass
class Leaf: 
    site: Point
    parent: Node | None
    circle_event: CircleEvent | None # Pointer in event queue

    def _add(self, site: Point, sweep_line_y: float, event_queue : EventQueue) -> None:
        # P: HandleSiteEvent where this leaf is alpha
        # Step 2:
        # Remove circle event if it's there
        if self.circle_event != None:
            event_queue.remove(self.circle_event)
            self.circle_event = None

        # Step 3:
        # Add subtree for which to replace leaf
        node_parent = Node(
            left = None,
            right= self,
            parent=self.parent,
            arc_points=(site, self.site),
            edge=None
        )

        # replace the leaf with the root of the subtree     
        if self.parent != None: #TODO: Check if this is works
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
        copy_self = Leaf(self.site.copy(), node_left, None)
        node_left.left = copy_self

        # Step 4: Edges
        breakpoint = node_parent.find_breakpoint(sweep_line_y, False)
        node_parent.edge = Edge(breakpoint, None, None, None, None)
        node_left.edge = Edge(breakpoint.copy(), None, None, None, None)
        node_parent.edge.twin = node_left.edge
        node_left.edge.twin = node_parent.edge 

        # Step 5
        # consecutive arcs to the right of the new arc
        p_i = node_parent.left.right
        p_j = p_i.next_leaf()
        p_k = p_j.next_leaf()
        check_circle_event(p_i, p_j, p_k, event_queue)

        # consecutive arcs to the left of the new arc
        p_i = node_parent.left.right
        p_j = p_i.prev_leaf()
        p_k = p_j.prev_leaf()
        check_circle_event(p_i, p_j, p_k, event_queue)       

    def copy(self) -> Leaf:
        return Leaf(self.site, self.parent, self.circle_event)
    
    def next_leaf(self) -> Leaf:
        """
        Precondition: self is not the rightmost leaf
        """
        node = self
        while node.parent is not None and node.parent.right == node:
            node = node.parent
        node = self.parent.right

        while not isinstance(node, Leaf):
            node = node.left
        
        return node
        
    def prev_leaf(self) -> Leaf:
        """
        Precondition: self is not the leftmost leaf
        """
        node = self
        while node.parent is not None and node.parent.left == node:
            node = node.parent
        node = self.parent.left

        while not isinstance(node, Leaf):
            node = node.right
        
        return node

    def print_subtree(self, level):
        indent = "  " * level
        print(f"{indent}Leaf: site={self.site}")
        
def check_circle_event(new_node: Leaf, middle: Leaf, end: Leaf, event_queue: EventQueue) -> None:
    """
    Checks if there is a circle event between the three sites and adds it to the event_queue if there 
    """
    # TODO: Might not work - check later
    # Calculate the circle formed by new_node, middle, and end
    # Get the determinant to ensure the points are not collinear
    ax, ay = new_node.site
    bx, by = middle.site
    cx, cy = end.site
    
    det = (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)
    
    if det >= 0:
        return  # No valid circle, as points are collinear or oriented in the wrong direction
    
    # Step 2: Calculate the circumcenter of the circle
    A = ax - bx
    B = ay - by
    C = ax - cx
    D = ay - cy
    
    E = A * (ax + bx) + B * (ay + by)
    F = C * (ax + cx) + D * (ay + cy)
    G = 2 * (A * (cy - by) - B * (cx - bx))
    
    if G == 0:
        return  # No circle, the points are collinear
    
    # Circumcenter (ux, uy)
    ux = (D * E - B * F) / G
    uy = (A * F - C * E) / G
    
    # Step 3: Calculate the radius of the circle
    r = ((ux - ax)**2 + (uy - ay)**2) ** 0.5
    
    # Step 4: Determine the lowest point on the circle (event location)
    lowest_y = uy - r
    
    # If the lowest point is below the sweep line, add a circle event
    if lowest_y < middle.sweep_y:
        print("Add circle event to queue")
        event = CircleEvent(middle, lowest_y)
        middle.event = event
        event_queue.insert(event)
