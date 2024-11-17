from events import CircleEvent, EventQueue, SiteEvent
from fortunes import delete_circle_event
from point import Point
from tree import *



def test_delete_circle_event():
    points = [Point(30, 110), Point(60, 140), Point(90, 120)]
    event_queue = EventQueue([SiteEvent(p) for p in points])

    leaf = Leaf(Point(30, 110), None, None)
    circle_event = CircleEvent(leaf, 50.0) # Example key (not important)
    leaf.circle_event = circle_event

    # ==================================

    assert event_queue.size == 3
    event_queue.add(circle_event)  
    assert event_queue.size == 4
    delete_circle_event(leaf,event_queue)
    assert event_queue.size == 3

    
