import cv2
import mysql.connector
import numpy as np
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
import sys
from PyQt5 import QtCore,QtGui,QtWidgets,uic
from PyQt5.QtCore import QThread, pyqtSignal
from ultralytics import YOLO
from PyQt5.QtCore import Qt
from main import Ui_MainWindow

class dangnhap(QMainWindow):
    def __init__(self):
        super(dangnhap, self).__init__()
        uic.loadUi('dangnhap.ui', self)
        self.run.clicked.connect(self.laythongtin)
        self.run2.clicked.connect(self.dk)
    def dk(self):
        Widget.setCurrentIndex(2)
    def laythongtin(self):
        un=self.tendn.text()
        psw=self.matkhau.text()
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="traicay"
        )
        self.dbcon = self.mydb.cursor()
        self.dbcon.execute("select * from user where TENDN= '"+un+"' and MATKHAU='"+psw+"' ")
        kt=self.dbcon.fetchone()
        if kt:
            QMessageBox.information(self,"Login output","Login Succsess")
            Widget.setCurrentIndex(1)
        else:
            QMessageBox.information(self,"Login output","Login Fail")

class dangky(QMainWindow):
    def __init__(self):
        super(dangky, self).__init__()
        uic.loadUi('dangky.ui', self)
        self.run3.clicked.connect(self.reg)
    def reg(self):
        un=self.tendn2.text()
        psw=self.matkhau2.text()
        em =self.email.text()
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="traicay"
        )
        self.dbcon = self.mydb.cursor()
        self.dbcon.execute("select * from user where TENDN= '"+un+"' and MATKHAU='"+psw+"' ")
        kt=self.dbcon.fetchone()
        if kt or len(un)== 0 or len(psw)== 0:
            QMessageBox.information(self,"Register output","Tai khoang da ton tai hoac ban chua nhap du")
        else:
            self.dbcon.execute("insert into user values ('""','"+un+"', '"+psw+"','"+em+"') ")
            self.mydb.commit()
            QMessageBox.information(self,"Register output","Register succsess")
            Widget.setCurrentIndex(0)
class nhandien(QMainWindow):
    def __init__(self):
        super().__init__()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)
        self.uic.Button_start.clicked.connect(self.start_capture_video)
        self.thread = {}

    def start_capture_video(self):
        self.thread[1] = live_stream(index=1)
        self.thread[1].start()
        self.thread[1].signal.connect(self.show_wedcam)

    def show_wedcam(self, cv_img):
        qt_img = convert_cv_qt(cv_img)
        self.uic.label.setPixmap(qt_img)


def convert_cv_qt(cv_img):
    """Convert from an opencv image to QPixmap"""
    rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w
    convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
    p = convert_to_Qt_format.scaled(700, 500, Qt.KeepAspectRatio)
    return QPixmap.fromImage(p)


class live_stream(QThread):
    signal = pyqtSignal(np.ndarray)

    def __init__(self, index):
        self.index = index
        print("start threading", self.index)
        super(live_stream, self).__init__()

    def run(self):
        model = YOLO("best.pt")  # load model (recommended for training)
        results = model('chuoi.jpg', show=True, stream=True)  # List of Results objects
        for result, frame in results:
            self.signal.emit(frame)


# xử lý
app=QApplication(sys.argv)
Widget=QtWidgets.QStackedWidget()
login_f=dangnhap()
main_f=nhandien()
register_f=dangky()
Widget.addWidget(login_f)
Widget.addWidget(main_f)
Widget.addWidget(register_f)
Widget.setCurrentIndex(0)
Widget.setFixedHeight(600)
Widget.setFixedWidth(800)
Widget.show()
app.exec()



