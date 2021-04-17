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

        self.tabs = HorizontalTabs.TabWidget()

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

        self.tabs.addTab(self.home_page, "Home Page")
        self.tabs.addTab(self.todo_page, "Todo page")
        self.tabs.addTab(self.program_page,  "Projects")
        self.tabs.addTab(self.goal_page, "Goals")
        self.tabs.addTab(self.settings, "Settings")
        self.load_icon()

        self.layout().addWidget(self.tabs)
        self.setMinimumSize(850, 450)

    def load_icon(self):
        self.tabs.setTabIcon(0, QtGui.QIcon(ImagePaths.get_image("home")))
        self.tabs.setTabIcon(1, QtGui.QIcon(ImagePaths.get_image("todo")))
        self.tabs.setTabIcon(2, QtGui.QIcon(ImagePaths.get_image("project")))
        self.tabs.setTabIcon(3, QtGui.QIcon(ImagePaths.get_image("goal")))
        self.tabs.setTabIcon(4, QtGui.QIcon(ImagePaths.get_image("settings")))


# if __name__ == '__main__':
#
#     app = QtWidgets.QApplication(sys.argv)
#     # app.setStyle(QtWidgets.QStyleFactory.create("Fusion"))
#     with open(r"Resources/LightTheme.qss") as file:
#         theme = file.read()
#
#     ImagePaths.set_theme(1)
#     message = TabbedWidget()
#     message.show()
#     app.setStyleSheet(theme)
#
#     sys.exit(app.exec())