# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(616, 479)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(40, 50, 121, 61))
        self.label.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(40, 200, 121, 61))
        self.label_2.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(40, 120, 121, 61))
        self.label_3.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(40, 280, 121, 61))
        self.label_4.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.label_4.setObjectName("label_4")
        self.ten_traicay = QtWidgets.QLineEdit(Form)
        self.ten_traicay.setGeometry(QtCore.QRect(180, 60, 271, 41))
        self.ten_traicay.setStyleSheet("font: 9pt \"MS Shell Dlg 2\";\n"
"")
        self.ten_traicay.setPlaceholderText("")
        self.ten_traicay.setObjectName("ten_traicay")
        self.soluong = QtWidgets.QLineEdit(Form)
        self.soluong.setGeometry(QtCore.QRect(180, 140, 271, 41))
        self.soluong.setStyleSheet("font: 9pt \"MS Shell Dlg 2\";\n"
"")
        self.soluong.setPlaceholderText("")
        self.soluong.setObjectName("soluong")
        self.gia = QtWidgets.QLineEdit(Form)
        self.gia.setGeometry(QtCore.QRect(180, 210, 271, 41))
        self.gia.setStyleSheet("font: 9pt \"MS Shell Dlg 2\";\n"
"")
        self.gia.setPlaceholderText("")
        self.gia.setObjectName("gia")
        self.diachi = QtWidgets.QLineEdit(Form)
        self.diachi.setGeometry(QtCore.QRect(180, 290, 271, 41))
        self.diachi.setStyleSheet("font: 9pt \"MS Shell Dlg 2\";\n"
"")
        self.diachi.setPlaceholderText("")
        self.diachi.setObjectName("diachi")
        self.run3 = QtWidgets.QPushButton(Form)
        self.run3.setGeometry(QtCore.QRect(210, 370, 161, 51))
        self.run3.setStyleSheet("\n"
"font: 14pt \"MS Shell Dlg 2\";")
        self.run3.setObjectName("run3")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Tên trái cây"))
        self.label_2.setText(_translate("Form", "Giá"))
        self.label_3.setText(_translate("Form", "Số lượng"))
        self.label_4.setText(_translate("Form", "Địa chỉ"))
        self.run3.setText(_translate("Form", "Thêm vào kho"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
