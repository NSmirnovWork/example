import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import UserListModel 1.0

Page {
    padding: 10

    UserListModel {
        id: userList
        repository: repositoryObj
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: 10

        Row {
            spacing: 8

            Button {
                text: "Add user"
                onClicked: addDialog.open()
            }
        }

        // -----------------------------
        // Header Row
        // -----------------------------
        Rectangle {
            Layout.fillWidth: true
            height: 40
            border.width: 0
            color: '#c2c2c2'

            RowLayout {
                anchors.fill: parent
                anchors.margins: 10
                spacing: 20

                Label { text: "ID"; Layout.preferredWidth: 80; font.bold: true }
                Label { text: "Name"; Layout.preferredWidth: 100; font.bold: true }
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
            model: userList
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
                    Label { text: model.name; Layout.preferredWidth: 100 }
                    Label { text: model.email; Layout.fillWidth: true; horizontalAlignment: Text.AlignLeft }

                    Button {
                        text: "Edit"
                        onClicked: {
                            editDialog.userId = id
                            editDialog.nameValue = name
                            editDialog.emailValue = email
                            editDialog.open()
                        }
                    }

                    Button {
                        text: "Delete"
                        onClicked: {
                            deleteDialog.userId = id
                            deleteDialog.open()
                        }
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
            visible: userList.isLoading
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
                    text: "< Previous "
                    enabled: userList.page > 1
                    onClicked: userList.previousPage()
                }

                Label {
                    text: "Page " + userList.page + " of " + userList.totalPages
                    font.pixelSize: 16
                }

                Button {
                    text: "Next >"
                    enabled: userList.page < userList.totalPages
                    onClicked: userList.nextPage()
                }
            }
        }
    
    }

    // -----------------
    // Add dialog
    // -----------------

    Dialog {
        id: addDialog
        anchors.centerIn: parent
        title: "Add User"
        modal: true
        width: 300

        property string nameValue: ""
        property string emailValue: ""
        property string nameError: ""
        property string emailError: ""

        ColumnLayout {
            anchors.fill: parent
            Layout.bottomMargin: 20
            spacing: 6

            // -------- Name field --------
            TextField {
                placeholderText: "Name"
                text: addDialog.nameValue
                Layout.fillWidth: true
                onTextChanged: {
                    addDialog.nameValue = text
                    addDialog.nameError = text.length < 2 ? "Name must be at least 2 characters" : ""
                }
            }

            Text {
                text: addDialog.nameError
                color: "red"
                font.pixelSize: 12
                visible: addDialog.nameError !== ""
            }

            // -------- Email field --------
            TextField {
                placeholderText: "Email"
                text: addDialog.emailValue
                Layout.fillWidth: true
                onTextChanged: {
                    addDialog.emailValue = text
                    // Simple email regex validation
                    const emailPattern = /^[^@]+@[^@]+\.[^@]+$/
                    addDialog.emailError = !emailPattern.test(text) ? "Invalid email" : ""
                }
            }

            Text {
                text: addDialog.emailError
                color: "red"
                font.pixelSize: 12
                visible: addDialog.emailError !== ""
            }

            // -------- Buttons --------
            RowLayout {
                Layout.fillWidth: true
                spacing: 8
                Button {
                    text: "Cancel"
                    Layout.fillWidth: true
                    onClicked: addDialog.close()
                }

                Button {
                    text: "Create"
                    Layout.fillWidth: true
                    enabled: addDialog.nameError === "" && addDialog.emailError === "" &&
                            addDialog.nameValue !== "" && addDialog.emailValue !== ""
                    onClicked: {
                        userList.createUser(addDialog.nameValue, addDialog.emailValue)
                        addDialog.close()
                    }
                }
            }
        }
    }
    // -----------------
    // Edit dialog
    // -----------------

    Dialog {
        id: editDialog
        anchors.centerIn: parent
        modal: true
        title: "Edit user"
        width: 300

        property int userId: -1
        property string nameValue
        property string emailValue

        ColumnLayout {
            anchors.fill: parent
            spacing: 6

            TextField {
                text: editDialog.nameValue
                onTextChanged: editDialog.nameValue = text
                Layout.fillWidth: true
            }

            TextField {
                text: editDialog.emailValue
                onTextChanged: editDialog.emailValue = text
                Layout.fillWidth: true
            }

            Button {
                text: "Save"
                onClicked: {
                    userList.updateUser(
                        editDialog.userId,
                        editDialog.nameValue,
                        editDialog.emailValue
                    )
                    editDialog.close()
                }
            }
        }
    }

    // -----------------
    // Delete dialog
    // -----------------

    Dialog {
        id: deleteDialog
        anchors.centerIn: parent
        modal: true
        title: "Delete user?"
        width: 300

        property int userId: -1

        Column {
            spacing: 6

            Text { text: "Confirm permanent user deletion" }

            Row {
                spacing: 8

                Button {
                    text: "Cancel"
                    onClicked: deleteDialog.close()
                }

                Button {
                    text: "Confirm"
                    onClicked: {
                        userList.deleteUser(deleteDialog.userId)
                        deleteDialog.close()
                    }
                }
            }
        }
    }


    Component.onCompleted: {
        userList.reload()
    }
}