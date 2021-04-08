from PyQt5 import QtCore


class DbChangeNotifier(QtCore.QObject):
    DbUpdated = QtCore.pyqtSignal()

    def __init__(self):  # only add items that need to be notified of the changes. Don't add all the notifiers
        self.subscribers = set()

    def register(self, item):
        self.subscribers.add(item)

    def unregister(self, item):
        self.subscribers.discard(item)

    def notify(self):
        for sub in self.subscribers:
                sub.db_update()
