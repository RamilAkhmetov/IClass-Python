# Главное и единственное окно приложения.
import tkinter as tk
from tkinter import ttk
import classesList
import os
import sqlite3

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.Scrollable_frame = ScrollableFrame(master)
        self.frame = self.Scrollable_frame.scrollable_frame
        self.Scrollable_frame.pack()
        self.master = master
        self.initUI()

    def initUI(self):
        self.master.title("iClass")

        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)


        classesMenu = tk.Menu(menubar)
        classesMenu.add_command(label="Показать", command=self.showClasses)
        classesMenu.add_command(label="Добавить новый", command=self.createClass)
        menubar.add_cascade(label="Мои классы", menu=classesMenu)

        testsMenu = tk.Menu(menubar)
        testsMenu.add_command(label="Показать", command=self.showTests)
        testsMenu.add_command(label="Создать новую работу", command=self.createTest)
        menubar.add_cascade(label="Проверочные работы", menu=testsMenu)

        manualMenu = tk.Menu(menubar)
        manualMenu.add_command(label="Показать", command=self.showManual)
        menubar.add_cascade(label="Руководство пользователя", menu=manualMenu)

    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def showClasses(self):
        self.clear_frame()
        classesList = classList(self.frame)

    def showTests(self):
        self.clear_frame()
        testsList = testList(self.frame)

    def createClass(self):
        self.clear_frame()
        newclass = newClass(self.frame)

    def createTest(self):
        self.clear_frame()
        newtest = newTest(self.frame)

    def showManual(self):
        pass

class testList(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.master = master
        self.grid()
        self.initUI()
    def initUI(self):
        if "tests.db" not in os.listdir():
            tk.Label(master=self.master,
            text="Список работ пуст.\n Добавьте проверочную работу \n в разделе 'Создать новую работу'",
                    font=('Arial', 25)).grid(row=0, column=4,
                                             padx=10, pady=10)
        else:
            pass

class newTest(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.master = master
        self.name_entry = tk.Entry(master=self.master)
        self.count_entry = tk.Entry(master=self.master)
        self.questions = []
        self.grid()
        self.initUI()
    def initUI(self):
        tk.Label(text="Название работы", master=self.master).grid(row=0, column=0, padx=10, pady=10)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)
        tk.Label(text="Количество вопросов", master=self.master).grid(row=0, column=2, padx=10, pady=10)
        self.count_entry.grid(row=0, column=3, padx=10, pady=10)
        tk.Button(text="Применить", master=self.master, command=self.generate_constructor).grid(row=0, column=4, padx=10, pady=10)
        tk.Button(text="Сохранить работу", bg="light green", master=self.master).grid(row=0, column=5,
                                                                                      padx=10, pady=10)
    def generate_constructor(self):
        for i in range(int(self.count_entry.get())):
            tk.Label(master=self.master, text="Вопрос №1").grid(row=i*7+1, column=0, padx=10, pady=10)
            q = tk.Text(master=self.master, height=10, width=40)
            q.grid(row=i*7+1, column=1, columnspan=2, rowspan=2, padx=10, pady=10)
            self.questions.append(q)
            tk.Label(master=self.master, text="Число вариантов ответа.\nНе больше 6").grid(row=i*7+1, column=3,
                                                                             padx=10, pady=10)
            count_entry = tk.Entry(master=self.master)
            count_entry.grid(row=i*7+1, column=4, padx=10, pady=10)
            tk.Button(master=self.master, text="Применить").grid(row=i*7+1, column=5, padx=10, pady=10)


class classList(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.initUI()

    def get_classes(self):
        conn = sqlite3.connect("classes.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM classes")
        data = cursor.fetchall()
        classes = [x[0] for x in data]
        counts = [x[1] for x in data]

        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()








        return classes, counts, students

    def initUI(self):
        if "classes.db" not in os.listdir():
            tk.Label(master=self.master,
                     text="Список классов пуст.\n Добавьте класс в разделе 'Добавить новый'",
                     font=('Arial', 25)).grid(row=0, column=3,
                                                                                            padx=10, pady=10)
        else:
            classes, counts, students = self.get_classes()
            tk.Label(text=classes[0], master=self.master).grid(row=0, column=0, padx=10, pady=10)
            j = 0
            while j < counts[0]:
                tk.Button(master=self.master, text=students[j][1], bg="white", width=50).grid(row=1 + j, column=0,
                                                                        padx=10) #добавить command
                txt = tk.Text(master=self.master, height=1)
                txt.insert(1.0, students[j][2])
                txt.grid(row=1 + j, column=1, padx=10)

                j += 1
            cnt = 1 + counts[0]
            for i in range(1, len(classes)):
                tk.Label(text=classes[i], master=self.master).grid(row=cnt, column=0, padx=10, pady=10)
                j = 0
                while j < counts[i]:
                    tk.Button(master=self.master,text=students[j+counts[i-1]][1], bg="white", width=50).grid(row=cnt+1+j,
                                                                column=0, padx=10) #добавить command
                    txt = tk.Text(master=self.master, height=1)
                    txt.insert(1.0, students[j+counts[i-1]][2])
                    txt.grid(row=cnt + 1 + j, column=1, padx=10)
                    j += 1
                cnt += 1 + counts[i]



class newClass(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.count_entry = tk.Entry(master=self.master)
        self.name_entry = tk.Entry(master=self.master)
        self.names = []
        self.emails = []
        self.grid()
        self.initUI()


    def generate_table(self):
        tk.Label(master=self.master, text="ФИО ученика").grid(row=1, column=0)
        tk.Label(master=self.master, text="Email ученика").grid(row=1, column=2)
        count = int(self.count_entry.get())

        for i in range(count):
            name_entry = tk.Entry(master=self.master)
            name_entry.grid(row=i+2, column=0, columnspan=2, sticky=tk.W+tk.E)
            email_entry = tk.Entry(master=self.master)
            email_entry.grid(row=i+2, column=2, columnspan=2, sticky=tk.W+tk.E)
            self.names.append(name_entry)
            self.emails.append(email_entry)

    def load_list(self):
        if "classes.db" not in os.listdir():
            conn = sqlite3.connect("classes.db")
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE classes
                              (name text, count integer)
                           """)
            cursor.execute("""CREATE TABLE students
                              (class text, name text, email integer)
                           """)
            st_data = [(self.name_entry.get(), self.names[i].get(), self.emails[i].get()) for i in range(len(self.names))]
            cl_data = [(self.name_entry.get(), len(self.names))]
            cursor.executemany("INSERT INTO students VALUES (?,?,?)", st_data)
            cursor.executemany("INSERT INTO classes VALUES (?,?)", cl_data)
            conn.commit()

        else:
            conn = sqlite3.connect("classes.db")
            cursor = conn.cursor()
            cl_data = [(self.name_entry.get(), len(self.names))]
            st_data = [(self.name_entry.get(), self.names[i].get(), self.emails[i].get()) for i in range(len(self.names))]
            cursor.executemany("INSERT INTO students VALUES (?,?,?)", st_data)
            cursor.executemany("INSERT INTO classes VALUES (?,?)", cl_data)
            conn.commit()



    def initUI(self):

        self.columnconfigure(0)
        self.columnconfigure(1)
        self.columnconfigure(2)
        self.columnconfigure(3)
        self.columnconfigure(4)

        tk.Label(master=self.master, text="Количество учеников").grid(row=0, column=0, padx=10, pady=10)

        self.count_entry.grid(row=0, column=1, padx=10, pady=10)

        count_button = tk.Button(master=self.master, text="Применить", command=self.generate_table)
        count_button.grid(row=0, column=2, padx=10, pady=10)

        tk.Label(master=self.master, text="Имя класса").grid(row=0, column=3, padx=10, pady=10)

        self.name_entry.grid(row=0, column=4, padx=10, pady=10)

        save_button = tk.Button(master=self.master, text="Сохранить класс", bg="light green", command=self.load_list)
        save_button.grid(row=0, column=5, padx=10, pady=10)



class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self, width=1000, height=800)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")









def main():
    root = tk.Tk()
    app = App(root)
    root.geometry("1100x800")
    root.mainloop()
if __name__ == "__main__":
    main()




