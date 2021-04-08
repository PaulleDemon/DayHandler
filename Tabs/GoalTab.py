from PyQt5 import  QtWidgets
from Todo import TodoScrollArea
from CreateWindow import AddWindow


class GoalPage(QtWidgets.QWidget):

    def __init__(self, db_notifier, *args, **kwargs):
        super(GoalPage, self).__init__(*args, **kwargs)

        self.hLayout = QtWidgets.QHBoxLayout(self)

        self.goals = TodoScrollArea.TodoScrollArea()
        self.create_new = QtWidgets.QPushButton("Create New Goal")
        self.create_new.clicked.connect(self.createNewGoal)

        self.hLayout.addWidget(self.goals)
        self.hLayout.addWidget(self.create_new)

        self.db_notifier = db_notifier

    def createNewGoal(self):
        window = AddWindow.AddWindow(self.db_notifier)

        if window.exec():
            pass
