
from __future__ import annotations
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
    def __init__(self, middle_leaf, circle_bottom_y: float): # middle_leaf is a Leaf but to avoid circular dependency, it cannot be type hinted
        super().__init__(circle_bottom_y)
        self.middle_leaf = middle_leaf

class EventQueue:
    def __init__(self, events: list[SiteEvent | CircleEvent] = []):
        self.events = SortedListWithKey(events, key = lambda event: event.key)
        self.size = len(events)

    def add(self, event: SiteEvent | CircleEvent) -> None:
        self.events.add(event)
        self.size += 1

    def pop(self) -> SiteEvent | CircleEvent:
        """
        Removes and returns the event with the highest y-coordinate.
        """
        self.size -= 1
        return self.events.pop()

    def remove(self, event: SiteEvent | CircleEvent) -> None:
       self.events.remove(event)

    def is_empty(self) -> bool:
        return self.size <= 0
        

