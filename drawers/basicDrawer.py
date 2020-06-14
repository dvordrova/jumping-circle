from abc import ABCMeta, abstractmethod


class BasicDrawer(metaclass=ABCMeta):
    @abstractmethod
    def draw(self, model):
        pass
