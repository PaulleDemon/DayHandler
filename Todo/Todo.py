from PyQt5 import QtWidgets


class Todo(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(Todo, self).__init__(*args, **kwargs)

        self.vBox = QtWidgets.QVBoxLayout()
        self.setLayout(self.vBox)

        self.scrollArea = QtWidgets.QScrollArea()

        self.scrollLayout = QtWidgets.QVBoxLayout()

    def InitUI(self):
        pass
