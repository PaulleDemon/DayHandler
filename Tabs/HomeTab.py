import datetime

from PyQt5 import QtWidgets
from Todo import TodoScrollArea
from DataBaseOperations import DBHandler, Query
from Todo import ToDoWidget


# todo: add what kind of event it is eg: add todo if its a todo event
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

        self.load_home_page()

    def load_home_page(self):  # loads events from Db and calls add_goal_to_scroll to add the goal to scroll area

        events = DBHandler.get_data(Query.get_all_tables_by_date)
        project_events = DBHandler.get_data(Query.get_all_projects)
        print("Home Page: ", events)

        self.todoScrollArea.delete_all()
        self.programScrollArea.delete_all()

        for info in events:
            event = ToDoWidget.ToDoWidget(info[0])
            event.set_info(*info[1:])
            event.set_event_type()
            self.add_events_to_todo_scroll(event)

        for info in project_events:
            project = ToDoWidget.ToDoWidget("Project")
            project.set_info(*info)
            self.add_project_to_todo_scroll(project)

    def add_events_to_todo_scroll(self, event: ToDoWidget.ToDoWidget):  # adds events to scroll area
        self.todoScrollArea.add_event(event)

    def add_project_to_todo_scroll(self, event: ToDoWidget.ToDoWidget):  # adds project to scroll area
        self.programScrollArea.add_event(event)

    def db_changed(self):
        print("Notified the change")
        self.load_home_page()
