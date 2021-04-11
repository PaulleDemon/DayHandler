import threading
import sqlite3
import datetime
import concurrent.futures

from DataBaseOperations import DBHandler, Query
from PyQt5 import  QtWidgets
from Todo import TodoScrollArea, ToDoWidget
from CreateWindow import AddWindow


# todo register the goal page to DbHandler and notify it when values are inserted to goal page and refresh this page
class GoalPage(QtWidgets.QWidget):

    def __init__(self, db_notifier, *args, **kwargs):
        super(GoalPage, self).__init__(*args, **kwargs)

        self.sql_file = r'UserResources/userTodo.db'

        self.hLayout = QtWidgets.QHBoxLayout(self)

        self.goals = TodoScrollArea.TodoScrollArea()
        self.create_new = QtWidgets.QPushButton("Create New Goal")
        self.create_new.clicked.connect(self.create_new_goal)

        self.hLayout.addWidget(self.goals)
        self.hLayout.addWidget(self.create_new)

        self.db_notifier = db_notifier
        self.load_goals()

    def load_from_db(self):
        with sqlite3.connect(self.sql_file, check_same_thread=False) as conn:
            curr = conn.cursor()
            curr.execute("SELECT * FROM goal ORDER BY datetime")
            items = curr.fetchall()

        return items

    def load_goals(self):

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self.load_from_db)
            executor.shutdown(True)
            goals = future.result()

        for index, info in enumerate(goals):
            goal = ToDoWidget.ToDoWidget()
            goal.set_info(*info)
            self.add_goal_to_scroll(goal)

    def add_goal_to_scroll(self, goal: ToDoWidget.ToDoWidget):
        self.goals.add_event(goal)

    def _add_goal(self, *args):

        select_date, select_time, goal_text, select_tag_name, select_tag_img_path = args

        def convert_to_24hrs(time):
            time_24hrs = datetime.datetime.strptime(' '.join(map(str, time)), '%I %M %p').time()
            return time_24hrs

        date = select_date.toString("yyyy-MM-dd")
        time_24hrs = convert_to_24hrs(select_time)

        date_time = f"{date} {time_24hrs}"
        DBHandler.insert_to_table(Query.insert_to_goal, *(date_time, select_tag_name, select_tag_img_path, goal_text))

    def create_new_goal(self):
        window = AddWindow.AddWindow(self.db_notifier)

        if window.exec():
            self._add_goal(*window.get_info())
