# 导入所需的库
from PyQt5 import QtWidgets, QtCore, QtGui
import datetime
from dateutil.relativedelta import relativedelta


class RTCWindow(QtWidgets.QMainWindow):
    # 创建RTC控制信号
    rtcControlSignal = QtCore.pyqtSignal(str)

    # 初始化函数
    def __init__(self):
        super().__init__()

        # 设置窗口标题
        self.setWindowTitle('RTC时间控制')

        # 设置窗口图标
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        # 设置窗口大小
        self.resize(400, 150)

        # 设置文本框
        self.system_year_text = QtWidgets.QLineEdit()
        self.system_mouth_text = QtWidgets.QLineEdit()
        self.system_day_text = QtWidgets.QLineEdit()
        self.system_hour_text = QtWidgets.QLineEdit()
        self.system_minute_text = QtWidgets.QLineEdit()
        self.system_second_text = QtWidgets.QLineEdit()
        self.system_weekday_text = QtWidgets.QLineEdit()

        self.RTC_year_text = QtWidgets.QLineEdit()
        self.RTC_mouth_text = QtWidgets.QLineEdit()
        self.RTC_day_text = QtWidgets.QLineEdit()
        self.RTC_hour_text = QtWidgets.QLineEdit()
        self.RTC_minute_text = QtWidgets.QLineEdit()
        self.RTC_second_text = QtWidgets.QLineEdit()
        self.RTC_weekday_text = QtWidgets.QLineEdit()

        self.difference_year_text = QtWidgets.QLineEdit()
        self.difference_mouth_text = QtWidgets.QLineEdit()
        self.difference_day_text = QtWidgets.QLineEdit()
        self.difference_hour_text = QtWidgets.QLineEdit()
        self.difference_minute_text = QtWidgets.QLineEdit()
        self.difference_second_text = QtWidgets.QLineEdit()
        self.difference_text = QtWidgets.QLineEdit()

        # 设置文本
        self.system_time_text = QtWidgets.QLabel("系统时间:")
        self.RTC_time_text = QtWidgets.QLabel("RTC时间:")
        self.difference_time_text = QtWidgets.QLabel("时间相差:")
        self.date_split_text1 = QtWidgets.QLabel("/")
        self.date_split_text2 = QtWidgets.QLabel("/")
        self.date_split_text3 = QtWidgets.QLabel("/")
        self.date_split_text4 = QtWidgets.QLabel("/")
        self.date_split_text5 = QtWidgets.QLabel("/")
        self.date_split_text6 = QtWidgets.QLabel("/")
        self.time_split_text1 = QtWidgets.QLabel(":")
        self.time_split_text2 = QtWidgets.QLabel(":")
        self.time_split_text3 = QtWidgets.QLabel(":")
        self.time_split_text4 = QtWidgets.QLabel(":")
        self.time_split_text5 = QtWidgets.QLabel(":")
        self.time_split_text6 = QtWidgets.QLabel(":")
        self.week_text1 = QtWidgets.QLabel("星期")
        self.week_text2 = QtWidgets.QLabel("星期")
        self.compare_text = QtWidgets.QLabel("同步")

        # 创建按钮
        self.synchronize_time_manual_button = QtWidgets.QPushButton('手动对时')
        self.synchronize_time_auto_button = QtWidgets.QPushButton('自动对时')

        # 创建水平布局
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addWidget(self.system_time_text)
        hbox1.addWidget(self.system_year_text)
        hbox1.addWidget(self.date_split_text1)
        hbox1.addWidget(self.system_mouth_text)
        hbox1.addWidget(self.date_split_text2)
        hbox1.addWidget(self.system_day_text)
        hbox1.addWidget(self.system_hour_text)
        hbox1.addWidget(self.time_split_text1)
        hbox1.addWidget(self.system_minute_text)
        hbox1.addWidget(self.time_split_text2)
        hbox1.addWidget(self.system_second_text)
        hbox1.addWidget(self.week_text1)
        hbox1.addWidget(self.system_weekday_text)

        hbox2 = QtWidgets.QHBoxLayout()
        hbox2.addWidget(self.RTC_time_text)
        hbox2.addWidget(self.RTC_year_text)
        hbox2.addWidget(self.date_split_text3)
        hbox2.addWidget(self.RTC_mouth_text)
        hbox2.addWidget(self.date_split_text4)
        hbox2.addWidget(self.RTC_day_text)
        hbox2.addWidget(self.RTC_hour_text)
        hbox2.addWidget(self.time_split_text3)
        hbox2.addWidget(self.RTC_minute_text)
        hbox2.addWidget(self.time_split_text4)
        hbox2.addWidget(self.RTC_second_text)
        hbox2.addWidget(self.week_text2)
        hbox2.addWidget(self.RTC_weekday_text)

        hbox3 = QtWidgets.QHBoxLayout()
        hbox3.addWidget(self.difference_time_text)
        hbox3.addWidget(self.difference_year_text)
        hbox3.addWidget(self.date_split_text5)
        hbox3.addWidget(self.difference_mouth_text)
        hbox3.addWidget(self.date_split_text6)
        hbox3.addWidget(self.difference_day_text)
        hbox3.addWidget(self.difference_hour_text)
        hbox3.addWidget(self.time_split_text5)
        hbox3.addWidget(self.difference_minute_text)
        hbox3.addWidget(self.time_split_text6)
        hbox3.addWidget(self.difference_second_text)
        hbox3.addWidget(self.compare_text)
        hbox3.addWidget(self.difference_text)

        # 创建垂直布局
        vbox = QtWidgets.QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addWidget(self.synchronize_time_manual_button)
        vbox.addWidget(self.synchronize_time_auto_button)

        # 将垂直布局添加到窗口
        self.setLayout(vbox)

        # 创建中心窗口
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(vbox)

        # 将中心窗口设置为主窗口的中心窗口
        self.setCentralWidget(central_widget)

        # 连接按钮事件
        self.synchronize_time_manual_button.clicked.connect(self.synchronize_time)
        self.synchronize_time_auto_button.clicked.connect(self.synchronize_time_auto)

        # 创建定时器
        self.updateTimeTimer = QtCore.QTimer(self)
        self.compareTimeTimer = QtCore.QTimer(self)
        self.compareTimeTimer = QtCore.QTimer(self)

        # 设置定时器事件
        self.updateTimeTimer.start(500)
        self.updateTimeTimer.timeout.connect(self.update_time)
        self.compareTimeTimer.start(50)
        self.updateTimeTimer.timeout.connect(self.compare_time)

        self.rtc_time = datetime.datetime.now()

    def update_time(self):
        system_time = datetime.datetime.now()
        self.system_year_text.setText(str(system_time.year))
        self.system_mouth_text.setText(str(system_time.month))
        self.system_day_text.setText(str(system_time.day))
        self.system_hour_text.setText(str(system_time.hour))
        self.system_minute_text.setText(str(system_time.minute))
        self.system_second_text.setText(str(system_time.second))
        self.system_weekday_text.setText(str(system_time.weekday() + 1))

    def compare_time(self):
        rtc_time = self.rtc_time
        system_time = datetime.datetime.now()
        difference_time = relativedelta(system_time, rtc_time)
        self.difference_year_text.setText(str(difference_time.years))
        self.difference_mouth_text.setText(str(difference_time.months))
        self.difference_day_text.setText(str(difference_time.days))
        self.difference_hour_text.setText(str(difference_time.hours))
        self.difference_minute_text.setText(str(difference_time.minutes))
        self.difference_second_text.setText(str(difference_time.seconds))
        difference_widgets = [self.difference_year_text, self.difference_mouth_text, self.difference_day_text,
                              self.difference_hour_text, self.difference_minute_text, self.difference_second_text]

        if all(x.text() == "0" for x in difference_widgets):
            self.difference_text.setText("√")
        else:
            self.difference_text.setText("×")

    def synchronize_time(self):
        self.rtcControlSignal.emit(datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S 星期%w"))

    def synchronize_time_auto(self):
        self.compareTimeTimer.start(60000)
        self.compareTimeTimer.timeout.connect(self.synchronize_time)
        self.synchronize_time_auto_button.setText("已开启自动对时，每60s自动同步时间")
