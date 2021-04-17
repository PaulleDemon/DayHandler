from PyQt5 import QtWidgets, QtGui, QtCore


# A text box with character count
class TextBox(QtWidgets.QTextEdit):

    def __init__(self, font="monospace", font_size=12, maxChar=100, *args, **kwargs):
        super(TextBox, self).__init__(*args, **kwargs)

        self.charCount = 0
        self.maxChar = maxChar

        self.textChanged.connect(self.changeCount)
        self.setAcceptRichText(False)

        # add a label to self.
        self.label = QtWidgets.QLabel('', self)
        self.label.setFixedSize(150, 15)
        self.label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)

        qfont = self.font()
        qfont.setPointSize(font_size)
        qfont.setFamily(font)

        self.setFont(qfont)

        qfont.setPointSize(8)
        self.label.setFont(qfont)

        self.label_palette = self.label.palette()

        self.changeCount()

    # the label text is updated when character count is changed
    def changeCount(self):
        self.charCount = len(self.toPlainText())

        if self.charCount > self.maxChar:
            self.setText(self.toPlainText()[:self.maxChar])

        if self.charCount < self.maxChar // 3:
            self.label.setStyleSheet("color: #03ab2a")

        if self.maxChar // 3 <= self.charCount < self.maxChar // 1.5:
            self.label.setStyleSheet("color: #cae002")

        elif self.charCount >= self.maxChar // 1.5:
            self.label.setStyleSheet("color: #fa0f23")

        self.label.setText(f'{self.charCount}/{self.maxChar}')

    # The position of the label needs to be updated manually when the size of the text box changes
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.label.move(event.size().width()-self.label.width(), event.size().height()-self.label.height())

    def keyPressEvent(self, event):

        if self.charCount < self.maxChar:
            super(TextBox, self).keyPressEvent(event)

        if self.charCount >= self.maxChar:
            if event.key() in [QtCore.Qt.Key_Backspace, QtCore.Qt.Key_Delete, QtCore.Qt.Key_Up,
                               QtCore.Qt.Key_Left, QtCore.Qt.Key_Right, QtCore.Qt.Key_Down]:
                super(TextBox, self).keyPressEvent(event)

            if event.key() & QtCore.Qt.Key_A and event.modifiers() & QtCore.Qt.ControlModifier:
                super(TextBox, self).keyPressEvent(event)
