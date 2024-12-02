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
    def __init__(
        self, sites: list[Point], circle_bottom_y: float
    ):  # middle_leaf is a Leaf but to avoid circular dependency, it cannot be type hinted
        super().__init__(circle_bottom_y)
        if len(sites) != 3:
            raise Exception("Circle events need 3 sites but were not given 3")
        self.sites = sites
    
    def __eq__(self, other: CircleEvent) -> bool:
        for i in range(len(self.sites)):
            if self.sites[i] != other.sites[i]:
                return False
        return True
    
    def __hash__(self) -> int:
        return hash(tuple(self.sites))


class EventQueue:
    def __init__(self, events: list[SiteEvent | CircleEvent] = []):
        self.events = SortedListWithKey(events, key=lambda event: event.key)
        self.size = len(events)

    def add_site(self, event: SiteEvent) -> None:
        self.events.add(event)
        self.size += 1
    
    def add_circle(self, event: CircleEvent) -> None:
        if event not in self.events:
            self.events.add(event)
            self.size += 1
        else:
            print("Event already in queue")

    def pop(self) -> SiteEvent | CircleEvent:
        """
        Removes and returns the event with the highest y-coordinate.
        """
        self.size -= 1
        return self.events.pop()

    def remove(self, event: SiteEvent | CircleEvent) -> None:
        self.events.remove(event)
        self.size -= 1

    def is_empty(self) -> bool:
        return self.size <= 0
