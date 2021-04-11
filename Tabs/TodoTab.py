import threading
import sqlite3
import datetime
import concurrent.futures

from PyQt5 import QtWidgets
from Todo import TodoScrollArea, ToDoWidget
from CreateWindow import AddWindow


class TodoPage(QtWidgets.QWidget):

    def __init__(self, db_change, *args, **kwargs):
        super(TodoPage, self).__init__(*args, **kwargs)

        self.db_change_notifier = db_change

        self.hLayout = QtWidgets.QHBoxLayout(self)

        self.todo = TodoScrollArea.TodoScrollArea()

        self.create_new = QtWidgets.QPushButton("Add Todo")
        self.create_new.clicked.connect(self.add_todo)

        self.hLayout.addWidget(self.todo)
        self.hLayout.addWidget(self.create_new)

    def add_todo(self):
        window = AddWindow.AddWindow(self.db_notifier)

        if window.exec():
            # select_date, select_time, goal_text, select_tag_name, select_tag_img_path = window.get_info()
            self._add_todo(*window.get_info())

    def load_from_db(self):
        with sqlite3.connect(self.sql_file, check_same_thread=False) as conn:
            curr = conn.cursor()
            curr.execute("SELECT * FROM goal ORDER BY datetime")
            items = curr.fetchall()

        return items

    def load_todo(self):

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self.load_from_db)
            executor.shutdown(True)
            goals = future.result()

        for index, info in enumerate(goals):
            goal = ToDoWidget.ToDoWidget()
            goal.set_info(*info)
            self.add_goal_to_scroll(goal)

    def add_todo_to_scroll(self, goal: ToDoWidget.ToDoWidget):
        self.goals.add_event(goal)

    def add_todo_to_db(self, *args):
        # print("ARgs: ", args)
        select_date, select_time, goal_text, select_tag_name, select_tag_img_path = args

        def convert_to_24hrs(time):
            time_24hrs = datetime.datetime.strptime(' '.join(map(str, time)), '%I %M %p').time()
            return time_24hrs

        date = select_date.toString("yyyy-MM-dd")
        time_24hrs = convert_to_24hrs(select_time)

        date_time = f"{date} {time_24hrs}"
        # print(f"Date and time: {date} {time_24hrs}")

        with sqlite3.connect(self.sql_file, check_same_thread=False) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS todo(datetime DATETIME , tag_name VARCHAR(30), "
                         "tag_img_path VARCHAR(100), goal_text VARCHAR(2000))")

            conn.execute("INSERT INTO goal VALUES(?, ?, ?, ?)", (date_time, select_tag_name,
                                                                 select_tag_img_path, goal_text))

            conn.commit()

    def _add_todo(self, *args):
        thread = threading.Thread(target=self.add_goal_to_db, args=args)
        thread.start()


