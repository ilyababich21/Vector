import time
from threading import Thread

import serial
from serial import SerialException


class Serka(Thread):
    def __init__(self,port,baudrate):
        super().__init__()
        self._angle = 0
        self._pizda = 0
        self.port = port
        self.baudrate = baudrate
        self.running = False
        self.stop = False

    def run(self):
        conn = self._angle
        while True:
            if self.running:
                if self.conn.is_open:
                    if conn != self._angle:
                        # print(self._angle)
                        conn = self._angle
                        stroka = str(int(conn)) +" "+str(int(self._pizda*100))+ "\n"
                        try:
                            print("tx: ",stroka)
                            self.conn.write(bytes(stroka,'ASCII'))
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
                time.sleep(1)

    def setAngle(self,angle,kek):
        self._angle = angle
        self._pizda = kek



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
