from PyQt5 import QtWidgets
import sys


class ExampleWidget(QtWidgets.QWidget):

    _style = """
            QPushButton#Btn1{
                color: #ffffff;
                background-color: transparent;
                font-size: 20px;
                font-family: Helvetica;
                font-style: bold;
            }
            
            QPushButton#Btn1:hover{
                color: red;
            }
            
            QPushButton#Btn2{
                background-color: blue;
                border-radius: 3px;
            }
            
            QPushButton#Btn2:hover{
                background-color: green;
            }
            
            QPushButton{
                color: #ffffff;
                background-color: transparent;
                font-size: 14px;
                border-radius: 3px;
                font-size: 14px;
                padding: 10px;
            }
            
           QPushButton:hover{
                background-color: rgba(219, 219, 219, 0.8);
            }
                
            """

    def __init__(self):
        super(ExampleWidget, self).__init__()
        v_layout = QtWidgets.QVBoxLayout(self)

        btn1 = QtWidgets.QPushButton("Button1")
        btn1.setObjectName("Btn1")

        btn2 = QtWidgets.QPushButton("Button2")
        btn2.setFixedSize(50, 10)
        btn2.setObjectName("Btn2")

        btn3 = QtWidgets.QPushButton("Button2")

        v_layout.addWidget(btn1)
        v_layout.addWidget(btn2)
        v_layout.addWidget(btn3)


        self.setStyleSheet(self._style)


def main():
    app = QtWidgets.QApplication(sys.argv)

    scroll = ExampleWidget()
    scroll.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()