import asyncio
import logging

from PySide6.QtCore import (
    Property,
    QAbstractListModel,
    QModelIndex,
    QObject,
    Qt,
    Signal,
    Slot,
)

from ...core.pagination import PaginationRequest
from ...domain.user.user_create import UserCreate
from ...domain.user.user_update import UserUpdate
from ...repository import Repository

log = logging.getLogger(__name__)


class UserListModel(QAbstractListModel):
    IdRole = Qt.UserRole + 1
    NameRole = Qt.UserRole + 2
    EmailRole = Qt.UserRole + 3

    repositoryChanged = Signal()

    loadingChanged = Signal()
    errorChanged = Signal()
    pageChanged = Signal()
    totalChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._repository: Repository | None = None
        self._items = []
        self._loading = False
        self._error = ""
        self._page = 1
        self._per_page = 10
        self._total = 0

    def getRepository(self):
        return self._repository

    def setRepository(self, repository):
        if self._repository is repository:
            return

        self._repository = repository
        self.repositoryChanged.emit()

    repository = Property(
        QObject, getRepository, setRepository, notify=repositoryChanged
    )

    @Property(bool, notify=loadingChanged)
    def isLoading(self):
        return self._loading

    @Property(str, notify=errorChanged)
    def error(self):
        return self._error

    @Property(int, notify=pageChanged)
    def page(self):
        return self._page

    @Property(int, notify=totalChanged)
    def totalPages(self):
        if self._total % self._per_page == 0:
            return self._total // self._per_page
        return (self._total // self._per_page) + 1

    def rowCount(self, parent=QModelIndex()):
        return len(self._items)

    def data(self, index, role):
        if not index.isValid():
            return None

        user = self._items[index.row()]

        return {
            self.IdRole: user.id,
            self.NameRole: user.name,
            self.EmailRole: user.email,
        }[role]

    def roleNames(self):
        return {
            self.IdRole: b"id",
            self.NameRole: b"name",
            self.EmailRole: b"email",
        }

    @Slot()
    def reload(self):
        asyncio.create_task(self._reload())

    @Slot()
    def nextPage(self):
        self._page += 1
        asyncio.create_task(self._reload())

    @Slot()
    def previousPage(self):
        self._page -= 1
        asyncio.create_task(self._reload())

    @Slot(str, str)
    def createUser(self, name, email):
        asyncio.create_task(self._create_user(name, email))

    @Slot(int, str, str)
    def updateUser(self, user_id, name, email):
        asyncio.create_task(self._update_user(user_id, name, email))

    @Slot(int)
    def deleteUser(self, user_id):
        asyncio.create_task(self._delete_user(user_id))

    def _setLoading(self, value):
        if self._loading != value:
            self._loading = value
            self.loadingChanged.emit()

    def _setError(self, value):
        self._error = value
        self.errorChanged.emit()

    async def _reload(self):
        try:
            self._setLoading(True)

            pagination_request = PaginationRequest(self._page, self._per_page)
            response = await self._repository.user.list(pagination_request)
            self.beginResetModel()
            self._items = list(response.items)
            self.endResetModel()
            self._total = response.total

            self.pageChanged.emit()
            self.totalChanged.emit()

        except Exception as e:
            log.error(e)
            self._setError(str(e))
        finally:
            self._setLoading(False)

    async def _create_user(self, name, email):
        try:
            await self._repository.user.create(UserCreate(name, email))
            await self._reload()
        except Exception as e:
            log.error(e)
            self._setError(str(e))

    async def _update_user(self, user_id, name, email):
        try:
            await self._repository.user.update(
                user_update=UserUpdate(user_id, name, email),
            )
            await self._reload()
        except Exception as e:
            log.error(e)
            self._setError(str(e))

    async def _delete_user(self, user_id):
        try:
            await self._repository.user.delete(user_id)
            await self._reload()
        except Exception as e:
            log.error(e)
            self._setError(str(e))
