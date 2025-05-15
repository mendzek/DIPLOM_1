import sqlite3
from datetime import datetime
from tkinter import *
from tkinter import ttk
import sv_ttk
import DataFile


class AddItemWin(Tk):

    def __init__(self):
        super().__init__()

        self.connect = DataFile.connectMain
        self.cursor = self.connect.cursor()
        self.columns = ()
        self.list = ["Integer", "Text"]
        self.LabelList = list()
        self.entrysList = list()
        self.nameOfTable = "Main"
        for x in range(self.cursor.execute(f"SELECT COUNT(*) FROM pragma_table_info('Main')").fetchone()[0]):
            self.columns += self.cursor.execute(f"SELECT name FROM pragma_table_info('Main') Where cid={x}").fetchone()
        self.label2 = ttk.Label(self, text="Наименование")
        self.label2.grid(row=0, column=0, pady=10, padx=10)
        self.LabelList.append(self.label2)
        self.entry2 = ttk.Entry(self, name="entry_" + str(1), state=NORMAL)
        self.entry2.grid(row=1, column=0, pady=10, padx=10)
        self.entrysList.append(self.entry2)
        self.label3 = ttk.Label(self, text="Ед. изм.")
        self.label3.grid(row=2, column=0, pady=10, padx=10)
        self.LabelList.append(self.label3)
        self.entry3 = ttk.Entry(self, name="entry_" + str(2), state=NORMAL)
        self.entry3.grid(row=3, column=0, pady=10, padx=10)
        self.entrysList.append(self.entry3)
        self.label5 = ttk.Label(self, text="Ост. факт.")
        self.label5.grid(row=4, column=0, pady=10, padx=10)
        self.LabelList.append(self.label5)
        self.entry5 = ttk.Entry(self, name="entry_" + str(5), state=NORMAL)
        self.entry5.grid(row=5, column=0, pady=10, padx=10)
        self.entrysList.append(self.entry5)
        self.label7 = ttk.Label(self, text="Цена продажи")
        self.label7.grid(row=6, column=0, pady=10, padx=10)
        self.LabelList.append(self.label7)
        self.entry7 = ttk.Entry(self, name="entry_" + str(7), state=NORMAL)
        self.entry7.grid(row=7, column=0, pady=10, padx=10)
        self.entrysList.append(self.entry7)
        self.label8 = ttk.Label(self, text="Цена закупки")
        self.label8.grid(row=8, column=0, pady=10, padx=10)
        self.LabelList.append(self.label8)
        self.entry8 = ttk.Entry(self, name="entry_" + str(8), state=NORMAL)
        self.entry8.grid(row=9, column=0, pady=10, padx=10)
        self.entrysList.append(self.entry8)
        self.label9 = ttk.Label(self, text="Поставщик")
        self.label9.grid(row=10, column=0, pady=10, padx=10)
        self.LabelList.append(self.label9)
        self.entry9 = ttk.Entry(self, name="entry_" + str(9), state=NORMAL)
        self.entry9.grid(row=11, column=0, pady=10, padx=10)
        self.entrysList.append(self.entry9)

        self.title("ProgramPython - Добавить наименование")
        self.geometry("620x600")
        self.resizable(False, False)
        sv_ttk.set_theme("dark", self)


        self.BT_OK = ttk.Button(self, text="Сохранить", command=self.BT_OK)
        self.BT_OK.grid(row=12, column=0, pady=10, padx=10, columnspan=2)

    def BT_OK(self):
        self.strTemp = "("
        self.check=True
        for x in range(len(self.columns)):

            if self.check==True:
                self.strTemp += f"'id'"
                self.check=False
            else:
                self.strTemp += ", "
                self.strTemp += f"'{self.columns[x]}'"
        self.strTemp += ")"

        self.strTemp2 = "("
        self.check=True
        for x in range(len(self.entrysList)):
            if self.check==True:
                self.strTemp2 += f"'{self.cursor.execute(f"SELECT id FROM {self.nameOfTable} ORDER BY id desc").fetchone()[0]+1}'"
                self.strTemp2 += ", "
                self.strTemp2 += f"'{self.entrysList[x].get()}'"
                self.check=False
            elif self.LabelList[x].cget("text") == "Ост. факт.":
                self.strTemp2 += f", '{self.entrysList[x].get()}'"
                self.strTemp2 += f", '{self.entrysList[x].get()}'"
                self.strTemp2 += f", '0'"
            else:
                self.strTemp2 += ", "
                self.strTemp2 += f"'{self.entrysList[x].get()}'"
        self.strTemp2 += ")"

        self.cursor.execute("INSERT INTO %(third)s%(first)s VALUES %(second)s" % {"first": self.strTemp, "second": self.strTemp2, "third": self.nameOfTable})
        self.connect.commit()
        self.destroy()