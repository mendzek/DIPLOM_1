from tkinter import *
from tkinter import ttk
import sqlite3

import DataFile
import MainWindow
from tkinter.messagebox import showwarning

from MainWindow import *


class ChangeItemWin(Tk):

    textFromTextBox=""

    def __init__(self):
        super().__init__()

        self.connect = DataFile.connectMain
        self.cursor = self.connect.cursor()

        self.entrysList = list()
        self.LabelList = list()
        self.selectedProjectsList = MainWindow.MainWindow.selectedProjectsList
        self.columns = tuple()
        for x in range(self.cursor.execute(f"SELECT COUNT(*) FROM pragma_table_info('Main')").fetchone()[0]):
            self.columns += self.cursor.execute(f"SELECT name FROM pragma_table_info('Main') Where cid={x}").fetchone()

        self.title("Изменить наименование")
        self.geometry("800x700")


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
        sv_ttk.set_theme("dark", self)

    def BT_save(self):
        self.cursor = self.connect.cursor()
        updates = []
        params = []

        for x in range(len(self.columns)):
            column = self.columns[x]
            value = self.entrysList[x].get()

            updates.append(f'"{column}" = ?')
            params.append(value)

        params.append(self.selectedProjectsList[0])

        query = f"UPDATE Main SET {', '.join(updates)} WHERE ID = ?"

        self.cursor.execute(query, params)
        self.connect.commit()

        self.destroy()
