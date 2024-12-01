import math
from point import Point
from events import *
from tree import *
from dcel import *
import numpy as np
from find_breakpoint import define_circle
from visualization.dcel_plot import print_decl


def fortunes(points: list[Point]) -> Edge:
    event_queue = EventQueue([SiteEvent(p) for p in points])

    status = Tree(None, event_queue)
    dcel: Edge = None
    
    def handle_circle_event(event: CircleEvent) -> None:
        nonlocal dcel

        # Get neighbour leaves
        p = event.middle_leaf
        p_next = p.next_leaf()
        p_next_next = p_next.next_leaf() if p_next else None
        p_prev = p.prev_leaf() 
        p_prev_prev = p_prev.prev_leaf() if p_prev else None
        parent = p.parent
        grand_parent = parent.parent
        p_is_left_child = id(parent.left) == id(p)

        print("Tree before")
        p.print_tree(event.key)

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
        grand_parent.replace_child(parent, parent.right if p_is_left_child else parent.left)
        # TODO: Remove
        parent.left = None

        # POSSIBLE REPLACEMENT FOR THE LINE ABOVE:
        #   p.parent.parent.right = p.parent.left
        #   p.parent.left.parent = p.parent.parent
        
        top_parent = None
        if p_is_left_child:
            top_parent = grand_parent.find_ancestor(p_prev.site, p.site)
            top_parent.arc_points[1] = p_next.site
        else: 
            top_parent = grand_parent.find_ancestor(p.site, p_next.site)
            top_parent.arc_points[0] = p_prev.site


        # Remove other circle events that use the arc
        # This can only be the next or previous leaves.
        delete_circle_event(p_next, event_queue)
        delete_circle_event(p_prev, event_queue)

        # Step 2
        center_of_circle, r = define_circle(
            p_prev.site, p.site, p_next.site
        )
        if center_of_circle is None:  # TODO: REMOVE
            raise ValueError("Circle center is None in handle_circle_event")
        vertex = Vertex(
            center_of_circle.x, center_of_circle.y, None
        )  # TODO: Set edge reference (if needed)

        # print("")
        # print(f"Center of circle: {center_of_circle.x, center_of_circle.y}, r: {r}")
        # print(" ")

        vertex.edge = Edge(vertex, None, None, None, None)

        new_edge = Edge(Point(vertex.x, vertex.y), vertex.edge, None, None, None)  # The edge of the new breakpoint
        vertex.edge.twin = new_edge
        # print("new edge origin on init: ", new_edge.origin)
        # TODO: check if all the pointers are set correctly
        if p_is_left_child:  # Parent is the breakpoint coming from the right
            # print("Parent is coming from right")
            # print("Parent edge origin: ", parent.edge.origin)
            # print("Parent twin edge origin: ", parent.edge.twin.origin)
            # print("Grand parent edge origin: ", top_parent.edge.origin)
            # print("Grand parent twin edge origin: ", top_parent.edge.twin.origin)
            new_edge.set_next(parent.edge)
            parent.edge.twin.set_next(top_parent.edge)
            parent.edge.origin = vertex
            top_parent.edge.origin = vertex
            vertex.edge.set_prev(top_parent.edge.twin)
        else:  # Parent is the breakpoint coming from the left
            # print("Parent is coming from left")
            # print("Parent edge origin: ", parent.edge.origin)
            # print("Parent twin edge origin: ", parent.edge.twin.origin)
            # print("Grand parent edge origin: ", top_parent.edge.origin)
            # print("Grand parent twin edge origin: ", top_parent.edge.twin.origin)
            new_edge.set_next(top_parent.edge)
            top_parent.edge.twin.set_next(parent.edge)
            top_parent.edge.origin = vertex
            parent.edge.origin = vertex
            vertex.edge.set_prev(parent.edge.twin)
        # print("After:")
        # print("Parent edge origin: ", parent.edge.origin)
        # print("Parent twin edge origin: ", parent.edge.twin.origin)
        # print("Grand parent edge origin: ", top_parent.edge.origin)
        # print("Grand parent twin edge origin: ", top_parent.edge.twin.origin)
        top_parent.edge = new_edge
        # print("Top parent: ", top_parent.arc_points, " new edge origin: ", top_parent.edge.origin)

        # TODO: Make less hacky
        if dcel is None:
            dcel = vertex.edge

        
        print("Tree before after")
        p_prev.print_tree(event.key)    
        print()    

        # Step 3
        if p_prev_prev is not None:
            # TODO: Set top_parent as either left_middle_arc or right_middle_arc based on p_is_left_child
            check_circle_event_for_site_event(p_prev_prev, p_prev, p_next, event_queue, event.key)
        if p_next_next is not None:
            # TODO: Set top_parent as either left_middle_arc or right_middle_arc based on p_is_left_child
            check_circle_event_for_site_event(p_prev, p_next, p_next_next, event_queue,  event.key)  
        # print("After check circle events: top parent: ", top_parent.arc_points, " new edge origin: ", top_parent.edge.origin)
        print("Tree after")
        p_prev.print_tree(event.key)        


    sweep_line_y = 0
    while not event_queue.is_empty():
        event = event_queue.pop()
        if isinstance(event, SiteEvent):
            # handle_site_event(event)
            print("In site event: ", event.site)
            sweep_line_y = event.site.y # TODO: Make prettier
            status.add(event.site, event.site.y)
            # print("After site event:")
            # status.print_tree()
        else:
            event.middle_leaf.circle_event = None
            print("In circle event: ", event.middle_leaf.site)
            sweep_line_y = event.key # TODO: Make prettier
            handle_circle_event(event)
            # print("After circle event:")
            # status.print_tree()
            print()
            print()
            print()


    sweep_line_y -= 10
    status.update_breakpoints(sweep_line_y)

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
