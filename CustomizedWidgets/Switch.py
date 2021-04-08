from PyQt5 import QtWidgets, QtGui, QtCore


class Switch(QtWidgets.QPushButton):

    """ creates a switch like button"""

    def __init__(self, parent = None):
        super().__init__(parent)
        print('init')
        self.setCheckable(True)
        self.setMinimumWidth(66)
        self.setMinimumHeight(22)
        
        self.dark_color, self.dark_lbl = QtCore.Qt.darkGray, "Dark"
        self.light_color, self.light_lbl = QtCore.Qt.lightGray, "Light"
        
        self.radius = 10
        self.switch_width = 32

    def paintEvent(self, event):
        label = self.dark_lbl if self.isChecked() else self.light_lbl
        bg_color = self.dark_color if self.isChecked() else self.light_color

        center = self.rect().center()

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.translate(center)
        painter.setBrush(QtGui.QColor(0,0,0))

        pen = QtGui.QPen(QtCore.Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)

        painter.drawRoundedRect(QtCore.QRect(-self.switch_width, -self.radius, 2*self.switch_width, 2*self.radius),
                                self.radius, self.radius)

        painter.setBrush(QtGui.QBrush(bg_color))
        sw_rect = QtCore.QRect(-self.radius, -self.radius, self.switch_width + self.radius, 2*self.radius)
        if not self.isChecked():
            sw_rect.moveLeft(-self.switch_width)

        painter.drawRoundedRect(sw_rect, self.radius, self.radius)
        painter.drawText(sw_rect, QtCore.Qt.AlignCenter, label)