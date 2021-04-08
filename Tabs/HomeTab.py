from PyQt5 import  QtWidgets
from Todo import TodoScrollArea


class HomePage(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(HomePage, self).__init__(*args, **kwargs)

        self.hLayout = QtWidgets.QHBoxLayout()
        self.setLayout(self.hLayout)

        self.btnContainer = QtWidgets.QVBoxLayout()
        self.hLayout.addLayout(self.btnContainer)

        self.todoScrollArea = TodoScrollArea.TodoScrollArea()
        self.programScrollArea = TodoScrollArea.TodoScrollArea()

        self.hLayout.addWidget(self.todoScrollArea)
        self.hLayout.addWidget(self.programScrollArea)
