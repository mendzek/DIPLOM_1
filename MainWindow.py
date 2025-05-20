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
from DataFile import *

class MainWindow(Tk):
    selectedProjectsList = list()
    def __init__(self):
        super().__init__()

        selectedProjects = None
        self.title(DataFile.MainWindow_Title)
        self.geometry("1000x500")

        sv_ttk.set_theme("dark", )

    def AddItem(self):
        addItemWin = AddItemWin()
    def ChangeItem(self):
        pass
    def DeleteItem(self):
        pass
    def AddWorker(self):
        addWorkerWin = AddWorkerWin()
    def ChangeWorker(self):
        MainWindow.selectedProjectsList = MainWindow.selectedProjectsList
        changeWorkerWin = ChangeWorkerWin()
    def DeleteWorker(self):
        pass
    def select(event):

        for selected_item in MainWindow.tree.selection():
            MainWindow.selectedProjectsList.clear()
            selectedProjects = ""
            item = MainWindow.tree.item(selected_item)
            project = item["values"]
            selectedProjectsList = item["values"].copy()
            selectedProjects = f"{selectedProjects}{project}\n"
        MainWindow.label["text"] = selectedProjects
        print(selectedProjects)

    def CleanWindow(self):
        for widgets in MainWindow.winfo_children():
            widgets.destroy()

    def OpenWorkers(self):
        self.CleanWindow()

        def select(event):
            for selected_item in MainWindow.tree.selection():
                MainWindow.selectedProjectsList.clear()
                selectedProjects = ""
                item = MainWindow.tree.item(selected_item)
                project = item["values"]
                selectedProjectsList = item["values"].copy()
                selectedProjects = f"{selectedProjects}{project}\n"
            MainWindow.label["text"] = selectedProjects
            print(selectedProjects)

        FRTabs = ttk.Frame(height=20)
        FRTabs.pack(anchor=N, fill=X, expand=1)

        WorkersMainLabel = ttk.Label( width=30, font=DataFile.BIG_FONT, text="Работники")
        WorkersMainLabel.pack(anchor=CENTER, pady=20)

        label = ttk.Label( text="-")
        label.pack(anchor=N, fill=X, expand=1)

        BTtabsMainTable = ttk.Button(FRTabs, text="Главная таблица", width=20, command=self.OpenMainTable)
        BTtabsMainTable.pack(anchor=W, expand=1)

        BTaddWorker = ttk.Button(FRTabs, text="Добавить работника", width=20, command=self.AddWorker)
        BTaddWorker.pack(anchor=W, expand=1)

        BTchangeWorker = ttk.Button(FRTabs, text="Редактировать работника", width=20, command=self.ChangeWorker)
        BTchangeWorker.pack(anchor=W, expand=1)

        BTdeleteWorker = ttk.Button(FRTabs, text="Удалить работника", width=20, command=self.DeleteWorker)
        BTdeleteWorker.pack(anchor=W, expand=1)

        BTtabsCreateDocxWorkers = ttk.Button(FRTabs, text="Создать отчет", width=20, command=self.CreateDocxWorkers)
        BTtabsCreateDocxWorkers.pack(anchor=W, expand=1)

        connect = DataFile.connectMain
        cursor = connect.cursor()
        columns = ()
        cursor.execute(f"SELECT COUNT(*) FROM Workers")
        numOfRows = cursor.fetchone()[0]
        numOfColumns = \
            cursor.execute(f"SELECT COUNT(*) FROM pragma_table_info('Workers')").fetchone()[0]
        for x in range(numOfColumns):
            columns += cursor.execute(
                f"SELECT name FROM pragma_table_info('Workers') Where cid={x}").fetchone()
        tree = ttk.Treeview( columns=columns, show="headings")
        tree.pack(anchor=S, fill=BOTH, expand=1)
        for x in columns:
            tree.heading(x, text=x)

        tree.bind("<<TreeviewSelect>>", select)

        for x in tree.get_children():
            tree.delete(x)

        checkTemp = False
        self.tableValues.clear()

        for x in range(numOfRows + 1):
            cursor.execute(f"SELECT * FROM Workers WHERE id={x}")
            if checkTemp == False:
                checkTemp = True
            else:
                self.tableValues.append(cursor.fetchone())
        for x in self.tableValues:
            try:
                tree.insert("", END, values=x)
            except:
                pass

        tableName = "workers"

    def OpenMainTable(self):
        self.CleanWindow()

        def select(event):
            for selected_item in MainWindow.tree.selection():
                MainWindow.selectedProjectsList.clear()
                selectedProjects = ""
                item = MainWindow.tree.item(selected_item)
                project = item["values"]
                selectedProjectsList = item["values"].copy()
                selectedProjects = f"{selectedProjects}{project}\n"
            MainWindow.label["text"] = selectedProjects
            print(selectedProjects)

        FRTabs = ttk.Frame(height=20)
        FRTabs.pack(anchor=N, fill=X, expand=1)

        MainLabel = ttk.Label( width=30, font=DataFile.BIG_FONT, text="Товары")
        MainLabel.pack(anchor=CENTER, pady=20)

        label = ttk.Label( text="-")
        label.pack(anchor=N, fill=X, expand=1)

        BTtabsWorkers = ttk.Button(FRTabs, text="Работники", width=20, command=self.OpenWorkers)
        BTtabsWorkers.pack(anchor=W, expand=1)


        BTaddItem = ttk.Button(FRTabs, text="Добавить наименование", width=20, command=self.AddItem)
        BTaddItem.pack(anchor=W, expand=1)

        BTchangeItem = ttk.Button(FRTabs, text="Редактировать наименование", width=20, command=self.ChangeItem)
        BTchangeItem.pack(anchor=W, expand=1)

        BTdeleteItem = ttk.Button(FRTabs, text="Удалить наименование", width=20, command=self.DeleteItem)
        BTdeleteItem.pack(anchor=W, expand=1)

        BTtabsCreateDocxMain = ttk.Button(FRTabs, text="Создать отчет", width=20, command=self.CreateDocxMain)
        BTtabsCreateDocxMain.pack(anchor=W, expand=1)


        connect = DataFile.connectMain
        cursor = connect.cursor()
        columns = ()
        cursor.execute(f"SELECT COUNT(*) FROM Main")
        numOfRows = cursor.fetchone()[0]
        numOfColumns = \
            cursor.execute(f"SELECT COUNT(*) FROM pragma_table_info('Main')").fetchone()[0]
        for x in range(numOfColumns):
            columns += cursor.execute(
                f"SELECT name FROM pragma_table_info('Main') Where cid={x}").fetchone()
        tree = ttk.Treeview(columns=columns, show="headings")
        tree.pack(anchor=S, fill=BOTH, expand=1)
        for x in columns:
            tree.heading(x, text=x)

        tree.bind("<<TreeviewSelect>>", select)

        for x in tree.get_children():
            tree.delete(x)

        checkTemp = False
        self.tableValues.clear()

        for x in range(numOfRows + 1):
            cursor.execute(f"SELECT * FROM Main WHERE id={x}")
            if checkTemp == False:
                checkTemp = True
            else:
                self.tableValues.append(cursor.fetchone())
        for x in self.tableValues:
            try:
                tree.insert("", END, values=x)
            except:
                pass

        tableName = "main"





    def CreateDocxWorkers(self):
        doc = DocxTemplate("workerTemplate.docx")
        BigText = ""
        workOpAll = 0
        junkAll = 0
        GOBAll = ""
        if self.tableName == "workers":
            for x in self.tableValues:
                num = x[0]
                fullName = x[1] + " " + x[2][0:1] + "." + x[3][0:1] + "."
                job = x[4]
                workTime = x[9]
                workOp = x[10]
                junk = x[11]
                GOB = x[12]
                other = "-"

                workOpAll += x[10]
                junkAll += x[11]

                BigText += f"{num}. {fullName} \n    - Должность: {job} \n    - Кол-во часов: {workTime} \n    - Кол-во операций: {workOp} \n    - Кол-во брака: {junk} \n    - Производительность: {GOB} \n    - Результат: {other} \n\n"
            context = {
                'text1': f"Отчет по сотрудникам склада\n(на основе данных за {datetime.now()}"[0:59]+")",
                'text1.5':"Ключевые показатели:",
                'text2': f"Общий объем обработанных товаров: {workOpAll} единиц \nКол-во инцидентов/брака: {junkAll}",
                'mainText': BigText
            }
            doc.render(context)
            doc.save("workers.docx")
            print("created workers docx")

    def CreateDocxMain(self):
        doc = DocxTemplate("mainTemplate.docx")
        BigText = ""
        workOpAll = 0
        junkAll = 0
        GOBAll = ""
        if self.tableName == "main":
            for x in self.tableValues:
                num = x[0]
                fullName = x[1] + " " + x[2][0:1] + "." + x[3][0:1] + "."
                job = x[4]
                workTime = x[9]
                workOp = x[10]
                junk = x[11]
                GOB = x[12]
                other = "-"

                workOpAll += x[10]
                junkAll += x[11]

                BigText += f"{num}. {fullName} \n    - Должность: {job} \n    - Кол-во часов: {workTime} \n    - Кол-во операций: {workOp} \n    - Кол-во брака: {junk} \n    - Производительность: {GOB} \n    - Результат: {other} \n\n"
            context = {
                'text1': f"Отчет по сотрудникам склада\n(на основе данных за {datetime.now()}"[0:59]+")",
                'text1.5':"Ключевые показатели:",
                'text2': f"Общий объем обработанных товаров: {workOpAll} единиц \nКол-во инцидентов/брака: {junkAll}",
                'mainText': BigText
            }
            doc.render(context)
            doc.save("main.docx")
            print("created main docx")



    tableName = ""
    tableValues = list()
    headValues = list()
    numOfRows = any

    FRTabs = ttk.Frame(height=20)
    FRTabs.pack(anchor=N, fill=X, expand=1)

    MainLabel = ttk.Label(width=30, font=("Arial", 30), text="Товары")
    MainLabel.pack(anchor=CENTER, pady=20)

    label = ttk.Label(text="-")
    label.pack(anchor=N, fill=X, expand=1)

    BTtabsWorkers = ttk.Button(FRTabs, text="Работники", width=20, command=OpenWorkers)
    BTtabsWorkers.pack(anchor=W, expand=1)

    BTaddItem = ttk.Button(FRTabs, text="Добавить наименование", width=20, command=AddItem)
    BTaddItem.pack(anchor=W, expand=1)

    BTchangeItem = ttk.Button(FRTabs, text="Редактировать наименование", width=20, command=ChangeItem)
    BTchangeItem.pack(anchor=W, expand=1)

    BTdeleteItem = ttk.Button(FRTabs, text="Удалить наименование", width=20, command=DeleteItem)
    BTdeleteItem.pack(anchor=W, expand=1)

    BTtabsCreateDocxMain = ttk.Button(FRTabs, text="Создать отчет", width=20, command=CreateDocxMain)
    BTtabsCreateDocxMain.pack(anchor=W, expand=1)

    connect = sqlite3.connect("Main.db")
    cursor = connect.cursor()
    columns = ()
    cursor.execute(f"SELECT COUNT(*) FROM Main")
    numOfRows = cursor.fetchone()[0]
    numOfColumns = \
        cursor.execute(f"SELECT COUNT(*) FROM pragma_table_info('Main')").fetchone()[0]
    for x in range(numOfColumns):
        columns += cursor.execute(
            f"SELECT name FROM pragma_table_info('Main') Where cid={x}").fetchone()
    tree = ttk.Treeview(columns=columns, show="headings")
    tree.pack(anchor=S, fill=BOTH, expand=1)
    for x in columns:
        tree.heading(x, text=x)

    tree.bind("<<TreeviewSelect>>", select)

    for x in tree.get_children():
        tree.delete(x)

    checkTemp = False
    tableValues.clear()

    for x in range(numOfRows + 1):
        cursor.execute(f"SELECT * FROM Main WHERE id={x}")
        if checkTemp == False:
            checkTemp = True
        else:
            tableValues.append(cursor.fetchone())
    for x in tableValues:
        try:
            tree.insert("", END, values=x)
        except:
            pass

    tableName = "main"

