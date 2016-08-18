"""To Do:
Create more relevant database object
init:
Connect to database
methods:
- return_table()
    - will return table strucuture as lists
"""

import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from database_link import *
import scrypt

class WindowContainer():
    def __init__(self):
        self.windows = []
        self.user = None

class User():
    def __init__(self, data):
        data = list(data)[0]
        self.id = data[0]
        self.username = data[1]
        self.name = data[2]
        self.permission = data[3]

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

            localhost_config = {
                "user": "root",
                "password": "root",
                "host": "localhost",
                "database": "users"
            }

            login_db = Database(localhost_config)

            query = "SELECT * FROM `Users`"
            users_raw = login_db.return_execution(query)

            self.login = False

            for (id, username, salt, hash, name, perm) in users_raw:
                if username == attempt_username:
                    hash = str(hash)
                    salt = str(salt)
                    new_hash = str(scrypt.hash(attempt_password, salt))
                    if new_hash == hash:
                        self.login = True
                        self.id = id
                        self.perm = perm
                        container.user = User(login_db.return_execution("SELECT id, username, name, perm FROM `Users` WHERE id = " + str(id)))
                        break
                    else:
                        self.login = False
                else:
                    self.login = False

            if self.login:
                self.successfulLogin()
            else:
                self.failedLogin()

        elif event.key() == Qt.Key_Escape:
            sys.exit(app.exec_())


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

        main_window_initalize(self.perm)


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

        self.banner_label = QLabel(self)
        self.banner_pixmap = QPixmap("/sandbox/banner.png")
        self.banner_label.setPixmap(self.banner_pixmap)
        self.banner_size = QSize(1200, 60)
        self.banner_label.resize(self.banner_size)
        self.banner_label.move(0, 0)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(5)
        self.shadow.setOffset(0)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(2)
        self.banner_label.setGraphicsEffect(self.shadow)

        self.title = QLabel("<font color='white'>Physical Education Inventory</font>", self)

        self.titlefont = QFont()
        self.titlefont.setFamily("nicelight")
        self.titlefont.setPointSize(20)
        self.titlefont.setWeight(0)

        self.title.setFont(self.titlefont)

        self.title.move(50, 20)
        self.title.adjustSize()

        self.usernamelabelfont = self.titlefont
        self.usernamelabelfont.setPointSize(18)

        self.usernamelabel = QLabel("<font color='white'>" + container.user.name + "</font>", self)
        self.usernamelabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.usernamelabel.setFont(self.usernamelabelfont)
        self.usernamelabel.adjustSize()

        self.usernamelabel.move(1150 - self.usernamelabel.frameGeometry().width(), 20)

        self.dropper = QPushButton('', self)
        self.dropper.clicked.connect(self.user_drop)
        self.dropper.setIcon(QIcon('/sandbox/triangle.png'))
        self.dropper.setIconSize(QSize(16,16))
        self.dropper.move(1160, 20)
        self.dropper.resize(QSize(24, 24))

        localhost_config = {
            "user": "root",
            "password": "root",
            "host": "localhost",
            "database": "data"
        }

        login_db = Database(localhost_config)

        query = """SELECT n.ItemID, n.Name, n.Quantity, s.Issued, l.StorageLocation, r.Room
                FROM Inventory n
                LEFT JOIN Issues s ON n.ItemID=s.ItemID
                LEFT JOIN Locations l on n.ItemID=l.ItemID
                LEFT JOIN Rooms r on l.RoomID=r.RoomID"""

        inventory_raw = login_db.return_execution(query)
        self.inventory_data = []


        for (id, name, quantity, issued, location, room) in inventory_raw:
            self.inventory_data.append((str(id), name, str(quantity), "No", str(location) + ", " + str(room)))

        self.datatable = QTableWidget(self)
        self.datatable.setRowCount(len(self.inventory_data))
        self.datatable.setColumnCount(5)
        self.datatable.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.datatable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.datatable.setAlternatingRowColors(True)
        self.datatable.setShowGrid(False)
        self.datatable.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.datatable.setHorizontalHeaderItem(0, QTableWidgetItem("#"))
        self.datatable.setHorizontalHeaderItem(1, QTableWidgetItem("Item"))
        self.datatable.setHorizontalHeaderItem(2, QTableWidgetItem("Quantity"))
        self.datatable.setHorizontalHeaderItem(3, QTableWidgetItem("Location"))
        self.datatable.setHorizontalHeaderItem(4, QTableWidgetItem("Issued"))

        self.datatable.setColumnWidth(0, 50)
        self.datatable.setColumnWidth(1, 400)
        self.datatable.setColumnWidth(2, 150)
        self.datatable.setColumnWidth(3, 400)
        self.datatable.setColumnWidth(4, 195)

        self.id_font = QFont()
        self.id_font.setFamily('Open Sans')
        self.id_font.setWeight(0)
        self.id_font.setPointSize(16)

        self.name_font = QFont()
        self.name_font.setFamily('nicelight')
        self.name_font.setWeight(99)
        self.name_font.setPointSize(16)

        self.id_colour = QColor()
        self.id_colour.setNamedColor("#727272")
        self.id_brush = QBrush(self.id_colour)

        current_row = 0
        for item in self.inventory_data:
            self.datatable.setItem(current_row, 0, QTableWidgetItem(item[0]))
            self.datatable.item(current_row, 0).setTextAlignment(Qt.AlignCenter)
            self.datatable.item(current_row, 0).setFont(self.id_font)
            self.datatable.item(current_row, 0).setForeground(self.id_brush)
            self.datatable.setItem(current_row, 1, QTableWidgetItem(item[1]))
            self.datatable.item(current_row, 1).setTextAlignment(Qt.AlignCenter)
            self.datatable.item(current_row, 1).setFont(self.name_font)
            self.datatable.setItem(current_row, 2, QTableWidgetItem(item[2]))
            self.datatable.item(current_row, 2).setTextAlignment(Qt.AlignCenter)
            self.datatable.item(current_row, 2).setFont(self.id_font)
            self.datatable.item(current_row, 2).setForeground(self.id_brush)
            self.datatable.setItem(current_row, 3, QTableWidgetItem(item[4]))
            self.datatable.item(current_row, 3).setTextAlignment(Qt.AlignCenter)
            self.datatable.item(current_row, 3).setFont(self.id_font)
            self.datatable.item(current_row, 3).setForeground(self.id_brush)
            self.datatable.setItem(current_row, 4, QTableWidgetItem(item[3]))
            self.datatable.item(current_row, 4).setTextAlignment(Qt.AlignCenter)
            self.datatable.item(current_row, 4).setFont(self.id_font)
            self.datatable.item(current_row, 4).setForeground(self.id_brush)
            current_row += 1


        self.datatable.setStyleSheet("""
        QTableWidget {
        alternate-background-color: #f3f3f3;
        background-color: #ffffff;
        }
        """)
        self.datatable.verticalHeader().setVisible(False)
        self.datatable.move(0, 60)
        self.datatable.setFixedSize(QSize(1200, 440))



        self.show()

    def gen_window(self):
        if perm == 5:
            self.setFixedSize(1200, 500)
        elif perm == 4:
            self.setFixedSize(1200, 800)
            """issue + return tabs"""
        elif perm == 3:
            self.setFixedSize(1200, 800)
            """issue, return, add, remove tabs"""
        elif perm == 2:
            self.setFixedSize(1200, 800)
            """issue, return, add, remove tabs"""
            """user modification"""
        elif perm == 1:
            """admin window"""


    def user_drop(self, event):
        d = QDialog()
        d.setWindowFlags(Qt.FramelessWindowHint)
        d.setWindowModality(Qt.ApplicationModal)
        d.exec_()

def main_window_initalize(perm):
    container.windows.append(ViewWindow(perm))

def runMain(container):
    app = QApplication(sys.argv)
    container.windows.append(LoginWindow())
    # container.windows.append(MainWindow())
    sys.exit(app.exec_())

container = WindowContainer()
runMain(container)
