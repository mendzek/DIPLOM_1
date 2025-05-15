from tkinter import *
from tkinter import ttk
import sv_ttk
from tkinter.messagebox import showwarning
import MainWindow
from MainWindow import *
import DataFile
from MenuWindow import MenuWindow
from RegistrationWindow import RegistrationWindow


class LogPassWindow(Tk):
    def __init__(self):
        super().__init__()

        self.title("Вход в систему")
        self.geometry("600x400")
        self.resizable(False, False)

        self.MainLabel = ttk.Label(self, width=30, font=DataFile.BIG_FONT, text="УЧЕТ ХРАНЕНИЯ НА СКЛАДЕ")
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

        self.BTLogPassAccept = ttk.Button(self, text="Войти", width=20,  command=self.AcceptLogPass)
        self.BTLogPassAccept.pack(anchor=CENTER)

        sv_ttk.set_theme("dark")

    def AcceptLogPass(self):
        LogPassBool = False
        if DataFile.cursorLogPass.execute("SELECT * FROM LogPass WHERE login = ? AND password = ?", (self.EntryLog.get(), self.EntryPass.get())).fetchone() != None:
            LogPassBool = True
        DataFile.connectLogPass.commit()

        if LogPassBool:
            print("nice")
            menuWindow = MenuWindow()
        else:
            print("not nice")
            showwarning(title="Ошибка", message="Неверный логин или пароль, попробуйте снова")

    def Register(self):
        registrationWindow = RegistrationWindow()

    def ForgotPassword(self):
        pass

    def on_entry_click1(self, event):
        if self.EntryLog.get() == 'Login':
            self.EntryLog.delete(0, "end")
            self.EntryLog.insert(0, '')
            self.EntryLog.config(foreground='white')
    def on_focusout1(self, event):
        if self.EntryLog.get() == '':
            self.EntryLog.insert(0, 'Login')
            self.EntryLog.config(foreground='grey')
    def on_entry_click2(self, event):
        if self.EntryPass.get() == 'Password':
            self.EntryPass.delete(0, "end")
            self.EntryPass.insert(0, '')
            self.EntryPass.config(foreground='white')
    def on_focusout2(self, event):
        if self.EntryPass.get() == '':
            self.EntryPass.insert(0, 'Password')
            self.EntryPass.config(foreground='grey')


logPassWindow = LogPassWindow()
logPassWindow.mainloop()