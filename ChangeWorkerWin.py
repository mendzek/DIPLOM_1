from tkinter import *
from tkinter import ttk
import sqlite3
import MainWindow
from tkinter.messagebox import showwarning

from MainWindow import *


class ChangeWorkerWin(Tk):

    textFromTextBox=""

    def __init__(self):
        super().__init__()

        self.connect = DataFile.connectMain
        self.cursor = self.connect.cursor()

        self.entrysList = list()
        self.LabelList = list()
        self.selectedProjectsList = MainWindow.MainWindow.selectedProjectsList
        self.columns = tuple()
        for x in range(self.cursor.execute(f"SELECT COUNT(*) FROM pragma_table_info('Workers')").fetchone()[0]):
            self.columns += self.cursor.execute(f"SELECT name FROM pragma_table_info('Workers') Where cid={x}").fetchone()

        self.title("ProgramPython - Selected work window")
        self.geometry("800x300")


        for x in range(len(self.selectedProjectsList)):
            self.label = ttk.Label(self, text=f"{self.columns[x]}")
            self.label.pack(expand=1)
            self.LabelList.append(self.label)
            self.entry = ttk.Entry(self,name="entry_"+str(x), state=NORMAL)
            self.entry.insert(0,f"{self.selectedProjectsList[x]}")
            self.entry.pack(expand=1)
            self.entrysList.append(self.entry)

        self.BT_save = ttk.Button(self, text="Сохранить", command=self.BT_save)
        self.BT_save.pack(expand=1,side=BOTTOM)

    def BT_save(self):
        self.cursor = self.connect.cursor()         #НЕ РАБОТАЕТ НА ДАТЕ ЗАЧИСЛЕНИЯ
        for x in range(len(self.columns)):
            self.cursor.execute("UPDATE Workers SET %(first)s = '%(second)s' WHERE ID = '%(third)s'" % {"first": self.columns[x], "second": self.entrysList[x].get(), "third": self.selectedProjectsList[0]})
            self.connect.commit()
        self.destroy()