
from __future__ import annotations
from dataclasses import dataclass
import math

@dataclass
class Point:
    x: float
    y: float

    def distance(self, other: Point) -> float:
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def is_close_to(self, other: Point, relative_diff: float = 1) -> bool:
        return math.isclose(self.x, other.x, rel_tol=relative_diff) and math.isclose(self.y, other.y, rel_tol=relative_diff)

    def __repr__(self) -> str:
        return f"Point({self.x:.2f}, {self.y:.2f})"

    def __str__(self) -> str:
        return f"Point({self.x:.2f}, {self.y:.2f})"

    def __eq__(self, other: object) -> bool:
        return (isinstance(other, Point) and 
                math.isclose(self.x, other.x) and math.isclose(self.y, other.y))

    def copy(self) -> Point:
        return Point(self.x, self.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __iter__(self):
        return iter((self.x, self.y))

    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)

