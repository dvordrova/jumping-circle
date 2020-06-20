from random import randint
from typing import Callable
from itertools import cycle
from copy import copy
from collections import defaultdict
from datetime import timedelta

import numpy as np
from pyrr import Vector3
from pyrr.vector import interpolate, set_length
from pyrr import vector3

from drawers import BasicDrawer
from utils import Point, Color
from views import ModelView


class Rope:
    def __init__(self, create_drawer: Callable[..., BasicDrawer], left: Point, right: Point, segments_count=5):
        if not isinstance(segments_count, int) or segments_count < 3:
            raise RuntimeError(f"Can't create rope with segments_count={segments_count}")

        self._drawer = create_drawer([Point(0.0, 0.0, left.color), Point(1.0, 1.0, right.color)])
        self._elements = [Vector3(interpolate(left._vector, right._vector, delta)) + 
                          + randint(-10, 10)*vector3.create_unit_length_x()
                          + randint(-10, 10)*vector3.create_unit_length_y()  
                          for delta in np.linspace(0, 1, segments_count + 1)]
        self._default_element_positions = [Vector3(interpolate(left._vector, right._vector, delta))
                                           for delta in np.linspace(0, 1, segments_count + 1)]
        self._forces = []
        self._normal_segment_length = 0
        self._k = 1
        self._velocities = [Vector3() for i in range(segments_count + 1)]
        self._forces = defaultdict(Vector3)
        self._was_moved = True

        self._joint_mass = 5


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
                   and abs((segment ^ left_to_center).z) / segment.length <= circle.radius  # checking distance, hack with living in z=0 plane
               )
    
    @property
    def forces(self):
        if self._was_moved:
            self._forces = defaultdict(Vector3)
            for i in range(1, len(self._elements) - 1):
                direction = self._elements[i] - self._default_element_positions[i]
                if abs(self._normal_segment_length - direction.length) > 0.00001:
                    self._forces[i] += set_length(direction, self._k * (self._normal_segment_length - direction.length))
            self._was_moved = False
        return self._forces
    
    def collide_with_circles(self, circles):
        # TODO: case when it's end point
        force_was_applied = set()
        for c in circles:
            for i in range(len(self._elements) - 1):
                if self._is_segment_intersect_circle(self._elements[i], self._elements[i + 1], c):
                    if i not in force_was_applied:
                        c.add_force(self.forces[i])
                    if i + 1 not in force_was_applied:
                        c.add_force(self.forces[i + 1])
                    force_was_applied.update((i, i + 1))
            
    def move_around_circles(self, circles):
        # TODO: case when it's end point
        for c in circles:
            for i in range(len(self._elements) - 1):
                left = self._elements[i]
                right = self._elements[i + 1]

                if self._is_segment_intersect_circle(left, right, c):
                    segment = left - right
                    left_to_center = left - c.center

                    height = (segment ^ left_to_center).z
                    length_delta = (c.radius - abs(height) / segment.length) * np.sign(height)
                    delta = set_length(- segment ^ vector3.create_unit_length_z(), length_delta)
                    if i != 0:
                        self._elements[i] += delta
                    if i + 1 != len(self._elements) - 1:
                        self._elements[i + 1] += delta

    def _apply_forces(self):
        for i, f in self.forces.items():
            self._velocities[i] += f / self._joint_mass
    
    def move(self):
        self._apply_forces()
        for i, v in enumerate(self._velocities):
            self._elements[i] += v
            self._velocities[i] = v * 0.5  # to avoid haotic movments of rope
        self._was_moved = True

