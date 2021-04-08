import datetime
import os
import re
import shutil
import sqlite3
import threading
import concurrent.futures
import DbHandler

from PyQt5 import QtWidgets, QtGui, QtCore


class SelectTodo(QtWidgets.QWidget):

    """ This create the combobox with existing tags and a button to create new tags"""

    def __init__(self, db_notifier, *args, **kwargs):
        super(SelectTodo, self).__init__(*args, **kwargs)

        self.tag_image_dir = 'UserResources/tag_images'
        self.sql_file = 'UserResources/userTodo.db'
        self.new_tag_name = ""
        self.new_tag_img = ""
        self.tag_items = []
        self.db_notifier = db_notifier

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

    def get_tags_from_db(self):
        with sqlite3.connect(self.sql_file, check_same_thread=False) as conn:
            curr = conn.cursor()
            try:
                curr.execute("SELECT * FROM tag")
                items = curr.fetchall()

            except sqlite3.OperationalError:
                items = []

        return items

    def load_tags(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self.get_tags_from_db)
            self.tag_items = future.result()

        for item in self.tag_items:
            self.add_item(item[0], item[1])

    def get_file_names(self):  # Returns the sql file name and tag image directory
        return self.sql_file, self.tag_image_dir

    def add_item(self, value='', img=''):  # method to add values to combobox

        if self.combo_box.itemText(0) == self.place_holder_text:
            self.combo_box.removeItem(0)

        self.combo_box.addItem(QtGui.QIcon(img), value)
        self.combo_box.setCurrentIndex(self.combo_box.count() - 1)

    def add_new_tag(self):  # This method will call a pop-up to create a new tag
        self._create_db()
        new = NewTag(self)

        if new.exec():
            self.new_tag_name, self.new_tag_img = new.get_tag()
            self.add_item(self.new_tag_name, self.new_tag_img)

            if not os.path.isdir(self.tag_image_dir):  # check if the image folder exists if it doesn't exits create it
                os.mkdir(self.tag_image_dir)

            if os.path.isdir(self.tag_image_dir):
                thread = threading.Thread(target=self.commit_to_db, daemon=True)
                thread.start()

    def _create_db(self):  # creates the sql table if it doesn't exist
        with sqlite3.connect(self.sql_file) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS tag(tag_name VARCHAR(30) UNIQUE, tag_path VARCHAR(100) "
                         "UNIQUE)")

    def commit_to_db(self):  # All the files saving will be done here

        # makes a copy of the file and places it in tag_image folder
        copy_path = shutil.copy2(self.new_tag_img, f'{self.tag_image_dir}/')
        self.new_tag_img = copy_path

        with sqlite3.connect(self.sql_file, check_same_thread=False) as conn:

            try:
                conn.execute("INSERT INTO tag(tag_name, tag_path) VALUES(?, ?)", (self.new_tag_name, copy_path))
                conn.commit()
                self.db_notifier.notify()

            except sqlite3.IntegrityError:
                print("Not Unique")

    def get_tag(self):  # method that returns current tag from combobox
        return self.combo_box.currentIndex() if self.combo_box.itemText(0) != self.place_holder_text else None


class NewTag(QtWidgets.QDialog):

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
            items = []
            with sqlite3.connect(db_path, check_same_thread=False) as conn:
                curr = conn.cursor()
                curr.execute("SELECT * FROM tag")
                items = curr.fetchall()

            tag_name, file_loc = self.get_tag()
            img_exists = os.path.isfile(
                os.path.join(img_folder, os.path.basename(file_loc)))  # checks if the image already exists

            return any(tag_name == x[0] for x in items) or img_exists

        return_val = False
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(check_db, self)
            return_val = future.result()

        if return_val:
            self.messege_lbl.setText("This tag name or image already exists")
            return

        self.accept()


class ToDoWidget(QtWidgets.QWidget):
    """ Widget that adds information, tag and time about an event"""

    def __init__(self, *args, **kwargs):
        super(ToDoWidget, self).__init__(*args, **kwargs)

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

        self.widget_layout.addWidget(self.tag, 0, 1, QtCore.Qt.AlignRight)
        self.widget_layout.addWidget(self.time_info, 0, 0)
        self.widget_layout.addWidget(self.toDo_info, 1, 0)

    def setText(self, message):
        self.toDo_info.setText(message)
        self.time_info.setText(
            datetime.datetime.now().strftime("%A, %b %d, %Y, %H:%M %p"))  # todo: change this to the time the user picks

    def setTag(self, tag, imgPath):
        self.tag.setTag(tag, imgPath)


class Tag(QtWidgets.QWidget):
    """ widget that creates the tag with a image and text
        Images ↓
     _________________
    | ☕ Coffee break |
    ------------------
    """

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)

        self.hLayout = QtWidgets.QHBoxLayout()
        self.hLayout.setContentsMargins(0, 0, 0, 0)
        self.hLayout.setSpacing(0)

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
