from typing import Type

from drawers import BasicDrawer
from shaders.shadersProgram import ShadersProgram


class WaitingDrawer(BasicDrawer):
    """waiting for first usage, openGL context creation in a thread"""
    def __init__(self, real_drawer_type, shaders_program, *args, **kwargs):
        self._real_drawer_type = real_drawer_type
        self._shaders_program = shaders_program
        self._args = args
        self._kwargs = kwargs
        self._real_drawer = None

    def draw(self, model):
        if self._real_drawer is None:
            self._real_drawer = self._real_drawer_type(self._shaders_program, *self._args, **self._kwargs)
        return self._real_drawer.draw(model)


def get_drawer_creator(drawer_type: Type[BasicDrawer], shaders_program: ShadersProgram):
    def create_drawer(*args, **kwargs):
        return WaitingDrawer(drawer_type, shaders_program, *args, **kwargs)

    return create_drawer
