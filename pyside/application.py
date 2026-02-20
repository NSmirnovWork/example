from PySide6.QtCore import (
    Property,
    QAbstractListModel,
    QModelIndex,
    QObject,
    Qt,
    Signal,
    Slot,
)

from core import Pagination


class UsersModel(QAbstractListModel):
    IdRole = Qt.UserRole + 1
    NameRole = Qt.UserRole + 2
    EmailRole = Qt.UserRole + 3

    def __init__(self, users=None):
        super().__init__()
        self._users = users or []

    def rowCount(self, parent=QModelIndex()):
        return len(self._users)

    def data(self, index, role):
        user = self._users[index.row()]

        if role == self.IdRole:
            return user.id
        if role == self.NameRole:
            return user.name
        if role == self.EmailRole:
            return user.email

    def roleNames(self):
        return {
            self.IdRole: b"id",
            self.NameRole: b"name",
            self.EmailRole: b"email",
        }


class UsersViewModel(QObject):
    loadingChanged = Signal()
    pageChanged = Signal()
    totalChanged = Signal()

    def __init__(self, service):
        super().__init__()
        self._service = service
        self._model = UsersModel()
        self._loading = False
        self._pagination = Pagination()

    @Property(QObject, constant=True)
    def usersModel(self):
        return self._model

    @Property(bool, notify=loadingChanged)
    def loading(self):
        return self._loading

    @Property(int, notify=pageChanged)
    def page(self):
        return self._pagination.page

    @Property(int, notify=totalChanged)
    def totalPages(self):
        return self._pagination.total_pages

    @Slot()
    def next_page(self):
        if self.page < self.totalPages:
            self._pagination.page += 1
            self.pageChanged.emit()
            self.load_users()

    @Slot()
    def prev_page(self):
        if self.page > 1:
            self._pagination.page -= 1
            self.pageChanged.emit()
            self.load_users()

    @Slot()
    def load_users(self):
        self._loading = True
        self.loadingChanged.emit()

        result = self._service.get_users(
            page=self._pagination.page, page_size=self._pagination.page_size
        )

        self._pagination.total = result.total

        self._model.beginResetModel()
        self._model._users = result.items
        self._model.endResetModel()

        self._loading = False
        self.loadingChanged.emit()
        self.totalChanged.emit()
