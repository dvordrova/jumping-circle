import pyrr

from utils import Point


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
            pyrr.Vector3([0, 0, 100]),
            pyrr.Vector3([0, 0, 0]),
            pyrr.Vector3([0, 1, 0])
        )


class ModelView:
    def __init__(self, scale: float, position: Point):
        self.scale = scale
        self.position = position
