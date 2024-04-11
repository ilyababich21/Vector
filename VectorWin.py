import math
import os
import sys
import threading
import serial.tools.list_ports as ser
from PyQt6 import uic, QtGui
from PyQt6.QtCore import QVariantAnimation, QSize
from PyQt6.QtGui import QBrush, QPixmap, QColor
from PyQt6.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsRectItem, QGraphicsItem,  \
    QHBoxLayout
from serial import SerialException

from Scene import  Viewha
from math import *


from Serka import Serka


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.getcwd()
    return os.path.join(base_path, relative_path)


class VectorWin(QMainWindow):
    thread = None

    def __init__(self):
        super().__init__()

        uic.loadUi(resource_path("view.ui"), self)
        self.conn = False
        self.speed=0
        self.rect_width = 105
        self.med = self.rect_width*sqrt(3)/2
        self.graphicsView = Viewha()
        lyt = QHBoxLayout()
        self.config()

        lyt.addWidget(self.graphicsView)
        self.widget.setLayout(lyt)
        ports = ser.comports()

        for port, desc, hwid in ports:
            self.comPorts.addItem(str(port))
        self.slider.setValue(0)
        self.rect.setRotation(0)

        self.animation = QVariantAnimation()
        self.animation.setStartValue(0)
        self.animation.setEndValue(360)
        self.animation.setDuration(60000)  # длительность анимации в миллисекундах (60 секунд)
        self.animation.setLoopCount(-1)
        self.animation.valueChanged.connect(self.ratata)
        # self.animation.start()

        self.slider.valueChanged.connect(self.setAnimationSpeed)

        self.graphicsView.mySignal.connect(self.rotate)
        self.conBut.clicked.connect(self.serial_connect)
        self.button.clicked.connect(self.play)
        self.maxRot.editingFinished.connect(self.changeMax)

    def changeMax(self):
        try:
            max = int(self.maxRot.text())
            self.slider.setMaximum(max)

        except Exception as e:
            print("ne sudba", e)

    def setAnimationSpeed(self, value):
        if value != 0:
            self.speed=value
            duration = 60000 / value
            self.animation.setDuration(int(duration))
            if not self.animation.state() =="Running":
                self.animation.start()
        else: self.animation.stop()

    def ratata(self, angle):
        self.rect.setRotation( -angle)
        if self.rect_width >= self.med:self.rect_width = 105
        self.vectora(angle,self.rect_width)
        if self.conn:
            self.thread.setAngle(angle,self.rect_width/105,self.speed)

    def serial_connect(self):
        if self.conBut.text() == "Connect":
            port = self.comPorts.currentText()
            print(port)
            try:
                baudrate = int(self.baudrates.text())
                print(baudrate)
                self.thread = Serka(port=port, baudrate=baudrate)
                self.thread.openConnection()
                self.thread.start()
                self.conBut.setText("Отключиться")
                self.button.setEnabled(True)
            except SerialException as y:
                print("Net Soedinenia: ", y)
            except Exception as e:
                print(e)
        elif self.conBut.text() == "Отключиться":
            self.conn = False
            self.thread.stop = True
            self.thread.running = False
            self.thread.closeConnection()
            self.thread.join()
            self.conBut.setText("Connect")
            self.button.setEnabled(False)
            self.button.setText("Play")

    def play(self):
        if self.button.text() == "Play":
            if self.thread is not None:
                if self.thread.is_open():
                    self.conn = True
                    self.thread.running = True
                    self.button.setText("Pause")

        elif self.button.text() == "Pause":
            self.thread.running = False
            self.conn = False
            self.button.setText("Play")

    def rotate(self, X, Y):

        centerX = self.graphicsView.width() / 2
        centerY = self.graphicsView.height() / 2
        x_width = X - centerX
        x_hight = centerY - Y
        # print(x_width, "   ", x_hight)
        radians = atan2(x_hight, x_width)
        angle = degrees(radians)
        # print("angle= ", angle, "cur_rotation= ", self.rect.rotation())
        self.rect.setRotation(-angle)

        self.rect_width = x_width / math.cos(radians)
        if angle < 0: angle = 360 + angle


        self.vectora(angle,self.rect_width)

        if self.conn:
            self.thread.setAngle(angle,self.rect_width/105,0)

    def vectora(self,angle,u_vect):

        sector = int(angle//60)
        angle = angle%60
        bet = abs(angle-30)
        crinzh = self.med/math.cos(math.radians(bet))
        if self.rect_width >crinzh: self.rect_width = crinzh
        b1_width = (2/sqrt(3))*self.rect_width*math.sin(math.radians(60-angle))
        b2_wedth = (2/sqrt(3))*self.rect_width*math.sin(math.radians(angle))
        self.rect.setRect(self.scene.width() / 2, self.scene.height() / 2, self.rect_width, 2.5)
        self.b1_vector.setRect(self.scene.width() / 2, self.scene.height() / 2, b1_width, 4)
        self.b2_vector.setRect(self.scene.width() / 2, self.scene.height() / 2, b2_wedth, 4)
        self.b1_vector.setRotation(-(sector*60))
        self.b2_vector.setRotation(-(sector*60+60))

    def config(self):
        self.scene = QGraphicsScene(0,0,300,300)
        # self.scene.setBackgroundBrush(QBrush(QPixmap("radiani2.jpg")))
        pixmap = QPixmap(resource_path("radiani5.jpg"))
        pixmap = pixmap.scaled(QSize(300,300))

        self.scene.addPixmap(pixmap)
        self.rect = QGraphicsRectItem(self.scene.width() / 2, self.scene.height() / 2, self.rect_width, 3)
        self.b1_vector = QGraphicsRectItem(0,0,0,0)
        self.b2_vector = QGraphicsRectItem(0,0,0,0)
        self.rect.setTransformOriginPoint(self.scene.width() / 2, self.scene.height() / 2 + 1.25)
        self.b1_vector.setTransformOriginPoint(self.scene.width() / 2, self.scene.height() / 2 + 1.25)
        self.b2_vector.setTransformOriginPoint(self.scene.width() / 2, self.scene.height() / 2 + 1.25)

        # rect.setPos(50, 20)

        # Define the brush (fill).
        brush = QBrush(QColor(0,255,0))
        self.rect.setBrush(brush)

        # Define the pen (line)
        brush_v1 = QBrush(QColor(255, 0,0))
        self.b1_vector.setBrush(brush_v1)

        brush_v2 = QBrush(QColor(255, 0, 0))
        self.b2_vector.setBrush(brush_v2)

        self.scene.addItem(self.rect)
        self.scene.addItem(self.b1_vector)
        self.scene.addItem(self.b2_vector)

        self.rect.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)

        self.graphicsView.setScene(self.scene)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self.thread:
            self.thread.running = False
            self.thread.stop = True
            self.thread.closeConnection()
            self.thread.join()
            threads = threading.enumerate()
            print("Active threads:", threads)
