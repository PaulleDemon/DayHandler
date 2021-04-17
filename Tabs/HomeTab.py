from PyQt5 import QtWidgets
from Todo import EventScrollArea
from Utils.DataBaseOperations import DBHandler, Query
from Todo import EventDisplayer


class HomePage(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(HomePage, self).__init__(*args, **kwargs)

        self.hLayout = QtWidgets.QHBoxLayout()
        self.setLayout(self.hLayout)

        self.btnContainer = QtWidgets.QVBoxLayout()
        self.hLayout.addLayout(self.btnContainer)

        self.todoScrollArea = EventScrollArea.EventScrollArea()
        self.programScrollArea = EventScrollArea.EventScrollArea()

        self.hLayout.addWidget(self.todoScrollArea)
        self.hLayout.addWidget(self.programScrollArea)

        self.load_home_page()

    def load_home_page(self):  # loads events from Db and calls add_goal_to_scroll to add the goal to scroll area

        events = DBHandler.get_data(Query.get_all_tables_by_date)
        project_events = DBHandler.get_data(Query.get_all_projects)
        self.todoScrollArea.delete_all()
        self.programScrollArea.delete_all()

        for info in events:
            event = EventDisplayer.EventDisplayer(info[0])
            event.set_info(*info[1:])
            event.set_event_type()
            self.add_events_to_todo_scroll(event)

        for info in project_events:
            project = EventDisplayer.EventDisplayer("Project")
            project.set_info(*info)
            self.add_project_to_todo_scroll(project)

    def add_events_to_todo_scroll(self, event: EventDisplayer.EventDisplayer):  # adds events to scroll area
        self.todoScrollArea.add_event(event)

    def add_project_to_todo_scroll(self, event: EventDisplayer.EventDisplayer):  # adds project to scroll area
        self.programScrollArea.add_event(event)

    def db_changed(self):
        self.load_home_page()
