import sqlite3
import concurrent.futures
import threading
from PyQt5 import QtWidgets, QtGui
from CustomizedWidgets import Switch
from Todo.TagDisplayer import TagDisplayer


class Settings(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(Settings, self).__init__(*args, **kwargs)

        self.sql_file = r"UserResources/userTodo.db"

        self.grid = QtWidgets.QGridLayout(self)
        self.switch_btn = Switch.Switch()
        self.tags_scroll_area = AvailableTagScrollArea()

        self.grid.addWidget(QtWidgets.QLabel("Theme"), 0, 0)
        self.grid.addWidget(self.switch_btn, 0, 1)

        self.btn = QtWidgets.QPushButton("Reload")
        self.btn.clicked.connect(self.load_tags)

        self.grid.addWidget(self.tags_scroll_area, 1, 0)
        self.grid.addWidget(self.btn, 2, 0)

        self.tag_items = None
        self.load_tags()
        print("SELF: ", self)

    def get_tags_from_db(self):
        with sqlite3.connect(self.sql_file, check_same_thread=False) as conn:
            curr = conn.cursor()
            try:
                curr.execute("SELECT * FROM tag  ORDER BY tag_name ASC;")
                items = curr.fetchall()

            except sqlite3.OperationalError:
                print("SQl error occured")
                items = []

        return items

    def db_update(self):  # todo: this doesn't update correctly temporarily use the reload button
        # self.load_tags()
        # print("EMIT Received", self)
        pass

    def load_tags(self):

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self.get_tags_from_db)
            self.tag_items = future.result()

        self.tags_scroll_area.delete_all()

        print("Tags from DB: ", self.tag_items)
        for tag in self.tag_items:
            new_tag = TagDisplayer(tag[0], tag[1])
            new_tag.DeleteTagSignal.connect(self.delete_tag)
            self.add_to_scroll_area(new_tag)

    def delete_tag_from_db(self, tag_name, tag_img_path):
        print("Thread: ", tag_name, tag_img_path)
        with sqlite3.connect(self.sql_file, check_same_thread=False) as conn:
            conn.execute("DELETE FROM tag WHERE tag_name = (?) AND tag_path = (?)", (tag_name, tag_img_path))
            conn.commit()
            # curr = conn.cursor()
            # curr.execute("SELECT * FROM tag  ORDER BY tag_name ASC;")
            # items = curr.fetchall()
            # print("Items: ", items)
        # todo delete the file also from tag_images pls do it in the same thread

    def delete_tag(self, tag_name: str, tag_img_path: str):
        print("Notified")
        thread = threading.Thread(target=self.delete_tag_from_db, args=(tag_name, tag_img_path))
        thread.start()

    def add_to_scroll_area(self, tag: TagDisplayer):
        self.tags_scroll_area.add_tag(tag)
        # print("Widget: ", self.tags_scroll_area.count_widgets(), self.tags_scroll_area)


class AvailableTagScrollArea(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(AvailableTagScrollArea, self).__init__(*args, **kwargs)

        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.vlayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.vlayout)

        self.scroll_widget = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout()
        self.scroll_widget.setLayout(self.scroll_layout)

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)

        self.scroll_area.setMinimumHeight(100)
        self.scroll_area.setMaximumHeight(400)

        self.vlayout.addWidget(self.scroll_area)

    def count_widgets(self):
        return self.scroll_layout.count()

    def add_tag(self, todoWidget: TagDisplayer):  # adds todoWidget to scroll area
        print("Got Tag: ", todoWidget.tag_name.text(), self.scroll_layout.count())
        self.scroll_layout.addWidget(todoWidget)

    def delete_at_index(self, index):
        try:
            self.scroll_layout.itemAt(index).widget().deleteLater()
        except Exception:
            pass

    def delete_all(self):
        layout = self.scroll_layout
        print("Deleted ALl")
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            print("Deleting")
            if widget is not None:
                widget.deleteLater()

        print("scroll Layout :", layout.count())