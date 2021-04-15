import sys

from ImagePaths import ImagePaths
from PyQt5 import QtWidgets, QtGui, QtCore
from DataBaseOperations import DBHandler
from CustomizedWidgets import HorizontalTabs
from Tabs import HomeTab, TodoTab, ProjectsTab, GoalTab, Settings


class TabbedWidget(QtWidgets.QWidget):
    shown = False

    def __init__(self, *args, **kwargs):
        super(TabbedWidget, self).__init__(*args, **kwargs)

        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.vlayout.setContentsMargins(0, 0, 0 , 0)
        ImagePaths.set_theme(0)
        self.tabs = HorizontalTabs.TabWidget()
        self.tabs.setStyleSheet("QTabBar::tab {min-height: 250px; min-width: 50px}")  # todo_scroll: remove this and paste it in qss

        DBHandler.initialize_files()

        self.home_page = HomeTab.HomePage()
        self.todo_page = TodoTab.TodoPage()
        self.program_page = ProjectsTab.ProgramPage()
        self.goal_page = GoalTab.GoalPage()
        self.settings = Settings.Settings()

        DBHandler.register("home_page", self.home_page)
        DBHandler.register("project_page", self.program_page)
        DBHandler.register("goal_page", self.goal_page)
        DBHandler.register("todo_page", self.todo_page)
        DBHandler.register("settings", self.settings)

        self.tabs.addTab(self.home_page, QtGui.QIcon(ImagePaths.get_image("home")), "Home Page")
        self.tabs.addTab(self.todo_page, QtGui.QIcon(ImagePaths.get_image("todo")), "Todo page")
        self.tabs.addTab(self.program_page, QtGui.QIcon(ImagePaths.get_image("project")), "Projects")
        self.tabs.addTab(self.goal_page, QtGui.QIcon(ImagePaths.get_image("goal")), "Goals")
        self.tabs.addTab(self.settings, QtGui.QIcon(ImagePaths.get_image("settings")), "Settings")

        self.layout().addWidget(self.tabs)
        self.setMinimumSize(850, 450)


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    # app.setStyle(QtWidgets.QStyleFactory.create("Fusion"))
    with open(r"DarkTheme.qss") as file:
        theme = file.read()

    print("Theme; ", theme)

    message = TabbedWidget()
    message.show()
    app.setStyleSheet(theme)

    sys.exit(app.exec())