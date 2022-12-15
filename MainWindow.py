# 导入所需的库
from PyQt5 import QtWidgets, QtCore, QtGui
import serial
import serial.tools.list_ports
from datetime import datetime
from LedWindow import LedWindow


class MainWindow(QtWidgets.QMainWindow):
    # 初始化函数
    def __init__(self):
        super().__init__()

        # 创建下级窗口
        self.led_window = LedWindow()

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
        self.led_button = QtWidgets.QPushButton('灯光控制')
        self.groupFrames_button = QtWidgets.QRadioButton('组帧')

        # 创建文本
        self.port_text = QtWidgets.QLabel('串口号:')
        self.baud_text = QtWidgets.QLabel('波特率:')
        self.start_text = QtWidgets.QLabel('帧头:')
        self.end_text = QtWidgets.QLabel('帧尾:')


        # 创建文本框
        self.input_text = QtWidgets.QLineEdit()
        self.output_text = QtWidgets.QTextEdit()
        self.start_text_edit = QtWidgets.QLineEdit()
        self.end_text_edit = QtWidgets.QLineEdit()

        # 设置默认帧头和帧尾
        self.start_text_edit.setText('@')
        self.end_text_edit.setText('#')

        # 创建下拉列表
        self.port_list = QtWidgets.QComboBox()
        self.baudrate_list = QtWidgets.QComboBox()

        # 设置定时器
        self.refreshPortListTimer = QtCore.QTimer(self)
        self.receiveDataTimer = QtCore.QTimer(self)

        # 设置下拉列表内容
        self.baudrate_list.addItems(['9600', '19200', '38400', '57600', '115200'])
        self.baudrate_list.setCurrentIndex(4)

        # 设置按钮样式
        self.switch_button.setStyleSheet(
            'QPushButton {color: #ffffff; background-color: #00A65A; border-radius: 4px; padding: 5px 10px;}')
        self.send_button.setStyleSheet(
            'QPushButton {color: #ffffff; background-color: #00c0ef; border-radius: 4px; padding: 5px 10px;}')
        self.led_button.setStyleSheet(
            'QPushButton {color: #ffffff; background-color: #00c0ef; border-radius: 4px; padding: 5px 10px;}')

        # 创建水平布局
        hbox1 = QtWidgets.QHBoxLayout()

        hbox1_1 = QtWidgets.QHBoxLayout()
        hbox1_1.addWidget(self.port_text)
        hbox1_1.addWidget(self.port_list)

        hbox1_2 = QtWidgets.QHBoxLayout()
        hbox1_2.addWidget(self.baud_text)
        hbox1_2.addWidget(self.baudrate_list)

        hbox1_3 = QtWidgets.QHBoxLayout()
        hbox1_3.addWidget(self.start_text)
        hbox1_3.addWidget(self.start_text_edit)

        hbox1_4 = QtWidgets.QHBoxLayout()
        hbox1_4.addWidget(self.end_text)
        hbox1_4.addWidget(self.end_text_edit)

        hbox1.addLayout(hbox1_1)
        hbox1.addLayout(hbox1_2)
        hbox1.addLayout(hbox1_3)
        hbox1.addLayout(hbox1_4)
        hbox1.addWidget(self.switch_button)

        hbox2 = QtWidgets.QHBoxLayout()
        hbox2.addWidget(self.input_text)
        hbox2.addWidget(self.groupFrames_button)
        hbox2.addWidget(self.send_button)

        # 创建垂直布局
        vbox = QtWidgets.QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addWidget(self.output_text)
        vbox.addLayout(hbox2)
        vbox.addWidget(self.led_button)

        # 创建中心窗口
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(vbox)

        # 将中心窗口设置为主窗口的中心窗口
        self.setCentralWidget(central_widget)

        # 连接按钮事件
        self.switch_button.clicked.connect(self.switch_port)
        self.send_button.clicked.connect(lambda: self.send_data(self.input_text.text()))
        self.led_button.clicked.connect(self.led_control)

        # 连接定时器事件
        self.refreshPortListTimer.start(500)
        self.refreshPortListTimer.timeout.connect(self.refreshPortList)

    def refreshPortList(self):
        self.port_list.clear()
        if len(serial.tools.list_ports.comports()) == 0:
            self.port_list.addItems(["没有找到串口"])
        else:
            for i in range(len(list(serial.tools.list_ports.comports()))):
                self.port_list.addItems([list(list(serial.tools.list_ports.comports())[i])[0]])
            self.refreshPortListTimer.stop()

    def switch_port(self):
        if len(serial.tools.list_ports.comports()) == 0:
            QtWidgets.QMessageBox.critical(self, "警告", "没有检测到端口！")
            return
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
            self.receiveDataTimer.start(100)
            self.receiveDataTimer.timeout.connect(self.read_data)

            # 改变UI
            self.setWindowTitle(port_name + '串口已连接 波特率:' + baudrate)
            self.switch_button.setText("关闭串口")
            self.switch_button.setStyleSheet(
                'QPushButton {color: #ffffff; background-color: #FF6347; border-radius: 4px; padding: 5px 10px;}')

        else:
            # 关闭串口
            self.serial_port.close()

            # 关闭读取数据定时器
            self.receiveDataTimer.stop()

            # 改变按钮外观
            self.setWindowTitle('Python 上位机 未连接串口')
            self.switch_button.setText("打开串口")
            self.switch_button.setStyleSheet(
                'QPushButton {color: #ffffff; background-color: #00A65A; border-radius: 4px; padding: 5px 10px;}')

    def send_data(self, data: str):
        if data == "":
            return
        if self.groupFrames_button.isChecked():
            if self.start_text_edit.text() != "":
                data = self.start_text_edit.text() + data
            if self.end_text_edit.text() != "":
                data = data + self.end_text_edit.text()

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
            self.output_text.append(datetime.now().strftime("%H:%M:%S.%f") + " <- " + data)

    def led_control(self):
        self.led_window.show()
        self.led_window.ledControlSignal.connect(self.send_data)
