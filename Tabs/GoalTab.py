import threading
import sqlite3
import datetime
import concurrent.futures

from DataBaseOperations import DBHandler, Query
from PyQt5 import  QtWidgets
from Todo import TodoScrollArea, ToDoWidget
from CreateWindow import AddWindow


# todo_scroll register the goal page to DbHandler and notify it when values
# are inserted to goal page and refresh this page
class GoalPage(QtWidgets.QWidget):

    def __init__(self,  *args, **kwargs):
        super(GoalPage, self).__init__(*args, **kwargs)

        self.sql_file = r'UserResources/userTodo.db'

        self.hLayout = QtWidgets.QHBoxLayout(self)

        self.goals = TodoScrollArea.TodoScrollArea()
        self.create_new = QtWidgets.QPushButton("Create New Goal")
        self.create_new.clicked.connect(self.create_new_goal)

        self.hLayout.addWidget(self.goals)
        self.hLayout.addWidget(self.create_new)

        self.load_goals()

    def load_goals(self):  # loads goals from Db and calls add_goal_to_scroll to add the goal to scroll area

        goals = DBHandler.get_data(Query.get_all_goals)

        self.goals.delete_all()

        for info in goals:
            goal = ToDoWidget.ToDoWidget()
            goal.set_info(*info)
            self.add_goal_to_scroll(goal)

    def add_goal_to_scroll(self, goal: ToDoWidget.ToDoWidget):  # adds goal to scroll area
        self.goals.add_event(goal)

    def _add_goal(self, *args):  # adds goal to data base
        select_date, select_time, goal_text, select_tag_name, select_tag_img_path = args

        def convert_to_24hrs(time):
            time_24hrs = datetime.datetime.strptime(' '.join(map(str, time)), '%I %M %p').time()
            return time_24hrs

        date = select_date.toString("yyyy-MM-dd")
        time_24hrs = convert_to_24hrs(select_time)

        date_time = f"{date} {time_24hrs}"
        DBHandler.insert_to_table(Query.insert_to_goal, *(date_time, select_tag_name, select_tag_img_path, goal_text))

    def create_new_goal(self):  # a pop-up asking user to create a new goal
        window = AddWindow.AddWindow()

        if window.exec():
            self._add_goal(*window.get_info())
            self.load_goals()

    def db_changed(self):
        print("Notified the change")
        self.load_goals()