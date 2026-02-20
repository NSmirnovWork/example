import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: root
    width: 1200
    height: 800
    visible: true
    title: "CRM Admin"
    minimumWidth: 1000
    minimumHeight: 600

    property string currentPage: "dashboard"

    RowLayout {
        anchors.fill: parent

        // -------------------------
        // Sidebar
        // -------------------------
        Rectangle {
            width: 220
            Layout.fillHeight: true

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 20

                Label {
                    text: "CRM"
                    font.pixelSize: 22
                    font.bold: true
                }

                Button { text: "Dashboard"; Layout.fillWidth: true; onClicked: root.currentPage = "dashboard" }
                Button { text: "Users"; Layout.fillWidth: true; onClicked: root.currentPage = "users" }
                Button { text: "Orders"; Layout.fillWidth: true; onClicked: root.currentPage = "orders" }

                Item { Layout.fillHeight: true }

                Button {
                    text: "Logout"
                    Layout.fillWidth: true
                    contentItem: Label { text: "Logout"; horizontalAlignment: Text.AlignHCenter }
                }
            }
        }

        // -------------------------
        // Main Content Area
        // -------------------------
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true

            // Lazy-loading pages with Loader
            Loader {
                id: dashboardLoader
                active: root.currentPage === "dashboard"
                source: "pages/DashboardPage.qml"
                anchors.fill: parent
            }

            Loader {
                id: usersLoader
                active: root.currentPage === "users"
                source: "pages/UsersPage.qml"
                anchors.fill: parent
            }

            Loader {
                id: ordersLoader
                active: root.currentPage === "orders"
                source: "pages/OrdersPage.qml"
                anchors.fill: parent
            }
        }
    }
}