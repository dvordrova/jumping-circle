import numpy as np

from pyrr import Vector3

class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def as_array(self):
        return [self.r, self.g, self.b]

    @classmethod
    def size(cls):
        return 3


class Point:
    def __init__(self, x: float = 0., y: float = 0., color: Color = Color(1., 1., 1.)):
        self._vector = Vector3([x, y, 0], dtype=np.float32)
        self.color = color
    
    @property
    def x(self):
        return self._vector.x
    
    @property
    def y(self):
        return self._vector.y

    def as_array(self):
        return [self.x, self.y] + self.color.as_array()

    @classmethod
    def size(cls):
        return 2

    def __iadd__(self, other):
        if isinstance(other, Vector3):
            self._vector += other
        elif isinstance(other, Point):
            self._vector += other._vector
        else:
            raise RuntimeError(f"Can't __iadd__ Point and {other.__class__.__name__}")
        return self
    
    def __sub__(self, other):
        return self._vector - other._vector


ORIGINAL_POINT = Point()
