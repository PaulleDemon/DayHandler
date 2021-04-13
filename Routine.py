import sys
from DataBaseOperations import DBHandler

from PyQt5 import QtWidgets, QtGui

from CustomizedWidgets import HorizontalTabs
from Tabs import HomeTab, TodoTab, ProjectsTab, GoalTab, Settings


class TabbedWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(TabbedWidget, self).__init__(*args, **kwargs)

        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.vlayout.setContentsMargins(0, 0, 0 , 0)

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

        self.tabs.addTab(self.home_page, QtGui.QIcon(r'Resources/Images/Home_Black.png'), "Home Page")
        self.tabs.addTab(self.todo_page, QtGui.QIcon(r'Resources/Images/Todo_black.png'), "Todo page")
        self.tabs.addTab(self.program_page, QtGui.QIcon(r'Resources/Images/Project_black.png'), "Projects")
        self.tabs.addTab(self.goal_page, QtGui.QIcon(r'Resources/Images/Goal_black.png'), "Goals")
        self.tabs.addTab(self.settings, QtGui.QIcon(r'Resources/Images/Settings_black.png'), "Settings")

        self.layout().addWidget(self.tabs)
        self.setMinimumSize(850, 450)


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    message = TabbedWidget()
    message.show()

    sys.exit(app.exec())