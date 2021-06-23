# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'connect_me.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
#导入程序运行必须模块
import sys
#PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中
from PyQt5.QtWidgets import QApplication, QMainWindow
#导入designer工具生成的login模块
from clientstartui import Ui_Dialog
from client import socket_client
import string
import re
import os
import socket

class MyMainForm(QMainWindow, Ui_Dialog):
	def __init__(self, parent=None):
		super(MyMainForm, self).__init__(parent)
		self.setupUi(self)
		self.ok_Button.clicked.connect(self.getip)

	def isIP(self,str):
    """
    判断输入是否为IP地址
    Args:
        str:输入字符串
    """	
		p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
		if p.match(str):
			return True
		else:
			return False
		
	def getip(self):
    """
    获取用户输入的IP地址，判断是否为IP
    获取用户输入的端口号，判断是否合法
    """
		host = self.ip_lineEdit.text()
		port = self.port_lineEdit.text()
		tag = False
		if (self.isIP(host) == False):
			self.information.setText("IP错误，请重新输入！")
		else:
			try:
				port = int(port)
				self.close()
				socket_client(host, port)
			except BaseException as e:
				self.information.setText("非法端口，请重新输入！")

if __name__ == "__main__":
 #固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
 app = QApplication(sys.argv)
 #初始化
 myWin = MyMainForm()
 #将窗口控件显示在屏幕上
 myWin.show()
 #程序运行，sys.exit方法确保程序完整退出。
 sys.exit(app.exec_())

 