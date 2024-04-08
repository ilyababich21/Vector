import time
from threading import Thread
import numpy as np
import serial
from numpy import uint16
from serial import SerialException


class Serka(Thread):
    def __init__(self,port,baudrate):
        super().__init__()
        self._angle = 0
        self._pizda = 0
        self._speed = 0
        self.port = port
        self.baudrate = baudrate
        self.running = False
        self.stop = False

    def run(self):
        angle = self._angle
        while True:
            if self.running:
                if self.conn.is_open:
                    if angle != self._angle:
                        # print(self._angle)
                        angle = self._angle
                        stroka = str(int(angle)) +" "+str(int(self._pizda*100))+" "+str(self._speed)+ "\n"
                        numbers = np.array([angle,int(self._pizda*100),self._speed],dtype=np.uint16).tobytes()
                        try:
                            self.conn.write(numbers)
                            print("tx: ",stroka)
                            # self.angle.write(bytes(stroka,'ASCII'))
                            # print("otpravil")
                            line = self.conn.readline()
                            # print("kek")


                            if line:
                                print("rx: ", line)

                        except Exception as e:
                            print("exception ===",e)
            else:
                if self.stop:
                    break
                # print([self._angle,self._pizda*100,self._speed])
                # numbers = np.array([int(self._angle), int(self._pizda * 100)], dtype=uint16)
                # print(numbers)
                time.sleep(1)

    def setAngle(self,angle,kek,speed):
        self._angle = angle
        self._pizda = kek
        self._speed = speed



    def openConnection(self):

            self.conn = serial.Serial(port=self.port,baudrate=self.baudrate)
            if not self.is_open:
                self.conn.open()
            # self.conn.open()


    def closeConnection(self):
        if self.conn.is_open:
            self.conn.close()

    def is_open(self):
        return True if self.conn.is_open else False
