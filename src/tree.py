from __future__ import annotations
from dataclasses import dataclass

import numpy as np
from dcel import Edge
from point import Point
from events import CircleEvent, EventQueue
from find_breakpoint import find_breakpoint, define_circle


# Binary search tree
@dataclass
class Tree:
    root: Node | Leaf | None
    event_queue: EventQueue

    def add(self, site: Point, sweep_line_y: float) -> None:
        if self.root == None:
            self.root = Leaf(site, None, None)  # P: HandleSiteEvent step 1
        else:
            self.root._add(site, sweep_line_y, self.event_queue)
            if isinstance(self.root, Leaf):
                self.root = self.root.get_root()

    def print_tree(self, sweep_line_y: float):
        if self.root is not None:
            self.root.print_subtree(0, sweep_line_y)
        else:
            print("Tree is empty.")

    def update_breakpoints(self, sweep_line_y: float) -> None:
        if self.root is not None and isinstance(self.root, Node):
            self.root.update_breakpoints(sweep_line_y)


@dataclass
class Node:
    left: Node | Leaf
    right: Node | Leaf
    parent: Node | None
    arc_points: list[Point]
    edge: Edge  # Pointer in the doubley connected edge list

    def update_breakpoints(self, sweep_line_y: float) -> None:
        self.find_breakpoint(sweep_line_y)
        if self.left is not None and isinstance(self.left, Node):
            self.left.update_breakpoints(sweep_line_y)
        if self.right is not None and isinstance(self.right, Node):
            self.right.update_breakpoints(sweep_line_y)

    def bp_going_towards(self, sweep_line_y: float, towards: Point) -> bool:
        """Returns whether the breakpoint of this node is going towards the point towards""" 
        bp1 = self.find_breakpoint(sweep_line_y)
        bp2 = self.find_breakpoint(
            sweep_line_y - 100, False
        )  # Simulate that the sweep line has passed a bit
        dir_actual = bp2 - bp1
        dir_target = towards - bp1
        if dir_actual.x >= 0 and dir_target.x >= 0:
            if dir_actual.y >= 0 and dir_target.y >= 0:
                return True
            elif dir_actual.y <= 0 and dir_target.y <= 0:
                return True
        elif dir_actual.x <= 0 and dir_target.x <= 0:
            if dir_actual.y >= 0 and dir_target.y >= 0:
                return True
            elif dir_actual.y <= 0 and dir_target.y <= 0:
                return True
        return False

    def _add(self, site: Point, sweep_line_y: float, event_queue: EventQueue) -> None:
        if site.x < self.find_breakpoint(sweep_line_y).x:
            self.left._add(site, sweep_line_y, event_queue)
        else:
            self.right._add(site, sweep_line_y, event_queue)

    def find_breakpoint(self, sweep_line_y: float, update_edge_origin: bool = True) -> Point: 
        bps = find_breakpoint(self.arc_points[0], self.arc_points[1], sweep_line_y)
        if len(bps) == 1: # If the arc defined by one of the site is a vertical line on the sweep line, there is only one breakpoint (bp)
            bp = bps[0]
        else:
            bp = bps[1] if self.arc_points[0].y < self.arc_points[1].y else bps[0]

        if update_edge_origin and isinstance(self.edge.origin, Point):
            self.edge.origin.x = bp.x 
            self.edge.origin.y = bp.y 

        return bp

    def replace_child(self, cur_child, new_child) -> None:
        """
        Precondition: cur_child is either self.left or self.right
        """
        if id(self.left) == id(cur_child):
            self.left = new_child
        elif id(self.right) == id(cur_child):
            self.right = new_child

        new_child.parent = self
        cur_child.parent = None

    def right_most(self) -> Leaf:
        """
        Get the right-most child of the current nodes parents left subtree
        """
        return self.right.right_most()  # Assume all nodes have a right child

    def print_subtree(self, level):
        indent = "  " * level
        print(f"{indent}Node: arc_points={self.arc_points}, edge={self.edge}")
        if self.left is not None:
            self.left.print_subtree(level + 1)
        if self.right is not None:
            self.right.print_subtree(level + 1)

    def find_parent(self, left_arc_point: Point, right_arc_point: Point) -> Node:
        node = self
        while (node.arc_points[0] != left_arc_point or node.arc_points[1] != right_arc_point):
            node = node.parent
        return node

@dataclass
class Leaf:
    site: Point
    parent: Node | None
    circle_event: CircleEvent | None  # Pointer in event queue

    def _add(self, site: Point, sweep_line_y: float, event_queue: EventQueue) -> None:
        # P: HandleSiteEvent where this leaf is alpha
        # Step 2:
        # Remove circle event if it's there
        if self.circle_event != None:
            event_queue.remove(self.circle_event)
            self.circle_event = None

        # Step 3:
        # Add subtree for which to replace leaf
        node_parent = Node(
            left=None,
            right=self,
            parent=self.parent,
            arc_points=[site, self.site],
            edge=None,
        )

        # replace the leaf with the root of the subtree
        if self.parent != None:
            self.parent.replace_child(self, node_parent)
        self.parent = node_parent

        node_left = Node(
            left=None,
            right=None,
            parent=node_parent,
            arc_points=[self.site, site],
            edge=None,
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
        if p_k is not None:
            check_circle_event(
                p_i, p_j, p_k, node_parent, None, sweep_line_y, event_queue
            )

        # consecutive arcs to the left of the new arc
        p_i = node_parent.left.right
        p_j = p_i.prev_leaf()
        p_k = p_j.prev_leaf()
        if p_k is not None:
            check_circle_event(
                p_k, p_j, p_i, None, None, sweep_line_y, event_queue
            )

    def right_most(self) -> Leaf:
        return self

    def get_root(self) -> Node | Leaf:
        root = self
        while root.parent is not None:
            root = root.parent
        return root

    def print_tree(self):
        self.get_root().print_subtree(0)

    def copy(self) -> Leaf:
        return Leaf(self.site, self.parent, self.circle_event)

    def next_leaf(self) -> Leaf:
        node = self
        while node.parent is not None and id(node.parent.right) == id(node):
            node = node.parent

        if node.parent is None:  # we are at the root = self is the rightmost leaf
            return None

        node = node.parent.right

        while not isinstance(node, Leaf):
            node = node.left

        return node

    def prev_leaf(self) -> Leaf:
        node = self
        while node.parent is not None and id(node.parent.left) == id(node):
            node = node.parent

        if node.parent is None:  # we are at the root = self is the leftmost leaf
            return None

        node = node.parent.left

        while not isinstance(node, Leaf):
            node = node.right

        return node

    def print_subtree(self, level):
        indent = "  " * level
        print(f"{indent}Leaf: site={self.site}")


def check_circle_event(
    left_arc: Leaf,
    middle_arc: Leaf,
    right_arc: Leaf,
    left_middle_node: Node | None,
    middle_end_node: Node | None,
    sweep_line_y: float,
    event_queue: EventQueue,
) -> None:
    p, r = define_circle(left_arc.site, middle_arc.site, right_arc.site)
    if p is None:
        return

    if left_middle_node is None:
        left_middle_node = left_arc.parent.find_parent(left_arc.site, middle_arc.site)
    if middle_end_node is None:
        middle_end_node = middle_arc.parent.find_parent(middle_arc.site, right_arc.site)

    if left_middle_node.bp_going_towards(sweep_line_y, p) and middle_end_node.bp_going_towards(sweep_line_y, p):
        lowest_y = p.y - r
        event = CircleEvent(middle_arc, lowest_y)
        middle_arc.circle_event = event
        event_queue.add(event)


def check_circle_event_for_site_event(
    start_arc: Leaf,
    middle_arc: Leaf,
    end_arc: Leaf,
    event_queue: EventQueue,
    sweep_line_y: float,
    is_left_most: bool,
) -> None:
    """
    Check the triple of consecutive arcs where the me_arc is the left arc or right arc to see if the breakpoints converge
    """
    print("Check circle event for site event")
    p, r = define_circle(start_arc.site, middle_arc.site, end_arc.site)
    if p is None:
        print("No circle event")
        print()
        return  # not circle event

    lowest_y = p.y - r

    if lowest_y < sweep_line_y:
        if is_left_most and p.x > start_arc.site.x:
            event = CircleEvent(middle_arc, lowest_y)
            middle_arc.circle_event = event
            print("added circle event")
            event_queue.add(event)
        elif not is_left_most and p.x < start_arc.site.x:
            event = CircleEvent(middle_arc, lowest_y)
            middle_arc.circle_event = event
            print("added circle event")
            event_queue.add(event)
        else:
            print("No circle event")
            print()
            return
    else:
        print("Circle event is above the sweep line")
