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

class Container():
    def __init__(self):
        """Stores all currently open windows, and also current user information"""
        self.windows = [] # Defines the list of windows as empty
        self.user = None # Defines a None user object
        self.panels = {} # Defines the list of panels for the main window
        self.inv_db = InventoryDatabase() # Defines the inventory database for the entire program
        self.user_db = UserDatabase() # Defines the username database for the entire program

class LoginWindow(QMainWindow):
    def __init__(self):
        """Window to handle the login of users when the program is first run"""
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
        print()
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
        print("lame af")
        self.entryuser.setText('') # Reset the entry for username
        self.entrypass.setText('') # Reset the entry for password
        self.entryuser.setDisabled(False) # Enables the entry for username
        self.entrypass.setDisabled(False) # Enables the entry for password

    def successfulLogin(self):
        """Function is called when the login is verified"""
        container.windows.append(MainWindow()) # Adds the MainWindow to th window container
        self.close() # Closes the login window

class MainWindow(QMainWindow):
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
            # Shows datatable only
            self.setFixedSize(1200, 500)
        elif perm <= 3:
            # Shows datatable and panel area
            self.setFixedSize(1200, 800)

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
        """Function adds the various window panels to the MainWindow"""
        perm = int(container.user['perm']) # Get the permission level of the current user
        if perm <= 3:
            panels = QTabWidget(self) # Define panels as QTabWidget
            panels.resize(QSize(1160, 270)) # Resizes the QTabWidget
            panels.move(20, 510) # Moves the QTabWidget to fit under datatable
            container.panels["panel_issue"] = PanelIssue() # Adds a PanelIssue() item to the panel container
            container.panels["panel_return"] = PanelReturn() # Adds a PanelReturn() item to the panel container
            panels.addTab(container.panels["panel_issue"], "Issue") # Add a PanelIssue() item to the QTabWidget
            panels.addTab(container.panels["panel_return"], "Return") # Add a PanelReturn() item to the QTabWidget
            if perm <= 2:
                container.panels["panel_add"] = PanelAdd() # Adds a PanelAdd() item to the panel container
                container.panels["panel_remove"] = PanelRemove() # Adds a PanelRemove() item to the panel container
                panels.addTab(container.panels["panel_add"], "Add Item") # Add a PanelAdd() item to the QTabWidget
                panels.addTab(container.panels["panel_remove"], "Remove Item") # Add a PanelRemove() item to the QTabWidget
            if perm <= 1:
                container.panels["panel_users_add"] = PanelUsersAdd() # Adds a PanelUsers() item to the panel container
                panels.addTab(container.panels["panel_users_add"], "Add User") # Add a PanelUsers() item to the QTabWidget

    def user_drop(self, event):
        """Disables the dropdown window of users"""
        d = QDialog() # Defines the dropdown window object type
        d.setWindowFlags(Qt.FramelessWindowHint) # Makes the dropdown window frameless
        d.setWindowModality(Qt.ApplicationModal) # Makes the dropdown window a modal
        d.exec_() # Shows the dropdown modal

    def refresh_datatable(self):
        """Refreshes the data on the datatable from the inventory database"""
        self.datatable.clearContents() # Clears the current datatable
        inventory_raw = self.database.return_all_list() # Gets all relevant information out of the database
        self.datatable.setRowCount(len(inventory_raw)) # Sets the number of rows in the datatable to the length of the inventory data

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

class PanelAdd(QWidget):
    def __init__(self):
        """Panel that allows items to be added to the inventory"""
        super().__init__()
        self.initUI() # Initalizes the GUI

    def initUI(self):
        label_font = QFont() # Defines a new font based on open-sans light
        label_font.setFamily("nicelight")
        label_font.setPointSize(18)
        label_font.setWeight(0)

        layout1 = QGridLayout() # Sets layout1 to be a grid layout

        item_id_label = QLabel("Item ID") # Defines Item ID label
        item_id_label.setFont(label_font)

        layout1.addWidget(item_id_label, 0, 0, 1, 1) # Adds Item ID label to the layout

        item_name_label = QLabel("Item Name") # Defines Item Name label
        item_name_label.setFont(label_font)

        layout1.addWidget(item_name_label, 0, 1, 1, 1) # Adds Item Name label to the layout

        quantity_label = QLabel("Quantity") # Defines Quantity Label
        quantity_label.setFont(label_font)

        layout1.addWidget(quantity_label, 0, 2, 1, 1) # Adds Quantity labe to the layout

        self.id_edit = QLineEdit() # Defines id_edit as a QLineEdit
        self.new_id = self.new_id_gen() # Assigns the new_id value to be the next valid ID
        self.id_edit.setText(" #" + str(self.new_id)) # Assigns the text value of the line edit to new_id
        self.id_edit.setDisabled(True) # Disabes the editing of the QLineEdit
        self.id_edit.setFixedSize(QSize(60, 35)) # Resizes id_edit
        self.id_edit.setFont(label_font)

        layout1.addWidget(self.id_edit, 1, 0, 1, 1) # Adds id_edit to the layout

        self.item_name_edit = QLineEdit() # Defines item name edit as a QLineEdit
        self.item_name_edit.setFixedSize(QSize(400, 35)) # Resizes item name edit
        self.item_name_edit.setFont(label_font)

        layout1.addWidget(self.item_name_edit, 1, 1, 1, 1) # Adds item name edit to the layout

        self.quantity_edit = QLineEdit() # Defines quantity edit as a QLineEdit
        self.quantity_edit.setFixedSize(QSize(100, 35)) # Resizes quantity edit
        self.quantity_edit.setFont(label_font)
        self.quantity_edit.setValidator(QIntValidator()) # Only allows integers to be typed

        layout1.addWidget(self.quantity_edit, 1, 2, 1, 1) # Adds quantity edit to the layout

        ######

        layout2 = QGridLayout() # Defines layout 2 as a grid layout

        room_label = QLabel("Room") # Defines room label
        room_label.setFont(label_font)

        layout2.addWidget(room_label, 0, 0, 1, 1) # Adds room label to the layout

        location_label = QLabel("Location") # Defines location label
        location_label.setFont(label_font)

        layout2.addWidget(location_label, 0, 1, 1, 1) # Adds location label to the layout

        self.room_combobox = QComboBox() # Defines room combobox as a QComboBox
        self.room_combobox.setFixedSize(300, 50) # Resizes the room combobox
        self.room_combobox.setFont(label_font)
        self.propogate_room_combobox() # Propogates the room combobox
        self.room_combobox.currentIndexChanged.connect(self.room_combobox_change) # Connects the combobox to combobox change function when the value is updated

        layout2.addWidget(self.room_combobox, 1, 0, 1, 1) # Adds room combobox to the layout

        # location combobox starts disabled, is enabled when a valid room is selected
        self.location_combobox = QComboBox() # Defines location combobox as a QComboBox
        self.location_combobox.setFixedSize(300, 50) # Reszies location combobox
        self.location_combobox.setFont(label_font)
        self.location_combobox.addItem("None") # Adds None item to the list as default value
        # Get list of locations out of the room
        self.location_combobox.addItem("+ Add New Location") # Adds new location item to list as final value
        self.location_combobox.currentIndexChanged.connect(self.location_combobox_change) # Connects the combobox to combobox change function when the value is updated
        self.location_combobox.setDisabled(True) # Sets location combobox to be disabled

        layout2.addWidget(self.location_combobox, 1, 1, 1, 1) # Adds location combobox to layout

        ######

        layout3 = QHBoxLayout() # Defines layout3 as a QHBoxLayout

        submit_button = QPushButton("Submit") # Defines submit button
        submit_button.setFixedSize(120, 40) # Resizes the submit buton
        submit_button.clicked.connect(self.submit_new_item) # Connects the button the the new item function

        layout3.addWidget(submit_button) # Adds submit button the layout

        ######

        final_layout = QVBoxLayout() # Defines the final_layout to a QVBoxLayout
        final_layout.setAlignment(Qt.AlignHCenter) # Sets the alignment of the layout to horizontally centred
        final_layout.addLayout(layout1) # Adds layout1 to the final layout
        final_layout.addLayout(layout2) # Adds layout2 to the final layout
        final_layout.addLayout(layout3) # Adds layout3 to the final layout

        self.setLayout(final_layout) # Sets the layout of the widget to the final_layout

        self.show() # Shows the widget

    def new_id_gen(self):
        """Returns the next valid inventory_id value"""
        inventory_list = container.inv_db.return_all_list() # Gets the inventory data
        if len(inventory_list) > 0:
            new_id = container.inv_db.return_all_list()[-1][0] + 1 # Sets the value of new_id to the highest in the invenotry + 1
        else:
            new_id = 1 # If the inventory is empty, sets new_id to #1
        return new_id # Returns the new_id

    def propogate_room_combobox(self):
        """Propogates the room_combobox with all rooms in the inventory database"""
        self.room_combobox.clear() # Clears the room_combobox
        self.room_combobox.addItem("None") # Adds the default value
        rooms = container.inv_db.return_room_list() # Gets the list of rooms
        self.room_combobox.addItems(rooms) # Adds all rooms to the list
        self.room_combobox.addItem("+ Add New Room") # Adds the new room item

    def room_combobox_change(self, i):
        """Function handles when the room_combobox is changed by the user"""
        combobox_length = self.room_combobox.count() # Gets the length of the room combobox
        if combobox_length > 1:
            combobox_length -= 1
            combobox_length = int(combobox_length)
            if i == combobox_length:
                container.windows.append(NewRoomDialog())
                self.location_combobox.setDisabled(True)
                self.room_combobox.setCurrentIndex(0)
                pass
            elif i == 0:
                self.location_combobox.setDisabled(True)
            else:
                self.location_combobox.clear()
                room = str(self.room_combobox.currentText())
                self.propogate_location_combobox(room)
                self.location_combobox.setDisabled(False)

    def propogate_location_combobox(self, room):
        self.location_combobox.clear()
        self.location_combobox.addItem("None")
        location_dict = container.inv_db.return_location_dictionary()
        new_locations = location_dict[room]
        self.location_combobox.addItems(new_locations)
        self.location_combobox.addItem("+ Add New Location")

    def location_combobox_change(self, i):
        # Display new room dialog
        combobox_length = self.location_combobox.count()
        if combobox_length > 1:
            combobox_length -= 1
            combobox_length = int(combobox_length)
            if i == combobox_length:
                container.windows.append(NewLocationDialog())
                self.location_combobox.setCurrentIndex(0)
                pass

    def submit_new_item(self):
        name_not_empty = False # Predefines empty name
        if self.item_name_edit.text() != "":
            name_not_empty = True # Checks for valid item name
        quantity_not_empty = False # Predefines quantity name
        if self.quantity_edit.text() != "":
            quantity_not_empty = True # Checks for valid quantity value
        valid_location = False # Predefines valid location
        current_index = self.location_combobox.currentIndex() # Gets index of the combobox
        safe_length = self.room_combobox.count() # Gets length of rom combobox
        safe_length -= 1 # Does this for some reason
        safe_length = int(safe_length) # Converts safe length to integer
        if current_index != 0 & current_index != safe_length:
            valid_location = True # Checks that "none" isn't selected, and "+ add new item" isn't selected

        if name_not_empty & quantity_not_empty & valid_location: # Checks if all aspects are valid
            item_id = int(self.new_id) # Defines item_id to be passed
            item_name = self.item_name_edit.text() # Defines item_name to be passed
            quantity = int(self.quantity_edit.text()) # Defines quantity to be passed

            query = 'SELECT `LocationID` FROM `Locations` WHERE `StorageLocation` = "{}" AND `RoomID` = {}'.format(self.location_combobox.currentText(), self.room_combobox.currentIndex()) # Defines the query to get the location ID
            location_id = container.inv_db.return_execution(query)[0][0] # Defines the location idea from the pervious query

            container.inv_db.add_item(item_id, item_name, quantity, location_id) # Calls the function to add the item to the database

            self.new_id = self.new_id_gen() # Gets a new valid id
            self.id_edit.setText(" #" + str(self.new_id)) # Assigns the value of the id_edit to be the new id value
            self.item_name_edit.setText("") # Clears the item_name_edit entry
            self.quantity_edit.setText("") # Clears the quantity_edit entry
            container.windows[1].refresh_datatable() # Refreshes the datatable

class PanelRemove(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI() # Initalizes the GUI

    def initUI(self):

        label_font = QFont() # Defines a new font based on open-sans light
        label_font.setFamily("nicelight")
        label_font.setPointSize(18)
        label_font.setWeight(0)

        layout1 = QVBoxLayout() # Defines layout1 as a QVBoxLayout

        spacer = QSpacerItem(20,40,QSizePolicy.Minimum,QSizePolicy.Expanding) # Defines the spacer item

        layout1.addItem(spacer) # Adds the spacer item to the layout

        item_id_label = QLabel("Item ID") # Defines the item id label
        item_id_label.setFont(label_font)

        layout1.addWidget(item_id_label) # Adds the item id label to the layout

        self.id_edit = QLineEdit() # Defines id_edit as a QLineEdit
        self.id_edit.setFixedSize(QSize(100, 35)) # Resizes the id_edit
        self.id_edit.setFont(label_font)

        layout1.addWidget(self.id_edit) # Adds the id edit to the layout

        submit_button = QPushButton("Submit") # Defines the submit button as a QPushButton
        submit_button.setFixedSize(120, 40) # Resizes the submit button
        submit_button.clicked.connect(self.remove_item) # Connects the submit button to remove_item function

        layout1.addWidget(submit_button) # Adds the submit button to the layout

        layout1.addItem(spacer) # Adds another spacer to the botton of the layout

        final_layout = QHBoxLayout() # Defines the final layout as a QHBoxLayout
        final_layout.addLayout(layout1) # Adds layout1 to the final layout

        self.setLayout(final_layout) # Sets the layout of the widget to final_layout

        self.show() # Shows the widget

    def remove_item(self):
        """Removes an item"""
        if self.id_edit.text() != "": # Checks that there is something entered in the id edit entry
            container.inv_db.remove_item(self.id_edit.text()) # Calls the function to remove the item
            self.id_edit.setText("") # Clears the id_edit entry
            container.windows[1].refresh_datatable() # Refreshes the datatable
            new_id = container.panels["panel_add"].new_id_gen() # Gets a new valid id for the panel_add page
            container.panels["panel_add"].id_edit.setText(" #" + str(new_id)) # Updates the id_edit value in the panel_add panel

class PanelIssue(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI() # Initalizes the GUI

    def initUI(self):
        pass

class PanelReturn(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI() # Initalizes the GUI

    def initUI(self):
        pass

class PanelUsersAdd(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI() # Initalizes the GUI

    def initUI(self):
        label_font = QFont() # Defines a new font based on open-sans light
        label_font.setFamily("nicelight")
        label_font.setPointSize(18)
        label_font.setWeight(0)
        layout1 = QGridLayout() # Defines Layout1 as a QGridLayout

        username_label = QLabel("Username")
        password_label = QLabel("Password")
        name_label = QLabel("Real Name")
        perm_label = QLabel("Permission")

        username_label.setFont(label_font)
        password_label.setFont(label_font)
        name_label.setFont(label_font)
        perm_label.setFont(label_font)

        layout1.addWidget(username_label, 0, 0)
        layout1.addWidget(password_label, 0, 1)
        layout1.addWidget(name_label, 0, 2)
        layout1.addWidget(perm_label, 0, 3)

        self.username_entry = QLineEdit()
        self.password_entry = QLineEdit()
        self.name_entry = QLineEdit()
        self.perm_entry = QLineEdit()

        self.password_entry.setEchoMode(QLineEdit.Password) # Sets the password entry field to be in a password safe format

        self.username_entry.setFixedSize(QSize(240, 35))
        self.password_entry.setFixedSize(QSize(240, 35))
        self.name_entry.setFixedSize(QSize(240, 35))
        self.perm_entry.setFixedSize(QSize(100, 35))

        self.username_entry.setFont(label_font)
        self.password_entry.setFont(label_font)
        self.name_entry.setFont(label_font)
        self.perm_entry.setFont(label_font)

        layout1.addWidget(self.username_entry, 1, 0)
        layout1.addWidget(self.password_entry, 1, 1)
        layout1.addWidget(self.name_entry, 1, 2)
        layout1.addWidget(self.perm_entry, 1, 3)

        submit_button = QPushButton("Submit") # Defines the submit button
        submit_button.setFixedSize(120, 40) # Resizes the submit buton
        submit_button.clicked.connect(self.add_user)

        final_layout = QVBoxLayout() # Defines the final layout as a QVBoxLayout
        final_layout.setAlignment(Qt.AlignHCenter) # Sets the alignment of the final layout to centre
        spacer = QSpacerItem(20,40,QSizePolicy.Minimum,QSizePolicy.Expanding) # Defines the spacer item
        final_layout.addItem(spacer) # Adds a spacer item to the final layout
        final_layout.addLayout(layout1) # Adds layout1 to the final layout
        final_layout.addWidget(submit_button)
        final_layout.addItem(spacer) # Adds a spacer item to the final layout

        self.setLayout(final_layout)
        self.show()

    def add_user(self):
        username = self.username_entry.text()
        password = self.password_entry.text()
        name = self.name_entry.text()
        permission = self.perm_entry.text()

        if (username != "") & (password != "") & (name != "") & (permission != ""):
            container.user_db.add_user(name, username, password, permission)
            self.username_entry.setText("")
            self.password_entry.setText("")
            self.name_entry.setText("")
            self.perm_entry.setText("")

class NewLocationDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI() # Initalizes the GUI

    def initUI(self):
        self.setWindowModality(Qt.ApplicationModal) # Makes the dropdown window a modal

        label_font = QFont() # Defines a new font based on open-sans light
        label_font.setFamily("nicelight")
        label_font.setPointSize(18)
        label_font.setWeight(0)

        ######

        layout1 = QGridLayout() # Defines layout1 as a QGridLayout

        location_id_label = QLabel("LocationID") # Defines the location id label
        location_id_label.setFont(label_font)

        layout1.addWidget(location_id_label, 0, 0) # Adds the location id label to the layout

        room_label = QLabel("Room") # Defines the room label
        room_label.setFont(label_font)

        layout1.addWidget(room_label, 0, 1) # Adds the room label to the layout

        location_id_edit = QLineEdit() # Defines location id edit as a QLineEdit
        location_id = len(container.inv_db.return_location_list())+1 # Gets the value for the next valid location id
        location_id_edit.setText(" #" + str(location_id)) # Assigns the text of the location id edit to the location id
        location_id_edit.setDisabled(True) # Disables the location id edit
        location_id_edit.setFixedSize(QSize(60, 35)) # Resizes the location id edit
        location_id_edit.setFont(label_font)

        layout1.addWidget(location_id_edit, 1, 0) # Adds the location id edit to the layout

        self.room_combobox = QComboBox() # Defines the room combobox as a QComboBox
        self.room_combobox.setFixedSize(300, 50) # Resizes the combobox
        self.room_combobox.setFont(label_font)
        rooms = container.inv_db.return_room_list() # Gets a list of the rooms
        self.room_combobox.addItems(rooms) # Adds the list of rooms to the combobox

        layout1.addWidget(self.room_combobox, 1, 1) # Adds the room combobox to the layout

        ######

        layout2 = QGridLayout() # Defines layout2 as a QGridLayout

        location_label = QLabel("Location") # Defines location label
        location_label.setFont(label_font)

        layout2.addWidget(location_label, 0, 0) # Adds location label to the layout

        self.location_name_edit = QLineEdit() # Defines location name edit as a QLineEdit
        self.location_name_edit.setFixedSize(QSize(400, 35)) # Resizes the location name edit
        self.location_name_edit.setFont(label_font)

        layout2.addWidget(self.location_name_edit, 1, 0, 1, 2) # Adds the location name edit to the layout

        ######

        layout3 = QHBoxLayout() # Defines layout3 as a QHBoxLayout

        submit_button = QPushButton("Sumbit") # Defines the submit button
        submit_button.clicked.connect(self.add_location) # Connects the submit button to the add_location function

        layout3.addWidget(submit_button) # Adds the submit button to the layout

        ######

        final_layout = QVBoxLayout() # Defines the final layout as a QVBoxLayout
        final_layout.addLayout(layout1) # Adds layout1 to the final layout
        final_layout.addLayout(layout2) # Adds layout2 to the final layout
        final_layout.addLayout(layout3) # Adds layout3 to the final layout

        ######

        self.setLayout(final_layout) # Sets the layout of the QDialog

        self.exec_() # Shows the QDialog

    def add_location(self):
        room_name = self.room_combobox.currentText() # Gets the current value of the room combobox
        location_name = self.location_name_edit.text() # Gets the current value of the location name combobox
        container.inv_db.add_location(location_name, room_name) # Calls the function which adds the location to the database
        container.panels["panel_add"].propogate_location_combobox(room_name) # Refreshes the location combobox in the panel_add panel
        self.close() # Closes the dialog

class NewRoomDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI() # Initalizes the GUI

    def initUI(self):
        print(container.windows)
        self.setWindowModality(Qt.ApplicationModal) # Makes the dropdown window a modal

        label_font = QFont() # Defines a new font based on open-sans light
        label_font.setFamily("nicelight")
        label_font.setPointSize(18)
        label_font.setWeight(0)

        ######

        layout1 = QGridLayout() # Defines layout1 as a QGirdLayout

        room_id_label = QLabel("LocationID") # Defines the room id label
        room_id_label.setFont(label_font)

        layout1.addWidget(room_id_label, 0, 0) # Adds the room id label to the layout

        room_name_label = QLabel("Room") # Defines the room label
        room_name_label.setFont(label_font)

        layout1.addWidget(room_name_label, 0, 1) # Adds the room label to the layout

        room_id_edit = QLineEdit() # Defines the room id edit as a QLineEdit
        room_id = len(container.inv_db.return_room_list())+1 # Gets the next valid room id
        room_id_edit.setText(" #" + str(room_id)) # Assigns the text of the room id edit to be the room id
        room_id_edit.setDisabled(True) # Disables the room id edit
        room_id_edit.setFixedSize(QSize(60, 35)) # Resizes the room id edit
        room_id_edit.setFont(label_font)

        layout1.addWidget(room_id_edit, 1, 0) # Adds the room id edit to the layout

        self.room_name_entry = QLineEdit() # Defines room name entry as a QLineEdit
        self.room_name_entry.setFixedSize(QSize(400, 35)) # Resizes room name entry
        self.room_name_entry.setFont(label_font)

        layout1.addWidget(self.room_name_entry, 1, 1, 1, 2) # Adds room name entry to the layout

        ######

        layout2 = QHBoxLayout() # Defines layout2 as a QHBoxLayout

        submit_button = QPushButton("Sumbit") # Defines the submit button
        submit_button.clicked.connect(self.add_room) # Connects the submit button to the add_room function

        layout2.addWidget(submit_button) # Adds the submit button to the layout

        ######

        final_layout = QVBoxLayout() # Defines the final layout as a QVBoxLayout
        final_layout.addLayout(layout1) # Adds layout1 to the final layout
        final_layout.addLayout(layout2) # Adds layout2 to the final layout

        ######

        self.setLayout(final_layout) # Sets the layout of the QDialog to final_layout

        self.exec_() # Shows the QDialog

    def add_room(self):
        room_name = self.room_name_entry.text() # Gets the current text of the room
        container.inv_db.add_room(room_name) # Calls the function which adds a new room to the database
        container.panels["panel_add"].propogate_room_combobox() # Refreshes the room combobox in the panel_add panel
        self.close() # Closes the dialog

if __name__ == "__main__":
    container = Container() # Defines the window container
    app = QApplication(sys.argv) # Defines the QApplication
    container.windows.append(LoginWindow()) # Adds the LoginWindow to the window container
    #container.user = {
    #"id": 1,
    #"username": "test",
    #"perm": 1,
    #"name": "lame"}
    #main = MainWindow()
    #test = PanelUsersAdd()
    #container.windows.append(test)
    sys.exit(app.exec_()) # Ends the program
