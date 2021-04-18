from PyQt5 import QtWidgets, QtCore
from CustomizedWidgets import ClockWidget


class TimePicker(QtWidgets.QDialog):

    """  Adds the time time-period, analog time picker and ok-cancel button
        Also,  responsible for switching between hours analog time and minutes analog time
    """

    def __init__(self, *args, **kwargs):
        super(TimePicker, self).__init__(*args, **kwargs)

        self.setWindowTitle("Time Picker")
        self.setObjectName("TimePicker")
        self.setModal(True)  # keeps focus on dialog until closed
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

        self.vlyout = QtWidgets.QVBoxLayout(self)
        self.hour = 12
        self.minutes = 0

        self.time_period = "AM"

        self.initUi()

        self.setWindowFlag(QtCore.Qt.Dialog)
        self.setFixedSize(self.layout().geometry().width(), self.layout().geometry().height())

    def initUi(self):

        self.timelbl_layout = QtWidgets.QHBoxLayout()
        self.period_layout = QtWidgets.QVBoxLayout()

        self.hours_btn = QtWidgets.QPushButton("12")
        self.minutes_btn = QtWidgets.QPushButton("0")

        self.hours_btn.setCheckable(True)
        self.minutes_btn.setCheckable(True)

        self.hours_btn.clicked.connect(self.enable_hour_clock)
        self.minutes_btn.clicked.connect(self.enable_minutes_clock)

        self.am_btn = QtWidgets.QPushButton("AM")
        self.pm_btn = QtWidgets.QPushButton("PM")

        self.am_btn.setCheckable(True)
        self.am_btn.setChecked(True)
        self.pm_btn.setCheckable(True)

        self.am_btn.clicked.connect(lambda: self.switch_meridian("AM"))
        self.pm_btn.clicked.connect(lambda: self.switch_meridian("PM"))

        self.period_layout.addWidget(self.am_btn)
        self.period_layout.addWidget(self.pm_btn)

        self.timelbl_layout.addWidget(self.hours_btn)
        self.timelbl_layout.addWidget(self.minutes_btn)
        self.timelbl_layout.addLayout(self.period_layout)

        self.hoursClock = ClockWidget.ClockWidget(1, 13)
        self.hoursClock.current_index = 11
        self.hoursClock.setMinimumSize(450, 450)

        self.minutesClock = ClockWidget.ClockWidget(start=0, end=60, steps=5)
        self.minutesClock.turn_angle = 11
        self.minutesClock.current_index = 0
        self.minutesClock.setMinimumSize(450, 450)

        self.hoursClock.clicked_signal.connect(self.change_hours)
        self.minutesClock.clicked_signal.connect(self.change_minutes)

        self.vlyout.addLayout(self.timelbl_layout)
        self.vlyout.addWidget(self.hoursClock)
        self.vlyout.addWidget(self.minutesClock)

        self.h_layout = QtWidgets.QHBoxLayout()
        self.ok_btn = QtWidgets.QPushButton("ok")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.close)

        self.h_layout.addWidget(self.ok_btn)
        self.h_layout.addWidget(self.cancel_btn)

        self.vlyout.addLayout(self.h_layout)

        self.enable_hour_clock()

    def enable_minutes_clock(self):

        self.hours_btn.setChecked(False)
        self.minutes_btn.setChecked(True)
        self.hoursClock.hide()
        self.minutesClock.show()

    def enable_hour_clock(self):

        self.minutes_btn.setChecked(False)
        self.hours_btn.setChecked(True)
        self.minutesClock.hide()
        self.hoursClock.show()

    def change_hours(self, value):
        self.hours_btn.setText(value)
        self.hour = value
        self.enable_minutes_clock()

    def change_minutes(self, value):
        self.minutes = value
        self.minutes_btn.setText(value)

        # self.enable_hour_clock()

    def switch_meridian(self, btn):

        if btn == "AM":
            self.am_btn.setChecked(True)
            self.pm_btn.setChecked(False)
            self.time_period = "AM"

        else:
            self.pm_btn.setChecked(True)
            self.am_btn.setChecked(False)
            self.time_period = "PM"

    def get_current_time(self):
        return self.hour, self.minutes, self.time_period

    def get_formatted_time(self):
        return str(self.hour) + ':' + \
               (str(self.minutes) if len(str(self.minutes)) > 1 else '0' + str(self.minutes)) + \
               " " + self.time_period
