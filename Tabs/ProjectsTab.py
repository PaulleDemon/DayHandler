from PyQt5 import QtWidgets

from Utils import Utils
from Todo import EventDisplayer
from Todo import EventScrollArea
from CreateWindow import AddWindow
from Utils.DataBaseOperations import DBHandler, Query


class ProgramPage(QtWidgets.QWidget):

    def __init__(self,  *args, **kwargs):
        super(ProgramPage, self).__init__(*args, **kwargs)

        self.hLayout = QtWidgets.QHBoxLayout(self)

        self.program = EventScrollArea.EventScrollArea()
        self.create_new = QtWidgets.QPushButton("Create New Project")
        self.create_new.clicked.connect(self.create_new_project)

        self.hLayout.addWidget(self.program)
        self.hLayout.addWidget(self.create_new)

        self.load_projects()

    def load_projects(self):  # loads projects from Db and calls add_goal_to_scroll to add the goal to scroll area

        projects = DBHandler.get_data(Query.get_all_projects)

        self.program.delete_all()

        for info in projects:
            project = EventDisplayer.EventDisplayer("Project")
            project.set_info(*info)
            self.add_project_to_scroll(project)

    def add_project_to_scroll(self, project: EventDisplayer.EventDisplayer):  # adds goal to scroll area
        self.program.add_event(project)

    def _add_project(self, *args):  # adds goal to data base
        select_date, select_time, goal_text, select_tag_name, select_tag_img_path = args

        date = select_date.toString("yyyy-MM-dd")
        time_24hrs = Utils.convert12hrsTo24hrs(' '.join(map(str, select_time)), "%I %M %p")

        date_time = f"{date} {time_24hrs}"
        DBHandler.insert_to_table(Query.insert_to_project, *(date_time, select_tag_name, select_tag_img_path, goal_text))

    def create_new_project(self):  # a pop-up asking user to create a new goal
        window = AddWindow.AddWindow()

        if window.exec():
            self._add_project(*window.get_info())
            self.load_projects()
            DBHandler.notify("home_page")

    def db_changed(self):
        self.load_projects()



