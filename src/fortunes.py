
import math
from point import Point
from events import *
from tree import *
from dcel import *
import numpy as np

def fortunes(points: list[Point]) -> None:
    event_queue = EventQueue([SiteEvent(p) for p in points])
    
    status = Tree(None)
    dcel = None 

    while not event_queue.is_empty():
        event = event_queue.pop()
        if isinstance(event, SiteEvent):
            handle_site_event(event)
        else:
            handle_circle_event(event)
    # TODO: Step 7
    # TODO: Step 8


    def handle_site_event(event: SiteEvent) -> None:
        # step 1
        if status.isEmpty():
            status.add(Leaf(event.site))
            return
        
        # step 2
        alpha = status.find_above(event.site.x)
        if alpha.circle_event != None:
            event_queue.remove(alpha.circle_event)
            alpha.circle_event = None

        # step 3
        subtree = create_subtree(alpha, event.site)
        subtree.parent = alpha.parent
        subtree.parent.replace_child(alpha, subtree)
        
        # step 4 
        internal_node1 = subtree
        internal_node2 = subtree.left
        internal_node1.edge = Edge(internal_node1.find_breakpoint(), None, None, None, None)
        internal_node2.edge = Edge(internal_node2.find_breakpoint(), internal_node1.edge, None, None, None)
        internal_node1.edge.twin = internal_node2.edge

        # step 5
        # consecutive arcs to the right of the new arc
        p_i = subtree.left.right
        p_j = p_i.next_leaf()
        p_k = p_j.next_leaf()
        check_circle_event(p_i, p_j, p_k)

        # consecutive arcs to the left of the new arc
        p_i = subtree.left.right
        p_j = p_i.prev_leaf()
        p_k = p_j.prev_leaf()
        check_circle_event(p_i, p_j, p_k)       
        

    def handle_circle_event(event: CircleEvent) -> None:
        # step 1 
        status.remove(event.leaf) 
        # TODO: Assuming that the removed element is replaced all the way up the tree with the left-most leaf.
        #       Also, assume that it's always the middle arc that is removed by a circle event, i.e., it always has a leaf to the left and to the right of it.
        #       Check with Kim if this is correct 
        
        # Remove other circle events that use the arc
        p_next = event.leaf.next_leaf()     
        p_next_next = p_next.next_leaf()

        p_prev = event.leaf.prev_leaf()
        p_prev_prev = p_prev.prev_leaf()

        delete_circle_event_if_using(event.leaf, p_next)
        delete_circle_event_if_using(event.leaf, p_next_next)
        delete_circle_event_if_using(event.leaf, p_prev)
        delete_circle_event_if_using(event.leaf, p_prev_prev)
            
        # update the tree
        event.leaf.parent.parent.arc_points[0] = p_prev.site
        event.leaf.parent.parent.left = p_prev.site
        p_prev.parent = event.leaf.parent.parent


        # step 2 

        

    def create_subtree(old, new) -> Node:
        """
        Returns the root of the subtree.
        Does not change the old leaf.
        """
        raise NotImplementedError()

    def check_circle_event(new_node, middle, end) -> None:
        """
        Checks if there is a circle event between the three sites and adds it to the event_queue if there 
        """
        raise NotImplementedError()

        
       
     
    # def find_breakpoint(site1: Point, site2: Point) -> Point:
    #     """
    #     Returns the intersection between the two parabolas that are defined by the two sites
    #     """
    #     raise NotImplementedError()
    
    def find_breakpoint(site1: Point, site2: Point, sweep_line_y: float) -> Point:
        """
        Returns the breakpoint between the two parabolas defined by site1 and site2
        at the current sweep line position.
        """
        x1, y1 = site1
        x2, y2 = site2
        l = sweep_line_y

        # Handle the special case when both sites are at the same y-coordinate
        if y1 == y2:
            x = (x1 + x2) / 2.0
            y = ( (x - x1)**2 ) / (2 * (y1 - l)) + (y1 + l) / 2.0
            return Point(x, y)

        # Compute coefficients for the quadratic equation
        # a*x^2 + b*x + c = 0
        d1 = 2.0 * (y1 - l)
        d2 = 2.0 * (y2 - l)

        # Avoid division by zero (sites below the sweep line)
        if d1 == 0 or d2 == 0:
            raise ValueError("Division by zero encountered; site(s) may be below the sweep line.")

        # Coefficients of the quadratic equation
        a = 1.0 / d1 - 1.0 / d2
        b = -2.0 * ( x1 / d1 - x2 / d2 )
        c = ( x1**2 + y1**2 - l**2 ) / d1 - ( x2**2 + y2**2 - l**2 ) / d2

        # Check if the equation is linear (a is zero)
        if abs(a) < 1e-10:
            # Linear equation: a is approximately zero
            x = -c / b
        else:
            # Quadratic equation
            discriminant = b**2 - 4 * a * c
            if discriminant < 0:
                raise ValueError("No real intersection points (discriminant < 0).")

            sqrt_discriminant = math.sqrt(discriminant)

            # Calculate both possible x values
            x1_root = (-b + sqrt_discriminant) / (2 * a)
            x2_root = (-b - sqrt_discriminant) / (2 * a)

            # Select the correct root based on context
            # For Fortune's algorithm, the correct breakpoint depends on the relative positions
            # Here, we'll choose the breakpoint with the larger y-coordinate
            y1_root = ( (x1_root - x1)**2 ) / (2 * (y1 - l)) + (y1 + l) / 2.0
            y2_root = ( (x2_root - x1)**2 ) / (2 * (y1 - l)) + (y1 + l) / 2.0

            if y1_root > y2_root:
                x, y = x1_root, y1_root
            else:
                x, y = x2_root, y2_root

        return Point(x, y)
 


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
    