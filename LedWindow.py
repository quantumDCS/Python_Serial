# 导入所需的库
from PyQt5 import QtWidgets, QtCore, QtGui


class LedWindow(QtWidgets.QMainWindow):
    # 创建LED控制信号
    ledControlSignal = QtCore.pyqtSignal(str)

    # 初始化函数
    def __init__(self):
        super().__init__()

        # 设置窗口标题
        self.setWindowTitle('LED灯光控制')

        # 设置窗口图标
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        # 设置窗口大小
        self.resize(400, 200)

        # 创建按钮
        self.redLED_button = QtWidgets.QPushButton('红色')
        self.blueLED_button = QtWidgets.QPushButton('蓝色')
        self.greenLED_button = QtWidgets.QPushButton('绿色')
        self.cyanLED_button = QtWidgets.QPushButton('青色')
        self.purpleLED_button = QtWidgets.QPushButton('紫色')
        self.yellowLED_button = QtWidgets.QPushButton('黄色')
        self.whiteLED_button = QtWidgets.QPushButton('白色')
        self.closeLED_button = QtWidgets.QPushButton('关灯')

        # 创建水平布局
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addWidget(self.redLED_button)
        hbox1.addWidget(self.blueLED_button)
        hbox1.addWidget(self.greenLED_button)
        hbox1.addWidget(self.cyanLED_button)

        hbox2 = QtWidgets.QHBoxLayout()
        hbox2.addWidget(self.purpleLED_button)
        hbox2.addWidget(self.yellowLED_button)
        hbox2.addWidget(self.whiteLED_button)
        hbox2.addWidget(self.closeLED_button)

        # 创建垂直布局
        vbox = QtWidgets.QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)

        # 将垂直布局添加到窗口
        self.setLayout(vbox)

        # 创建中心窗口
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(vbox)

        # 将中心窗口设置为主窗口的中心窗口
        self.setCentralWidget(central_widget)

        # 连接按钮事件
        self.redLED_button.clicked.connect(lambda: self.ledControl("red"))
        self.blueLED_button.clicked.connect(lambda: self.ledControl("blue"))
        self.greenLED_button.clicked.connect(lambda: self.ledControl("green"))
        self.cyanLED_button.clicked.connect(lambda: self.ledControl("cyan"))
        self.purpleLED_button.clicked.connect(lambda: self.ledControl("purple"))
        self.yellowLED_button.clicked.connect(lambda: self.ledControl("yellow"))
        self.whiteLED_button.clicked.connect(lambda: self.ledControl("white"))
        self.closeLED_button.clicked.connect(lambda: self.ledControl("close"))

    def ledControl(self, ledColor: str):
        self.ledControlSignal.emit(ledColor)
