from itertools import chain
from typing import List

import numpy as np
from OpenGL.GL import glBindBuffer, glGenVertexArrays, glBindVertexArray, glGenBuffers, glBufferData, GL_ARRAY_BUFFER, \
    GL_STATIC_DRAW, GL_FALSE, GL_FLOAT, glVertexAttribPointer, glEnableVertexAttribArray, GL_ELEMENT_ARRAY_BUFFER, \
    GL_LINE_STRIP, ctypes, glDrawElements, GL_UNSIGNED_INT

from drawers.basicDrawer import BasicDrawer
from utils import Point, Color
from shaders.shadersProgram import ShadersProgram

POSITION_LAYOUT = 0
COLOR_LAYOUT = 1


class LinesDrawer(BasicDrawer):
    def __init__(self, shaders_program: ShadersProgram, points: List[Point]):
        self._shaders_program = shaders_program

        self._VAO = glGenVertexArrays(1)
        glBindVertexArray(self._VAO)

        self.vertices = np.array(
            list(chain.from_iterable(p.as_array() for p in points)),
            dtype=np.float32
        )
        self._indices = np.array(
            list(range(len(points))),
            dtype=np.uint32
        )

        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(POSITION_LAYOUT)
        glVertexAttribPointer(POSITION_LAYOUT, Point.size(), GL_FLOAT, GL_FALSE,
                              self.vertices.itemsize * (Point.size() + Color.size()), ctypes.c_void_p(0))

        glEnableVertexAttribArray(COLOR_LAYOUT)
        glVertexAttribPointer(COLOR_LAYOUT, Color.size(), GL_FLOAT, GL_FALSE,
                              self.vertices.itemsize * (Point.size() + Color.size()),
                              ctypes.c_void_p(self.vertices.itemsize * Point.size()))

        ebo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self._indices.nbytes, self._indices, GL_STATIC_DRAW)

        glBindVertexArray(0)

    def draw(self, model):
        glBindVertexArray(self._VAO)
        self._shaders_program.scale = model.scale
        self._shaders_program.position = model.position
        self._shaders_program.use()
        glDrawElements(GL_LINE_STRIP, len(self._indices), GL_UNSIGNED_INT, None)
