from PySide6.QtCore import Property, QObject

from ..repository.user.i_user_repository import IUserRepository
from .user.fake_user_repository import FakeUserRepository


class Repository(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._user = None

    def getUser(self):
        return self._user

    def setUser(self, value):
        self._user = value

    user: IUserRepository = Property(QObject, getUser, setUser)

    def initFake(self):
        self._user = FakeUserRepository()
