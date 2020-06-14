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
    def __init__(self, x: float, y: float, color: Color = Color(1., 1., 1.)):
        self.x = x
        self.y = y
        self.color = color

    def as_array(self):
        return [self.x, self.y] + self.color.as_array()

    @classmethod
    def size(cls):
        return 2

    def __add__(self, other):
        return Point(
            self.x + other.x,
            self.y + other.y,
            color=self.color
        )

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self


ORIGINAL_POINT = Point(0, 0)
