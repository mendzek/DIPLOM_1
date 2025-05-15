from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showwarning
from MainWindow import *
import sv_ttk
import DataFile



class RegistrationWindow(Tk):
    def __init__(self):
        super().__init__()

        self.CHKShowPass_State = IntVar()
        self.temp = 0

        self.title("Регистрация")
        self.geometry("600x400")

        self.MainLabel = ttk.Label(self, width=30, font=DataFile.REGULAR_FONT, text="Придумайте логин и пароль для входа")
        self.MainLabel.pack(anchor=CENTER, pady=20)

        self.EntryLog = ttk.Entry(self, width=15, font=DataFile.REGULAR_FONT, foreground='grey')
        self.EntryLog.insert(0, "Login")
        self.EntryLog.bind('<FocusIn>', self.on_entry_click1)
        self.EntryLog.bind('<FocusOut>', self.on_focusout1)
        self.EntryLog.pack(anchor=CENTER, pady=20)

        self.EntryPass = ttk.Entry(self, width=15, font=DataFile.REGULAR_FONT, foreground='grey')
        self.EntryPass.config(show="*")
        self.EntryPass.insert(0, "Password")
        self.EntryPass.bind('<FocusIn>', self.on_entry_click2)
        self.EntryPass.bind('<FocusOut>', self.on_focusout2)
        self.EntryPass.pack(anchor=CENTER)

        self.CHKShowPass = ttk.Checkbutton(self, text="Показать пароль", width=20, variable=self.CHKShowPass_State, command=self.CheckShowPass)
        self.CHKShowPass.pack(anchor=CENTER)

        self.BTRegister = ttk.Button(self, text="Зарегистрироваться", width=20, command=self.Register)
        self.BTRegister.pack(anchor=CENTER)

        sv_ttk.set_theme("dark", self)

    def Register(self):
        idTemp = DataFile.cursorLogPass.execute(f"SELECT COUNT(*) FROM LogPass").fetchone()[0]
        DataFile.cursorLogPass.execute(f"INSERT INTO LogPass VALUES({idTemp+1}, \"{self.EntryLog.get()}\",\"{self.EntryPass.get()}\")")
        DataFile.connectLogPass.commit()

    def on_entry_click1(self, event):
        if self.EntryLog.get() == 'Login':
            self.EntryLog.delete(0, "end")
            self.EntryLog.insert(0, '')
            self.EntryLog.config(foreground='black')
    def on_focusout1(self, event):
        if self.EntryLog.get() == '':
            self.EntryLog.insert(0, 'Login')
            self.EntryLog.config(foreground='grey')
    def on_entry_click2(self, event):
        if self.EntryPass.get() == 'Password':
            self.EntryPass.delete(0, "end")
            self.EntryPass.insert(0, '')
            self.EntryPass.config(foreground='black')
    def on_focusout2(self, event):
        if self.EntryPass.get() == '':
            self.EntryPass.insert(0, 'Password')
            self.EntryPass.config(foreground='grey')

    def CheckShowPass(self):
        if self.temp == 0:
            self.CHKShowPass_State.set(1)
            self.temp = 1
        else:
            self.CHKShowPass_State.set(0)
            self.temp = 0
        if self.CHKShowPass_State.get() == 1:
            self.EntryPass.config(show="")
        else:
            self.EntryPass.config(show="*")


