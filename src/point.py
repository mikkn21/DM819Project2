
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"

    def __str__(self) -> str:
        return f"Point({self.x}, {self.y})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Point) and (self.x, self.y) == (other.x, other.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __iter__(self):
        return iter((self.x, self.y))

    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)

