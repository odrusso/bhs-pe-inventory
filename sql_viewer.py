"""Module (And program) for displaying the GUI for """
from tkinter import *
from tkinter.ttk import *
from database_link import *

class SQLGui(object):
    "Defines the GUI class"
    def __init__(self, window, database):
        self.database = database
        self.what = StringVar()
        self.what.set("loading")
        self.title = Label(window,
                            textvariable = self.what)
        self.title.grid(row=0, column=0)
        self.entry = Entry(window)
        self.entry.grid(row=1, column=0)
        self.entry.bind("<Return>", self.handle_new)
        self.refresh()

    def handle_new(self, nothing):
        try:
            ExampleDB = Database(database_config)
            values = tuple(self.entry.get().split())
            self.database.add_person(*values)
        except Exception as e:
            error_popup = ErrorGUI(e)

        query = "SELECT * FROM `people`"                                        # Example query
        response = self.database.return_execution(query)
        self.refresh()



        self.entry.delete(0, 'end')

    def refresh(self):
        try:
            text_table = ''
            for (PersonID, FirstName, LastName) in response:                        #Print the returned information
                text_table += "{} {} {} \n".format(PersonID, FirstName, LastName)
            if text_table[-1:] == "\n":
                text_table = text_table[:-1]
            self.what.set(text_table)
        except Exception as e:
            error_popup = ErrorGUI(e)

class ErrorGUI(object):
    def __init__(self, error):
        self.window = Tk()
        self.error = "An error has occured: \n" + str(error)
        self.title = Label(self.window, text = self.error)
        self.title.grid(row=0, column=0)
        self.window.mainloop()

class LoadingGUI(object):
    def __init__(self):
        self.window = Tk()
        self.title = Label(self.window, text="Loading...")
        self.window.mainloop()

    def endit(self):
        self.window.quit()



if __name__ == "__main__":
    #Database configuration and connection
    database_config = {
    "user": "root",
    "password": "5sQ-Hsd-ekt-bzS",
    "host": "bhs-pe-inventory.ci3pushvdxiu.us-west-2.rds.amazonaws.com",
    "database": "test"
    }

    ExampleDB = Database(database_config)                                   #Inniltalise the Database object

    query = "SELECT * FROM `people`"                                        # Example query
    response = ExampleDB.return_execution(query)

    window = Tk()
    gui = SQLGui(window, ExampleDB)
    window.mainloop()
