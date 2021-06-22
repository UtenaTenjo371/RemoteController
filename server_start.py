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
from serverstartui import Ui_Dialog
from server import socket_service
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
		p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
		if p.match(str):
			return True
		else:
			return False

	def get_host_ip(self):
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			s.connect(('8.8.8.8', 80))
			ip = s.getsockname()[0]
		finally:
			s.close()

		return ip   
		
	def getip(self):
		host = self.ip_lineEdit.text()
		port = self.port_lineEdit.text()
		tag = False
		if (self.isIP(host) == False):
			self.information.setText("IP错误，请重新输入！")
		else:
			if (self.get_host_ip() == host):
				try:
					port = int(port)
					self.close()
					socket_service(host,port)
				except BaseException as e:
					self.information.setText("非法端口，请重新输入！")
			else:
				self.information.setText("不是本机IP地址，请重新输入！")

if __name__ == "__main__":
 #固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
 app = QApplication(sys.argv)
 #初始化
 myWin = MyMainForm()
 #将窗口控件显示在屏幕上
 myWin.show()
 #程序运行，sys.exit方法确保程序完整退出。
 sys.exit(app.exec_())

 