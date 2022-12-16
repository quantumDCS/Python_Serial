# 导入所需的库
from PyQt5 import QtWidgets, QtCore, QtGui


class WaveWindow(QtWidgets.QMainWindow):
    # 创建波形控制信号
    waveControlSignal = QtCore.pyqtSignal(str)

    # 初始化函数
    def __init__(self):
        super().__init__()

        # 设置窗口标题
        self.setWindowTitle('DAC波形控制')

        # 设置窗口图标
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        # 设置窗口大小
        self.resize(400, 150)

        # 创建按钮
        self.triangularWave_button = QtWidgets.QPushButton('三角波')
        self.squareWave_button = QtWidgets.QPushButton('方波')
        self.sineWave_button = QtWidgets.QPushButton('正弦波')
        self.trapezoidalWave_button = QtWidgets.QPushButton('梯形波')

        # 创建水平布局
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addWidget(self.triangularWave_button)
        hbox1.addWidget(self.squareWave_button)
        hbox1.addWidget(self.sineWave_button)
        hbox1.addWidget(self.trapezoidalWave_button)

        # 创建垂直布局
        vbox = QtWidgets.QVBoxLayout()
        vbox.addLayout(hbox1)

        # 将垂直布局添加到窗口
        self.setLayout(vbox)

        # 创建中心窗口
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(vbox)

        # 将中心窗口设置为主窗口的中心窗口
        self.setCentralWidget(central_widget)

        # 连接按钮事件
        self.triangularWave_button.clicked.connect(lambda: self.waveControl("1"))
        self.squareWave_button.clicked.connect(lambda: self.waveControl("2"))
        self.sineWave_button.clicked.connect(lambda: self.waveControl("3"))
        self.trapezoidalWave_button.clicked.connect(lambda: self.waveControl("4"))

    def waveControl(self, waveform: str):
        self.waveControlSignal.emit(waveform)
