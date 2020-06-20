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
    @property
    def matrix(self):
        return pyrr.matrix44.create_look_at(
            pyrr.Vector3([0, 0, 100], dtype=np.float32),
            pyrr.Vector3([0, 0, 0], dtype=np.float32),
            pyrr.Vector3([0, 1, 0], dtype=np.float32)
        )


class ModelView:
    def __init__(self, scale: pyrr.Vector3, position: pyrr.Vector3):
        self.scale = scale
        self.position = position
