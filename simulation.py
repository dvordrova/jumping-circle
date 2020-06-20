from threading import Thread
from time import sleep
from pyrr import Vector3
from itertools import combinations, chain

import numpy as np

from drawers import TrianglesDrawer, LinesDrawer, get_drawer_creator
from figures import Circle, Rope
from utils import Point, Color
from shaders.shadersProgram import ShadersProgram


class Simulation(Thread):
    def __init__(self, camera_view, projection_view):
        super(Simulation, self).__init__()
        # self._gravity = Vector3([0, 0, 0], dtype=np.float32)
        self._gravity = Vector3([0, -0.098, 0], dtype=np.float32)
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
                center=Point(550, 550, color=Color(1., 0., 0.)),
                radius=20,
                initial_velocity=Vector3([-1, -1, 0], dtype=np.float32),
                gravity=self._gravity
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
                center=Point(200, 350),
                radius=20,
                initial_velocity=Vector3([.5, 2, 0], dtype=np.float32),
                gravity=self._gravity
            )
        ]
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
                left=Point(100, 220, color=Color(1., 0., 0.)),
                right=Point(550, 230),
                segments_count=10
            )
        ]
        self._is_running = True

        self._camera_view = camera_view
        self._projection_view = projection_view
    
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
                center=Point(x, y),
                radius=20,
                initial_velocity=Vector3([0, 0, 0], dtype=np.float32),
                gravity=self._gravity
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
        for c1, c2 in combinations(self._circles, 2):
            c1.collide_with_circle(c2)
            c2.collide_with_circle(c1)
        for r in self._ropes:
            r.collide_with_circles(self._circles)
        for c in self._circles:
            c.move()
        for r in self._ropes:
            r.move_around_circles(self._circles)
