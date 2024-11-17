import math
from point import Point
from events import *
from tree import *
from dcel import *
import numpy as np
from tree import check_circle_event
from find_breakpoint import define_circle


def fortunes(points: list[Point]) -> Edge:
    event_queue = EventQueue([SiteEvent(p) for p in points])

    status = Tree(None, event_queue)
    dcel: Edge = None
    
    def handle_circle_event(event: CircleEvent) -> None:
        nonlocal dcel

        # if event.middle_leaf.parent.left is None: # TODO: Remove. Just used for debugging
        #     print("WE GOT AN OLD TREE")
        #     return

        # Step 1
        # status.remove(event.middle_leaf)
        # TODO: Assuming that the removed element is replaced all the way up the tree with the left-most leaf.
        #       Also, assume that it's always the middle arc that is removed by a circle event, i.e., it always has a leaf to the left and to the right of it.
        #       Check with Kim if this is correct

        # Get neighbour leaves
        p = event.middle_leaf
        p_next = p.next_leaf()
        p_next_next = p_next.next_leaf() if p_next else None
        p_prev = p.prev_leaf() 
        p_prev_prev = p_prev.prev_leaf() if p_prev else None
        parent = p.parent
        grand_parent = parent.parent

        print("@@@@@@")
        p.print_tree()
        print(f"Handle circle event: {p_prev.site} - {p.site} - {p_next.site}")
        print(f"Sweep line position: {event.key}")


        # Update the tuples representing the breakpoints at the internal nodes
        # TODO: Can we assume we can do this in all cases?
        #       If it works, it might be because we don't balance the tree, and we always create a subtree in the format below.
        # grand_parent.arc_points[0] = p_prev.site
        # # grand_parent.left = p_prev
        # # p_prev.parent = grand_parent
        # grand_parent.left = parent.left
        # parent.left.parent = grand_parent


        # Replace the middle leaf with the correct subtree ? 
        # we talk to kim about this # TODO: Remove
        site = p_prev.site
        grand_parent.replace_child(parent, parent.left if id(parent.right) == id(p) else parent.right)
        # TODO: Remove
        parent.left = None
        parent.parent = None # THIS FUCKS IT UP BUT SHOULD BE OKAY. next_leaf() for some reason still uses some old pointers so removing this pointer creates issues.

        # POSSIBLE REPLACEMENT FOR THE LINE ABOVE:
        #   p.parent.parent.right = p.parent.left
        #   p.parent.left.parent = p.parent.parent
        node = grand_parent
        print(f"|________node___________| : {node.arc_points[0], node.arc_points[1]}")
        while node.arc_points[0] != p.site and node.arc_points[1] != p.site: # TODO: Try without the arc_points[1] stuff
            print(f"node : {node.arc_points[0], node.arc_points[1]}")
            node = node.parent
        if node.arc_points[0] == p.site:
            print("Arc point equals site: ", node.arc_points[0], p.site)
            node.arc_points[0] = site
        elif node.arc_points[1] == p.site: # TODO: Make nicer
            print("Arc point equals site: ", node.arc_points[1], p.site)
            node.arc_points[1] = site
        else:
            raise ValueError("The leaf is not in the tree")
        top_parent = node
        # node.arc_points[0] = site
        


        print("")
        print(
            f"Parent: {parent.arc_points[0]} {parent.arc_points[1]} {parent.edge.origin}, Top parent: {top_parent.arc_points[0], top_parent.arc_points[1], top_parent.edge.origin}"
        )
        print(" ")

        # Remove other circle events that use the arc
        # This can only be the next or previous leaves.
        delete_circle_event(p_next, event_queue)
        delete_circle_event(p_prev, event_queue)

        # Step 2
        center_of_circle, r = define_circle(
            p_prev.site, p.site, p_next.site
        )
        if center_of_circle is None:  # TODO: REMOVE
            print(f"Circle center is None in handle_circle_event: {p_prev.site} - {p.site} - {p_next.site}")
            raise ValueError("Circle center is None in handle_circle_event")
        vertex = Vertex(
            center_of_circle.x, center_of_circle.y, None
        )  # TODO: Set edge reference (if needed)

        print("")
        print(f"Center of circle: {center_of_circle.x, center_of_circle.y}, r: {r}")
        print(" ")

        vertex.edge = Edge(vertex, None, None, None, None)

        new_edge = Edge(Point(vertex.x, vertex.y), vertex.edge, None, None, None)  # The edge of the new breakpoint
        vertex.edge.twin = new_edge
        # TODO: check if all the pointers are set correctly
        if id(p) == id(parent.right):  # Parent is the breakpoint coming from the left
            print("Parent is coming from left")
            print("Parent edge origin: ", parent.edge.origin)
            print("Parent twin edge origin: ", parent.edge.twin.origin)
            print("Grand parent edge origin: ", top_parent.edge.origin)
            print("Grand parent twin edge origin: ", top_parent.edge.twin.origin)
            new_edge.set_next(parent.edge)
            parent.edge.twin.set_next(top_parent.edge)
            parent.edge.origin = vertex
            top_parent.edge.origin = vertex
            # top_parent.edge.twin.set_next(vertex.edge)
            vertex.edge.set_prev(top_parent.edge.twin)
        else:  # Parent is the breakpoint coming from the right
            print("Parent is coming from right")
            new_edge.set_next(top_parent.edge)
            top_parent.edge.twin.set_next(parent.edge)
            top_parent.edge.origin = vertex
            parent.edge.origin = vertex
            vertex.edge.set_prev(parent.edge.twin)
        print("After:")
        print("Parent edge origin: ", parent.edge.origin)
        print("Parent twin edge origin: ", parent.edge.twin.origin)
        print("Grand parent edge origin: ", top_parent.edge.origin)
        print("Grand parent twin edge origin: ", top_parent.edge.twin.origin)
        top_parent.edge = new_edge

        # TODO: Make less hacky
        if dcel is None:
            dcel = vertex.edge

        # Step 3
        if p_prev_prev is not None:
            check_circle_event(p_prev_prev, p_prev, p_next, event.key, event_queue)
        if p_next_next is not None:
            check_circle_event(p_prev, p_next, p_next_next, event.key, event_queue)

    while not event_queue.is_empty():
        event = event_queue.pop()
        if isinstance(event, SiteEvent):
            # handle_site_event(event)
            print("In site event: ", event.site)
            status.add(event.site, event.site.y)
            print("After site event:")
            status.print_tree()
        else:
            event.middle_leaf.circle_event = None
            print("In circle event: ", event.middle_leaf.site)
            handle_circle_event(event)
            print("After circle event:")
            status.print_tree()
    # TODO: Step 7

    # TODO: Step 8 (Skip for now)

    return dcel

def delete_circle_event(leaf: Leaf, event_queue: EventQueue) -> None:
    """
    Deletes the circle event on leaf from the event_queue if it exists.
    """
    if leaf.circle_event is not None:
        print("Deleting a circle event because it's using the leaf")
        event_queue.remove(leaf.circle_event)
        leaf.circle_event = None
