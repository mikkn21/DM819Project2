
from dataclasses import dataclass
from sortedcontainers import SortedListWithKey
from point import Point

@dataclass
class Event:
    key: float

class SiteEvent(Event):
    def __init__(self, site: Point):
        super().__init__(site.y)
        self.site = site

class CircleEvent(Event):
    def __init__(self, top_site: Point, circle_bottom_y: float):
        super().__init__(circle_bottom_y)
        self.top_site = top_site

class EventQueue:
    def __init__(self, events: list[SiteEvent | CircleEvent] = []):
        self.events = SortedListWithKey(events, key = lambda event: event.key)

    def add(self, event: SiteEvent | CircleEvent) -> None:
        self.events.add(event)

    def pop(self) -> SiteEvent | CircleEvent:
        return self.events.pop()

