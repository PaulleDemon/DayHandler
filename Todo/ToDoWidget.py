import os
import re
import shutil
from datetime import datetime

import ImagePaths
import concurrent.futures
from CreateWindow import AddWindow
from DataBaseOperations import DBHandler, Query

from datetime import datetime
from PyQt5 import QtWidgets, QtGui, QtCore


class SelectTodo(QtWidgets.QWidget):
    """ This create the combobox with existing tags and a button to create new tags"""

    def __init__(self, *args, **kwargs):
        super(SelectTodo, self).__init__(*args, **kwargs)

        self.tag_image_dir = 'UserResources/tag_images'
        self.sql_file = 'UserResources/userTodo.db'
        self.new_tag_name = ""
        self.new_tag_img = ""
        self.tag_items = []
        self.place_holder_text = "--- Select Tag ---"

        self.combo_box = QtWidgets.QComboBox()
        self.combo_box.addItem(self.place_holder_text)

        model = self.combo_box.model()
        item = model.item(0, 0)
        item.setEnabled(False)

        self.new_tag = QtWidgets.QPushButton("Add New Tag")
        self.new_tag.clicked.connect(self.add_new_tag)

        self.h_layout = QtWidgets.QHBoxLayout(self)

        self.h_layout.addWidget(self.combo_box)
        self.h_layout.addWidget(self.new_tag)

        self.load_tags()

    def load_tags(self):

        self.tag_items = DBHandler.get_data(Query.get_all_tags)
        for item in self.tag_items:
            self.add_item(item[0], item[1])

    def set_current_tag(self, tag_name: str):
        index = self.combo_box.findData(tag_name)
        if index > -1:
            self.combo_box.setCurrentIndex(index)

    def get_file_names(self):  # Returns the sql file name and tag image directory
        return self.sql_file, self.tag_image_dir

    def add_item(self, value='', img=''):  # method to add values to combobox

        if self.combo_box.itemText(0) == self.place_holder_text:
            self.combo_box.removeItem(0)

        self.combo_box.addItem(QtGui.QIcon(img), value)
        self.combo_box.setCurrentIndex(self.combo_box.count() - 1)

    def add_new_tag(self):  # This method will call a pop-up to create a new tag

        new = NewTag(self)

        if new.exec():
            self.new_tag_name, self.new_tag_img = new.get_tag()
            self.add_item(self.new_tag_name, self.new_tag_img)

            if not os.path.isdir(self.tag_image_dir):  # check if the image folder exists if it doesn't exits create it
                os.mkdir(self.tag_image_dir)

            if os.path.isdir(self.tag_image_dir):
                self.commit_to_db()

    def commit_to_db(self):  # All the files saving will be done here

        # makes a copy of the file and places it in tag_image folder
        copy_path = shutil.copy2(self.new_tag_img, f'{self.tag_image_dir}/')
        self.new_tag_img = copy_path
        DBHandler.insert_to_table(Query.insert_to_tag, self.new_tag_name, copy_path)
        DBHandler.notify("settings")  # notifies the setting class about the change

    def get_tag(self):  # returns tag_name and image_path as a list
        try:
            if self.combo_box.itemText(0) != self.place_holder_text:
                print("Current: ", self.combo_box.currentText())
                current_tag = self.combo_box.currentText()
                current_selected_tag = DBHandler.get_data(Query.get_tag_where, current_tag)[0]
                return current_selected_tag

        except Exception as e:
            print("Exception: Occured", e)
            return None


class NewTag(QtWidgets.QDialog):
    # creates a new tag window where the user will be asked to enter a tag name and an image

    def __init__(self, parent, *args, **kwargs):
        super(NewTag, self).__init__(*args, **kwargs)
        self.parent = parent

        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        self.setWindowTitle("Select Tag")
        self.setModal(True)

        self.setFixedSize(350, 250)

        self.v_layout = QtWidgets.QVBoxLayout(self)
        self.g_layout = QtWidgets.QGridLayout()

        self.messege_lbl = QtWidgets.QLabel('')
        self.messege_lbl.setStyleSheet("QLabel{color: red;}")

        self.img_lbl = QtWidgets.QLabel()
        self.img = QtGui.QPixmap()

        self.tag_name = QtWidgets.QLineEdit()
        # self.tag_name.property("mandatoryfield")
        self.tag_name.setStyleSheet("QLineEdit[mandatoryfield=True]{border: 1px solid red;}")

        self.tag_name.setMaxLength(25)

        self.tag_image = QtWidgets.QPushButton("Add Images")
        self.tag_image.setStyleSheet("QPushButton[mandatoryfield=True]{border: 1px solid red;}")

        self.tag_image.setMaximumWidth(100)
        self.tag_image.clicked.connect(self.openFileDialog)

        self.g_layout.addWidget(QtWidgets.QLabel("Tag Name:"), 0, 0)
        self.g_layout.addWidget(QtWidgets.QLabel("Select Images"), 0, 1)
        self.g_layout.addWidget(self.tag_name, 1, 0)
        self.g_layout.addWidget(self.tag_image, 1, 1)

        self.img_h_layout = QtWidgets.QHBoxLayout()

        self.img_h_layout.addWidget(QtWidgets.QLabel("Images: "))
        self.img_h_layout.addWidget(self.img_lbl)

        self.ok_cancel_layout = QtWidgets.QHBoxLayout()

        self.ok_btn = QtWidgets.QPushButton("ok")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        self.ok_btn.clicked.connect(self.confirm)
        self.cancel_btn.clicked.connect(self.close)

        self.ok_cancel_layout.addWidget(self.ok_btn)
        self.ok_cancel_layout.addWidget(self.cancel_btn)

        self.v_layout.addWidget(self.messege_lbl)
        self.v_layout.addLayout(self.g_layout)
        self.v_layout.addLayout(self.img_h_layout)
        self.v_layout.addLayout(self.ok_cancel_layout)

        self.filePath = ""

    def openFileDialog(self):
        self.filePath = QtWidgets.QFileDialog.getOpenFileName(self, 'OpenFile',
                                                              filter="Images files (*.jpg *.gif *.png)")[0]
        self.img.load(self.filePath)
        self.img = self.img.scaled(200, 100, QtCore.Qt.KeepAspectRatio)
        self.img_lbl.setPixmap(self.img)

    def get_tag(self):
        return self.tag_name.text(), self.filePath

    def confirm(self):

        self.tag_name.setProperty("mandatoryfield", 'False')
        self.tag_image.setProperty("mandatoryfield", 'False')

        self.tag_name.style().unpolish(self.tag_name)
        self.tag_name.style().polish(self.tag_name)

        self.tag_image.style().unpolish(self.tag_image)
        self.tag_image.style().polish(self.tag_image)
        self.update()

        text = self.tag_name.text()

        strCheck = re.match('^[\w ]+$', text) is not None

        if len(text) < 2 or text == self.parent.place_holder_text or not strCheck:
            self.tag_name.setProperty("mandatoryfield", 'True')
            self.tag_name.style().unpolish(self.tag_name)
            self.tag_name.style().polish(self.tag_name)
            self.update()
            return

        if self.filePath == '':
            self.tag_image.setProperty("mandatoryfield", 'True')
            self.tag_image.style().unpolish(self.tag_image)
            self.tag_image.style().polish(self.tag_image)
            self.update()
            return

        def check_db(self):
            db_path, img_folder = self.parent.get_file_names()
            items = DBHandler.get_data(Query.get_all_tags)

            tag_name, file_loc = self.get_tag()
            img_exists = os.path.isfile(
                os.path.join(img_folder, os.path.basename(file_loc)))  # checks if the image already exists

            return any(tag_name == x[0] for x in items) or img_exists

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(check_db, self)
            return_val = future.result()

        if return_val:
            self.messege_lbl.setText("This tag name or image already exists")
            return

        self.accept()


# todo: scroll the display of the event is not good looking there is lot of space between date and todo_scroll info
# todo: display time in words
# todo: add completed button
class ToDoWidget(QtWidgets.QWidget):
    """ Widget that adds information, tag and time about an event"""
    event_types = {"Goal": ["goal_page", Query.delete_goal_where_id, Query.update_goal_where_id],
                   "Project": ["project_page", Query.delete_project_where_id, Query.update_project_where_id],
                   "Todo": ["todo_page", Query.delete_todo_where_id, Query.update_todo_where_id]}

    def __init__(self, event_type: str, *args, **kwargs):
        super(ToDoWidget, self).__init__(*args, **kwargs)

        self.setObjectName("EventDisplayer")

        self.type = event_type
        self.event_id = None


        # self.setStyleSheet("background-color: transparent;")

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.backgroundFrame = QtWidgets.QFrame()
        self.layout.addWidget(self.backgroundFrame)

        self.widget_layout = QtWidgets.QGridLayout(self.backgroundFrame)

        self.tag = Tag()

        self.time_info = QtWidgets.QLabel()
        self.time_info.setMaximumHeight(50)

        self.toDo_info = QtWidgets.QLabel()
        self.toDo_info.setWordWrap(True)

        self.event_type = QtWidgets.QLabel()  # used to specify the type of event when displaying in home page

        self.edit_btn = QtWidgets.QPushButton("🖊")
        self.delete_btn = QtWidgets.QPushButton()
        self.delete_btn.setIcon(QtGui.QIcon(ImagePaths.ImagePaths.get_image("delete")))

        self.edit_btn.clicked.connect(self.edit_event)
        self.delete_btn.clicked.connect(self.delete_event)
        self.widget_layout.addWidget(self.delete_btn, 0, 0)
        self.widget_layout.addWidget(self.edit_btn, 0, 1)

        self.widget_layout.addWidget(self.event_type, 1, 0)
        self.widget_layout.addWidget(self.time_info, 2, 0)
        self.widget_layout.addWidget(self.tag, 2, 1, QtCore.Qt.AlignRight)
        self.widget_layout.addWidget(self.toDo_info, 3, 0)

    def set_event_id(self, event_id):
        self.event_id = event_id

    def set_info(self, *args):
        self.event_id, date_time, tag_name, tag_img_path, text = args

        def change_format(_date_time):
            _date, _time = _date_time.split()
            time_24hrs = datetime.strptime(_time, "%H:%M:%S")
            date_yy_mm_dd = datetime.strptime(_date, "%Y-%m-%d")
            return date_yy_mm_dd.strftime("%d/%m/%Y"), time_24hrs.strftime("%I:%M %p")

        date, time = change_format(date_time)

        self.time_info.setText(f"{time} {date}")
        self.toDo_info.setText(text)
        self.set_tag(tag_name, tag_img_path)
        print("CHANGED: ", self.event_id, date_time, tag_name, tag_img_path, text)

    def set_tag(self, tag, imgPath):
        self.tag.setTag(tag, imgPath)

    def set_event_type(self):
        self.event_type.setText(f"Event type: {self.type}")

    def delete_event(self):
        delete = QtWidgets.QMessageBox.No

        def messageBox():
            nonlocal delete
            msg = QtWidgets.QMessageBox()

            msg.setWindowTitle("Confirmation")
            msg.setText("Are you sure you want to delete this event? ")
            msg.setStandardButtons(msg.Yes | msg.No)
            delete = msg.exec_()

        messageBox()
        if delete == QtWidgets.QMessageBox.Yes:
            query = self.event_types[self.type][1]
            DBHandler.delete_data(query, self.event_id)
            self.deleteLater()
            self.notify()

    def edit_event(self):
        window = AddWindow.AddWindow("Update")

        time, time_period, date = self.time_info.text().split()
        date = list(map(int, date.split('/')[::-1]))
        time = time.split(':')
        time.append(time_period)

        window.preset(*(date, time, self.tag.getTag(), self.toDo_info.text()))

        if window.exec():
            query = self.event_types[self.type][2]
            select_date, select_time, goal_text, select_tag_name, select_tag_img_path = window.get_info()

            def convert_to_24hrs(time):
                time_24hrs = datetime.strptime(' '.join(map(str, time)), '%I %M %p').time()
                return time_24hrs

            date = select_date.toString("yyyy-MM-dd")
            time_24hrs = convert_to_24hrs(select_time)

            date_time = f"{date} {time_24hrs}"
            DBHandler.update_data(query, *(date_time, select_tag_name, select_tag_img_path, goal_text), self.event_id)
            self.set_info(*(self.event_id, date_time, select_tag_name, select_tag_img_path, goal_text))
            self.notify()

    def notify(self):
        DBHandler.notify("home_page")
        DBHandler.notify(self.event_types[self.type][0])


class Tag(QtWidgets.QWidget):
    """ widget that creates the tag with a image and text
        Images ↓
     _________________
    | ☕ Coffee break |
    ------------------
    """

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)

        self.setObjectName("Tag")

        self.hLayout = QtWidgets.QHBoxLayout()
        self.hLayout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.hLayout)

        self.tag_name = QtWidgets.QLabel()
        self.tag_image = QtWidgets.QLabel()
        self.pixMap = QtGui.QPixmap()

        self.hLayout.addWidget(self.tag_image)
        self.hLayout.addWidget(self.tag_name)

    def setTag(self, tag: str, imagePath: str):
        self.pixMap.load(imagePath)
        self.pixMap = self.pixMap.scaled(50, 50, QtCore.Qt.KeepAspectRatio)

        self.tag_image.setPixmap(self.pixMap)
        self.tag_name.setText(tag)

    def getTag(self):
        return self.tag_name.text()