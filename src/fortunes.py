
import math
from point import Point
from events import *
from tree import *
from dcel import *
import numpy as np
from find_breakpoint import find_breakpoint

def fortunes(points: list[Point]) -> None:
    event_queue = EventQueue([SiteEvent(p) for p in points])
    
    status = Tree(None, event_queue)
    dcel = None 

    while not event_queue.is_empty():
        event = event_queue.pop()
        if isinstance(event, SiteEvent):
            # handle_site_event(event)
            status.add(event.site)
        else:
            handle_circle_event(event)
    # TODO: Step 7
    # TODO: Step 8

    def handle_circle_event(event: CircleEvent) -> None:
        # Step 1 
        status.remove(event.leaf) 
        # TODO: Assuming that the removed element is replaced all the way up the tree with the left-most leaf.
        #       Also, assume that it's always the middle arc that is removed by a circle event, i.e., it always has a leaf to the left and to the right of it.
        #       Check with Kim if this is correct 
        
        # Get neighbour leaves
        p_next = event.leaf.next_leaf()     
        p_next_next = p_next.next_leaf()
        p_prev = event.leaf.prev_leaf()
        p_prev_prev = p_prev.prev_leaf()

        # Update the tuples representing the breakpoints at the internal nodes
        # TODO: Can we assume we can do this in all cases?
        #       If it works, it might be because we don't balance the tree, and we always create a subtree in the format below.
        event.leaf.parent.parent.arc_points[0] = p_prev.site
        event.leaf.parent.parent.left = p_prev.site
        p_prev.parent = event.leaf.parent.parent
    
        # Remove other circle events that use the arc
        delete_circle_event_if_using(event.leaf, p_next)
        delete_circle_event_if_using(event.leaf, p_next_next)
        delete_circle_event_if_using(event.leaf, p_prev)
        delete_circle_event_if_using(event.leaf, p_prev_prev)

        # Step 2
        center_of_circle = center_of_circle_from_three_points(p_prev.site, event.leaf.site, p_next.site) 
        vertex = Vertex(center_of_circle.x, center_of_circle.y, None) # TODO: Set edge reference (if needed)
        

        parent: Node = event.middle_leaf.parent
        grand_parent: Node = parent.parent
        old_breakpoint = event.middle_leaf.parent.edge
        vertex.edge = Edge(vertex, None, None, None, None)
        new_node = status.find_above(center_of_circle.x).parent # TODO: Maybe move into status.remove so we don't have to search in the tree to find it but rather just have it
        new_node.edge = Edge(Point(vertex.x, vertex.y), vertex.edge, None, None, None)
        vertex.edge.twin = new_node.edge
        if event.middle_leaf == parent.right: # Parent is the breakpoint coming from the left
            new_node.edge.next = parent.edge
            vertex.edge.prev = grand_parent.edge.twin
        else: # Parent is the breakpoint coming from the right
            new_node.edge.next = grand_parent.edge
            vertex.edge.prev = parent.edge.twin
        

        # Step 3

        
        

    def delete_circle_event_if_using(using_leaf, leaf) -> None:
        """
        Deletes the circle event on leaf from the event_queue if the using_leaf is a part of the circle event
        Except if the using_leaf is in the middle :)
        """
        if leaf.circle_event != None and (leaf.circle_event.left_arc == using_leaf or leaf.circle_event.right_arc == using_leaf):
            event_queue.remove(leaf.circle_event)
            leaf.circle_event = None

def center_of_circle_from_three_points(p1, p2, p3) -> Point:
    """
    Returns the center of the circle that goes through the three points
    """
    m1 = np.array(
        [
            [2*p1.x, 2*p1.y, 1],
            [2*p2.x, 2*p2.y, 1],
            [2*p3.x, 2*p3.y, 1]
        ]
    )
    m2 = np.array(
        [ 
            [-(p1.x**2 + p1.y**2)],
            [-(p2.x**2 + p2.y**2)],
            [-(p3.x**2 + p3.y**2)]
        ]
    )
    a, b, *_ = np.linalg.solve(m1, m2)
    point = Point(-a[0], -b[0])
    print(point)
    return point

