from typing import Callable

from drawers import BasicDrawer
from utils import Point, ORIGINAL_POINT
from views import ModelView


# class Segment:
#     def __init__(self, left: Point, right: Point, left_can_move=False, right_can_move=False):
#         self._left = left
#         self._right = right
#         self.left_can_move = left_can_move
#         self.right_can_move = right_can_move
#         self.default_length = 1
#         self.m = 0


class Rope:
    def __init__(self, create_drawer: Callable[..., BasicDrawer], left: Point, right: Point, segments_count=50):
        self._drawer = create_drawer([
            Point(left.x + i * (right.x - left.x) / segments_count, left.y + i * (right.y - left.y) / segments_count)
            for i in range(segments_count)
        ])

    def draw(self):
        self._drawer.draw(ModelView(1., ORIGINAL_POINT))
