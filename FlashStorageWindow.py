# 导入所需的库
from PyQt5 import QtWidgets, QtCore, QtGui
import datetime
import functions


class FlashStorageWindow(QtWidgets.QMainWindow):
    # 创建时间控制信号
    flashstorageSignal = QtCore.pyqtSignal(str)

    # 初始化函数
    def __init__(self):
        super().__init__()

        # 设置窗口标题
        self.setWindowTitle('Flash写入')

        # 设置窗口图标
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        # 设置窗口大小
        self.resize(400, 120)

        # 设置输入框
        self.no_edit = QtWidgets.QLineEdit()
        self.name_edit = QtWidgets.QLineEdit()
        self.score1_edit = QtWidgets.QSpinBox()
        self.score2_edit = QtWidgets.QSpinBox()
        self.score3_edit = QtWidgets.QSpinBox()

        # 设置输入范围
        self.score1_edit.setRange(0, 999)
        self.score2_edit.setRange(0, 999)
        self.score3_edit.setRange(0, 999)

        # 设置文本
        self.no_text = QtWidgets.QLabel("学号")
        self.name_text = QtWidgets.QLabel("姓名")
        self.score1_text = QtWidgets.QLabel("项目1成绩:")
        self.score2_text = QtWidgets.QLabel("项目2成绩:")
        self.score3_text = QtWidgets.QLabel("项目3成绩:")

        # 创建按钮
        self.send_button = QtWidgets.QPushButton('写入Flash')

        # 创建水平布局
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addWidget(self.no_text)
        hbox1.addWidget(self.no_edit)
        hbox1.addWidget(self.name_text)
        hbox1.addWidget(self.name_edit)

        hbox2 = QtWidgets.QHBoxLayout()
        hbox2.addWidget(self.score1_text)
        hbox2.addWidget(self.score1_edit)
        hbox2.addWidget(self.score2_text)
        hbox2.addWidget(self.score2_edit)
        hbox2.addWidget(self.score3_text)
        hbox2.addWidget(self.score3_edit)

        # 创建垂直布局
        vbox = QtWidgets.QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addWidget(self.send_button)

        # 将垂直布局添加到窗口
        self.setLayout(vbox)

        # 创建中心窗口
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(vbox)

        # 将中心窗口设置为主窗口的中心窗口
        self.setCentralWidget(central_widget)

        # 连接按钮事件
        self.send_button.clicked.connect(self.flashWrite)

    def flashWrite(self, time: str):
        self.flashstorageSignal.emit(functions.format_no(self.no_edit.text()) + functions.format_score(self.score1_edit.value()) + functions.format_score(self.score2_edit.text()) + functions.format_score(
            self.score3_edit.text()) + self.name_edit.text())
