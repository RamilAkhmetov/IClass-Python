# Главное окно приложения.
# Позволяет

import tkinter as tk

class App(tk.Frame):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.master.title("iClass")

        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)
        classesMenu = tk.Menu(menubar)
        classesMenu.add_command(label="Показать", command=self.showClasses)
        classesMenu.add_command(label="Добавить новый", command=self.createClass)
        menubar.add_cascade(label="Мои классы", menu=classesMenu)
        testsMenu = tk.Menu(self.master)
        testsMenu.add_command(label="Показать", command=self.showTests)
        testsMenu.add_command(label="Создать новую работу", command=self.createTest)
        menubar.add_cascade(label="Проверочные работы", menu=testsMenu)
    def showClasses(self):
        pass
    def showTests(self):
        pass
    def createClass(self):
        pass
    def createTest(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = App()
    root.geometry("750x700")
    root.mainloop()




