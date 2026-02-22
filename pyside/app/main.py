import asyncio
import sys

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickControls2 import QQuickStyle
from qasync import QEventLoop

from .application import register_types
from .repository import Repository


from PySide6.QtCore import QObject, Property, Signal


class TestObject(QObject):
    textChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._text = "Hello QML"

    def getText(self):
        return self._text

    def setText(self, value):
        if self._text != value:
            self._text = value
            self.textChanged.emit()

    text = Property(str, getText, setText, notify=textChanged)


def main():
    QQuickStyle.setStyle("Universal")

    app = QGuiApplication(sys.argv)

    engine = QQmlApplicationEngine()

    repository = Repository()
    repository.initFake()

    register_types()

    engine.rootContext().setContextProperty("repositoryObj", repository)
    engine.load("app/presentation/main.qml")

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    with loop:
        loop.run_forever()


if __name__ == "__main__":
    main()
