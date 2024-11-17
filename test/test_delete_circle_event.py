from events import CircleEvent, EventQueue, SiteEvent
from fortunes import delete_circle_event_if_using
from point import Point
from tree import *



def test_delete_circle_event_if_using():
    points = [Point(30, 110), Point(60, 140), Point(90, 120)]
    event_queue = EventQueue([SiteEvent(p) for p in points])

    root = Node(None, None, None, [], None)
    node_left = Node(None, None, root, [], None)
    root.left = node_left
    leaf1 = Leaf(Point(30, 110), node_left, None)
    node_left.left = leaf1
    leaf2 = Leaf(Point(60, 140), node_left, None)
    node_left.right = leaf2
    leaf3 = Leaf(Point(90, 120), root, None)
    root.right = leaf3

    next_leaf = leaf1.next_leaf()
    next_next_leaf = next_leaf.next_leaf()
    prev_leaf = leaf3.prev_leaf()
    prev_prev_leaf = prev_leaf.prev_leaf()

    assert id(next_leaf) == id(leaf2)
    assert id(next_next_leaf) == id(leaf3)
    assert id(prev_leaf) == id(leaf2)
    assert id(prev_prev_leaf) == id(leaf1)
    
    circle_event = CircleEvent(leaf2, 50.0) # Example key (not important)
    leaf2.circle_event = circle_event
    leaf1.circle_event = circle_event
    assert event_queue.size == 3
    event_queue.add(circle_event)  
    assert event_queue.size == 4
    
    assert(leaf1.circle_event is not None)
    delete_circle_event_if_using(leaf2, leaf1, event_queue)
    print(leaf1.next_leaf().site)
    assert id(leaf1.next_leaf()) == id(leaf2)
    assert(leaf1.circle_event is None)

    assert event_queue.size == 3

    
