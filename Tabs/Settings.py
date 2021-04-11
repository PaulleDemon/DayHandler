import os

from DataBaseOperations import DBHandler, Query
from PyQt5 import QtWidgets, QtGui
from CustomizedWidgets import Switch
from Todo.TagDisplayer import TagDisplayer


# todo: please check before deleting tags if there are events associated with that tag
class Settings(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(Settings, self).__init__(*args, **kwargs)

        self.sql_file = r"UserResources/userTodo.db"

        self.grid = QtWidgets.QGridLayout(self)
        self.switch_btn = Switch.Switch()
        self.tags_scroll_area = AvailableTagScrollArea()

        self.grid.addWidget(QtWidgets.QLabel("Theme"), 0, 0)
        self.grid.addWidget(self.switch_btn, 0, 1)

        self.btn = QtWidgets.QPushButton("Reload")  # todo: this button is no longer needed
        self.btn = QtWidgets.QPushButton("Reload")  # todo: this button is no longer needed
        self.btn.clicked.connect(self.load_tags)

        self.grid.addWidget(self.tags_scroll_area, 1, 0)
        self.grid.addWidget(self.btn, 2, 0)

        self.tag_items = None
        self.load_tags()

    def load_tags(self):

        self.tag_items = DBHandler.get_data(Query.get_all_tags)
        print("Tag items: ", self.tag_items)
        self.tags_scroll_area.delete_all()

        # print("Tags from DB: ", self.tag_items)
        for tag in self.tag_items:
            new_tag = TagDisplayer(tag[0], tag[1])
            new_tag.DeleteTagSignal.connect(self.delete_tag)
            self.add_to_scroll_area(new_tag)

    def delete_tag(self, tag_name: str, tag_img_path: str):

        try:
            DBHandler.delete_data(Query.delete_tag, tag_name, tag_img_path)
            os.remove(tag_img_path)

        except FileNotFoundError:
            print("File not found")

    def add_to_scroll_area(self, tag: TagDisplayer):
        self.tags_scroll_area.add_tag(tag)

    def db_changed(self):
        print("Notified the change")
        self.load_tags()


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
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            widget.deleteLater()
