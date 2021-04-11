from PyQt5 import  QtWidgets
from Todo import TodoScrollArea
from CreateWindow import AddWindow


class ProgramPage(QtWidgets.QWidget):

    def __init__(self,  *args, **kwargs):
        super(ProgramPage, self).__init__(*args, **kwargs)

        self.hLayout = QtWidgets.QHBoxLayout(self)

        self.program = TodoScrollArea.TodoScrollArea()
        self.create_new = QtWidgets.QPushButton("Create New Project")
        self.create_new.clicked.connect(self.createNewPgm)

        self.hLayout.addWidget(self.program)
        self.hLayout.addWidget(self.create_new)

    def createNewPgm(self):
        window = AddWindow.AddWindow()

        if window.exec():
            pass



