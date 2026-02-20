import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Page {
    padding: 20

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        // -----------------------------
        // Header Row
        // -----------------------------
        Rectangle {
            Layout.fillWidth: true
            height: 40
            border.width: 0

            RowLayout {
                anchors.fill: parent
                anchors.margins: 10
                spacing: 20

                Label { text: "ID"; Layout.preferredWidth: 80; font.bold: true }
                Label { text: "Name"; Layout.fillWidth: true; font.bold: true }
                Label { text: "Email"; Layout.fillWidth: true; font.bold: true }
                Label { text: "Actions"; Layout.preferredWidth: 80; font.bold: true }
            }
        }

        // -----------------------------
        // ListView with Delegate
        // -----------------------------
        ListView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            model: usersVM.usersModel
            clip: true

            delegate: Rectangle {
                width: ListView.view.width
                height: 60
                border.width: 0

                RowLayout {
                    anchors.fill: parent
                    anchors.margins: 10
                    spacing: 20

                    Label { text: model.id; Layout.preferredWidth: 80 }
                    Label { text: model.name; Layout.fillWidth: true }
                    Label { text: model.email; Layout.fillWidth: true }

                    Button {
                        text: "Edit"
                        Layout.preferredWidth: 80
                        background: Rectangle { radius: 4 }
                        contentItem: Label { text: "Edit"; horizontalAlignment: Text.AlignHCenter }
                    }
                }
            }

            ScrollBar.vertical: ScrollBar {}
        }

        // -------------------------
        // Loading Overlay
        // -------------------------
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            visible: usersVM.loading
            z: 100

            BusyIndicator {
                anchors.centerIn: parent
                running: true
            }
        }

        // -------------------------
        // Pagination Footer
        // -------------------------
        Rectangle {
            Layout.fillWidth: true
            height: 60

            RowLayout {
                anchors.centerIn: parent
                spacing: 20

                Button {
                    text: "< Previous"
                    enabled: usersVM.page > 1
                    onClicked: usersVM.prev_page()
                }

                Label {
                    text: "Page " + usersVM.page + " of " + usersVM.totalPages
                    font.pixelSize: 16
                }

                Button {
                    text: "Next >"
                    enabled: usersVM.page < usersVM.totalPages
                    onClicked: usersVM.next_page()
                }
            }
        }
    }

    Component.onCompleted: {
        usersVM.load_users()
    }
}