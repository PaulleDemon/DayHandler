from PyQt5 import QtWidgets, QtCore
from Todo import ToDoWidget
from CreateWindow import TimePicker
from datetime import datetime


class AddWindow(QtWidgets.QDialog):
    """ This window creates the with calender time-picker, a tag-selector and a Text box"""

    def __init__(self, db_notifier, *args, **kwargs):
        super(AddWindow, self).__init__(*args, **kwargs)

        self.db_notifier = db_notifier

        self.setWindowTitle("Create")
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        self.setModal(True)  # Ensures that the window doesn't lose focus

        self.time = [12, 0, "PM"]

        self.vLayout = QtWidgets.QVBoxLayout(self)

        self.select_date_lbl = QtWidgets.QLabel("Select Date and Time")

        self.h_layout = QtWidgets.QHBoxLayout()

        self.calender = QtWidgets.QCalendarWidget()
        today = QtCore.QDate().currentDate()

        self.date = today
        self.calender.setDateRange(today, QtCore.QDate(today.addYears(50)))

        self.calender.clicked.connect(self.set_date)

        self.time_btn = QtWidgets.QPushButton("12:00 PM")
        self.time_btn.clicked.connect(self.select_time)

        self.h_layout.addWidget(self.calender)
        self.h_layout.addWidget(self.time_btn)

        self.tag = ToDoWidget.SelectTodo(self.db_notifier)

        self.text = QtWidgets.QTextEdit()

        self.h_ok_cancel_layout = QtWidgets.QHBoxLayout()
        self.create_new = QtWidgets.QPushButton("Create")
        self.cancel = QtWidgets.QPushButton("Cancel")

        self.create_new.clicked.connect(self.confirm)

        self.h_ok_cancel_layout.addWidget(self.create_new)
        self.h_ok_cancel_layout.addWidget(self.cancel)

        self.vLayout.addWidget(self.select_date_lbl)
        self.vLayout.addLayout(self.h_layout)
        self.vLayout.addWidget(self.tag)
        self.vLayout.addWidget(self.text)
        self.vLayout.addLayout(self.h_ok_cancel_layout)

    def select_time(self):
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

        def error_msg_window(title, message):  # Shows an error dialog
            msg_window = QtWidgets.QDialog()
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
            error_msg_window("Error", "Please select upcoming time")
            return

        if self.tag.get_tag() is None:
            error_msg_window("Error", "Please select a tag")
            return

        if len(self.text.toPlainText()) < 15:
            error_msg_window("Error", "Please Enter at least 15 characters in the text box")
            return

        self.accept()

    # todo: instead of `self.tag.get_tag()` we must pass just the text and the image path
    def get_info(self):
        return self.date, self.time, self.tag.get_tag(),  self.text.toPlainText()

