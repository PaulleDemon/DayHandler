from PyQt5 import QtWidgets
from Todo import ToDoWidget


class TodoScrollArea(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(TodoScrollArea, self).__init__(*args, **kwargs)

        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.vlayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.vlayout)

        self.scroll_widget = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout()
        self.scroll_widget.setLayout(self.scroll_layout)

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)

        self.vlayout.addWidget(self.scroll_area)

    def add_event(self, todoWidget: ToDoWidget.ToDoWidget):  # adds todoWidget to scroll area
        self.scroll_layout.addWidget(todoWidget)

    def addTodo(self, text: str, tag_name: str, tag_icon: str):
        todo = ToDoWidget.ToDoWidget()
        todo.setText(text)
        todo.setTag(tag_name, tag_icon)
        todo.setStyleSheet('background: blue')

        self.add_event(todo)
