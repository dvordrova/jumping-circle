import numpy as np
import pyrr


class ProjectionView:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    @property
    def matrix(self):
        return pyrr.matrix44.create_orthogonal_projection(
            0, self.width,
            0, self.height,
            -1000, 1000
        )


class CameraView:
    def __init__(self):
        self.eye = pyrr.Vector3([0, 0, 100], dtype=np.float32)
        self.target = pyrr.Vector3([0, 0, 0], dtype=np.float32)
        self.up = pyrr.Vector3([0, 1, 0], dtype=np.float32)

    @property
    def matrix(self):
        return pyrr.matrix44.create_look_at(self.eye, self.target, self.up)


class ModelView:
    def __init__(self, scale: pyrr.Vector3, position: pyrr.Vector3):
        self.scale = scale
        self.position = position
