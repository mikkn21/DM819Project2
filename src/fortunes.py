from Timer import Timer
from point import Point
from events import *
from tree import *
from dcel import *
from tree import check_circle_event
from geometry import define_circle


def fortunes(points: list[Point]) -> Edge:
    event_queue = EventQueue([SiteEvent(p) for p in points])
    
    find_bp_timer = Timer()
    step_5a_timer = Timer()
    step_5b_timer = Timer()
    status = Tree(None, event_queue, find_bp_timer, step_5a_timer, step_5b_timer)
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

        grand_parent.replace_child(parent, parent.right if p_is_left_child else parent.left)

        if p_is_left_child:
            top_parent = grand_parent.find_parent(p_prev.site, p.site)
            top_parent.arc_points[1] = p_next.site
        else: 
            top_parent = grand_parent.find_parent(p.site, p_next.site)
            top_parent.arc_points[0] = p_prev.site

        # Remove other circle events that use the arc
        # This can only be the next or previous leaves.
        delete_circle_event(p_next, event_queue)
        delete_circle_event(p_prev, event_queue)

        # Step 2
        center_of_circle, r = define_circle(
            p_prev.site, p.site, p_next.site
        )
        
        vertex = Vertex(
            center_of_circle.x, center_of_circle.y, None
        )  
        vertex.edge = Edge(vertex, None, None, None)

        new_edge = Edge(Point(vertex.x, vertex.y), vertex.edge, None, None)  # The edge of the new breakpoint
        vertex.edge.twin = new_edge
        if p_is_left_child:  # Parent is the breakpoint coming from the right
            new_edge.set_next(parent.edge)
            parent.edge.twin.set_next(top_parent.edge)
            parent.edge.origin = vertex
            top_parent.edge.origin = vertex
            vertex.edge.set_prev(top_parent.edge.twin)
        else:  # Parent is the breakpoint coming from the left
            new_edge.set_next(top_parent.edge)
            top_parent.edge.twin.set_next(parent.edge)
            top_parent.edge.origin = vertex
            parent.edge.origin = vertex
            vertex.edge.set_prev(parent.edge.twin)
        top_parent.edge = new_edge

        if dcel is None:
            dcel = vertex.edge

        # Step 3
        if p_prev_prev is not None:
            check_circle_event(p_prev_prev, p_prev, p_next, None, None, event.key, event_queue)
          
        if p_next_next is not None:
            check_circle_event(p_prev, p_next, p_next_next, None, None, event.key, event_queue)  


    
    site_event_timer = Timer() 
    circle_event_timer = Timer()
    update_timer = Timer()
    sweep_line_y = 0
    while not event_queue.is_empty():
        event = event_queue.pop()
        if isinstance(event, SiteEvent):
            sweep_line_y = event.site.y
            site_event_timer.start() 
            status.add(event.site, event.site.y)
            site_event_timer.stop()
        else:
            sweep_line_y = event.key 
            circle_event_timer.start()
            handle_circle_event(event)
            circle_event_timer.stop()


    # We simulate the sweep line is a bit lower and
    # update the breakpoint. This is necessary so that all
    # infinite edges still have a direction.
    sweep_line_y -= 10
    update_timer.start()
    status.update_breakpoints(sweep_line_y) # Force update all breakpoints by moving the sweep line down
    update_timer.stop()

    print(f"Site event total time: {site_event_timer.get_total_time()} ")
    print(f"Site circle total time: {circle_event_timer.get_total_time()} ")
    print(f"update total time: {update_timer.get_total_time()} ")
    print(f"Find breakpoint total time: {find_bp_timer.get_total_time()} ")
    print(f"Step 5a total time: {step_5a_timer.get_total_time()} ")
    print(f"Step 5b total time: {step_5b_timer.get_total_time()} ")
    return dcel

def delete_circle_event(leaf: Leaf, event_queue: EventQueue) -> None:
    """
    Deletes the circle event on leaf from the event_queue if it exists.
    """
    if leaf.circle_event is not None:
        event_queue.remove(leaf.circle_event)
        leaf.circle_event = None
