from PyQt5 import QtWidgets
from Event import EventDisplayer


class EventScrollArea(QtWidgets.QWidget):

    """ Scroll area class. Add events to this scroll area class"""

    def __init__(self, *args, **kwargs):
        super(EventScrollArea, self).__init__(*args, **kwargs)

        self.setObjectName("TodoScroll")

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

    def add_event(self, todoWidget: EventDisplayer.EventDisplayer):  # adds todoWidget to scroll area
        self.scroll_layout.addWidget(todoWidget)

    def delete_at_index(self, index):  # deletes the widgets at specific index
        try:
            self.scroll_layout.itemAt(index).widget().deleteLater()
        except Exception:
            pass

    def delete_all(self):  # deletes all the widgets in the scroll area
        layout = self.scroll_layout
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            widget.deleteLater()

