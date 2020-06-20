import numpy as np
import pyrr
from OpenGL.GL import glUseProgram, GL_VERTEX_SHADER, GL_FRAGMENT_SHADER, glUniformMatrix4fv, glGetUniformLocation
from OpenGL.GL.shaders import compileProgram, compileShader, GL_FALSE


class ShadersProgram:
    def __init__(self, camera_view, projection, vertex_shaders=None, fragment_shaders=None):
        self._scale = pyrr.Vector3([1, 1, 1], dtype=np.float32)
        self._position = pyrr.Vector3([0, 0, 0], dtype=np.float32)
        self.camera_view = camera_view
        self.projection = projection

        self.vertex_shaders = vertex_shaders or None
        self.fragment_shaders = fragment_shaders or None
        self._program = None

    @property
    def program(self):
        if self._program is None:
            shaders = []
            for vertex_shader_path in self.vertex_shaders:
                with open(vertex_shader_path) as f:
                    shaders.append(compileShader(f.read(), GL_VERTEX_SHADER))
            for fragment_shader_path in self.fragment_shaders:
                with open(fragment_shader_path) as f:
                    shaders.append(compileShader(f.read(), GL_FRAGMENT_SHADER))
            self._program = compileProgram(*shaders)
        return self._program

    def __setattr__(self, key, value):
        if key == 'scale':
            self._scale = value
        elif key == 'position':
            self._position = value
        else:
            super(ShadersProgram, self).__setattr__(key, value)

    def use(self):
        glUseProgram(self.program)
        glUniformMatrix4fv(
            glGetUniformLocation(self.program, "model"),
            1,
            GL_FALSE,
            pyrr.matrix44.create_from_scale(self._scale) @
            pyrr.matrix44.create_from_translation(self._position)
        )
        glUniformMatrix4fv(
            glGetUniformLocation(self.program, "view"),
            1,
            GL_FALSE,
            self.camera_view.matrix
        )
        glUniformMatrix4fv(
            glGetUniformLocation(self.program, "projection"),
            1,
            GL_FALSE,
            self.projection.matrix
        )
