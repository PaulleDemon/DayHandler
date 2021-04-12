from PyQt5 import QtWidgets, QtGui, QtCore
from DataBaseOperations import DBHandler, Query


class TagDisplayer(QtWidgets.QWidget):
    DeleteTagSignal = QtCore.pyqtSignal(str, str, list)

    def __init__(self, tag_name, img_path, *args, **kwargs):
        super(TagDisplayer, self).__init__(*args, **kwargs)

        self.f_layout = QtWidgets.QFormLayout(self)
        self.img_path = img_path

        self.tag_name = QtWidgets.QLabel(tag_name)
        self.tag_image = QtWidgets.QLabel()
        self.deleteBtn = QtWidgets.QPushButton(icon=QtGui.QIcon(r'Resources/Images/Delete_black.png'))
        self.deleteBtn.clicked.connect(self.delete_tag)

        self.img = QtGui.QPixmap(self.img_path)
        self.img = self.img.scaled(50, 50)

        self.tag_image.setPixmap(self.img)

        self.f_layout.addRow(self.tag_name, self.tag_image)
        self.f_layout.addRow(self.deleteBtn)

    def delete_tag(self):
        delete = QtWidgets.QMessageBox.No

        associates = ""
        associate_events = []
        associate_msg = "There are {events} associated with this tag"

        tag = self.tag_name.text()

        def messageBox(self):
            nonlocal delete
            msg = QtWidgets.QMessageBox()
            msg.setIcon(msg.NoIcon)

            message =  f"Are you sure you want to delete this tag? "

            if associate_events:
                message = f"<div style='color:red'>{associates}</div>. " + message

            delete = msg.question(self, "Confirmation", message, msg.Yes | msg.No)

        goal = DBHandler.get_data(Query.get_goal_where_tag, tag)
        todo = DBHandler.get_data(Query.get_todo_where_tag, tag)

        if goal:
            associate_events.append("goals")

        if todo:
            associate_events.append("todos")

        associates = associate_msg.format(events=', '.join(associate_events))
        messageBox(self)

        print("associated events", associate_events)
        if delete == QtWidgets.QMessageBox.Yes:
            self.DeleteTagSignal.emit(tag, self.img_path, associate_events)
            self.deleteLater()
