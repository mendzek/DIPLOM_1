import sqlite3
from datetime import datetime
from tkinter import *
from tkinter import ttk
import sv_ttk
import DataFile


class AddWorkerWin(Tk):

    def __init__(self):
        super().__init__()

        self.connect = DataFile.connectMain
        self.cursor = self.connect.cursor()
        self.columns = ()
        self.list = ["Integer", "Text"]
        self.LabelList = list()
        self.entrysList = list()
        self.nameOfTable = "Workers"
        for x in range(self.cursor.execute(f"SELECT COUNT(*) FROM pragma_table_info('Workers')").fetchone()[0]):
            self.columns += self.cursor.execute(f"SELECT name FROM pragma_table_info('Workers') Where cid={x}").fetchone()
        self.label2 = ttk.Label(self, text="Фамилия")
        self.label2.grid(row=0, column=0, pady=10, padx=10)
        self.LabelList.append(self.label2)
        self.entry2 = ttk.Entry(self, name="entry_" + str(1), state=NORMAL)
        self.entry2.grid(row=1, column=0, pady=10, padx=10)
        self.entrysList.append(self.entry2)
        self.label3 = ttk.Label(self, text="Имя")
        self.label3.grid(row=2, column=0, pady=10, padx=10)
        self.LabelList.append(self.label3)
        self.entry3 = ttk.Entry(self, name="entry_" + str(2), state=NORMAL)
        self.entry3.grid(row=3, column=0, pady=10, padx=10)
        self.entrysList.append(self.entry3)
        self.label4 = ttk.Label(self, text="Отчество")
        self.label4.grid(row=4, column=0, pady=10, padx=10)
        self.LabelList.append(self.label4)
        self.entry4 = ttk.Entry(self, name="entry_" + str(3), state=NORMAL)
        self.entry4.grid(row=5, column=0, pady=10, padx=10)
        self.entrysList.append(self.entry4)
        self.label5 = ttk.Label(self, text="Должность")
        self.label5.grid(row=6, column=0, pady=10, padx=10)
        self.LabelList.append(self.label5)
        self.entry5 = ttk.Entry(self, name="entry_" + str(5), state=NORMAL)
        self.entry5.grid(row=7, column=0, pady=10, padx=10)
        self.entrysList.append(self.entry5)
        self.label6 = ttk.Label(self, text="Ставка")
        self.label6.grid(row=8, column=0, pady=10, padx=10)
        self.LabelList.append(self.label6)
        self.Tables = ["Полная", "Половина"]
        self.Tables_var = StringVar(value=self.Tables[0])
        self.comboBox = ttk.Combobox(self, textvariable=self.Tables_var, values=self.Tables, state="readonly")
        self.comboBox.grid(row=9, column=0)
        self.entrysList.append(self.comboBox)

        self.title("ProgramPython - Добавить работника")
        self.geometry("420x500")
        self.resizable(False, False)
        sv_ttk.set_theme("dark", self)


        self.BT_OK = ttk.Button(self, text="Сохранить", command=self.BT_OK)
        self.BT_OK.grid(row=10, column=0, pady=10, padx=10, columnspan=2)

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
            elif self.LabelList[x].cget("text") == "Должность":
                self.strTemp2 += f", '{self.entrysList[x].get()}'"
                self.strTemp2 += f", '{datetime.now()}'"
                self.strTemp2 += ", "
            elif self.LabelList[x].cget("text") == "Ставка":
                self.strTemp2 += f"'{self.entrysList[x].get()}'"
                if self.entrysList[x].get() == "Полная":
                    self.strTemp2 += f", 22000"
                elif self.entrysList[x].get() == "Половина":
                    self.strTemp2 += f", 15000"
                self.strTemp2 += f", 'Нет', '0', '0', '0', 'Норма'"
            else:
                self.strTemp2 += ", "
                self.strTemp2 += f"'{self.entrysList[x].get()}'"
        self.strTemp2 += ")"

        self.cursor.execute("INSERT INTO %(third)s%(first)s VALUES %(second)s" % {"first": self.strTemp, "second": self.strTemp2, "third": self.nameOfTable})
        self.connect.commit()
        self.destroy()