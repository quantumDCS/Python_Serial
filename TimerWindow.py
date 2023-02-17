# 导入所需的库
from PyQt5 import QtWidgets, QtCore, QtGui
import datetime
import functions

class TimerWindow(QtWidgets.QMainWindow):
    # 创建时间控制信号
    timerControlSignal = QtCore.pyqtSignal(str)

    # 初始化函数
    def __init__(self):
        super().__init__()

        # 设置窗口标题
        self.setWindowTitle('Timer控制')

        # 设置窗口图标
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        # 设置窗口大小
        self.resize(400, 150)

        # 设置文本框
        self.hour_text = QtWidgets.QLineEdit()
        self.minute_text = QtWidgets.QLineEdit()
        self.second_text = QtWidgets.QLineEdit()
        self.blinking_interval = QtWidgets.QLineEdit()

        # 设置默认文本
        self.hour_text.setText("00")
        self.minute_text.setText("00")
        self.second_text.setText("00")
        self.blinking_interval.setText("1")

        # 设置文本居中
        self.hour_text.setAlignment(QtCore.Qt.AlignCenter)
        self.minute_text.setAlignment(QtCore.Qt.AlignCenter)
        self.second_text.setAlignment(QtCore.Qt.AlignCenter)
        self.blinking_interval.setAlignment(QtCore.Qt.AlignCenter)

        # 设置文本
        self.time_split_text1 = QtWidgets.QLabel(":")
        self.time_split_text2 = QtWidgets.QLabel(":")
        self.blinking_interval_text = QtWidgets.QLabel("LED闪烁间隔")

        # 创建按钮
        self.get_system_time_button = QtWidgets.QPushButton('获取系统时间')
        self.send_button = QtWidgets.QPushButton('覆写Timer')

        # 创建水平布局
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addWidget(self.hour_text)
        hbox1.addWidget(self.time_split_text1)
        hbox1.addWidget(self.minute_text)
        hbox1.addWidget(self.time_split_text2)
        hbox1.addWidget(self.second_text)

        hbox2 = QtWidgets.QHBoxLayout()
        hbox2.addWidget(self.blinking_interval_text)
        hbox2.addWidget(self.blinking_interval)

        # 创建垂直布局
        vbox = QtWidgets.QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addWidget(self.get_system_time_button)
        vbox.addWidget(self.send_button)

        # 将垂直布局添加到窗口
        self.setLayout(vbox)

        # 创建中心窗口
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(vbox)

        # 将中心窗口设置为主窗口的中心窗口
        self.setCentralWidget(central_widget)

        # 连接按钮事件
        self.get_system_time_button.clicked.connect(self.get_system_time)
        self.send_button.clicked.connect(self.timerControl)

    def get_system_time(self):
        now = datetime.datetime.now()
        hour = now.strftime("%H")
        minute = now.strftime("%M")
        second = now.strftime("%S")
        self.hour_text.setText(hour)
        self.minute_text.setText(minute)
        self.second_text.setText(second)

    def timerControl(self, time: str):
        self.timerControlSignal.emit(functions.format_time(self.hour_text.text()) + functions.format_time(self.minute_text.text()) + functions.format_time(self.second_text.text()) + functions.format_time(self.blinking_interval.text()))

