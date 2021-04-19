import math
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtProperty


class ClockWidget(QtWidgets.QWidget):
    """ Custom analog time picker abstract model must modify the members to make the clock"""

    clicked_signal = QtCore.pyqtSignal(str)

    r = 19.0
    current_index = 0

    def __init__(self, start=0, end=0, steps=1, lst=[], *args, **kwargs):
        super(ClockWidget, self).__init__(*args, **kwargs)

        self.L = lst
        self.steps = steps
        if not self.L:
            self.L = [x for x in range(start, end)]

        self.DELTA_ANGLE = (360 / len(self.L)) * (math.pi / 180)

        self.turn_angle = 5.25

        font = self.font()
        font.setPointSize(14)

        self.current_value = self.L[self.current_index]
        self.setFont(font)

        self._text_color = QtGui.QColor("#ffffff")
        self._pointer_color = QtGui.QColor("#c40202")

        self._clock_outline_color = QtGui.QColor("#ffffff")
        self._clock_bg_color = QtGui.QColor("#8f8b8b")

        self.setObjectName("ClockWidget")

    def text_color(self):
        return self._text_color

    def set_text_color(self, qcolor: QtGui.QColor):
        self._text_color = qcolor

    def pointer_color(self):
        return self._pointer_color

    def set_pointer_color(self, qcolor: QtGui.QColor):
        self._pointer_color = qcolor

    def clock_bg_color(self):
        return self._clock_bg_color

    def set_clock_bg_color(self, qcolor: QtGui.QColor):
        self._clock_bg_color = qcolor

    def clock_outline(self):
        return self._clock_outline_color

    def set_clock_outline(self, qcolor: QtGui.QColor):
        self._clock_outline_color = qcolor

    TextColor = pyqtProperty(QtGui.QColor, text_color, set_text_color)
    PointerColor = pyqtProperty(QtGui.QColor, pointer_color, set_pointer_color)

    ClockOutlineColor = pyqtProperty(QtGui.QColor, clock_outline, set_clock_outline)
    ClockColor = pyqtProperty(QtGui.QColor, clock_bg_color, set_clock_bg_color)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        r = min(self.rect().width(), self.rect().height()) / 2
        margin = 4

        rect = QtCore.QRectF(0, 0, 2 * r - margin, 2 * r - margin)
        rect.moveCenter(self.rect().center())

        painter.setPen(self._clock_outline_color)
        painter.setBrush(self._clock_bg_color)
        painter.drawEllipse(rect)

        rect = QtCore.QRectF(0, 0, self.r + 20, self.r + 20)

        if 0 <= self.current_index < len(self.L) + 1:
            c = self.center_by_index(self.current_index)
            rect.moveCenter(c)
            pen = QtGui.QPen(self._pointer_color)
            pen.setWidth(5)
            painter.setPen(pen)
            painter.drawLine(c, self.rect().center())

            painter.setBrush(self._pointer_color)
            painter.drawEllipse(rect.adjusted(5, 5, -5, -5))

        painter.setPen(self._text_color)
        for index, i in enumerate(self.L):
            c = self.center_by_index(index)
            rect.moveCenter(c)

            if index % self.steps == 0:
                painter.drawText(rect, QtCore.Qt.AlignCenter, str(i))

            else:
                painter.setBrush(self._text_color)
                painter.drawEllipse(QtCore.QRectF(rect.adjusted(22, 22, -22, -22)))

    def center_by_index(self, index):
        R = min(self.rect().width(), self.rect().height()) / 2

        angle = self.DELTA_ANGLE * index + self.turn_angle
        center = self.rect().center()

        return center + (R - self.r) * QtCore.QPointF(math.cos(angle), math.sin(angle))

    @property
    def current_value(self):
        return self._current_value

    @current_value.setter
    def current_value(self, value):
        self._current_value = value
        self.clicked_signal.emit(str(self._current_value))

    def index_by_click(self, pos):
        for index, i in enumerate(self.L):
            c = self.center_by_index(index)

            delta = QtGui.QVector2D(pos).distanceToPoint(QtGui.QVector2D(c))
            if delta < self.r:
                return index, i
        return -1, self.current_value

    def mousePressEvent(self, event):
        i, value = self.index_by_click(event.pos())

        if i >= 0:
            self.current_index = i
            self.update()
            self.current_value = value

    def minumumSizeHint(self):
        return QtCore.QSize(100, 100)
