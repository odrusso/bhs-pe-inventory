"""To Do:
Create more relevant database object
init:
Connect to database
methods:
- return_table()
    - will return table strucuture as lists
"""


import scrypt
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from database_link import *
import security

class WindowContainer():
    def __init__(self):
        self.windows = []
        self.user = None

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setFixedSize(900, 350)
        self.setWindowTitle("")
        self.setStyleSheet("""QMainWindow {
                                background-image: url(/sandbox/bg_small.jpg)
                            }""")

        QFontDatabase.addApplicationFont("/sandbox/nicelight.ttf")
        QFontDatabase.addApplicationFont("/sandbox/nicereg.ttf")

        self.label1 = QLabel("<font color='white'>Physical Education Department Inventory</font>", self)
        self.label2 = QLabel("<font color='white'>Burnside High School</font>", self)

        self.label1font = QFont()
        self.label1font.setFamily("nicelight")
        self.label1font.setPointSize(18)
        self.label1font.setWeight(0)

        self.label2font = QFont()
        self.label2font.setFamily("nicelight")
        self.label2font.setPointSize(16)
        self.label2font.setWeight(0)

        self.label1.setFont(self.label1font)
        self.label2.setFont(self.label2font)

        self.label1.move(100, 50)
        self.label1.adjustSize()
        self.label2.move(100, 80)
        self.label2.adjustSize()

        self.logo = QLabel(self)
        self.pixmap = QPixmap("/sandbox/logo.png")
        self.logo.setPixmap(self.pixmap)
        self.logo.move(30, 30)
        self.logo.adjustSize()

        self.labeluser = QLabel("<font color='white'>Username:</font>", self)
        self.labelpass = QLabel("<font color='white'>Password:</font>", self)

        self.labeluser.setFont(self.label2font)
        self.labelpass.setFont(self.label2font)

        self.labeluser.move(560, 190)
        self.labeluser.adjustSize()
        self.labelpass.move(565, 240)
        self.labeluser.adjustSize()

        self.entryuser = QLineEdit(self)
        self.entrypass = QLineEdit(self)

        self.entrysize = QSize(180, 30)

        self.entryuser.resize(self.entrysize)
        self.entrypass.resize(self.entrysize)

        self.entrypass.setEchoMode(QLineEdit.Password)

        self.entryuser.move(670, 185)
        self.entrypass.move(670, 235)

        self.loadingmovie = QMovie("/sandbox/loading.gif")
        self.loadinglabel = QLabel(self)
        self.loadinglabel.setMovie(self.loadingmovie)
        self.loadinglabel.move(1000, 1000)

        self.failedlabel = QLabel("<font color='white'>Invalid Login</font>", self)
        self.failedlabel.setFont(self.label2font)
        self.failedlabel.move(1000, 1000)

        self.successlabel = QLabel("<font color='white'>Connecting to Database</font>", self)
        self.successlabel.setFont(self.label1font)
        self.successlabel.move(1000, 1000)

        self.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.entryuser.setDisabled(True)
            self.entrypass.setDisabled(True)

            self.loadinglabel.move(700, 230)
            self.loadingmovie.start()
            self.loadinglabel.adjustSize()

            self.loadinglabel.move(1000, 1000)

            attempt_username = self.entryuser.text()
            attempt_password = self.entrypass.text()

            if self.verify_login(attempt_username, attempt_password):
                self.successfulLogin()

            else:
                self.failedLogin()



        elif event.key() == Qt.Key_Escape:
            sys.exit(app.exec_())

    def verify_login(self, attempt_username, attempt_password):
        """Verfifies a user login completely"""
        user_db = UserDatabase(db_local_users())
        user = user_db.get_user(attempt_username)
        if user != None:
            if security.verify_password(user[2], user[3], attempt_password):
                container.user = {
                "id": user[0],
                "username": user[1],
                "perm": user[4],
                "name": user[5]}
                return True
            else:
                print("Invalid Password")
                return False
        else:
            print("Invalid Username")
            return False

    def failedLogin(self):
        self.entryuser.setText('')
        self.entrypass.setText('')
        self.entryuser.setDisabled(False)
        self.entrypass.setDisabled(False)
        self.failedlabel.move(700, 150)

    def successfulLogin(self):
        self.failedlabel.move(1000, 1000)
        self.label1.setParent(None)
        self.label2.setParent(None)
        self.logo.setParent(None)
        self.labeluser.setParent(None)
        self.labelpass.setParent(None)
        self.entrypass.setParent(None)
        self.entryuser.setParent(None)

        self.loadinglabel.move(400, 100)
        self.loadingmovie.start()
        self.loadinglabel.adjustSize()

        self.successlabel.move(350, 80)
        self.successlabel.adjustSize()

        container.windows.append(ViewWindow(container.user['perm']))

        self.close()

class ViewWindow(QMainWindow):
    """
    Break down into:
    - gen_header(width, username)
    - gen_viewport(location, dimensions)
    """
    def __init__(self, permission):
        super().__init__()
        self.permission = permission
        self.initUI()

    def initUI(self):
        # self.gen_window()
        # self.gen_header()

        self.setWindowTitle("")

        self.gen_window()

        banner_label = QLabel(self)
        banner_pixmap = QPixmap("/sandbox/banner.png")
        banner_label.setPixmap(banner_pixmap)
        banner_size = QSize(1200, 60)
        banner_label.resize(banner_size)
        banner_label.move(0, 0)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(5)
        shadow.setOffset(0)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        banner_label.setGraphicsEffect(shadow)

        title = QLabel("<font color='white'>Physical Education Inventory</font>", self)

        titlefont = QFont()
        titlefont.setFamily("nicelight")
        titlefont.setPointSize(20)
        titlefont.setWeight(0)

        title.setFont(titlefont)

        title.move(50, 20)
        title.adjustSize()

        usernamelabelfont = titlefont
        usernamelabelfont.setPointSize(18)

        usernamelabel = QLabel("<font color='white'>" + container.user['name'] + "</font>", self)
        usernamelabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        usernamelabel.setFont(usernamelabelfont)
        usernamelabel.adjustSize()

        usernamelabel.move(1150 - usernamelabel.frameGeometry().width(), 20)

        dropper = QPushButton('', self)
        dropper.clicked.connect(self.user_drop)
        dropper.setIcon(QIcon('/sandbox/triangle.png'))
        dropper.setIconSize(QSize(16,16))
        dropper.move(1160, 20)
        dropper.resize(QSize(24, 24))

        localhost_config = {
            "user": "root",
            "password": "root",
            "host": "localhost",
            "database": "data"
        }

        login_db = InventoryDatabase(db_local_data())

        query = """SELECT n.ItemID, n.Name, n.Quantity, s.Issued, l.StorageLocation, r.Room
                FROM Inventory n
                LEFT JOIN Issues s ON n.ItemID=s.ItemID
                LEFT JOIN Locations l on n.ItemID=l.ItemID
                LEFT JOIN Rooms r on l.RoomID=r.RoomID"""

        inventory_raw = login_db.return_execution(query)
        inventory_data = []


        for (id, name, quantity, issued, location, room) in inventory_raw:
            inventory_data.append((str(id), name, str(quantity), "No", str(location) + ", " + str(room)))

        datatable = QTableWidget(self)
        datatable.setRowCount(len(inventory_data))
        datatable.setColumnCount(5)
        datatable.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        datatable.setSelectionBehavior(QAbstractItemView.SelectRows)
        datatable.setAlternatingRowColors(True)
        datatable.setShowGrid(False)
        datatable.setEditTriggers(QAbstractItemView.NoEditTriggers)

        datatable.setHorizontalHeaderItem(0, QTableWidgetItem("#"))
        datatable.setHorizontalHeaderItem(1, QTableWidgetItem("Item"))
        datatable.setHorizontalHeaderItem(2, QTableWidgetItem("Quantity"))
        datatable.setHorizontalHeaderItem(3, QTableWidgetItem("Location"))
        datatable.setHorizontalHeaderItem(4, QTableWidgetItem("Issued"))

        datatable.setColumnWidth(0, 50)
        datatable.setColumnWidth(1, 400)
        datatable.setColumnWidth(2, 150)
        datatable.setColumnWidth(3, 400)
        datatable.setColumnWidth(4, 195)

        id_font = QFont()
        id_font.setFamily('Open Sans')
        id_font.setWeight(0)
        id_font.setPointSize(16)

        name_font = QFont()
        name_font.setFamily('nicelight')
        name_font.setWeight(99)
        name_font.setPointSize(16)

        id_colour = QColor()
        id_colour.setNamedColor("#727272")
        id_brush = QBrush(id_colour)

        current_row = 0
        for item in inventory_data:
            datatable.setItem(current_row, 0, QTableWidgetItem(item[0]))
            datatable.item(current_row, 0).setTextAlignment(Qt.AlignCenter)
            datatable.item(current_row, 0).setFont(id_font)
            datatable.item(current_row, 0).setForeground(id_brush)
            datatable.setItem(current_row, 1, QTableWidgetItem(item[1]))
            datatable.item(current_row, 1).setTextAlignment(Qt.AlignCenter)
            datatable.item(current_row, 1).setFont(name_font)
            datatable.setItem(current_row, 2, QTableWidgetItem(item[2]))
            datatable.item(current_row, 2).setTextAlignment(Qt.AlignCenter)
            datatable.item(current_row, 2).setFont(id_font)
            datatable.item(current_row, 2).setForeground(id_brush)
            datatable.setItem(current_row, 3, QTableWidgetItem(item[4]))
            datatable.item(current_row, 3).setTextAlignment(Qt.AlignCenter)
            datatable.item(current_row, 3).setFont(id_font)
            datatable.item(current_row, 3).setForeground(id_brush)
            datatable.setItem(current_row, 4, QTableWidgetItem(item[3]))
            datatable.item(current_row, 4).setTextAlignment(Qt.AlignCenter)
            datatable.item(current_row, 4).setFont(id_font)
            datatable.item(current_row, 4).setForeground(id_brush)
            current_row += 1


        datatable.setStyleSheet("""
        QTableWidget {
        alternate-background-color: #f3f3f3;
        background-color: #ffffff;
        }
        """)
        datatable.verticalHeader().setVisible(False)
        datatable.move(0, 60)
        datatable.setFixedSize(QSize(1200, 440))

        self.show()

    def gen_window(self):
        perm = int(container.user['perm'])
        if perm == 4:
            self.setFixedSize(1200, 500)
        elif perm == 3:
            self.setFixedSize(1200, 800)
            """issue + return tabs"""
        elif perm == 2:
            self.setFixedSize(1200, 800)
            """issue, return, add, remove tabs"""
        elif perm == 1:
            self.setFixedSize(1200, 800)
            """issue, return, add, remove tabs"""
            """user modification"""
        elif perm == 0:
            """admin window"""
            #temp
            self.setFixedSize(1200, 500)


    def user_drop(self, event):
        d = QDialog()
        d.setWindowFlags(Qt.FramelessWindowHint)
        d.setWindowModality(Qt.ApplicationModal)
        d.exec_()

def runMain(container):
    app = QApplication(sys.argv)
    container.windows.append(LoginWindow())
    # container.windows.append(MainWindow())
    sys.exit(app.exec_())

if __name__ == "__main__":
    container = WindowContainer()
    runMain(container)
else:
    print("Program designed to run as __MAIN__")
