from PyQt6.QtCore import pyqtSignal

from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView


class Scene(QGraphicsScene):
    def __init__(self):
        super().__init__()

    def mouseMoveEvent(self, event):
        print(f'x = {event.pos().x():>4.0f}, y = {event.pos().y():>4.0f} <- QGraphicsScene')


class Viewha(QGraphicsView):
    mySignal = pyqtSignal(int, int)

    def __init__(self):
        super().__init__()

    def mouseMoveEvent(self, event):
        # print(f'x = {event.pos().x():>4.0f}, y = {event.pos().y():>4.0f} <- QGraphicsView')

        self.mySignal.emit(event.pos().x().real, event.pos().y().real)
