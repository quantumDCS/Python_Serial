# 导入所需的库
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
import serial
import serial.tools.list_ports
from datetime import datetime

# 创建主窗口类
class MainWindow(QtWidgets.QMainWindow):
    # 初始化函数
    def __init__(self):
        super().__init__()

        # 设置窗口标题
        self.setWindowTitle('Python 上位机 未连接串口')

        # 设置窗口图标
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        # 设置窗口大小
        self.resize(800, 600)

        # 创建串口对象
        self.serial_port = serial.Serial()

        # 创建按钮
        self.switch_button = QtWidgets.QPushButton('打开串口')
        self.send_button = QtWidgets.QPushButton('发送数据')
        self.open_button = QtWidgets.QPushButton('OPEN')

        # 创建文本
        self.port_text = QtWidgets.QLabel('串口号:')
        self.baud_text = QtWidgets.QLabel('波特率:')

        # 创建文本框
        self.input_text = QtWidgets.QTextEdit()
        self.output_text = QtWidgets.QTextEdit()

        # 创建下拉列表
        self.port_list = QtWidgets.QComboBox()
        self.baudrate_list = QtWidgets.QComboBox()

        # 设置下拉列表内容
        if len(serial.tools.list_ports.comports()) == 0:
            self.port_list.addItems(["没有找到串口"])
        else:
            for i in range(len(list(serial.tools.list_ports.comports()))):
                self.port_list.addItems([list(list(serial.tools.list_ports.comports())[i])[0]])

        self.baudrate_list.addItems(['9600', '19200', '38400', '57600', '115200'])
        self.baudrate_list.setCurrentIndex(4)

        # 设置按钮样式
        self.switch_button.setStyleSheet(
            'QPushButton {color: #ffffff; background-color: #00A65A; border-radius: 4px; padding: 5px 10px;}')
        self.send_button.setStyleSheet(
            'QPushButton {color: #ffffff; background-color: #00c0ef; border-radius: 4px; padding: 5px 10px;}')
        self.open_button.setStyleSheet(
            'QPushButton {color: #ffffff; background-color: #00c0ef; border-radius: 4px; padding: 5px 10px;}')

        # 创建水平布局
        hbox1 = QtWidgets.QHBoxLayout()
        vbox1 = QtWidgets.QHBoxLayout()
        vbox1.addWidget(self.port_text)
        vbox1.addWidget(self.port_list)
        vbox2 = QtWidgets.QHBoxLayout()
        vbox2.addWidget(self.baud_text)
        vbox2.addWidget(self.baudrate_list)
        hbox1.addLayout(vbox1)
        hbox1.addLayout(vbox2)

        # 创建垂直布局
        vbox = QtWidgets.QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addWidget(self.switch_button)
        vbox.addWidget(self.input_text)
        vbox.addWidget(self.send_button)
        vbox.addWidget(self.output_text)

        # 将垂直布局添加到窗口
        self.setLayout(vbox)

        # 创建中心窗口
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(vbox)

        # 将中心窗口设置为主窗口的中心窗口
        self.setCentralWidget(central_widget)

        # 连接按钮事件
        self.switch_button.clicked.connect(self.switch_port)
        self.send_button.clicked.connect(self.send_data)
        self.open_button.clicked.connect(self.open)
    def switch_port(self):
        # 如果串口未打开
        if self.serial_port.is_open is not True:

            # 获取串口名和波特率
            port_name = self.port_list.currentText()
            baudrate = self.baudrate_list.currentText()

            # 设置串口参数
            self.serial_port.port = port_name
            self.serial_port.baudrate = baudrate
            self.serial_port.bytesize = serial.EIGHTBITS
            self.serial_port.stopbits = serial.STOPBITS_ONE
            self.serial_port.parity = serial.PARITY_NONE
            self.serial_port.timeout = 0.2

            # 打开串口
            self.serial_port.open()

            # 开启读取数据定时器

            self.timer = QtCore.QTimer(self)
            self.timer.start(100)
            self.timer.timeout.connect(self.read_data)

            # 改变外观
            self.setWindowTitle(port_name+'串口已连接 波特率:'+baudrate)
            self.switch_button.setText("关闭串口")
            self.switch_button.setStyleSheet(
                'QPushButton {color: #ffffff; background-color: #FF6347; border-radius: 4px; padding: 5px 10px;}')

        else:
            # 关闭串口
            self.serial_port.close()

            # 关闭读取数据定时器
            self.timer.stop()

            # 改变按钮外观
            self.setWindowTitle('Python 上位机 未连接串口')
            self.switch_button.setText("打开串口")
            self.switch_button.setStyleSheet(
                'QPushButton {color: #ffffff; background-color: #00A65A; border-radius: 4px; padding: 5px 10px;}')

    def send_data(self):
        # 获取输入框内容
        data = self.input_text.toPlainText()

        # 将内容转换为字节流
        data = data.encode()

        # 发送数据
        self.serial_port.write(data)

    def open(self):
        # 将内容转换为字节流
        data = "open#".encode()

        # 发送数据
        self.serial_port.write(data)

    def read_data(self):
        # 从串口读取数据
        data = self.serial_port.readline()

        # 将数据转换为字符串
        data = data.decode('gbk')
        if data != '':
            # 将数据显示到输出框
            self.output_text.append(datetime.now().strftime("%H:%M:%S.%f")+" <- "+data)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())



