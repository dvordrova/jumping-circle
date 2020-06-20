from random import randint
from typing import Callable
from itertools import cycle

import numpy as np
from pyrr import Vector3
from pyrr.vector import interpolate, set_length
from pyrr import vector3

from drawers import BasicDrawer
from utils import Point, Color, ORIGINAL_POINT
from views import ModelView


class Rope:
    def __init__(self, create_drawer: Callable[..., BasicDrawer], left: Point, right: Point, segments_count=5):
        if not isinstance(segments_count, int) or segments_count < 3:
            raise RuntimeError(f"Can't create rope with segments_count={segments_count}")

        self._drawer = create_drawer([Point(0.0, 0.0, left.color), Point(1.0, 1.0, right.color)])
        self._elements = [Vector3(interpolate(left._vector, right._vector, delta)) + 
                          randint(-10, 10)*vector3.create_unit_length_x() + 
                          randint(-10, 10)*vector3.create_unit_length_y()  
                          for delta in np.linspace(0, 1, segments_count + 1)]
        self._forces = []

        SOFT = 1
        self.type = SOFT

        self._normal_segment_length = (left - right).length / segments_count
        self._k = 0.2

    def draw(self):
        for left, right in zip(self._elements, self._elements[1:]):
            self._drawer.draw(ModelView(
                scale=right - left,
                position=left)
            )
    
    # TODO: calculate forces for points, fix length and k

    @staticmethod
    def _is_segment_intersect_circle(left: Vector3, right: Vector3, circle):
        # optimization for many segments
        min_x = min(left.x, right.x) - circle.radius
        max_x = max(left.x, right.x) + circle.radius
        if not min_x <= circle.center.x <= max_x:
            return False
        min_y = min(left.y, right.y) - circle.radius
        max_y = max(left.y, right.y) + circle.radius
        if not min_y <= circle.center.y <= max_y:
            return False
        
        left_to_center = left - circle.center
        right_to_center = right - circle.center
        segment = left - right

        return left_to_center.length < circle.radius or right_to_center.length < circle.radius or \
               (
                   left_to_center | segment >= 0 and right_to_center | segment <= 0  # can check distance to segment
                   and abs(segment ^ left_to_center).z / segment.length <= circle.radius  # checking sitance, hack with living in z=0 plane
               )
    
    def collide_with_circles(self, circles):
        for c in circles:
            for i in range(len(self._elements) - 1):
                left = self._elements[i]
                right = self._elements[i + 1]

                if self._is_segment_intersect_circle(left, right, c):
                    for vertex_i, neigbour_i in zip(
                        cycle((i, i + 1)),
                        range(i - 1, i + 3)
                    ):
                        if not 0 <= neigbour_i < len(self._elements):
                            continue
                        direction = self._elements[vertex_i] - self._elements[neigbour_i]
                        force = Vector3(set_length(direction, 2 * self._k * (self._normal_segment_length - direction.length)))
                        c.add_force(force)
    
    def move_around_circles(self, circles):
        for c in circles:
            for i in range(len(self._elements) - 1):
                left = self._elements[i]
                right = self._elements[i + 1]

                if self._is_segment_intersect_circle(left, right, c):
                    if i != 0:
                        self._elements[i] += c.velocity
                        # c.add_forces()
                    if i + 1 != len(self._elements) - 1:
                        self._elements[i + 1] += c.velocity
        for i in range(len(self._elements) - 1):
            for vertex_i, neigbour_i in zip(
                cycle((i, i + 1)),
                range(i - 1, i + 3)
            ):
                if vertex_i in (0, len(self._elements) - 1):
                    continue
                if not 0 <= neigbour_i < len(self._elements):
                    continue
                direction = self._elements[vertex_i] - self._elements[neigbour_i]
                delta_x = self._normal_segment_length - direction.length
                force = Vector3(set_length(direction, self._k * delta_x))
                # print(i, direction, delta_x, force)
                self._elements[vertex_i] += force
