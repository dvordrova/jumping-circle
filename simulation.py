from __future__ import annotations

from threading import Thread
from time import sleep
from pyrr import Vector3
from itertools import combinations, chain
from random import randint

import numpy as np

from drawers import TrianglesDrawer, LinesDrawer, get_drawer_creator
from figures import Circle, Rope
from utils import Point, random_color
from shaders.shadersProgram import ShadersProgram


class Simulation(Thread):
    def __init__(self, camera_view: CameraView, projection_view: ProjectionView):
        super(Simulation, self).__init__()
        self._gravity = Vector3([0, 0, 0], dtype=np.float32)
        self._gravity = Vector3([0, -0.02, 0], dtype=np.float32)
        self._ropes = [
            Rope(
                create_drawer=get_drawer_creator(
                    LinesDrawer,
                    ShadersProgram(
                        camera_view,
                        projection_view,
                        vertex_shaders=['shaders-src/vertex.vert'],
                        fragment_shaders=['shaders-src/fragment.vert'])
                ),
                left=Point(100, 200, color=random_color()),
                right=Point(600, 200, color=random_color()),
                segments_count=10
            ),  
            Rope(
                create_drawer=get_drawer_creator(
                    LinesDrawer,
                    ShadersProgram(
                        camera_view,
                        projection_view,
                        vertex_shaders=['shaders-src/vertex.vert'],
                        fragment_shaders=['shaders-src/fragment.vert'])
                ),
                left=Point(100, 500, color=random_color()),
                right=Point(600, 500, color=random_color()),
                segments_count=10
            )
        ]
        self._circles = [
            Circle(
                create_drawer=get_drawer_creator(
                    TrianglesDrawer,
                    ShadersProgram(
                        camera_view,
                        projection_view,
                        vertex_shaders=['shaders-src/vertex.vert'],
                        fragment_shaders=['shaders-src/fragment.vert'])
                ),
                center=Point(550, 550, color=random_color()),
                radius=10,
                initial_velocity=Vector3([-1, -1, 0], dtype=np.float32),
                gravity=self._gravity,
                color=random_color()
            ),
            Circle(
                create_drawer=get_drawer_creator(
                    TrianglesDrawer,
                    ShadersProgram(
                        camera_view,
                        projection_view,
                        vertex_shaders=['shaders-src/vertex.vert'],
                        fragment_shaders=['shaders-src/fragment.vert'])
                ),
                center=Point(350, 350, color=random_color()),
                radius=10,
                initial_velocity=Vector3([1, 1, 0], dtype=np.float32),
                gravity=self._gravity,
                color=random_color()
            )
        ]
        self._is_running = True

        self._camera_view = camera_view
        self._projection_view = projection_view
    
    def _is_circle_on_screen(self, circle: Circle):
        return not any((
            circle.center.x + circle.radius < 50,
            circle.center.y + circle.radius < 50,
            circle.center.x - circle.radius > self._projection_view.width - 50,
            circle.center.y - circle.radius > self._projection_view.height - 50,
        ))
    
    def create_circle(self, x, y):
        self._circles.append(
            Circle(
                create_drawer=get_drawer_creator(
                    TrianglesDrawer,
                    ShadersProgram(
                        self._camera_view,
                        self._projection_view,
                        vertex_shaders=['shaders-src/vertex.vert'],
                        fragment_shaders=['shaders-src/fragment.vert'])
                ),
                center=Point(x, y, color=random_color()),
                radius=10,
                initial_velocity=Vector3([0, 0, 0], dtype=np.float32),
                gravity=self._gravity,
                color=random_color()
            )
        )


    def run(self):
        while self._is_running:
            self.step()
            sleep(.01)

    def stop(self):
        self._is_running = False

    def draw(self):
        for o in chain(self._circles, self._ropes):
            o.draw()

    def step(self):
        self._circles = list(filter(self._is_circle_on_screen, self._circles))
        for c1, c2 in combinations(self._circles, 2):
            c1.collide_with_circle(c2)
            c2.collide_with_circle(c1)
        for r in self._ropes:
            r.collide_with_circles(self._circles)
        for o in chain(self._circles, self._ropes):
            o.move()

        for r in self._ropes:
            r.move_around_circles(self._circles)
