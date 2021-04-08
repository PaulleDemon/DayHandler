from PyQt5 import QtWidgets, QtGui, QtCore


class TagDisplayer(QtWidgets.QWidget):

    DeleteTagSignal = QtCore.pyqtSignal(str, str)

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

        def messageBox(self):
            nonlocal delete
            msg = QtWidgets.QMessageBox()
            delete = msg.question(self, "Confirmation", "Are you sure you want to delete this tag? ", msg.Yes | msg.No)

        messageBox(self)
        if delete == QtWidgets.QMessageBox.Yes:  # todo must delete from database also
            self.DeleteTagSignal.emit(self.tag_name.text(), self.img_path)
            self.deleteLater()

