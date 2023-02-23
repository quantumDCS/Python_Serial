# 导入所需的库
import time

from PyQt5 import QtWidgets, QtCore, QtGui
import serial
import serial.tools.list_ports
from datetime import datetime
import re

from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget

from LedWindow import LedWindow
from WaveWindow import WaveWindow
from SystickWindow import SystickWindow
from RTCWindow import RTCWindow
from TimerWindow import TimerWindow
from FlashStorageWindow import FlashStorageWindow
from DataBaseWindow import DataBaseWindow


class MainWindow(QtWidgets.QMainWindow):
    # 初始化函数
    def __init__(self):
        super().__init__()

        # 创建下级窗口
        self.led_window = LedWindow()
        self.wave_window = WaveWindow()
        self.systick_window = SystickWindow()
        self.rtc_window = RTCWindow()
        self.timer_window = TimerWindow()
        self.flashstroage_window = FlashStorageWindow()
        self.database_window = DataBaseWindow()

        # 设置窗口标题
        self.setWindowTitle('Python 上位机 未连接串口')

        # 设置窗口图标
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        # 设置窗口大小
        self.resize(800, 600)

        # 创建串口对象
        self.serial_port = serial.Serial()
        self.received_serial_data = ""
        self.received_log = []
        self.start_flag = '\x02'
        self.end_flag = '\x03'

        # 创建按钮
        self.switch_button = QtWidgets.QPushButton('打开串口')
        self.send_button = QtWidgets.QPushButton('发送数据')
        self.groupFrames_button = QtWidgets.QRadioButton('组帧')
        self.led_button = QtWidgets.QPushButton('灯光控制')
        self.wave_button = QtWidgets.QPushButton('波形控制')
        self.systick_button = QtWidgets.QPushButton('Systick控制')
        self.rtc_button = QtWidgets.QPushButton('RTC对时')
        self.timer_button = QtWidgets.QPushButton('Timer计时')
        self.flashstorage_button = QtWidgets.QPushButton('Flash写入')
        self.db_button = QtWidgets.QPushButton('数据库存取')

        # 创建文本
        self.port_text = QtWidgets.QLabel('串口号:')
        self.baud_text = QtWidgets.QLabel('波特率:')
        self.start_text = QtWidgets.QLabel('帧头:')
        self.end_text = QtWidgets.QLabel('帧尾:')

        # 创建文本框
        self.input_text = QtWidgets.QLineEdit()
        self.output_text = QtWidgets.QTextEdit()
        self.start_flag_edit = QtWidgets.QLineEdit()
        self.end_flag_edit = QtWidgets.QLineEdit()

        # 设置组帧
        self.start_flag_edit.setText('0x02')
        self.end_flag_edit.setText('0x03')
        self.groupFrames_button.setChecked(True)

        # 创建下拉列表
        self.port_list = QtWidgets.QComboBox()
        self.baudRate_list = QtWidgets.QComboBox()

        # 创建定时器
        self.refreshPortListTimer = QtCore.QTimer(self)
        self.receiveDataTimer = QtCore.QTimer(self)
        self.updateTimeTimer = QtCore.QTimer(self)
        self.updateDBTimer = QtCore.QTimer(self)

        # 设置下拉列表内容
        self.baudRate_list.addItems(['9600', '19200', '38400', '57600', '115200'])
        self.baudRate_list.setCurrentIndex(4)

        # 设置按钮样式
        self.switch_button.setStyleSheet(
            'QPushButton {color: #ffffff; background-color: #00A65A; border-radius: 4px; padding: 5px 10px;}')
        self.send_button.setStyleSheet(
            'QPushButton {color: #ffffff; background-color: #00c0ef; border-radius: 4px; padding: 5px 10px;}')
        self.led_button.setStyleSheet(
            'QPushButton {color: #ffffff; background-color: #FFA500; border-radius: 4px; padding: 5px 10px;}')
        self.wave_button.setStyleSheet(
            'QPushButton {color: #ffffff; background-color: #605654; border-radius: 4px; padding: 5px 10px;}')
        self.systick_button.setStyleSheet(
            'QPushButton {color: #ffffff; background-color: #00687C; border-radius: 4px; padding: 5px 10px;}')
        self.rtc_button.setStyleSheet(
            'QPushButton {color: #ffffff; background-color: #6D557E; border-radius: 4px; padding: 5px 10px;}')
        self.timer_button.setStyleSheet(
            'QPushButton {color: #ffffff; background-color: #B84E39; border-radius: 4px; padding: 5px 10px;}')
        self.flashstorage_button.setStyleSheet(
            'QPushButton {color: #ffffff; background-color: #7B4F4D; border-radius: 4px; padding: 5px 10px;}')
        self.db_button.setStyleSheet(
            'QPushButton {color: #ffffff; background-color: #BF373D; border-radius: 4px; padding: 5px 10px;}')

        # 创建水平布局
        hbox1 = QtWidgets.QHBoxLayout()

        hbox1_1 = QtWidgets.QHBoxLayout()
        hbox1_1.addWidget(self.port_text)
        hbox1_1.addWidget(self.port_list)

        hbox1_2 = QtWidgets.QHBoxLayout()
        hbox1_2.addWidget(self.baud_text)
        hbox1_2.addWidget(self.baudRate_list)

        hbox1_3 = QtWidgets.QHBoxLayout()
        hbox1_3.addWidget(self.start_text)
        hbox1_3.addWidget(self.start_flag_edit)

        hbox1_4 = QtWidgets.QHBoxLayout()
        hbox1_4.addWidget(self.end_text)
        hbox1_4.addWidget(self.end_flag_edit)

        hbox1.addLayout(hbox1_1)
        hbox1.addLayout(hbox1_2)
        hbox1.addLayout(hbox1_3)
        hbox1.addLayout(hbox1_4)
        hbox1.addWidget(self.switch_button)

        hbox2 = QtWidgets.QHBoxLayout()
        hbox2.addWidget(self.input_text)
        hbox2.addWidget(self.groupFrames_button)
        hbox2.addWidget(self.send_button)

        hbox3 = QtWidgets.QHBoxLayout()
        hbox3.addWidget(self.led_button)
        hbox3.addWidget(self.wave_button)
        hbox3.addWidget(self.systick_button)
        hbox3.addWidget(self.rtc_button)
        hbox3.addWidget(self.timer_button)

        hbox4 = QtWidgets.QHBoxLayout()
        hbox4.addWidget(self.flashstorage_button)
        hbox4.addWidget(self.db_button)

        # 创建垂直布局
        vbox = QtWidgets.QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addWidget(self.output_text)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)

        # 创建中心窗口
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(vbox)

        # 将中心窗口设置为主窗口的中心窗口
        self.setCentralWidget(central_widget)

        # 连接按钮事件
        self.start_flag_edit.textChanged.connect(self.flagChanged)
        self.end_flag_edit.textChanged.connect(self.flagChanged)
        self.switch_button.clicked.connect(self.switch_port)
        self.send_button.clicked.connect(lambda: self.send_data(self.input_text.text()))
        self.led_button.clicked.connect(self.led_control)
        self.wave_button.clicked.connect(self.wave_control)
        self.systick_button.clicked.connect(self.time_control)
        self.rtc_button.clicked.connect(self.rtc_control)
        self.timer_button.clicked.connect(self.timer_control)
        self.flashstorage_button.clicked.connect(self.flashstorage_control)
        self.db_button.clicked.connect(self.db_control)

        # 设置定时器事件
        self.refreshPortListTimer.start(500)
        self.refreshPortListTimer.timeout.connect(self.refreshPortList)
        self.updateDBTimer.timeout.connect(self.db_update)

    def flagChanged(self):
        if self.start_flag_edit.text() == '0x02':
            self.start_flag = '\x02'
        else:
            self.start_flag = self.start_flag_edit.text()
        if self.end_flag_edit.text() == '0x03':
            self.end_flag = '\x03'
        else:
            self.end_flag = self.end_flag_edit.text()

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
            QtWidgets.QMessageBox.critical(self, "严重警告", "没有检测到串口！")
            return
        # 如果串口未打开
        if self.serial_port.is_open is not True:

            # 获取串口名和波特率
            port_name = self.port_list.currentText()
            baudrate = self.baudRate_list.currentText()

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
        if self.serial_port.is_open is not True:
            QtWidgets.QMessageBox.critical(self, "严重警告", "串口未打开！")
            return
        if data == "":
            QtWidgets.QMessageBox.warning(self, "警告", "发送数据不能为空")
            return

        if self.groupFrames_button.isChecked():
            if self.start_flag != "":
                data = self.start_flag + data
            if self.end_flag != "":
                data = data + self.end_flag
        # 将内容转换为字节流
        data_bytes = data.encode('gbk')
        # 发送数据
        self.serial_port.write(data_bytes)
        # 将数据显示到输出框
        self.output_text.append(datetime.now().strftime("%H:%M:%S.%f") + " → " + data.rstrip("\n\r"))

    def decode_bytes(self, byte_stream: bytes):
        try:
            decoded_string = byte_stream.decode("gbk", "replace")
            return decoded_string
        except:
            return "?".join("?" for _ in byte_stream)

    def read_data(self):
        # 从串口读取数据
        data = self.serial_port.readline()
        if data == b'':
            return
        # 将数据转换为字符串
        data = self.decode_bytes(data).strip("\r\n")
        if data == '':
            return
        # 将数据显示到输出框
        self.output_text.append(datetime.now().strftime("%H:%M:%S.%f") + " ← " + data.strip("\r\n"))
        self.received_serial_data = data
        self.received_log.append(data)

    def led_control(self):
        self.led_window.show()
        self.led_window.ledControlSignal.connect(self.send_data)

    def wave_control(self):
        self.wave_window.show()
        self.wave_window.waveControlSignal.connect(self.send_data)

    def time_control(self):
        self.systick_window.show()
        self.systick_window.timeControlSignal.connect(self.send_data)

    def rtc_control(self):
        self.rtc_window.show()
        self.updateTimeTimer.start(50)
        self.updateTimeTimer.timeout.connect(self._rtc_window_update_time)
        self.rtc_window.rtcControlSignal.connect(self.send_data)

    def _rtc_window_update_time(self):
        try:
            rtc_time = datetime.strptime(self.received_serial_data, "%y/%m/%d %H:%M:%S 星期%w\r\n")
        except:
            return
        self.rtc_window.rtc_time = rtc_time
        self.rtc_window.RTC_year_text.setText(str(rtc_time.year))
        self.rtc_window.RTC_mouth_text.setText(str(rtc_time.month))
        self.rtc_window.RTC_day_text.setText(str(rtc_time.day))
        self.rtc_window.RTC_hour_text.setText(str(rtc_time.hour))
        self.rtc_window.RTC_minute_text.setText(str(rtc_time.minute))
        self.rtc_window.RTC_second_text.setText(str(rtc_time.second))
        self.rtc_window.RTC_weekday_text.setText(str(rtc_time.weekday() + 1))

    def timer_control(self):
        self.timer_window.show()
        self.timer_window.timerControlSignal.connect(self.send_data)

    def flashstorage_control(self):
        self.flashstroage_window.show()
        self.flashstroage_window.flashstorageSignal.connect(self.send_data)

    def db_control(self):
        self.database_window.show()
        self.database_window.dbSignal.connect(self.send_data)
        self.database_window.readSignal.connect(self.db_send)

    def db_send(self, data: str):
        self.database_window.read_table.setRowCount(0)
        self.database_window.read_table.clearContents()
        self.database_window.read_table.setHorizontalHeaderLabels(['学号', '姓名', '成绩'])
        if self.serial_port.is_open is not True:
            QtWidgets.QMessageBox.critical(self, "严重警告", "串口未打开！")
            return
        if data == "":
            QtWidgets.QMessageBox.warning(self, "警告", "发送数据不能为空")
            return

        if self.groupFrames_button.isChecked():
            data = '\x05' + data
            if self.end_flag != "":
                data = data + self.end_flag
        # 将内容转换为字节流
        data_bytes = data.encode('gbk')
        # 发送数据
        self.serial_port.write(data_bytes)
        # 将数据显示到输出框
        self.output_text.append(datetime.now().strftime("%H:%M:%S.%f") + " → " + data.rstrip("\n\r"))
        self.updateDBTimer.setSingleShot(True)
        self.updateDBTimer.start(250*self.database_window.num_edit.value())

    def db_update(self):
        # 读取最后 num_records 条记录
        num_records = self.database_window.num_edit.value()
        log_records = self.received_log[-num_records:]
        for record in log_records:
            # 使用正则表达式分割记录
            match = re.match(r"(\d{10})(\d{3})([\u4e00-\u9fa5]+)", record)
            if match:
                # 分别获取第一部分、第三部分、第二部分
                part1, part2, part3 = match.groups()
                # 判断第一部分是否已经在表格中存在
                exists = False
                for row in range(self.database_window.read_table.rowCount()):
                    if self.database_window.read_table.item(row, 0).text() == part1:
                        exists = True
                        break
                # 如果第一部分不存在，则插入该条记录
                if not exists:
                    row_count = self.database_window.read_table.rowCount()
                    self.database_window.read_table.insertRow(row_count)
                    self.database_window.read_table.setItem(row_count, 0, QtWidgets.QTableWidgetItem(part1))
                    self.database_window.read_table.setItem(row_count, 1, QtWidgets.QTableWidgetItem(part3))
                    self.database_window.read_table.setItem(row_count, 2, QtWidgets.QTableWidgetItem(part2))
