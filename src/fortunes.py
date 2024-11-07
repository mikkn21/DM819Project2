
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

    def delete_circle_event_if_using(using_leaf, leaf) -> None:
        """
        Deletes the circle event on leaf from the event_queue if the using_leaf is a part of the circle event
        Except if the using_leaf is in the middle :)
        """
        if leaf.circle_event is not None and (id(leaf.circle_event.left_arc) == id(using_leaf) or id(leaf.circle_event.right_arc) == id(using_leaf)):
            print("Deleting a circle event because it's using the leaf")
            event_queue.remove(leaf.circle_event)
            leaf.circle_event = None

    def handle_circle_event(event: CircleEvent) -> None:
        nonlocal dcel
        # Step 1 
        # status.remove(event.middle_leaf) 
        # TODO: Assuming that the removed element is replaced all the way up the tree with the left-most leaf.
        #       Also, assume that it's always the middle arc that is removed by a circle event, i.e., it always has a leaf to the left and to the right of it.
        #       Check with Kim if this is correct 
        
        # Get neighbour leaves
        p_next = event.middle_leaf.next_leaf()     
        p_next_next = p_next.next_leaf()
        p_prev = event.middle_leaf.prev_leaf()
        p_prev_prev = p_prev.prev_leaf()
        parent = event.middle_leaf.parent
        grand_parent = parent.parent

        # Update the tuples representing the breakpoints at the internal nodes
        # TODO: Can we assume we can do this in all cases?
        #       If it works, it might be because we don't balance the tree, and we always create a subtree in the format below.
        grand_parent.arc_points[0] = p_prev.site
        # grand_parent.left = p_prev
        # p_prev.parent = grand_parent
        grand_parent.left = parent.left
        parent.left.parent = grand_parent
    
        # Remove other circle events that use the arc
        delete_circle_event_if_using(event.middle_leaf, p_next)
        delete_circle_event_if_using(event.middle_leaf, p_next_next)
        delete_circle_event_if_using(event.middle_leaf, p_prev)
        delete_circle_event_if_using(event.middle_leaf, p_prev_prev)

        # Step 2
        center_of_circle, r = define_circle(p_prev.site, event.middle_leaf.site, p_next.site)
        if center_of_circle is None: # TODO: REMOVE 
            raise ValueError("Circle center is None in handle_circle_event")
        vertex = Vertex(center_of_circle.x, center_of_circle.y, None) # TODO: Set edge reference (if needed)

        vertex.edge = Edge(vertex, None, None, None, None)

        # TODO: Make less hacky 
        if dcel is None:
            print("DCEL is not none anymore")
            dcel = vertex.edge

        new_edge = Edge(Point(vertex.x, vertex.y), vertex.edge, None, None, None)
        vertex.edge.twin = new_edge
        # TODO: check if all the pointers are set correctly
        if event.middle_leaf == parent.right: # Parent is the breakpoint coming from the left
            new_edge.set_next(parent.edge)
            vertex.edge.set_prev(grand_parent.edge.twin)
        else: # Parent is the breakpoint coming from the right
            new_edge.set_next(grand_parent.edge)
            vertex.edge.set_prev(parent.edge.twin)
        grand_parent.edge = new_edge

        # Step 3
        check_circle_event(p_prev_prev, p_prev, p_next, event.key, event_queue)
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
            print("In circle event: ", event.middle_leaf.site)
            handle_circle_event(event)
            print("After circle event:")
            status.print_tree()
    # TODO: Step 7
    
    
    # TODO: Step 8 (Skip for now)

    return dcel
