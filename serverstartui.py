# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'server.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(600, 200)
        Dialog.setMinimumSize(QtCore.QSize(600, 200))
        Dialog.setMaximumSize(QtCore.QSize(600, 200))
        self.ip_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.ip_lineEdit.setGeometry(QtCore.QRect(150, 30, 200, 30))
        self.ip_lineEdit.setMinimumSize(QtCore.QSize(200, 30))
        self.ip_lineEdit.setMaximumSize(QtCore.QSize(200, 30))
        self.ip_lineEdit.setText("")
        self.ip_lineEdit.setObjectName("ip_lineEdit")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 30, 150, 30))
        self.label.setMinimumSize(QtCore.QSize(150, 30))
        self.label.setMaximumSize(QtCore.QSize(150, 30))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 90, 150, 30))
        self.label_2.setMinimumSize(QtCore.QSize(150, 30))
        self.label_2.setMaximumSize(QtCore.QSize(150, 30))
        self.label_2.setObjectName("label_2")
        self.port_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.port_lineEdit.setGeometry(QtCore.QRect(150, 90, 200, 30))
        self.port_lineEdit.setMinimumSize(QtCore.QSize(200, 30))
        self.port_lineEdit.setMaximumSize(QtCore.QSize(200, 30))
        self.port_lineEdit.setText("")
        self.port_lineEdit.setObjectName("port_lineEdit")
        self.ok_Button = QtWidgets.QPushButton(Dialog)
        self.ok_Button.setGeometry(QtCore.QRect(140, 150, 60, 30))
        self.ok_Button.setMinimumSize(QtCore.QSize(60, 30))
        self.ok_Button.setMaximumSize(QtCore.QSize(60, 30))
        self.ok_Button.setObjectName("ok_Button")
        self.information = QtWidgets.QTextBrowser(Dialog)
        self.information.setGeometry(QtCore.QRect(380, 30, 200, 150))
        self.information.setMinimumSize(QtCore.QSize(200, 150))
        self.information.setMaximumSize(QtCore.QSize(200, 150))
        self.information.setObjectName("information")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "控制端"))
        self.label.setText(_translate("Dialog", "控制端IP地址"))
        self.label_2.setText(_translate("Dialog", "控制端端口号"))
        self.ok_Button.setText(_translate("Dialog", "确定"))
        self.information.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">欢迎使用远程控制！</p></body></html>"))
