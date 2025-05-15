import sqlite3
from tkinter import *
from tkinter import ttk
from docxtpl import DocxTemplate

import sv_ttk

import DataFile
import datetime
from AddItemWin import *
from AddWorkerWin import *
from ChangeWorkerWin import *


class MainWindow(Tk):
    selectedProjectsList = list()
    def __init__(self):
        super().__init__()

        self.selectedProjects = None
        self.title(DataFile.MainWindow_Title)
        self.geometry("1000x500")

        self.tableName = ""
        self.tableValues = list()
        self.headValues = list()
        self.numOfRows = any
        self.selectedProjectsList = list()

        self.FRTabs = ttk.Frame(self, height=20)
        self.FRTabs.pack(anchor=N, fill=X, expand=1)

        self.MainLabel = ttk.Label(self, width=30, font=DataFile.BIG_FONT, text="Товары")
        self.MainLabel.pack(anchor=CENTER, pady=20)

        self.label = ttk.Label(self, text="-")
        self.label.pack(anchor=N, fill=X, expand=1)

        self.BTtabsWorkers = ttk.Button(self.FRTabs, text="Работники", width=20, command=self.OpenWorkers)
        self.BTtabsWorkers.pack(anchor=W, expand=1)
        self.BTtabsMainTable = ttk.Button(self.FRTabs, text="Главная таблица", width=20, command=self.OpenMainTable)
        self.BTtabsMainTable.pack(anchor=W, expand=1)

        self.connect = DataFile.connectMain
        self.cursor = self.connect.cursor()
        self.columns = ()
        self.cursor.execute(f"SELECT COUNT(*) FROM Main")
        self.numOfRows = self.cursor.fetchone()[0]
        self.numOfColumns = \
            self.cursor.execute(f"SELECT COUNT(*) FROM pragma_table_info('Main')").fetchone()[0]
        for x in range(self.numOfColumns):
            self.columns += self.cursor.execute(
                f"SELECT name FROM pragma_table_info('Main') Where cid={x}").fetchone()
        self.tree = ttk.Treeview(self, columns=self.columns, show="headings")
        self.tree.pack(anchor=S, fill=BOTH, expand=1)
        for x in self.columns:
            self.tree.heading(x, text=x)

        self.tree.bind("<<TreeviewSelect>>", self.select)

        for x in self.tree.get_children():
            self.tree.delete(x)

        self.headValues.extend(self.columns)
        self.checkTemp = False

        for x in range(self.numOfRows + 1):
            self.cursor.execute(f"SELECT * FROM Main WHERE id={x}")
            if self.checkTemp == False:
                self.checkTemp = True
            else:
                self.tableValues.append(self.cursor.fetchone())
        for x in self.tableValues:
            try:
                self.tree.insert("", END, values=x)
            except:
                pass

        self.tableName = "main"

        sv_ttk.set_theme("dark", self)

    def select(self,event):
        for selected_item in self.tree.selection():
            self.selectedProjectsList.clear()
            self.selectedProjects = ""
            self.item = self.tree.item(selected_item)
            self.project = self.item["values"]
            self.selectedProjectsList = self.item["values"].copy()
            self.selectedProjects = f"{self.selectedProjects}{self.project}\n"
        self.label["text"] = self.selectedProjects
        print(self.selectedProjects)

    def OpenWorkers(self):
        self.CleanWindow()

        self.FRTabs = ttk.Frame(self, height=20)
        self.FRTabs.pack(anchor=N, fill=X, expand=1)

        self.WorkersMainLabel = ttk.Label(self, width=30, font=DataFile.BIG_FONT, text="Работники")
        self.WorkersMainLabel.pack(anchor=CENTER, pady=20)

        self.label = ttk.Label(self, text="-")
        self.label.pack(anchor=N, fill=X, expand=1)

        self.BTtabsMainTable = ttk.Button(self.FRTabs, text="Главная таблица", width=20, command=self.OpenMainTable)
        self.BTtabsMainTable.pack(anchor=W, expand=1)

        self.BTaddWorker = ttk.Button(self.FRTabs, text="Добавить работника", width=20, command=self.AddWorker)
        self.BTaddWorker.pack(anchor=W, expand=1)

        self.BTchangeWorker = ttk.Button(self.FRTabs, text="Редактировать работника", width=20, command=self.ChangeWorker)
        self.BTchangeWorker.pack(anchor=W, expand=1)

        self.BTdeleteWorker = ttk.Button(self.FRTabs, text="Удалить работника", width=20, command=self.DeleteWorker)
        self.BTdeleteWorker.pack(anchor=W, expand=1)

        self.BTtabsCreateDocxWorkers = ttk.Button(self.FRTabs, text="Создать отчет", width=20, command=self.CreateDocxWorkers)
        self.BTtabsCreateDocxWorkers.pack(anchor=W, expand=1)

        self.connect = DataFile.connectMain
        self.cursor = self.connect.cursor()
        self.columns = ()
        self.cursor.execute(f"SELECT COUNT(*) FROM Workers")
        self.numOfRows = self.cursor.fetchone()[0]
        self.numOfColumns = \
            self.cursor.execute(f"SELECT COUNT(*) FROM pragma_table_info('Workers')").fetchone()[0]
        for x in range(self.numOfColumns):
            self.columns += self.cursor.execute(
                f"SELECT name FROM pragma_table_info('Workers') Where cid={x}").fetchone()
        self.tree = ttk.Treeview(self, columns=self.columns, show="headings")
        self.tree.pack(anchor=S, fill=BOTH, expand=1)
        for x in self.columns:
            self.tree.heading(x, text=x)

        self.tree.bind("<<TreeviewSelect>>", self.select)

        for x in self.tree.get_children():
            self.tree.delete(x)

        self.checkTemp = False
        self.tableValues.clear()

        for x in range(self.numOfRows + 1):
            self.cursor.execute(f"SELECT * FROM Workers WHERE id={x}")
            if self.checkTemp == False:
                self.checkTemp = True
            else:
                self.tableValues.append(self.cursor.fetchone())
        for x in self.tableValues:
            try:
                self.tree.insert("", END, values=x)
            except:
                pass

        self.tableName = "workers"

    def OpenMainTable(self):
        self.CleanWindow()

        self.FRTabs = ttk.Frame(self, height=20)
        self.FRTabs.pack(anchor=N, fill=X, expand=1)

        self.MainLabel = ttk.Label(self, width=30, font=DataFile.BIG_FONT, text="Товары")
        self.MainLabel.pack(anchor=CENTER, pady=20)

        self.label = ttk.Label(self, text="-")
        self.label.pack(anchor=N, fill=X, expand=1)

        self.BTtabsWorkers = ttk.Button(self.FRTabs, text="Работники", width=20, command=self.OpenWorkers)
        self.BTtabsWorkers.pack(anchor=W, expand=1)


        self.BTaddItem = ttk.Button(self.FRTabs, text="Добавить наименование", width=20, command=self.AddItem)
        self.BTaddItem.pack(anchor=W, expand=1)

        self.BTchangeItem = ttk.Button(self.FRTabs, text="Редактировать наименование", width=20, command=self.ChangeItem)
        self.BTchangeItem.pack(anchor=W, expand=1)

        self.BTdeleteItem = ttk.Button(self.FRTabs, text="Удалить наименование", width=20, command=self.DeleteItem)
        self.BTdeleteItem.pack(anchor=W, expand=1)

        self.BTtabsCreateDocxMain = ttk.Button(self.FRTabs, text="Создать отчет", width=20, command=self.CreateDocxMain)
        self.BTtabsCreateDocxMain.pack(anchor=W, expand=1)


        self.connect = DataFile.connectMain
        self.cursor = self.connect.cursor()
        self.columns = ()
        self.cursor.execute(f"SELECT COUNT(*) FROM Main")
        self.numOfRows = self.cursor.fetchone()[0]
        self.numOfColumns = \
            self.cursor.execute(f"SELECT COUNT(*) FROM pragma_table_info('Main')").fetchone()[0]
        for x in range(self.numOfColumns):
            self.columns += self.cursor.execute(
                f"SELECT name FROM pragma_table_info('Main') Where cid={x}").fetchone()
        self.tree = ttk.Treeview(self, columns=self.columns, show="headings")
        self.tree.pack(anchor=S, fill=BOTH, expand=1)
        for x in self.columns:
            self.tree.heading(x, text=x)

        self.tree.bind("<<TreeviewSelect>>", self.select)

        for x in self.tree.get_children():
            self.tree.delete(x)

        self.checkTemp = False
        self.tableValues.clear()

        for x in range(self.numOfRows + 1):
            self.cursor.execute(f"SELECT * FROM Main WHERE id={x}")
            if self.checkTemp == False:
                self.checkTemp = True
            else:
                self.tableValues.append(self.cursor.fetchone())
        for x in self.tableValues:
            try:
                self.tree.insert("", END, values=x)
            except:
                pass

        self.tableName = "main"

    def CleanWindow(self):
        for widgets in self.winfo_children():
            widgets.destroy()

    def AddItem(self):
        addItemWin = AddItemWin()
    def ChangeItem(self):
        pass
    def DeleteItem(self):
        pass
    def AddWorker(self):
        addWorkerWin = AddWorkerWin()
    def ChangeWorker(self):
        MainWindow.selectedProjectsList = self.selectedProjectsList
        changeWorkerWin = ChangeWorkerWin()
    def DeleteWorker(self):
        pass

    def CreateDocxWorkers(self):
        doc = DocxTemplate("workerTemplate.docx")
        self.BigText = ""
        self.workOpAll = 0
        self.junkAll = 0
        self.GOBAll = ""
        if self.tableName == "workers":
            for x in self.tableValues:
                self.num = x[0]
                self.fullName = x[1] + " " + x[2][0:1] + "." + x[3][0:1] + "."
                self.job = x[4]
                self.workTime = x[9]
                self.workOp = x[10]
                self.junk = x[11]
                self.GOB = x[12]
                self.other = "-"

                self.workOpAll += x[10]
                self.junkAll += x[11]

                self.BigText += f"{self.num}. {self.fullName} \n    - Должность: {self.job} \n    - Кол-во часов: {self.workTime} \n    - Кол-во операций: {self.workOp} \n    - Кол-во брака: {self.junk} \n    - Производительность: {self.GOB} \n    - Результат: {self.other} \n\n"
            self.context = {
                'text1': f"Отчет по сотрудникам склада\n(на основе данных за {datetime.datetime.now()}"[0:59]+")",
                'text1.5':"Ключевые показатели:",
                'text2': f"Общий объем обработанных товаров: {self.workOpAll} единиц \nКол-во инцидентов/брака: {self.junkAll}",
                'mainText': self.BigText
            }
            doc.render(self.context)
            doc.save("workers.docx")

    def CreateDocxMain(self):
        doc = DocxTemplate("mainTemplate.docx")
        self.BigText = ""
        self.workOpAll = 0
        self.junkAll = 0
        self.GOBAll = ""
        if self.tableName == "main":
            for x in self.tableValues:
                self.num = x[0]
                self.fullName = x[1] + " " + x[2][0:1] + "." + x[3][0:1] + "."
                self.job = x[4]
                self.workTime = x[9]
                self.workOp = x[10]
                self.junk = x[11]
                self.GOB = x[12]
                self.other = "-"

                self.workOpAll += x[10]
                self.junkAll += x[11]

                self.BigText += f"{self.num}. {self.fullName} \n    - Должность: {self.job} \n    - Кол-во часов: {self.workTime} \n    - Кол-во операций: {self.workOp} \n    - Кол-во брака: {self.junk} \n    - Производительность: {self.GOB} \n    - Результат: {self.other} \n\n"
            self.context = {
                'text1': f"Отчет по сотрудникам склада\n(на основе данных за {datetime.datetime.now()}"[0:59]+")",
                'text1.5':"Ключевые показатели:",
                'text2': f"Общий объем обработанных товаров: {self.workOpAll} единиц \nКол-во инцидентов/брака: {self.junkAll}",
                'mainText': self.BigText
            }
            doc.render(self.context)
            doc.save("main.docx")