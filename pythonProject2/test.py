import cv2
import string
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
from PyQt5.QtWidgets import QApplication, QMainWindow
from traicay1 import traicay_MainWindow
from phanloai import Ui_MainWindow
import datetime
class TRAICAY(QMainWindow):
    def __init__(self):
        super().__init__()
        self.uic = traicay_MainWindow()
        self.uic.setupUi(self)
        # self.uic.logout.triggered.connect(self.logout)
        # self.uic.phanloai.triggered.connect(self.phanloai)
        # self.uic.traicay.triggered.connect(self.traicay)
        # self.uic.kho.triggered.connect(self.kho)
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
        sql = "SELECT TENTRAICAY FROM fruit WHERE TENTRAICAY = %s and ID!=%s"
        self.dbcon.execute(sql, (ten,id))
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = TRAICAY()
    main_win.show()
    sys.exit(app.exec())