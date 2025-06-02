import sqlite3
from tkinter import *
from tkinter import ttk
from docxtpl import DocxTemplate

import sv_ttk

import DataFile
import datetime
from AddItemWin import *
from AddWorkerWin import *
from ChangeItemWin import ChangeItemWin
from ChangeWorkerWin import *


class MainWin(Tk):
    selectedProjectsList = list()
    def __init__(self):
        super().__init__()

        self.selectedProjects = None
        self.title(DataFile.MainWindow_Title)
        self.geometry("1000x500")
        sv_ttk.set_theme("dark",self)
        self.state('zoomed')

        self.tableName = ""
        self.tableValues = list()
        self.headValues = list()
        self.numOfRows = any
        self.selectedProjectsList = list()
        self.tabsList = ["Товары", "Работники", "Списания", "Поступления"]
        self.current_tab = "Товары"

        self.mainFrame = ttk.Frame(self)
        self.mainFrame.pack(fill='both', expand=True)

        self.tabFrame = ttk.Frame(self.mainFrame)
        self.tabFrame.pack(fill='x', pady=(0, 5))

        self.contentFrame = ttk.Frame(self.mainFrame)
        self.contentFrame.pack(fill='both', expand=True, padx=10, pady=10)

        self.notebook = ttk.Notebook(self.tabFrame)
        self.notebook.pack(expand=True, fill="both")
        self.notebook.bind("<Button-1>", self.switchTabs)
        for x in self.tabsList:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=x)

        self.OpenMainTable()

    def switchTabs(self, event):
        if self.notebook.identify(event.x, event.y) == 'label':
            self.index = self.notebook.index(f'@{event.x},{event.y}')

        if self.index == 0:
            self.OpenMainTable()
        elif self.index == 1:
            self.OpenWorkers()
        elif self.index == 2:
            self.OpenDobTable()
        elif self.index == 3:
            self.OpenSpisTable()

    def OpenMainTable(self):
        self.CleanWindow()

        self.BTaddItem = ttk.Button(self.contentFrame, text="Добавить наименование", width=20, command=self.AddItem)
        self.BTaddItem.pack(anchor=W, expand=1)

        self.BTchangeItem = ttk.Button(self.contentFrame, text="Редактировать наименование", width=20,
                                       command=self.ChangeItem)
        self.BTchangeItem.pack(anchor=W, expand=1)

        self.BTdeleteItem = ttk.Button(self.contentFrame, text="Удалить наименование", width=20, command=self.DeleteItem)
        self.BTdeleteItem.pack(anchor=W, expand=1)

        self.BTtabsCreateDocxMain = ttk.Button(self.contentFrame, text="Создать отчет по выбранным наименованиям",
                                               width=20, command=self.CreateDocxMain)
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
        self.tree = ttk.Treeview(self.contentFrame, columns=self.columns, show="headings")
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
    def OpenWorkers(self):
        self.CleanWindow()

        self.BTaddWorker = ttk.Button(self.contentFrame, text="Добавить работника", width=20, command=self.AddWorker)
        self.BTaddWorker.pack(anchor=W, expand=1)

        self.BTchangeWorker = ttk.Button(self.contentFrame, text="Редактировать работника", width=20, command=self.ChangeWorker)
        self.BTchangeWorker.pack(anchor=W, expand=1)

        self.BTdeleteWorker = ttk.Button(self.contentFrame, text="Удалить работника", width=20, command=self.DeleteWorker)
        self.BTdeleteWorker.pack(anchor=W, expand=1)

        self.BTtabsCreateDocxWorkers = ttk.Button(self.contentFrame, text="Создать отчет", width=20, command=self.CreateDocxWorkers)
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
        self.tree = ttk.Treeview(self.contentFrame, columns=self.columns, show="headings")
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
    def OpenSpisTable(self):
        self.CleanWindow()

        self.connect = DataFile.connectMain
        self.cursor = self.connect.cursor()
        self.columns = ()
        self.cursor.execute(f"SELECT COUNT(*) FROM Spis")
        self.numOfRows = self.cursor.fetchone()[0]
        self.numOfColumns = \
            self.cursor.execute(f"SELECT COUNT(*) FROM pragma_table_info('Spis')").fetchone()[0]
        for x in range(self.numOfColumns):
            self.columns += self.cursor.execute(
                f"SELECT name FROM pragma_table_info('Spis') Where cid={x}").fetchone()
        self.tree = ttk.Treeview(self.contentFrame, columns=self.columns, show="headings")
        self.tree.pack(anchor=S, fill=BOTH, expand=1)
        for x in self.columns:
            self.tree.heading(x, text=x)

        self.tree.bind("<<TreeviewSelect>>", self.select)

        for x in self.tree.get_children():
            self.tree.delete(x)

        self.checkTemp = False
        self.tableValues.clear()

        for x in range(self.numOfRows + 1):
            self.cursor.execute(f"SELECT * FROM Spis WHERE id={x}")
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
    def OpenDobTable(self):
        self.CleanWindow()

        self.connect = DataFile.connectMain
        self.cursor = self.connect.cursor()
        self.columns = ()
        self.cursor.execute(f"SELECT COUNT(*) FROM Dob")
        self.numOfRows = self.cursor.fetchone()[0]
        self.numOfColumns = \
            self.cursor.execute(f"SELECT COUNT(*) FROM pragma_table_info('Dob')").fetchone()[0]
        for x in range(self.numOfColumns):
            self.columns += self.cursor.execute(
                f"SELECT name FROM pragma_table_info('Dob') Where cid={x}").fetchone()
        self.tree = ttk.Treeview(self.contentFrame, columns=self.columns, show="headings")
        self.tree.pack(anchor=S, fill=BOTH, expand=1)
        for x in self.columns:
            self.tree.heading(x, text=x)

        self.tree.bind("<<TreeviewSelect>>", self.select)

        for x in self.tree.get_children():
            self.tree.delete(x)

        self.checkTemp = False
        self.tableValues.clear()

        for x in range(self.numOfRows + 1):
            self.cursor.execute(f"SELECT * FROM Dob WHERE id={x}")
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
        for widgets in self.contentFrame.winfo_children():
            widgets.destroy()

    def AddItem(self):
        addItemWin = AddItemWin()
    def ChangeItem(self):
        MainWindow.selectedProjectsList = self.selectedProjectsList
        changeItemWin = ChangeItemWin()
    def DeleteItem(self):
        self.connect = DataFile.connectMain
        self.cursor = self.connect.cursor()
        if (len(self.selectedProjectsList) == 0):
            self.label["text"] = "Ничего не выбрано"
        else:
            self.cursor.execute("INSERT INTO Spis VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (self.selectedProjectsList[0], self.selectedProjectsList[1], self.selectedProjectsList[2], self.selectedProjectsList[3], self.selectedProjectsList[4], self.selectedProjectsList[5], self.selectedProjectsList[6], self.selectedProjectsList[7], self.selectedProjectsList[8]))
            self.connect.commit()
            self.temp = f"{self.cursor.execute(f"SELECT id FROM Spis ORDER BY id desc").fetchone()[0]+1}"
            self.cursor.execute(f"UPDATE Spis SET id = {self.temp} WHERE id = {self.selectedProjectsList[0]}")
            self.connect.commit()
            self.cursor.execute(
                f"DELETE FROM Main WHERE ID = %(first)s" % {"first": self.selectedProjectsList[0]})
            self.connect.commit()
            self.OpenMainTable()

    def AddWorker(self):
        addWorkerWin = AddWorkerWin()
    def ChangeWorker(self):
        MainWindow.selectedProjectsList = self.selectedProjectsList
        changeWorkerWin = ChangeWorkerWin()
    def DeleteWorker(self):
        self.connect = DataFile.connectMain
        self.cursor = self.connect.cursor()
        if (len(self.selectedProjectsList) == 0):
            self.label["text"] = "Ничего не выбрано"
        else:
            self.cursor.execute(
                f"DELETE FROM Workers WHERE ID = %(first)s" % {"first": self.selectedProjectsList[0]})
            self.connect.commit()
            self.OpenWorkers()

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
                'text1': f"Отчет по сотрудникам склада\n(на основе данных за {datetime.now()}"[0:59]+")",
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
            for x in self.selectedProjectsList:
                self.num = x[0]
                self.name = x[1]
                self.edIzm = x[2]
                self.ostFact = x[3]
                self.ostDost = x[4]
                self.Bron = x[5]
                self.sellPrice = x[6]
                self.buyPrice = x[7]
                self.goodGuy = x[8]

                self.BigText += f"{self.num}. {self.name} {self.edIzm} {self.ostFact} {self.ostDost} {self.Bron} {self.sellPrice} {self.buyPrice} {self.goodGuy}\n\n"
            self.context = {
                'text1': f"Отчет по хранению\n(на основе данных за {datetime.now()}"[0:58]+")",
                'text1.5': f"id Наименование Ед.изм. Ост факт. Ост. доступно Бронь Цена продажи Цена Закупки Поставщик",
                'text2': f"Данные были выбраны вручную",
                'mainText': self.BigText
            }
            doc.render(self.context)
            doc.save("main.docx")

    def select(self,event):
        check = True
        for selected_item in self.tree.selection():
            if len(self.tree.selection()) == 1:
                self.selectedProjectsList.clear()
                self.selectedProjects = ""
                self.item = self.tree.item(selected_item)
                self.project = self.item["values"]
                self.selectedProjectsList = self.item["values"].copy()
                self.selectedProjects = f"{self.selectedProjects}{self.project}\n"
            if len(self.tree.selection()) > 1:
                if check:
                    self.selectedProjectsList.clear()
                    self.selectedProjects = ""
                    self.item = self.tree.item(selected_item)
                    self.project = self.item["values"]
                    self.selectedProjectsList.append(self.item["values"])
                    self.selectedProjects = f"{self.selectedProjects}{self.project}\n"
                    check = False
                else:
                    self.selectedProjects = ""
                    self.item = self.tree.item(selected_item)
                    self.project = self.item["values"]
                    self.selectedProjectsList.append(self.item["values"])
                    self.selectedProjects = f"{self.selectedProjects}{self.project}\n"
        self.label["text"] = self.selectedProjects
        check = True
        print(self.selectedProjects)