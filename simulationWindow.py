from threading import Thread

import glfw
from OpenGL.GL import glViewport, glClearColor, glClear
from OpenGL.GL import GL_COLOR_BUFFER_BIT

from simulation import Simulation
from views import ProjectionView, CameraView


class SimulationWindow(Thread):
    def __init__(self, width: int = 1020, height: int = 720):
        super(SimulationWindow, self).__init__()
        self._width = width
        self._height = height
        self._is_running = True
        self.projection = ProjectionView(width, height)
        self.camera_view = CameraView()
        self._simulation = Simulation(self.camera_view, self.projection)

        self._cursor_x = 0
        self._cursor_y = 0

        self._indices = []

    def window_size_callback(self, _, width, height):
        print(f"new width={width}, new height={height}")
        glViewport(0, 0, width, height)
        self.projection.width = width
        self.projection.height = height
    
    def cursor_pos_callback(self, _, x, y):
        self._cursor_x = x
        self._cursor_y = self._height - y
    
    def mouse_button_callback(self, _, button, action, mods):
        if action == glfw.RELEASE:
            self._simulation.create_circle(self._cursor_x, self._cursor_y)

    def run(self):
        self._init_glfw()
        glClearColor(0, 0.1, 0.2, 1.)
        self._simulation.start()
        while self._simulation.is_alive() and self._is_running and not glfw.window_should_close(self._window):
            glfw.swap_buffers(self._window)
            glClear(GL_COLOR_BUFFER_BIT)
            self._simulation.draw()
            glfw.poll_events()
        self._simulation.stop()
        glfw.terminate()
        self._simulation.join()

    def stop(self):
        self._is_running = False

    def _init_glfw(self):
        if not glfw.init():
            raise Exception("glfw can not be initialized")
        glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
        self._window = glfw.create_window(self._width, self._height, "Bouncing circle", None, None)
        if not self._window:
            glfw.terminate()
            raise Exception("glfw window can not be created")
        glfw.set_window_pos(self._window, 340, 140)
        glfw.show_window(self._window)
        glfw.set_window_size_limits(self._window, 500, 500, glfw.DONT_CARE, glfw.DONT_CARE)

        # callbacks
        glfw.set_window_size_callback(self._window, self.window_size_callback)
        glfw.set_mouse_button_callback(self._window, self.mouse_button_callback)
        glfw.set_cursor_pos_callback(self._window, self.cursor_pos_callback)

        glfw.make_context_current(self._window)
        glfw.swap_interval(1)
