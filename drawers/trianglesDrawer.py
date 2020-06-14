from itertools import chain
from typing import List, Tuple, Iterable

import numpy as np
from OpenGL.GL import glBindBuffer, glGenVertexArrays, glBindVertexArray, glGenBuffers, glBufferData, GL_ARRAY_BUFFER, \
    GL_STATIC_DRAW, GL_FALSE, GL_FLOAT, glVertexAttribPointer, glEnableVertexAttribArray, GL_ELEMENT_ARRAY_BUFFER, \
    GL_TRIANGLES, glDrawElements, GL_UNSIGNED_INT, ctypes

from drawers.basicDrawer import BasicDrawer
from utils import Point, Color
from shaders.shadersProgram import ShadersProgram
from views import ModelView

POSITION_LAYOUT = 0
COLOR_LAYOUT = 1


class TrianglesDrawer(BasicDrawer):
    def __init__(self, shaders_program: ShadersProgram, points: List[Point], triangles: Iterable[Tuple[int, int, int]]):
        self._shaders_program = shaders_program

        self._VAO = glGenVertexArrays(1)
        glBindVertexArray(self._VAO)

        vertices = np.array(
            list(chain.from_iterable(p.as_array() for p in points)),
            dtype=np.float32
        )
        self._indices = np.array(
            list(chain.from_iterable(t for t in triangles)),
            dtype=np.uint32
        )

        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(POSITION_LAYOUT)
        glVertexAttribPointer(POSITION_LAYOUT, Point.size(), GL_FLOAT, GL_FALSE,
                              vertices.itemsize * (Point.size() + Color.size()), ctypes.c_void_p(0))

        glEnableVertexAttribArray(COLOR_LAYOUT)
        glVertexAttribPointer(COLOR_LAYOUT, Color.size(), GL_FLOAT, GL_FALSE,
                              vertices.itemsize * (Point.size() + Color.size()),
                              ctypes.c_void_p(vertices.itemsize * Point.size()))

        ebo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self._indices.nbytes, self._indices, GL_STATIC_DRAW)

        glBindVertexArray(0)

    def draw(self, model_view: ModelView):
        glBindVertexArray(self._VAO)
        self._shaders_program.scale = model_view.scale
        self._shaders_program.position = model_view.position
        self._shaders_program.use()

        glDrawElements(GL_TRIANGLES, len(self._indices), GL_UNSIGNED_INT, None)
