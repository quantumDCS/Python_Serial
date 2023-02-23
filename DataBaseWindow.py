# 导入所需的库
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
import sqlite3
import functions
import time


class DataBaseWindow(QtWidgets.QMainWindow):
    # 创建控制信号
    dbSignal = QtCore.pyqtSignal(str)
    readSignal = QtCore.pyqtSignal(str)

    # 初始化函数
    def __init__(self):
        super().__init__()

        # 设置窗口标题
        self.setWindowTitle('数据库存取')

        # 设置窗口图标
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        # 设置窗口大小
        self.resize(530, 700)

        # 连接数据库
        self.conn = sqlite3.connect('.\\database.db')
        self.c = self.conn.cursor()

        # 读取Students表中的数据
        self.c.execute("SELECT * FROM Students")
        self.data = self.c.fetchall()

        # 创建表格和表头
        self.db_table = QTableWidget()
        self.db_table.setColumnCount(3)
        self.db_table.setHorizontalHeaderLabels(['学号', '姓名', '成绩'])

        self.read_table = QTableWidget()
        self.read_table.setColumnCount(3)
        self.read_table.setHorizontalHeaderLabels(['学号', '姓名', '成绩'])

        # 将数据填充到表格中
        self.db_table.setRowCount(len(self.data))
        for i in range(len(self.data)):
            for j in range(3):
                self.db_table.setItem(i, j, QTableWidgetItem(str(self.data[i][j])))

        # 设置输入框
        self.start_edit = QtWidgets.QSpinBox()
        self.num_edit = QtWidgets.QSpinBox()

        # 设置文本
        self.text1 = QtWidgets.QLabel("从第")
        self.text2 = QtWidgets.QLabel("条开始，读取")
        self.text3 = QtWidgets.QLabel("条数据")

        # 创建按钮
        self.send_button = QtWidgets.QPushButton('写入Flash')
        self.read_button = QtWidgets.QPushButton('从Flash读取')

        # 创建水平布局
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addWidget(self.text1)
        hbox1.addWidget(self.start_edit)
        hbox1.addWidget(self.text2)
        hbox1.addWidget(self.num_edit)
        hbox1.addWidget(self.text3)

        # 创建垂直布局
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.db_table)
        vbox.addWidget(self.send_button)
        vbox.addLayout(hbox1)
        vbox.addWidget(self.read_button)
        vbox.addWidget(self.read_table)

        # 将垂直布局添加到窗口
        self.setLayout(vbox)

        # 创建中心窗口
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(vbox)

        # 将中心窗口设置为主窗口的中心窗口
        self.setCentralWidget(central_widget)

        # 连接按钮事件
        self.send_button.clicked.connect(self.flashWrite)
        self.read_button.clicked.connect(self.flashRead)

    def flashWrite(self):
        for i in range(0, self.db_table.rowCount()):
            self.dbSignal.emit(self.db_table.item(i, 0).text() + functions.format_score(self.db_table.item(i, 2).text()) + functions.format_name(self.db_table.item(i,1).text()))
            time.sleep(2)

    def flashRead(self):
        self.readSignal.emit(
            functions.format_score(self.start_edit.value()) + functions.format_score(self.num_edit.value()))
