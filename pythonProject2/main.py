import cv2
import datetime
import os
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
from gui import Ui_MainWindow
from form1 import Ui_Form
from kho2 import kho_MainWindow
from traicay1 import traicay_MainWindow
import res



class dangnhap(QMainWindow):
    def __init__(self):
        super(dangnhap, self).__init__()
        uic.loadUi('loginUi3.ui', self)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.run.clicked.connect(self.laythongtin)
        self.run2.clicked.connect(self.dk)
    def dk(self):
        Widget.setCurrentIndex(2)
    def laythongtin(self):
        global tendndung
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
            tendndung=un
            Widget.setCurrentIndex(1)
        else:
            QMessageBox.information(self,"Login output","Login Fail")

class dangky(QMainWindow):
    def __init__(self):
        super(dangky, self).__init__()
        uic.loadUi('regUI.ui', self)
        self.run3.clicked.connect(self.reg)
    def reg(self):
        un=self.tendn_2.text()
        psw=self.matkhau_2.text()
        em =self.email_2.text()
        ho=self.ho.text()
        ten=self.ten.text()
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
            self.dbcon.execute("insert into user values ('""','""','"+ho+"','"+ten+"','"+un+"', '"+psw+"','"+em+"') ")
            self.mydb.commit()
            QMessageBox.information(self,"Register output","Register succsess")
            Widget.setCurrentIndex(0)
class CommonMethods():
    def logout(self):
        Widget.setCurrentIndex(0)
        QMessageBox.information(self, "", "Logout Succsess")
    def phanloai(self):
        Widget.setCurrentIndex(1)
    def kho(self):
        Widget.setCurrentIndex(3)
    def traicay(self):
        Widget.setCurrentIndex(4)
class nhandien(QMainWindow,CommonMethods):
    def __init__(self):
        super().__init__()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)
        self.uic.Button_start.clicked.connect(self.start_capture_video)
        self.uic.select.clicked.connect(self.addtraicay)
        self.uic.Button_stop.clicked.connect(self.form_kho)
        self.uic.Logout.triggered.connect(self.logout)
        self.uic.actionPh_n_Lo_i.triggered.connect(self.phanloai)
        self.uic.actionTr_i_C_y.triggered.connect(self.traicay)
        self.uic.actionKho.triggered.connect(self.kho)
        self.thread = {}
    #

    # phân loại
    def start_capture_video(self):
        self.thread[1] = live_stream(index=1)
        self.thread[1].start()
        self.thread[1].signal.connect(self.show_wedcam)

    def show_wedcam(self, cv_img):
        qt_img = convert_cv_qt(cv_img)
        self.uic.label.setPixmap(qt_img)
    def addtraicay(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="traicay"
        )
        print(tentraicay)
        self.dbcon = self.mydb.cursor()

        try:
            self.dbcon.execute("insert into fruit values ('""','""','" + tentraicay + "', '"+ pic +"','""') ")
            self.mydb.commit()
            QMessageBox.information(self, "thông báo", "thêm trái cây thành công")
            # thêm dữ liệu vào bảng phân loại
            self.dbcon.execute("select ID from user where TENDN= '"+ tendndung +"' ")
            a = self.dbcon.fetchone()
            ma_user = int(a[0])
            self.dbcon.execute("select ID from fruit where TENTRAICAY= '" + tentraicay + "' ")
            b = self.dbcon.fetchone()
            ma_fruit = int(b[0])
            ngaysd = datetime.date.today()
            float_value = float(ketqua.item())
            self.dbcon.execute("insert into phanloai values ('""','" + str(ma_user) + "', '"+str(ngaysd)+"','"+str(ma_fruit)+"','"+str(float_value)+"') ")
            self.mydb.commit()
        except mysql.connector.Error as error:
            QMessageBox.warning(self, "thông báo", f"Lỗi: {error}")
    def form_kho(self):
        self.dbcon.execute("select * from fruit where TENTRAICAY = '" + tentraicay + "'")
        kt = self.dbcon.fetchone()
        if kt:
            self.Second_window = QtWidgets.QMainWindow()
            self.uic1 = Ui_Form()
            self.uic1.setupUi(self.Second_window)
            self.Second_window.show()
        else:
            QMessageBox.information(self, "Thông báo", "Trái cây chưa có nên không thể thêm vào kho")
        self.uic1.ten_traicay.setText(tentraicay)
        self.uic1.run3.clicked.connect(self.addkho)

    def addkho(self):
        sl = self.uic1.soluong.text()
        gia = self.uic1.gia.text()
        dc = self.uic1.diachi.text()
        self.dbcon.execute("select ID from fruit where TENTRAICAY= '" + tentraicay + "' ")
        b = self.dbcon.fetchone()
        ma_fruit = int(b[0])
        try:
            self.dbcon.execute("insert into kho values ('""','"+str(ma_fruit)+"','"+tentraicay+"','" + sl + "', '" + gia + "','"+ dc +"') ")
            self.mydb.commit()
            QMessageBox.information(self, "thông báo", "thêm vào kho thành công")
        except mysql.connector.Error as error:
            QMessageBox.warning(self, "thông báo", f"Lỗi: {error}")
class KHO(QMainWindow,CommonMethods):
    def __init__(self):
        super().__init__()
        self.uic = kho_MainWindow()
        self.uic.setupUi(self)
        self.uic.logout.triggered.connect(self.logout)
        self.uic.phanloai.triggered.connect(self.phanloai)
        self.uic.traicay.triggered.connect(self.traicay)
        self.uic.kho.triggered.connect(self.kho)
        self.uic.loaddt.clicked.connect(self.loaddata)
        self.uic.update.clicked.connect(self.up)
        self.uic.delete_2.clicked.connect(self.xoa)

    def xoa(self):
        selected_row = self.uic.tableWidget.currentRow()
        # Kiểm tra xem có chọn dòng nào không
        if selected_row >= 0:
            # Lấy ID từ dòng được chọn
            id = self.uic.tableWidget.item(selected_row, 0).text()

            # Xóa dòng khỏi cơ sở dữ liệu
            sql = "DELETE FROM kho WHERE ID = %s"
            self.dbcon.execute(sql, (id,))
            self.mydb.commit()

            # Xóa dòng khỏi bảng hiển thị
            self.uic.tableWidget.removeRow(selected_row)

            # Thông báo cho người dùng biết rằng xóa thành công
            QMessageBox.information(self, "Thành công", "Xóa thành công!")
        else:
            # Thông báo cho người dùng biết rằng chưa chọn dòng nào
            QMessageBox.warning(self, "Cảnh báo", "Hãy chọn một dòng để xóa!")

    def up(self):
        selected_row = self.uic.tableWidget.currentRow()
        # Kiểm tra xem có chọn dòng nào không


        if selected_row >= 0:
            # Lấy dữ liệu từ bảng
            id = self.uic.tableWidget.item(selected_row, 0).text()
            ma = self.uic.tableWidget.item(selected_row, 1).text()
            ten = self.uic.tableWidget.item(selected_row, 2).text()
            soluong = self.uic.tableWidget.item(selected_row, 3).text()
            gia = self.uic.tableWidget.item(selected_row, 4).text()
            diachi = self.uic.tableWidget.item(selected_row, 5).text()


            # Cập nhật dữ liệu vào cơ sở dữ liệu
            sql = "UPDATE kho SET MA_TRAICAY = %s,TEN_TRAICAY = %s,SoLuong = %s, Gia_traicay = %s, Diachi = %s WHERE ID = %s"
            self.dbcon.execute(sql, (ten, ma, soluong, gia, diachi, id))
            self.mydb.commit()

            # Thông báo cho người dùng biết rằng cập nhật thành công
            QMessageBox.information(self, "Thành công", "Cập nhật thành công!")
        else:
            # Thông báo cho người dùng biết rằng chưa chọn dòng nào
            QMessageBox.warning(self, "Cảnh báo", "Hãy chọn một dòng để chỉnh sửa!(Bạn không thể chỉnh sữa ID)")

    def loaddata(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="traicay"
        )
        self.dbcon = self.mydb.cursor()
        self.dbcon.execute("select * from kho")
        column_names = [i[0] for i in self.dbcon.description]
        print(column_names)
        # fetchon lấy 1 fetchall chọn nhiều
        result = self.dbcon.fetchall()
        print(result)
        #tạo bảng
        self.uic.tableWidget.setColumnCount(len(column_names))
        self.uic.tableWidget.setHorizontalHeaderLabels(column_names)
        self.uic.tableWidget.setRowCount(20)
        #ghi lên ô
        table_row = 0
        for row in result:
            self.uic.tableWidget.setItem(table_row, 0, QTableWidgetItem(str(row[0])))
            self.uic.tableWidget.setItem(table_row, 1, QTableWidgetItem(str(row[1])))
            self.uic.tableWidget.setItem(table_row, 2, QTableWidgetItem(str(row[2])))
            self.uic.tableWidget.setItem(table_row, 3, QTableWidgetItem(str(row[3])))
            self.uic.tableWidget.setItem(table_row, 4, QTableWidgetItem(str(row[4])))
            self.uic.tableWidget.setItem(table_row, 5, QTableWidgetItem(str(row[5])))
            table_row +=1

class TRAICAY(QMainWindow,CommonMethods):
    def __init__(self):
        super().__init__()
        self.uic = traicay_MainWindow()
        self.uic.setupUi(self)
        self.uic.logout.triggered.connect(self.logout)
        self.uic.phanloai.triggered.connect(self.phanloai)
        self.uic.traicay.triggered.connect(self.traicay)
        self.uic.kho.triggered.connect(self.kho)
        self.uic.loaddt.clicked.connect(self.loaddata)
        self.uic.update.clicked.connect(self.up)
        self.uic.delete_2.clicked.connect(self.xoa)

    def xoa(self):
        selected_row = self.uic.tableWidget.currentRow()
        # Kiểm tra xem có chọn dòng nào không
        if selected_row >= 0:
            # Lấy ID từ dòng được chọn
            id = self.uic.tableWidget.item(selected_row, 0).text()

            # Xóa dòng khỏi cơ sở dữ liệu
            sql = "DELETE FROM fruit WHERE ID = %s"
            self.dbcon.execute(sql, (id,))
            self.mydb.commit()

            # Xóa dòng khỏi bảng hiển thị
            self.uic.tableWidget.removeRow(selected_row)

            # Thông báo cho người dùng biết rằng xóa thành công
            QMessageBox.information(self, "Thành công", "Xóa thành công!")
        else:
            # Thông báo cho người dùng biết rằng chưa chọn dòng nào
            QMessageBox.warning(self, "Cảnh báo", "Hãy chọn một dòng để xóa!")

    def up(self):
        selected_row = self.uic.tableWidget.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Cảnh báo", "Hãy chọn một dòng để chỉnh sửa!(Bạn không thể chỉnh sữa ID)")
            return
        id = self.uic.tableWidget.item(selected_row, 0).text()
        ma = self.uic.tableWidget.item(selected_row, 1).text()
        ten = self.uic.tableWidget.item(selected_row, 2).text()
        hinhanh = self.uic.tableWidget.item(selected_row, 3).text()
        mota = self.uic.tableWidget.item(selected_row, 4).text()

        # kiểm tra trái cây đã có chưa
        sql = "SELECT TENTRAICAY FROM fruit WHERE TENTRAICAY = %s"
        self.dbcon.execute(sql, (ten,))
        result = self.dbcon.fetchone()

        if result is not None:
            QMessageBox.warning(self, "Cảnh báo", "Trái cây đã tồn tại!")
            self.uic.tableWidget.item(selected_row, 2).setText(result[0])
        else:
            # Update the values in the database
            sql = "UPDATE fruit SET MA_TRAICAY = %s,TENTRAICAY = %s,HINHANH = %s, MOTA = %s WHERE ID = %s"
            self.dbcon.execute(sql, (ma, ten, hinhanh, mota, id))
            self.mydb.commit()

            # Inform the user that the update was successful
            QMessageBox.information(self, "Thành công", "Cập nhật thành công!")
    def loaddata(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="traicay"
        )
        self.dbcon = self.mydb.cursor()
        self.dbcon.execute("select * from fruit")
        column_names = [i[0] for i in self.dbcon.description]
        print(column_names)
        # fetchon lấy 1 fetchall chọn nhiều
        result = self.dbcon.fetchall()
        print(result)
        #tạo bảng
        self.uic.tableWidget.setColumnCount(len(column_names))
        self.uic.tableWidget.setHorizontalHeaderLabels(column_names)
        self.uic.tableWidget.setRowCount(20)
        #ghi lên ô
        table_row = 0
        for row in result:
            self.uic.tableWidget.setItem(table_row, 0, QTableWidgetItem(str(row[0])))
            self.uic.tableWidget.setItem(table_row, 1, QTableWidgetItem(str(row[1])))
            self.uic.tableWidget.setItem(table_row, 2, QTableWidgetItem(str(row[2])))
            self.uic.tableWidget.setItem(table_row, 3, QTableWidgetItem(str(row[3])))
            self.uic.tableWidget.setItem(table_row, 4, QTableWidgetItem(str(row[4])))
            table_row +=1

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
        global tentraicay,pic,ketqua
        files = QFileDialog.getOpenFileName()
        a = files[0]
        pic = os.path.basename(a)
        model = YOLO("best1.pt")  # load model (recommended for training)
        results = model(pic, show=True, stream=True)  # List of Results objects
        for result, frame in results:
            boxes = result[0].boxes.numpy()  # Boxes object for bbox outputs
            for box in boxes:  # there could be more than one detection
                print("class", box.cls)
                print("xyxy", box.xyxy)
                print("conf", box.conf)
                traicay = box.cls
                ketqua=box.conf
                tentraicay = ""
                for item in traicay:
                    if item == 0:
                        tentraicay = "chuoi"
                    elif item == 1:
                        tentraicay = "dau den"
                    elif item == 2:
                        tentraicay = "mam xoi"
                    elif item == 3:
                        tentraicay = "chanh"
                    elif item == 4:
                        tentraicay = "nho"
                    elif item == 5:
                        tentraicay = "ca chua"
                    elif item == 6:
                        tentraicay = "tao"
                    elif item == 7:
                        tentraicay = "ot"
            self.signal.emit(frame)

# xử lý
app=QApplication(sys.argv)
Widget=QtWidgets.QStackedWidget()
login_f=dangnhap()
main_f=nhandien()
register_f=dangky()
kho_f=KHO()
traicay_f=TRAICAY()
Widget.addWidget(login_f)
Widget.addWidget(main_f)
Widget.addWidget(register_f)
Widget.addWidget(kho_f)
Widget.addWidget(traicay_f)
Widget.setCurrentIndex(0)
Widget.setFixedHeight(650)
Widget.setFixedWidth(850)
Widget.show()
app.exec()




