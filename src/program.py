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
        self.panels = [] # Defines the list of panels for the main window
        self.inv_db = InventoryDatabase()

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

        self.database = container.inv_db # Initalizes the InventoryDatabase object to self.database

        self.setWindowTitle("") # Sets the window title to be blank

        self.gen_window() # Generates the window dimensions and initalizes the panels

        self.gen_banner() # Generates the banner of the main window

        self.gen_datatable() # Generates the datatable of the main window

        self.gen_panels()

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
            self.setFixedSize(1200, 800)
        elif perm == 0:
            """admin window"""
            #temp
            self.setFixedSize(1200, 500)

    def gen_banner(self):
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

    def gen_datatable(self):

        self.datatable = QTableWidget(self) # Assigns the datatable table widget
        self.datatable.setRowCount(len(self.database.return_all_list())) # Sets the datatable row count to the length of inventory data
        self.datatable.setColumnCount(5) # Sets 5 colums in the datatable
        self.datatable.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel) # Allows smooth scrolling in the datatable
        self.datatable.setSelectionBehavior(QAbstractItemView.SelectRows) # Allows the selection of rows in the table instead of cells
        self.datatable.setAlternatingRowColors(True) # Alternates the row colours in the datatable
        self.datatable.setShowGrid(False) # Hides the grid of the datatable
        self.datatable.setEditTriggers(QAbstractItemView.NoEditTriggers) # Disable editing of the datatable in the view mode

        # Sets the headings of the columns in the datatable
        self.datatable.setHorizontalHeaderItem(0, QTableWidgetItem("#"))
        self.datatable.setHorizontalHeaderItem(1, QTableWidgetItem("Item"))
        self.datatable.setHorizontalHeaderItem(2, QTableWidgetItem("Quantity"))
        self.datatable.setHorizontalHeaderItem(3, QTableWidgetItem("Location"))
        self.datatable.setHorizontalHeaderItem(4, QTableWidgetItem("Issued"))

        # Sets the width of the columns in the datatable
        self.datatable.setColumnWidth(0, 50)
        self.datatable.setColumnWidth(1, 400)
        self.datatable.setColumnWidth(2, 150)
        self.datatable.setColumnWidth(3, 400)
        self.datatable.setColumnWidth(4, 195)

        # Defines a font for the id text
        self.id_font = QFont()
        self.id_font.setFamily('Open Sans')
        self.id_font.setWeight(0)
        self.id_font.setPointSize(16)

        # Defines a font for the id text
        self.name_font = QFont()
        self.name_font.setFamily('nicelight')
        self.name_font.setWeight(99)
        self.name_font.setPointSize(16)

        # Defines a color for the id label
        id_colour = QColor()
        id_colour.setNamedColor("#727272")
        self.id_brush = QBrush(id_colour)

        self.refresh_datatable()

        self.datatable.setStyleSheet("""
        QTableWidget {
        alternate-background-color: #f3f3f3;
        background-color: #ffffff;
        }
        """) # Defines styles for the datatable
        self.datatable.verticalHeader().setVisible(False) # Hides the vertical headers in the datatable
        self.datatable.move(0, 60) # Moves the datatable
        self.datatable.setFixedSize(QSize(1200, 440)) # Sets the size of the datatable

    def gen_panels(self):
        panels = QTabWidget(self)
        panels.resize(QSize(1160, 270))
        panels.move(20, 510)
        panels.addTab(QWidget(), "Issue Item")
        panels.addTab(QWidget(), "Return Item")
        panels.addTab(PanelIssue(), "Add Item")
        panels.addTab(QWidget(), "Remove Item")

    def user_drop(self, event):
        """Disables the dropdown window of users"""
        d = QDialog() # Defines the dropdown window object type
        d.setWindowFlags(Qt.FramelessWindowHint) # Makes the dropdown window frameless
        d.setWindowModality(Qt.ApplicationModal) # Makes the dropdown window a modal
        d.exec_() # Shows the dropdown modal

    def refresh_datatable(self):
        self.datatable.clearContents()
        self.datatable.setRowCount(len(self.database.return_all_list()))
        inventory_raw = self.database.return_all_list() # Gets all relevant information out of the database

        inventory_data = [] # Defines empty inventory-data list
        for i in inventory_raw:
            inventory_data.append((str(i[0]), str(i[1]), str(i[2]), "No", str(i[4]) + ", " + str(i[5]))) # Converts the relevant inventory data to something more usable in the current program

        current_row = 0 # Defines a current row. Might be better replaced with an enumerate
        for item in inventory_data:
            # Fills in the table with data from the inventory data list
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
        #self.gen_datatable()

class PanelIssue(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        label_font = QFont() # Defines a new font based on open-sans light
        label_font.setFamily("nicelight")
        label_font.setPointSize(18)
        label_font.setWeight(0)

        layout1 = QGridLayout()

        item_id_label = QLabel("Item ID")
        item_id_label.setFont(label_font)

        layout1.addWidget(item_id_label, 0, 0, 1, 1)

        item_name_label = QLabel("Item Name")
        item_name_label.setFont(label_font)

        layout1.addWidget(item_name_label, 0, 1, 1, 1)

        quantity_label = QLabel("Quantity")
        quantity_label.setFont(label_font)

        layout1.addWidget(quantity_label, 0, 2, 1, 1)

        self.id_edit = QLineEdit()
        new_id = len(container.inv_db.return_all_list())+2
        self.id_edit.setText(str(new_id))
        self.id_edit.setDisabled(True)
        self.id_edit.setFixedSize(QSize(60, 35))
        self.id_edit.setFont(label_font)

        layout1.addWidget(self.id_edit, 1, 0, 1, 1)

        self.item_name_edit = QLineEdit()
        self.item_name_edit.setFixedSize(QSize(400, 35))
        self.item_name_edit.setFont(label_font)

        layout1.addWidget(self.item_name_edit, 1, 1, 1, 1)

        self.quantity_edit = QLineEdit()
        self.quantity_edit.setFixedSize(QSize(100, 35))
        self.quantity_edit.setFont(label_font)
        self.quantity_edit.setValidator(QIntValidator())

        layout1.addWidget(self.quantity_edit, 1, 2, 1, 1)

        ######

        layout2 = QGridLayout()

        room_label = QLabel("Room")
        room_label.setFont(label_font)

        layout2.addWidget(room_label, 0, 0, 1, 1)

        location_label = QLabel("Location")
        location_label.setFont(label_font)

        layout2.addWidget(location_label, 0, 1, 1, 1)

        self.room_combobox = QComboBox()
        self.room_combobox.setFixedSize(300, 50)
        self.room_combobox.setFont(label_font)
        self.room_combobox.addItem("None")
        self.propogate_room_combobox()
        self.room_combobox.addItem("+ Add New Room")
        self.room_combobox.currentIndexChanged.connect(self.room_combobox_change)

        layout2.addWidget(self.room_combobox, 1, 0, 1, 1)

        """Start with disabled, enable when valid room is selected"""
        self.location_combobox = QComboBox()
        self.location_combobox.setFixedSize(300, 50)
        self.location_combobox.setFont(label_font)
        self.location_combobox.addItem("None")
        # Get list of locations out of the room
        self.location_combobox.addItem("+ Add New Location")
        self.location_combobox.currentIndexChanged.connect(self.location_combobox_change)
        self.location_combobox.setDisabled(True)

        layout2.addWidget(self.location_combobox, 1, 1, 1, 1)

        ######

        layout3 = QHBoxLayout()

        submit_button = QPushButton("Submit")
        submit_button.setFixedSize(120, 40)
        submit_button.clicked.connect(self.submit_new_item)

        layout3.addWidget(submit_button)

        ######

        final_layout = QVBoxLayout()
        final_layout.setAlignment(Qt.AlignHCenter)
        final_layout.addLayout(layout1)
        final_layout.addLayout(layout2)
        final_layout.addLayout(layout3)

        self.setLayout(final_layout)

        self.show()

    def propogate_room_combobox(self):
        rooms = container.inv_db.return_room_list()
        self.room_combobox.addItems(rooms)

    def room_combobox_change(self, i):
        combobox_length = self.room_combobox.count()
        combobox_length -= 1
        combobox_length = int(combobox_length)
        if i == combobox_length:
            # Display new room dialog
            self.location_combobox.setDisabled(True)
            self.room_combobox.setCurrentIndex(0)
            pass
        elif i == 0:
            self.location_combobox.setDisabled(True)
        else:
            self.location_combobox.clear()
            self.location_combobox.addItem("None")
            location_dict = container.inv_db.return_location_dictionary()
            new_locations = location_dict[str(self.room_combobox.currentText())]
            self.location_combobox.addItems(new_locations)
            self.location_combobox.addItem("+ Add New Location")
            self.location_combobox.setDisabled(False)

    def location_combobox_change(self, i):
        # Display new room dialog
        combobox_length = self.location_combobox.count()
        combobox_length -= 1
        combobox_length = int(combobox_length)
        if i == combobox_length:
            # Display new room dialog
            self.location_combobox.setCurrentIndex(0)
            pass

    def submit_new_item(self):
        name_not_empty = False
        if self.item_name_edit.text() != "":
            name_not_empty = True
        quantity_not_empty = False
        if self.quantity_edit.text() != "":
            quantity_not_empty = True
        valid_location = False
        current_index = self.location_combobox.currentIndex()
        safe_length = self.room_combobox.count()
        safe_length -= 1
        safe_length = int(safe_length)
        if current_index != 0 & current_index != safe_length:
            valid_location = True

        if name_not_empty & quantity_not_empty & valid_location:
            item_id = int(self.id_edit.text())
            item_name = self.item_name_edit.text()
            quantity = int(self.quantity_edit.text())
            location_id = self.location_combobox.currentIndex()
            container.inv_db.add_item(item_id, item_name, quantity, location_id)

            self.id_edit.setText(str(int(self.id_edit.text())+1))
            self.item_name_edit.setText("")
            self.quantity_edit.setText("")
            container.windows[0].refresh_datatable()

if __name__ == "__main__":
    container = WindowContainer() # Defines the window container
    app = QApplication(sys.argv) # Defines the QApplication
    container.windows.append(LoginWindow()) # Adds the LoginWindow to the window container
    #container.user = {
    #"id": 1,
    #"username": "test",
    #"perm": 1,
    #"name": "lame"}
    #container.windows.append(MainWindow())
    sys.exit(app.exec_()) # Ends the program
else:
    print("Program designed to run as __MAIN__")
