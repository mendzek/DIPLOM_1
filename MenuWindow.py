from tkinter import *
from tkinter import ttk
import sv_ttk
from tkinter.messagebox import showwarning
import DataFile
from MainWindow import *


class MenuWindow(Tk):
    def __init__(self):
        super().__init__()

        self.title("Главное меню")
        self.geometry("800x300")
        self.resizable(False, False)

        self.BT1 = ttk.Button(self, text="Управление работниками", width=40,  command=self.Button1)
        self.BT1.grid(row=0, column=0, pady=30, padx=30)
        self.BT2 = ttk.Button(self, text="Управление товарами", width=40, command=self.Button2)
        self.BT2.grid(row=0, column=1, pady=30, padx=30)
        self.BT3 = ttk.Button(self, text="Просмотр списаний", width=40, command=self.Button3)
        self.BT3.grid(row=1, column=0, pady=30, padx=30)
        self.BT4 = ttk.Button(self, text="Просмотр поступлений", width=40, command=self.Button4)
        self.BT4.grid(row=1, column=1, pady=30, padx=30)

        sv_ttk.set_theme("dark", self)

    def Button1(self):
        mainWindow = MainWindow()
        mainWindow.OpenWorkers()
    def Button2(self):
        mainWindow = MainWindow()
        mainWindow.OpenMainTable()
    def Button3(self):
        mainWindow = MainWindow()
        mainWindow.OpenSpisTable()
    def Button4(self):
        mainWindow = MainWindow()
        mainWindow.OpenDobTable()