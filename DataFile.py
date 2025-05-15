import sqlite3
from tkinter import *
from tkinter import ttk

import RegistrationWindow
from RegistrationWindow import *

BIG_FONT = ("Arial", 30)
REGULAR_FONT = ("Arial", 20)
SMALL_FONT = ("Arial", 10)

MainWindow_Title = "unnamed"

connectLogPass = sqlite3.connect("LogPass.db")
connectMain = sqlite3.connect("Main.db")
cursorLogPass = connectLogPass.cursor()
cursorLogPass.execute("CREATE TABLE IF NOT EXISTS LogPass (id INTEGER NOT NULL UNIQUE, login TEXT, password TEXT, PRIMARY KEY(id AUTOINCREMENT));")