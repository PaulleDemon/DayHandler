from PyQt5 import  QtWidgets
from Todo import TodoScrollArea
from CreateWindow import AddWindow


class TodoPage(QtWidgets.QWidget):

    def __init__(self, db_change, *args, **kwargs):
        super(TodoPage, self).__init__(*args, **kwargs)

        self.db_change_notifier = db_change

        self.hLayout = QtWidgets.QHBoxLayout(self)

        self.todo = TodoScrollArea.TodoScrollArea()

        self.create_new = QtWidgets.QPushButton("Add Todo")
        self.create_new.clicked.connect(self.addTodo)

        self.hLayout.addWidget(self.todo)
        self.hLayout.addWidget(self.create_new)

    def addTodo(self):
        window = AddWindow.AddWindow(self.db_change_notifier)

        if window.exec():
            pass