# utf-8
# Python 3.5.1, PyQt5
# Software developed by Oscar Russo
# http://github.com/odrusso/bhs-pe-inventory

# Main program including objects and functions for the bhs-pe-inventory

import sys # Imports the sys library which is required for connecting to command line variables
from PyQt5.QtCore import * # Imports PyQt5 Core functions
from PyQt5.QtGui import * # Imports PyQt5 basic GUI functions
from PyQt5.QtWidgets import * # Imports PyQt5 basic widget functions
from database_link import * # Imports the database link program
import security # Imports the security program

class WindowContainer():
    """Stores all currently open windows, and also current user information"""
    def __init__(self):
        self.windows = [] # Defines the list of windows as empty
        self.user = None # Defines a None user object

class LoginWindow(QMainWindow):
    """Window to handle the login of users when the program is first run"""
    def __init__(self):
        super().__init__()
        self.initUI() # Initalizes the UI

    def initUI(self):
        """Defines all aspects of the inital GUI state"""
        self.setFixedSize(900, 350) # Defines fixed size of the window
        self.setWindowTitle("BHS PE Inventory Login") # Gives the window a title

        self.setStyleSheet("""QMainWindow {
                                background-image: url(/sandbox/bg_small.jpg)
                            }""") # Defines the background image of the login window

        QFontDatabase.addApplicationFont("/sandbox/nicelight.ttf") # Adds Open-Sans Light to the font library
        QFontDatabase.addApplicationFont("/sandbox/nicereg.ttf") # Adds Open-Sans Regular to the font library

        self.label1 = QLabel("<font color='white'>Physical Education Department Inventory</font>", self) # Defines the main heading label
        self.label2 = QLabel("<font color='white'>Burnside High School</font>", self) # Defines the subheading label

        self.label1font = QFont() # Defines a new font based on open-sans light
        self.label1font.setFamily("nicelight")
        self.label1font.setPointSize(18)
        self.label1font.setWeight(0)

        self.label2font = QFont() # Defines a new font based on open-sans light
        self.label2font.setFamily("nicelight")
        self.label2font.setPointSize(16)
        self.label2font.setWeight(0)

        self.label1.setFont(self.label1font) # Sets the font of the main heading
        self.label2.setFont(self.label2font) # Sets the font of the subheading

        self.label1.move(100, 50) # Moves the heading
        self.label1.adjustSize() # Adjusts the size of the main heading automatically
        self.label2.move(100, 80) # Moves the subheading
        self.label2.adjustSize() # Adjusts the size of the subheading automatically

        self.logo = QLabel(self) # Defines the label for the icon
        self.pixmap = QPixmap("/sandbox/logo.png") # Defines the pixmap for the icon
        self.logo.setPixmap(self.pixmap) # Sets the pixmap to the label
        self.logo.move(30, 30) # Moves the logo
        self.logo.adjustSize() # Adjusts the size of the logo automatically

        self.labeluser = QLabel("<font color='white'>Username:</font>", self) # Defines the username label
        self.labelpass = QLabel("<font color='white'>Password:</font>", self) # Defines the password label

        self.labeluser.setFont(self.label2font) # Sets the font of the username label
        self.labelpass.setFont(self.label2font) # Sets the font of the password label

        self.labeluser.move(560, 190) # Moves the username label
        self.labeluser.adjustSize() # Adjusts the size of the username label automatically
        self.labelpass.move(565, 240) # Moves the password label
        self.labeluser.adjustSize() # Adjusts the size of the password label automatically

        self.entryuser = QLineEdit(self) # Defines the text entry for the username
        self.entrypass = QLineEdit(self) # Defines the text entry for the password

        self.entrysize = QSize(180, 30) # Defines the size for the username and password entry

        self.entryuser.resize(self.entrysize) # Resizes the entry for username
        self.entrypass.resize(self.entrysize) # Reszies the entry for password

        self.entrypass.setEchoMode(QLineEdit.Password) # Sets the password entry field to be in a password safe format

        self.entryuser.move(670, 185) # Moves the username entry
        self.entrypass.move(670, 235) # Moves the password entry

        self.show() # Shows the window

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return: # If the return key is pressed
            self.entryuser.setDisabled(True) # Disable text entry of the username field
            self.entrypass.setDisabled(True) # Disable text entry of the password field

            attempt_username = self.entryuser.text() # Defines attempt_username as the entered text in the username entry
            attempt_password = self.entrypass.text() # Defines attempt_password as the entered text in the password entry

            if self.verify_login(attempt_username, attempt_password): # Verifies the login credentials
                self.successfulLogin() # Runs the succesfull login function if the credentials pass
            else:
                self.failedLogin() # Runs the failed login function if the credentials fail

        elif event.key() == Qt.Key_Escape: # If the escape key is pressed
            sys.exit(app.exec_()) # Quit the program

    def verify_login(self, attempt_username, attempt_password):
        """Verfifies a user login completely"""
        user_db = UserDatabase() # Defines the user database
        user = user_db.get_user(attempt_username) # Gets the details of the user from the datatable
        if user != None: # Checks to see if the username is valid
            if security.verify_password(user[2], user[3], attempt_password): # Verfies if the password is valid
                container.user = {
                "id": user[0],
                "username": user[1],
                "perm": user[4],
                "name": user[5]} # Defines the user object for the window container
                return True # Returns True if the login is verfified
            else:
                return False
        else:
            return False

    def failedLogin(self):
        """Function is called when the login cannot be verified"""
        self.entryuser.setText('') # Reset the entry for username
        self.entrypass.setText('') # Reset the entry for password
        self.entryuser.setDisabled(False) # Enables the entry for username
        self.entrypass.setDisabled(False) # Enables the entry for password

    def successfulLogin(self):
        """Function is called when the login is verified"""
        container.windows.append(MainWindow()) # Adds the MainWindow to th window container
        self.close() # Closes the login window

class MainWindow(QMainWindow):
    """
    Break down into:
    - gen_header(width, username)
    - gen_viewport(location, dimensions)
    """
    def __init__(self):
        super().__init__()
        self.permission = container.user["perm"] # Assigns the self.permission to the user permission from WindowContainer
        self.initUI() # Initalizes the GUI

    def initUI(self):

        self.database = InventoryDatabase() # Initalizes the InventoryDatabase object to self.database

        self.setWindowTitle("") # Sets the window title to be blank

        self.gen_window() # Generates the window dimensions and initalizes the panels

        banner_label = QLabel(self) # Defines the banner background label
        banner_pixmap = QPixmap("/sandbox/banner.png") # Defines the banner background pixap
        banner_label.setPixmap(banner_pixmap) # Assigns the banner label to the banner pixmap
        banner_label.resize(QSize(1200, 60)) # Resizes the banner to fit the window
        banner_label.move(0, 0) # Moves the banner to the top left

        shadow = QGraphicsDropShadowEffect(self) # Defines the shadow object
        shadow.setBlurRadius(5)
        shadow.setOffset(0)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        banner_label.setGraphicsEffect(shadow) # Assigns the shadow effect to the banner

        title = QLabel("<font color='white'>Physical Education Inventory</font>", self) # Defines the label for the title

        titlefont = QFont() # Defines the font for the title
        titlefont.setFamily("nicelight")
        titlefont.setPointSize(20)
        titlefont.setWeight(0)

        title.setFont(titlefont) # Assigns the font to the title

        title.move(50, 20) # Moves the title
        title.adjustSize() # Resizes the title label automatically

        usernamelabelfont = titlefont # Assigns username font to title font
        usernamelabelfont.setPointSize(18) # Resizes the username font

        usernamelabel = QLabel("<font color='white'>" + container.user['name'] + "</font>", self) # Defines the username label
        usernamelabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter) # Sets the text alignment of the username label
        usernamelabel.setFont(usernamelabelfont) # Assigns the username font to the username label
        usernamelabel.adjustSize() # Resizes the username label automatically

        usernamelabel.move(1150 - usernamelabel.frameGeometry().width(), 20) # Moves the username label to the right of the window

        dropper = QPushButton('', self) # Defines the dropper button
        dropper.clicked.connect(self.user_drop) # Assigns the function to the dropper button
        dropper.setIcon(QIcon('/sandbox/triangle.png')) # Assigns the icon the dropper button
        dropper.setIconSize(QSize(16,16)) # Resizes the dorpper button icon
        dropper.move(1160, 20) # Moves the dropper button
        dropper.resize(QSize(24, 24)) # Resizes the dropper button

        inventory_raw = self.database.return_all_list() # Gets all relevant information out of the database

        inventory_data = [] # Defines empty inventory-data list
        for i in inventory_raw:
            inventory_data.append((str(i[0]), str(i[1]), str(i[2]), "No", str(i[4]) + ", " + str(i[5]))) # Converts the relevant inventory data to something more usable in the current program

        datatable = QTableWidget(self) # Assigns the datatable table widget
        datatable.setRowCount(len(inventory_data)) # Sets the datatable row count to the length of inventory data
        datatable.setColumnCount(5) # Sets 5 colums in the datatable
        datatable.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel) # Allows smooth scrolling in the datatable
        datatable.setSelectionBehavior(QAbstractItemView.SelectRows) # Allows the selection of rows in the table instead of cells
        datatable.setAlternatingRowColors(True) # Alternates the row colours in the datatable
        datatable.setShowGrid(False) # Hides the grid of the datatable
        datatable.setEditTriggers(QAbstractItemView.NoEditTriggers) # Disable editing of the datatable in the view mode

        # Sets the headings of the columns in the datatable
        datatable.setHorizontalHeaderItem(0, QTableWidgetItem("#"))
        datatable.setHorizontalHeaderItem(1, QTableWidgetItem("Item"))
        datatable.setHorizontalHeaderItem(2, QTableWidgetItem("Quantity"))
        datatable.setHorizontalHeaderItem(3, QTableWidgetItem("Location"))
        datatable.setHorizontalHeaderItem(4, QTableWidgetItem("Issued"))

        # Sets the width of the columns in the datatable
        datatable.setColumnWidth(0, 50)
        datatable.setColumnWidth(1, 400)
        datatable.setColumnWidth(2, 150)
        datatable.setColumnWidth(3, 400)
        datatable.setColumnWidth(4, 195)

        # Defines a font for the id text
        id_font = QFont()
        id_font.setFamily('Open Sans')
        id_font.setWeight(0)
        id_font.setPointSize(16)

        # Defines a font for the id text
        name_font = QFont()
        name_font.setFamily('nicelight')
        name_font.setWeight(99)
        name_font.setPointSize(16)

        # Defines a color for the id label
        id_colour = QColor()
        id_colour.setNamedColor("#727272")
        id_brush = QBrush(id_colour)

        current_row = 0 # Defines a current row. Might be better replaced with an enumerate
        for item in inventory_data:
            # Fills in the table with data from the inventory data list
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
        """) # Defines styles for the datatable
        datatable.verticalHeader().setVisible(False) # Hides the vertical headers in the datatable
        datatable.move(0, 60) # Moves the datatable
        datatable.setFixedSize(QSize(1200, 440)) # Sets the size of the datatable

        self.show() # Shows the MainWindow

    def gen_window(self):
        """Function sets the size of the window to the relvant permissions of the user"""
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
        """Disables the dropdown window of users"""
        d = QDialog() # Defines the dropdown window object type
        d.setWindowFlags(Qt.FramelessWindowHint) # Makes the dropdown window frameless
        d.setWindowModality(Qt.ApplicationModal) # Makes the dropdown window a modal
        d.exec_() # Shows the dropdown modal

if __name__ == "__main__":
    container = WindowContainer() # Defines the window container
    app = QApplication(sys.argv) # Defines the QApplication
    container.windows.append(LoginWindow()) # Adds the LoginWindow to the window container
    sys.exit(app.exec_()) # Ends the program
else:
    print("Program designed to run as __MAIN__")
