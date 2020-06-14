from threading import Thread
from time import sleep

from drawers import TrianglesDrawer, LinesDrawer, get_drawer_creator
from figures import Circle, Rope
from utils import Point
from shaders.shadersProgram import ShadersProgram


class Simulation(Thread):
    def __init__(self, camera_view, projection_view):
        super(Simulation, self).__init__()
        self.circle = Circle(
            create_drawer=get_drawer_creator(
                TrianglesDrawer,
                ShadersProgram(
                    camera_view,
                    projection_view,
                    vertex_shaders=['shaders-src/vertex.vert'],
                    fragment_shaders=['shaders-src/fragment.vert'])
            ),
            center=Point(250, 250),
            radius=20,
            initial_velocity=Point(.1, 0)
        )
        self.rope = Rope(
            create_drawer=get_drawer_creator(
                LinesDrawer,
                ShadersProgram(
                    camera_view,
                    projection_view,
                    vertex_shaders=['shaders-src/vertex.vert'],
                    fragment_shaders=['shaders-src/fragment.vert'])
            ),
            left=Point(50, 20),
            right=Point(500, 30)
        )
        self.gravity = Point(0, -0.005)
        self._is_running = True

    def run(self):
        while self._is_running:
            self.step()
            sleep(.01)

    def stop(self):
        self._is_running = False

    def draw(self):
        self.circle.draw()
        self.rope.draw()

    def step(self):
        self.circle.update()
        self.circle.update_velocity(self.gravity)
