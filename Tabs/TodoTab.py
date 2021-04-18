from PyQt5 import QtWidgets

from Utils import Utils
from Event import EventScrollArea, EventDisplayer
from Utils.DataBaseOperations import DBHandler, Query
from CreateWindow import AddWindow


class TodoPage(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(TodoPage, self).__init__(*args, **kwargs)

        self.hLayout = QtWidgets.QHBoxLayout(self)

        self.todo_scroll = EventScrollArea.EventScrollArea()

        self.create_new = QtWidgets.QPushButton("Add Event")
        self.create_new.clicked.connect(self.create_new_todo)

        self.hLayout.addWidget(self.todo_scroll)
        self.hLayout.addWidget(self.create_new)

        self.load_todo()

    def load_todo(self):  # loads todos from Db and calls add_goal_to_scroll to add the goal to scroll area

        todos = DBHandler.get_data(Query.get_all_todo)

        self.todo_scroll.delete_all()

        for info in todos:
            goal = EventDisplayer.EventDisplayer("Event")
            goal.set_info(*info)
            self.add_todo_to_scroll(goal)

    def add_todo_to_scroll(self, todo: EventDisplayer.EventDisplayer):  # adds todos to scroll area
        self.todo_scroll.add_event(todo)

    # todo_scroll: This method seems redundant in all the pages maybe think of making it a static
    def _add_todo(self, *args):  # adds todos to data base
        select_date, select_time, todo_text, select_tag_name, select_tag_img_path = args

        date = select_date.toString("yyyy-MM-dd")
        time_24hrs = Utils.convert12hrsTo24hrs(' '.join(map(str, select_time)), input_format='%I %M %p')

        date_time = f"{date} {time_24hrs}"
        DBHandler.insert_to_table(Query.insert_to_todo, *(date_time, select_tag_name, select_tag_img_path, todo_text))

    def create_new_todo(self):  # a pop-up asking user to create a new todo_scroll
        window = AddWindow.AddWindow()

        if window.exec():
            self._add_todo(*window.get_info())
            self.load_todo()
            DBHandler.notify("home_page")

    def db_changed(self):
        self.load_todo()