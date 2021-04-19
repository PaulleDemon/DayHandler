import os

from Utils.ThemeController import ThemeController
from Utils.DataBaseOperations import DBHandler, Query
from PyQt5 import QtWidgets, QtCore
from CustomizedWidgets import Switch
from Event.TagDisplayer import TagDisplayer


class Settings(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(Settings, self).__init__(*args, **kwargs)

        self.setObjectName("Settings")
        self.grid = QtWidgets.QGridLayout(self)

        self.switch_btn = Switch.Switch()
        self.switch_btn.clicked.connect(self.change_theme)

        self.tags_scroll_area = AvailableTagScrollArea()

        self.grid.addWidget(QtWidgets.QLabel("Theme: "), 0, 0, QtCore.Qt.AlignLeft)
        self.grid.addWidget(self.switch_btn, 0, 1, QtCore.Qt.AlignLeft)

        self.grid.addWidget(QtWidgets.QLabel("Tags: "), 1, 0, QtCore.Qt.AlignLeft)
        self.grid.addWidget(self.tags_scroll_area, 2, 0, 1, 2)

        self.tag_items = None
        self.load_tags()
        self.set_switch_change()

    def load_tags(self):

        self.tag_items = DBHandler.get_data(Query.get_all_tags)
        self.tags_scroll_area.delete_all()

        for tag in self.tag_items:
            new_tag = TagDisplayer(tag[0], tag[1])
            new_tag.DeleteTagSignal.connect(self.delete_tag)
            self.add_to_scroll_area(new_tag)

    def delete_tag(self, tag_name: str, tag_img_path: str, associated_event: list):

        associated_dict = {"projects": [Query.delete_project_where_tag, "project_page"],
                           "goals": [Query.delete_goal_where_tag, "goal_page"],
                           "todos": [Query.delete_todo_where_tag, "todo_page"]}

        try:

            for event in associated_event:
                query, notify_page = associated_dict[event]
                DBHandler.delete_data(query, tag_name)
                DBHandler.notify(notify_page)

            if associated_event:
                DBHandler.notify("home_page")

            DBHandler.delete_data(Query.delete_tag, tag_name, tag_img_path)
            os.remove(tag_img_path)

        except FileNotFoundError:
            pass

    def add_to_scroll_area(self, tag: TagDisplayer):
        self.tags_scroll_area.add_tag(tag)

    def db_changed(self):
        self.load_tags()

    def change_theme(self):

        if self.switch_btn.isChecked():
            ThemeController.load_theme(0)

        else:
            ThemeController.load_theme(1)

    def set_switch_change(self):  # sets the switch_button to correct side
        theme = ThemeController.get_current_theme_index()
        self.switch_btn.setChecked(not theme)


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
