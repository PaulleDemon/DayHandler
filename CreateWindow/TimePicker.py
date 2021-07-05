from PyQt5 import QtWidgets, QtCore, QtGui

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
        self.setMinimumSize(300, 300)

    def initUi(self):

        self.timelbl_layout = QtWidgets.QHBoxLayout()
        self.period_layout = QtWidgets.QVBoxLayout()

        self.hours_btn = TimeWidget(1, 12)
        self.hours_btn.valueChanged.connect(self.change_hours)

        self.minutes_btn = TimeWidget(0, 60)
        self.minutes_btn.valueChanged.connect(self.change_minutes)

        self.hours_btn.setCheckable(True)
        self.minutes_btn.setCheckable(True)

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

        self.vlyout.addLayout(self.timelbl_layout)

        self.h_layout = QtWidgets.QHBoxLayout()
        self.ok_btn = QtWidgets.QPushButton("ok")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")

        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.close)

        self.h_layout.addWidget(self.ok_btn)
        self.h_layout.addWidget(self.cancel_btn)

        self.vlyout.addLayout(self.h_layout)

    def change_hours(self, value):
        self.hour = value

    def change_minutes(self, value):
        self.minutes = value

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


class TimeWidget(QtWidgets.QPushButton):

    valueChanged = QtCore.pyqtSignal(int)

    def __init__(self, min=0, max=12, current=None, *args, **kwargs):
        super(TimeWidget, self).__init__(*args, **kwargs)
        self.range = list(range(min, max + 1))
        print(self.range)
        if current:
            self.current = current

        else:
            self.current = min

        self.previous_key = [self.current]
        self.updateText()

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:

        if event.angleDelta().y() >= 120:

            if self.current < self.range[-1]:
                self.current += 1

        else:
            print(self.current)
            if self.current > self.range[0]:
                self.current -= 1

        self.updateText()

    def updateText(self):
        self.setText(f"{self.current}")
        self.valueChanged.emit(self.current)

    def emptyPreviousKey(self):
        self.previous_key = []

    def delayedKey(self, key):

        if len(self.previous_key) >= len(str(self.range[-1])):
            self.previous_key.pop(0)

        self.previous_key.append(key)

        number = int(''.join(map(str, self.previous_key)))

        if number in self.range:
            self.current = number

        self.updateText()

        QtCore.QTimer.singleShot(1000, self.emptyPreviousKey)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:

        try:
            number = int(QtGui.QKeySequence(event.key()).toString())

            if number in self.range:
                self.delayedKey(number)

        except ValueError:
            pass
