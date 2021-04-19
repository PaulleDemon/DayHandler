from PyQt5 import QtWidgets, QtCore, QtGui
from Event import EventDisplayer
from CreateWindow import TimePicker
from datetime import datetime
from CustomizedWidgets import TextBox


# todo: timepicker widget should not open when the return key is pressed
class AddWindow(QtWidgets.QDialog):
    """ This window creates the with calender time-picker, a tag-selector and a Text box"""

    def __init__(self, create_btn_name="Create", *args, **kwargs):
        super(AddWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle(create_btn_name)
        self.setObjectName("CreateWindow")
        self.setFocusPolicy(QtCore.Qt.NoFocus)

        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        self.setModal(True)  # Ensures that the window doesn't lose focus

        self.time = [12, 0, "PM"]

        self.setLayout(QtWidgets.QVBoxLayout(self))
        self.layout().setContentsMargins(0, 0, 0, 0)

        frame = QtWidgets.QFrame()
        self.layout().addWidget(frame)

        self.vLayout = QtWidgets.QVBoxLayout(frame)

        self.select_date_lbl = QtWidgets.QLabel("Select Date and Time")

        self.h_layout = QtWidgets.QHBoxLayout()

        self.calender = QtWidgets.QCalendarWidget()
        self.calender.setFocusPolicy(QtCore.Qt.ClickFocus)
        today = QtCore.QDate().currentDate()

        self.date = today
        self.calender.setDateRange(today, QtCore.QDate(today.addYears(50)))
        self.calender.clicked.connect(self.set_date)

        self.time_btn = QtWidgets.QPushButton("12:00 PM")
        self.time_btn.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.time_btn.clicked.connect(self.select_time)

        self.h_layout.addWidget(self.calender)
        self.h_layout.addWidget(self.time_btn)

        self.tag = EventDisplayer.SelectTag(self)

        self.text = TextBox.TextBox(maxChar=1500)
        self.text.setAcceptRichText(False)
        self.text.setPlaceholderText("Enter your event details here")

        self.h_ok_cancel_layout = QtWidgets.QHBoxLayout()
        self.create_new = QtWidgets.QPushButton(create_btn_name)
        self.cancel = QtWidgets.QPushButton("Cancel")

        self.create_new.clicked.connect(self.confirm)
        self.cancel.clicked.connect(self.close)

        self.h_ok_cancel_layout.addWidget(self.create_new)
        self.h_ok_cancel_layout.addWidget(self.cancel)

        self.vLayout.addWidget(self.select_date_lbl)
        self.vLayout.addLayout(self.h_layout)
        self.vLayout.addWidget(self.tag)
        self.vLayout.addWidget(self.text)
        self.vLayout.addLayout(self.h_ok_cancel_layout)

    def select_time(self):  # opens the time-picker widget
        timePicker = TimePicker.TimePicker(self)

        if timePicker.exec():
            _hour, _min, _period = timePicker.get_current_time()
            self.time = [_hour, _min, _period]
            self.time_btn.setText(timePicker.get_formatted_time())

    def set_date(self, qdate):
        self.date = qdate

    def confirm(self):

        time = datetime.now()
        _hour, _minutes = time.hour, time.minute

        def check_time():  # converts 12 hrs format to 24 hrs format and compares time
            time_12hrs = datetime.strptime(' '.join(map(str, self.time)), '%I %M %p')
            __hour, __minutes = map(int, time_12hrs.strftime("%H %M").split())
            return __hour <= _hour and __minutes <= _minutes

        def error_msg_window(self, title, message):  # Shows an error dialog
            msg_window = QtWidgets.QDialog(self)
            msg_window.setModal(True)
            msg_window.setWindowTitle(title)
            msg_window.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
            v_layout = QtWidgets.QVBoxLayout(msg_window)
            v_layout.addWidget(QtWidgets.QLabel(message))
            btn = QtWidgets.QPushButton("OK")
            btn.clicked.connect(msg_window.close)
            v_layout.addWidget(btn)
            msg_window.setFixedSize(v_layout.contentsRect().width(), v_layout.contentsRect().height())
            msg_window.exec()

        if QtCore.QDate().currentDate() == self.date and check_time():
            #  check to make sure that time selected is an upcoming time
            error_msg_window(self, "Error", "Please select upcoming time")
            return

        if self.tag.get_tag() is None:
            error_msg_window(self, "Error", "Please select a tag")
            return

        if len(self.text.toPlainText()) < 5:
            error_msg_window(self, "Error", "Please Enter at least 5 characters in the text box")
            return

        self.accept()

    def get_info(self):  # returns the info such as date, time, text, tag
        return self.date, self.time, self.text.toPlainText(), *self.tag.get_tag()

    def preset(self, *args): # This is preset text, time, tag in case user decides to edit the event
        date, time, tag_name, text = args

        date = QtCore.QDate(*date)

        self.calender.setSelectedDate(date)
        self.text.setText(text)
        self.tag.set_current_tag(tag_name)

        self.time = list(map(int, time[:2]))
        self.time.append(time[2])
        self.time_btn.setText(':'.join(time[:2])+f" {time[2]}")


