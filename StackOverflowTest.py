import sys
from PyQt5 import QtWidgets


class ScrollingLayout(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(ScrollingLayout, self).__init__(*args, **kwargs)

        self.vlayout = QtWidgets.QVBoxLayout(self)
        self.vlayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.vlayout)

        self.scroll_widget = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout()
        self.scroll_widget.setLayout(self.scroll_layout)

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)

        self.scroll_area.setMinimumHeight(100)
        self.scroll_area.setMaximumHeight(400)

        self.vlayout.addWidget(self.scroll_area)

    def count_widgets(self):
        return self.scroll_layout.count()

    def add_label(self):
        lbl = QtWidgets.QLabel("Hello")
        lbl.setMinimumHeight(50)
        lbl.setStyleSheet("background-color: black; color: white")
        self.scroll_layout.addWidget(lbl)

    def delete_at_index(self, index):
        try:
            self.scroll_layout.itemAt(index).widget().deleteLater()
        except Exception:
            pass

    def delete_all(self):
        layout = self.scroll_layout

        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        print("scroll Layout :", self.scroll_layout)


def main():
    app = QtWidgets.QApplication(sys.argv)

    widget = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout(widget)

    scroll = ScrollingLayout()

    add_btn = QtWidgets.QPushButton("Add")
    add_btn.clicked.connect(scroll.add_label)

    delete_btn = QtWidgets.QPushButton("delete at index 0")
    delete_btn.clicked.connect(lambda: scroll.delete_at_index(0))

    delete_all_btn = QtWidgets.QPushButton("delete all")
    delete_all_btn.clicked.connect(scroll.delete_all)

    layout.addWidget(scroll)
    layout.addWidget(add_btn)
    layout.addWidget(delete_btn)
    layout.addWidget(delete_all_btn)

    widget.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()