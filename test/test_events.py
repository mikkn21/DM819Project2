
from events import *
from point import Point

def test_simple():
    queue = EventQueue([
        SiteEvent(Point(2,4)),
        SiteEvent(Point(3,5)),
        SiteEvent(Point(1,3)),
        SiteEvent(Point(0,2)),
        SiteEvent(Point(4,6)),
    ])

    assert queue.pop().site == Point(4,6)
    assert queue.pop().site == Point(3,5)
    assert queue.pop().site == Point(2,4)
    assert queue.pop().site == Point(1,3)
    assert queue.pop().site == Point(0,2)

def test_circle_events():
    queue = EventQueue([
        SiteEvent(Point(2,4)),
        SiteEvent(Point(3,5)),
        CircleEvent(Point(3,8), 3),
        SiteEvent(Point(0,2)),
        SiteEvent(Point(4,6)),
    ])

    queue.pop()
    queue.pop()
    queue.pop()

    event = queue.pop()
    # assert event.top_site == Point(3,8) and event.key == 3


