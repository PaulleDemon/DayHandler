import sys
from PyQt5 import QtWidgets, QtCore


class LoginBox(QtWidgets.QDialog):
    _style = """ 
            
            LoginBox{
                background-color: #36393f;
            }
            
            QFrame{
                background-color: #2f3136;
            }
            
            QLabel{
                color: #75787d;
                background-color: transparent;
                font-size: 12px;
            }
            
            QLineEdit{
                height: 30px;
                font-size: 14px;
                color: #ffffff;
                background-color: #303339;
                border: 1px solid #24262a;
                border-radius: 3px;
            }
            
            QLineEdit:focus{
                border: 1px solid #6a7ec5;
            }
            
            #Title{
                color: #ffffff;
                background-color: transparent;
                font-size: 20px;
                font-family: Helvetica;
                font-style: bold;
            }
            
            #CloseBtn{
                color: #ffffff;
                background-color: transparent;
                font-size: 20px;
                font-family: Helvetica;
                font-style: bold;
            }
            
            #CloseBtn:hover{
                color: red;
            }
            
            QPushButton#DoneButton{
                background-color: #7289da;
                border-radius: 3px;
                font-size: 14px;
                padding: 10px;
            }
            
            QPushButton#DoneButton:hover{
                background-color: #abbcf7;
            }
            
            QPushButton{
                color: #ffffff;
                background-color: transparent;
                border-radius: 3px;
                font-size: 14px;
                padding: 10px;
                }
            
           QPushButton:hover{
                background-color: rgba(219, 219, 219, 0.8);
            }
            
            #ErrorLbl{
                color: red;
            }
            
            """

    def __init__(self, *args, **kwargs):
        super(LoginBox, self).__init__(*args, **kwargs)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Popup)

        self.v_layout = QtWidgets.QVBoxLayout(self)
        self.v_layout.setContentsMargins(0, 0, 0, 0)

        self.inner_layout = QtWidgets.QVBoxLayout()
        self.inner_layout.setContentsMargins(10, 10, 10, 10)

        self.title = QtWidgets.QLabel("Enter an email address")
        self.title.setObjectName("Title")
        self.info = QtWidgets.QLabel("Enter an email address and an existing password")

        self.close_btn = QtWidgets.QPushButton("X")
        self.close_btn.setObjectName("CloseBtn")
        self.close_btn.setMinimumSize(20, 30)
        self.close_btn.clicked.connect(self.close)

        self.err_lbl = QtWidgets.QLabel()
        self.err_lbl.setObjectName("ErrorLbl")

        self.email_lbl = QtWidgets.QLabel("Email")
        self.email_field = QtWidgets.QLineEdit()

        self.passwd_lbl = QtWidgets.QLabel("Password")
        self.passwd_field = QtWidgets.QLineEdit()
        self.passwd_field.setEchoMode(self.passwd_field.Password)

        self.frame = QtWidgets.QFrame()
        self.ok_cancel_layout = QtWidgets.QHBoxLayout(self.frame)

        self.done = QtWidgets.QPushButton("Done")
        self.done.setObjectName("DoneButton")
        self.done.clicked.connect(self.confirm)

        self.cancel = QtWidgets.QPushButton("cancel")
        self.cancel.clicked.connect(self.close)

        self.ok_cancel_layout.setStretch(0, 0)
        self.ok_cancel_layout.addStretch()
        self.ok_cancel_layout.addWidget(self.cancel, 0, QtCore.Qt.AlignRight)
        self.ok_cancel_layout.addWidget(self.done, 0, QtCore.Qt.AlignRight)

        self.h_layout = QtWidgets.QHBoxLayout()
        self.h_layout.setContentsMargins(0, 0, 0, 0)
        self.h_layout.addStretch()
        self.h_layout.addWidget(self.title)
        self.h_layout.addStretch()
        self.h_layout.addWidget(self.close_btn)

        self.inner_layout.addLayout(self.h_layout)
        self.inner_layout.addWidget(self.info, 0, QtCore.Qt.AlignCenter)
        self.inner_layout.addWidget(self.err_lbl)
        self.inner_layout.addWidget(self.email_lbl)
        self.inner_layout.addWidget(self.email_field)
        self.inner_layout.addWidget(self.passwd_lbl)
        self.inner_layout.addWidget(self.passwd_field)

        self.v_layout.addLayout(self.inner_layout)
        self.v_layout.addWidget(self.frame)

        self.setStyleSheet(self._style)
        self.setMinimumSize(500, 250)

    def confirm(self):
        if len(self.email_field.text()) < 5:  # checks if email have at least 5 characters
            self.err_lbl.setText("Email must have at least 5 characters ")
            return

        self.accept()

    def get_info(self):
        return self.email_field.text(), self.passwd_field.text()


def login_form():
    log = LoginBox()

    if log.exec():
        email, passwd = log.get_info()
        print(f"Email: {email} Password:{passwd}")


def main():
    app = QtWidgets.QApplication(sys.argv)

    widget = QtWidgets.QWidget()

    layout = QtWidgets.QVBoxLayout(widget)
    btn = QtWidgets.QPushButton("Login")
    btn.clicked.connect(login_form)
    layout.addWidget(btn)
    widget.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
