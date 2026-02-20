import sys

from PySide6.QtQuickControls2 import QQuickStyle
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

# import your modules
from api import UsersService
from application import UsersViewModel


def main():
    QQuickStyle.setStyle("Universal")

    app = QGuiApplication(sys.argv)

    engine = QQmlApplicationEngine()

    users_service = UsersService()
    users_vm = UsersViewModel(users_service)

    engine.rootContext().setContextProperty("usersVM", users_vm)
    engine.load("ui/main.qml")
    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
