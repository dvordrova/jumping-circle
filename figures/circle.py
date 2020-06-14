import math
from math import pi
from typing import Callable, Any

from utils import Point, Color
from views import ModelView


class Circle:
    def __init__(self,
                 create_drawer: Callable[..., Any],
                 center: Point,
                 radius: float,
                 initial_velocity: Point,
                 color: Color = Color(0, 1, 0),
                 sectors_count=100
                 ):
        points = [Point(0, 0, color=center.color)]
        for i in range(sectors_count + 1):
            x = math.cos(i * 2 * pi / sectors_count)
            y = math.sin(i * 2 * pi / sectors_count)
            points.append(Point(x, y, color=color))
        triangles = ((0, i, i + 1) for i in range(1, sectors_count + 1))

        self._drawer = create_drawer(points, triangles)
        self._center = center
        self._radius = radius
        self._velocity = initial_velocity

    def update(self):
        next_center = self._center + self._velocity
        if next_center.x - self._radius < 0:
            self._velocity = Point(-self._velocity.x, self._velocity.y)
        if next_center.y - self._radius < 0:
            self._velocity = Point(self._velocity.x, -self._velocity.y)
        self._center += self._velocity

    def update_velocity(self, gravity):
        self._velocity += gravity

    def draw(self):
        self._drawer.draw(ModelView(scale=self._radius, position=self._center))
