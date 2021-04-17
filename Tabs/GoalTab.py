from Utils import Utils
from Utils.DataBaseOperations import DBHandler, Query
from PyQt5 import  QtWidgets
from Todo import EventScrollArea, EventDisplayer
from CreateWindow import AddWindow


class GoalPage(QtWidgets.QWidget):

    def __init__(self,  *args, **kwargs):
        super(GoalPage, self).__init__(*args, **kwargs)

        self.sql_file = r'UserResources/userTodo.db'

        self.hLayout = QtWidgets.QHBoxLayout(self)

        self.goals = EventScrollArea.EventScrollArea()
        self.create_new = QtWidgets.QPushButton("Create New Goal")
        self.create_new.clicked.connect(self.create_new_goal)

        self.hLayout.addWidget(self.goals)
        self.hLayout.addWidget(self.create_new)

        self.load_goals()

    def load_goals(self):  # loads goals from Db and calls add_goal_to_scroll to add the goal to scroll area

        goals = DBHandler.get_data(Query.get_all_goals)

        self.goals.delete_all()

        for info in goals:
            goal = EventDisplayer.EventDisplayer("Goal")
            goal.set_info(*info)
            self.add_goal_to_scroll(goal)

    def add_goal_to_scroll(self, goal: EventDisplayer.EventDisplayer):  # adds goal to scroll area
        self.goals.add_event(goal)

    def _add_goal(self, *args):  # adds goal to data base
        select_date, select_time, goal_text, select_tag_name, select_tag_img_path = args

        date = select_date.toString("yyyy-MM-dd")
        time_24hrs = Utils.convert12hrsTo24hrs(' '.join(map(str, select_time)), "%I %M %p")

        date_time = f"{date} {time_24hrs}"
        DBHandler.insert_to_table(Query.insert_to_goal, *(date_time, select_tag_name, select_tag_img_path, goal_text))

    def create_new_goal(self):  # a pop-up asking user to create a new goal
        window = AddWindow.AddWindow()

        if window.exec():
            self._add_goal(*window.get_info())
            self.load_goals()
            DBHandler.notify("home_page")

    def db_changed(self):
        self.load_goals()