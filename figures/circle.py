from __future__ import annotations

import math
from math import pi
from typing import List, Callable, Any

import numpy as np
from pyrr import Vector3
from pyrr.vector import set_length

from utils import Point, Color
from views import ModelView


class Circle:
    def __init__(self,
                 create_drawer: Callable[..., Any],
                 center: Point,
                 radius: float,
                 initial_velocity: Vector3,
                 color: Color = Color(0, 1, 0),
                 sectors_count=100,
                 gravity=Vector3([0, 0, 0], dtype=np.float32)
                 ):
        points = [Point(0, 0, color=center.color)]
        for i in range(sectors_count + 1):
            x = math.cos(i * 2 * pi / sectors_count)
            y = math.sin(i * 2 * pi / sectors_count)
            points.append(Point(x, y, color=color))
        triangles = ((0, i, i + 1) for i in range(1, sectors_count + 1))

        self._drawer = create_drawer(points, triangles)
        self._center = center._vector
        self._radius = radius
        self._velocity = initial_velocity
        self._forces: List[Vector3] = []
        self._gravity = gravity

        self.mass = 0.1 * radius**2
    
    @property
    def center(self):
        return self._center
    
    @property
    def radius(self):
        return self._radius
    
    @property
    def velocity(self):
        return self._velocity
    
    def add_force(self, force: Vector3):
        self._forces.append(force)

    def _apply_forces(self):
        for f in self._forces:
            self._velocity += f / self.mass
        self._velocity += self._gravity
        self._forces = []

    def move(self):
        self._apply_forces()
        self._center += self._velocity
    
    def gravity(self, acceleration):
        self._velocity += acceleration

    def draw(self):
        self._drawer.draw(ModelView(
            scale=Vector3([self._radius, self._radius, self._radius]),
            position=self._center
        ))
    
    def collide_with_circle(self, other: Circle):
        # optimization for many circles
        sum_radius = self.radius + other.radius
        min_x = self.center.x - sum_radius
        max_x = self.center.x + sum_radius
        if not min_x <= other.center.x <= max_x:
            return
        min_y = self.center.y - sum_radius
        max_y = self.center.y + sum_radius
        if not min_y <= other.center.y <= max_y:
            return

        if (self._center - other._center).length < self._radius + other._radius:
            force_vector = self._center - other._center
            force_length = abs((force_vector | self._velocity) + (force_vector | other._velocity)) / force_vector.length
            self.add_force(set_length(force_vector, other.mass * force_length))
