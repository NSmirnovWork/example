from PySide6.QtQml import qmlRegisterType

from .user_list_model import UserListModel


def register_types():
    qmlRegisterType(UserListModel, "UserListModel", 1, 0, "UserListModel")
