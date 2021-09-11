import tkinter as tk
from tkinter import ttk
import time
import re
import os
import sqlite3
import pathlib
from tkinter import messagebox as mb

light_green = "#C4F4CE"
light_yellow = "#F5EBCF",
base_font = ("Arial", 10)
weight="bold"
heading_font = ("Arial", 15, weight)
manual_font = ("Arial", 12)


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

    @staticmethod
    def clear_frame(frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def showClasses(self):
        self.clear_frame(self.frame)
        classesList = classList(self.frame)

    def showTests(self):
        self.clear_frame(self.frame)
        testsList = testList(self.frame)

    def createClass(self):
        self.clear_frame(self.frame)
        newclass = newClass(self.frame)

    def createTest(self):
        self.clear_frame(self.frame)
        newtest = newTest(self.frame)

    def showManual(self):
        self.clear_frame(self.frame)
        manual = Manual(self.frame)

class Manual(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.initUI()

    def initUI(self):
        tk.Label(master=self.master, font=heading_font, text="Описание программы").grid(
            row=0, column=0, sticky="w", padx=(0, 0))
        paragraph_1 = """\tiClass - это приложение для создания тренировочных работ. """
        tk.Label(master=self.master, font=manual_font, text=paragraph_1, wraplength=900, justify="left").grid(
            row=1, column=0, sticky="w", padx=(0 ,0)
        )

class testList(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.show_bts = []
        self.file_bts = []

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
            conn = sqlite3.connect("tests.db")
            cursor = conn.cursor()


            cursor.execute("SELECT * FROM tests;")
            data = cursor.fetchall()

            tests_count = len(data)
            for i in range(tests_count):
                test_frame = tk.Frame(master=self, bg="white",
                                  highlightbackground=light_green, highlightthickness=3,
                                  highlightcolor=light_green)
                test_frame.pack(side="top", fill="x")
                tk.Label(master=test_frame, font=base_font, bg="white", wraplength=600, justify="left",
                         text=data[i][1], ).pack(side=tk.LEFT, padx=(5, 0), pady=0)


                fl_bt = tk.Button(master=test_frame, font=base_font,
                          text=f"Выгрузить файл №{i+1}", )
                fl_bt.pack(side=tk.RIGHT, padx=0)
                fl_bt.bind(f"<Button-1>", self.on_click_fl_bt)
                sh_bt = tk.Button(master=test_frame, font=base_font,
                          text=f"Просмотреть/редактировать №{i+1}")
                sh_bt.pack(side=tk.RIGHT, padx=(30, 0))
                sh_bt.bind(f"<Button-1>", self.on_click_sh_bt)

    def on_click_fl_bt(self, event):
        button_text = event.widget.cget("text")
        bt_ind = list(button_text.split())[-1][-1]
        self.uploadFile(bt_ind)

    def on_click_sh_bt(self, event):
        button_text = event.widget.cget("text")
        bt_ind = list(button_text.split())[-1][-1]
        self.showTest(bt_ind)

    def showTest(self, index):
        App.clear_frame(self.master)
        test = Test(self.master, index)
        self.destroy()


    def uploadFile(self, index):

        conn = sqlite3.connect("tests.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tests WHERE id=?", [(index)])
        i, name, count_q = cursor.fetchone()

        cursor.execute("SELECT * FROM types WHERE test_name=?", [(name)])
        types = cursor.fetchall()
        types = [(types[i][1], types[i][2]) for i in range(len(types))]

        cursor.execute("SELECT * FROM tasks_with_questions WHERE test_name=?", [(name)])
        tasks_with_questions = cursor.fetchall()
        tasks_with_questions = [(tasks_with_questions[i][1], tasks_with_questions[i][2],) for i in range(len(tasks_with_questions))]

        cursor.execute("SELECT * FROM tasks_with_answers WHERE test_name=?", [(name)])
        tasks_with_answers = cursor.fetchall()
        tasks_with_answers = [(tasks_with_answers[i][1], tasks_with_answers[i][2], tasks_with_answers[i][3], tasks_with_answers[i][4])
                              for i in range(len(tasks_with_answers))]

        cursor.execute("SELECT * FROM tasks_with_variants WHERE test_name=?", [(name)])
        tasks_with_variants = cursor.fetchall()
        tasks_with_variants = [(tasks_with_variants[i][1], tasks_with_variants[i][2], tasks_with_variants[i][3])
                               for i in range(len(tasks_with_variants))]

        cursor.execute("SELECT * FROM  variants WHERE test_name=?", [(name)])
        variants = cursor.fetchall()
        variants = [(variants[i][1], variants[i][2], variants[i][3]) for i in range(len(variants))]

        if "tests" not in os.listdir():
            os.makedirs("tests")
        test_name = name[:200]
        test_name = re.sub(r'[/\\?%*:|"<>.,]', "", test_name)
        test_name = re.sub(r'[ ]', "_", test_name)
        test_name = re.sub(r'[\n]', "", test_name)


        test_path = str(pathlib.Path().resolve())+f"\\tests\\{test_name}.db"

        if test_path in os.listdir(r'tests'):
            os.remove(test_path)
        cnn = sqlite3.connect(test_path)
        curs = cnn.cursor()
        curs.execute("CREATE TABLE IF NOT EXISTS count_q(count integer);")
        cnn.commit()
        curs.execute("CREATE TABLE IF NOT EXISTS types(id integer primary key, test_name text, type integer);")
        cnn.commit()
        curs.execute("CREATE TABLE IF NOT EXISTS tasks_with_answers(id integer primary key, test_name text, task text, answer text, err real);")
        cnn.commit()
        curs.execute("CREATE TABLE IF NOT EXISTS tasks_with_variants(id integer primary key, test_name text, task text, count_variants integer);")
        cnn.commit()
        curs.execute("CREATE TABLE IF NOT EXISTS tasks_with_questions(id integer primary key, test_name text, task text);")
        cnn.commit()
        curs.execute("CREATE TABLE IF NOT EXISTS variants(id integer primary key, test_name text, variant text, status integer);")
        cnn.commit()

        curs.execute("INSERT INTO count_q(count) VALUES(?);",
                       (count_q,))
        conn.commit()
        curs.executemany("INSERT INTO types(test_name, type) VALUES(?, ?);",
                         types)
        conn.commit()
        curs.executemany("INSERT INTO tasks_with_answers(test_name, task, answer, err) VALUES(?, ?, ?, ?);",
                           tasks_with_answers)
        conn.commit()
        curs.executemany("INSERT INTO tasks_with_variants(test_name, task, count_variants) VALUES(?, ?, ?);",
                           tasks_with_variants)
        conn.commit()
        curs.executemany("INSERT INTO tasks_with_questions(test_name, task) VALUES(?, ?);", tasks_with_questions)
        conn.commit()
        curs.executemany("INSERT INTO variants(test_name, variant, status) VALUES(?, ?, ?);", variants)
        conn.commit()





class Test(tk.Frame):
    def __init__(self, master, index):
        super().__init__(master)
        self.master = master
        self.index = index
        self.name_text = tk.Text(master=self, width=30, height=4, wrap=tk.WORD)
        self.count_text = tk.Text(master=self, width=10, height=1)
        self.task_frame = tk.Frame(master=self, bg=light_green, highlightbackground="green", highlightcolor="green",
                                   highlightthickness=3)

        self.current_tsk_q = 0
        self.current_tsk_a = 0
        self.current_tsk_v = 0
        self.current_var = 0

        self.current_type = None
        self.current_task = ""

        self.current_flags_list = []
        self.current_variants_list = []

        self.current_answer = ""
        self.current_err = 0

        self.types = [None for i in range(100)]
        self.tasks = [None for i in range(100)]

        self.variants = [None for i in range(100)]
        self.flags = [None for i in range(100)]

        self.answers = [None for i in range(100)]
        self.errors = [None for i in range(100)]

        self.current = 1


        self.grid()
        self.initUI()

    def initUI(self):
        conn = sqlite3.connect("tests.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tests WHERE id=?", [(self.index)])
        data = cursor.fetchone()
        i, name, count_q = data

        cursor.execute("SELECT * FROM types WHERE test_name=?;", [(name)])
        types = cursor.fetchall()
        cursor.execute("SELECT * FROM tasks_with_answers WHERE test_name=?;", [(name)])
        tasks_with_answers = cursor.fetchall()
        cursor.execute("SELECT * FROM tasks_with_variants WHERE test_name=?;", [(name)])
        tasks_with_variants = cursor.fetchall()
        cursor.execute("SELECT * FROM variants WHERE test_name=?;", [(name)])
        variants = cursor.fetchall()
        cursor.execute("SELECT * FROM tasks_with_questions WHERE test_name=?;", [(name)])
        tasks_with_questions = cursor.fetchall()
        for i in range(count_q):
            if types[i][2] == 0:
                self.types[i] = 0
                self.tasks[i] = tasks_with_variants[self.current_tsk_v][2]
                count_v = tasks_with_variants[self.current_tsk_v][3]
                vrs = []
                fgs = []
                for j in range(count_v):
                    vrs.append(variants[self.current_var][2])
                    fgs.append(variants[self.current_var][3])
                    self.current_var += 1
                self.variants[i] = vrs
                self.flags[i] = fgs
                self.current_tsk_v += 1
            elif types[i][2] == 1:
                self.types[i] = 1
                self.tasks[i] = tasks_with_answers[self.current_tsk_a][2]
                self.answers[i] = tasks_with_answers[self.current_tsk_a][3]
                self.errors[i] = tasks_with_answers[self.current_tsk_a][4]
            elif types[i][2] == 2:
                self.types[i] = 2
                self.tasks[i] = tasks_with_questions[self.current_tsk_q][2]

        name = list(name.split(sep=") "))[1]

        tk.Label(text="Название работы", master=self, font=base_font).grid(
            row=0, column=0, padx=10, pady=10, sticky="n")
        self.name_text.grid(row=0, column=1, padx=10, pady=10, sticky="n")
        self.name_text.insert(1.0, name)
        tk.Label(text="Количество вопросов\n(не больше 100)", master=self, font=base_font).grid(
            row=0, column=2, padx=10, pady=10, sticky="n")
        self.count_text.grid(row=0, column=3, padx=10, pady=10, sticky="n")
        self.count_text.insert(1.0, str(count_q))
        tk.Button(text="Применить", master=self, command=self.generate_constructor, font=base_font).grid(
            row=0, column=4, padx=10, pady=10, sticky="n")
        tk.Button(text="Сохранить работу", bg="light green", master=self, font=base_font, command=self.save_test).grid(
            row=0, column=5, padx=10, pady=10, sticky="n")
        self.generate_constructor()

    def save_test(self):
        conn = sqlite3.connect("tests.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tests WHERE id=?", [(self.index)])
        old_i, old_name, old_count_q = cursor.fetchone()
        test_name = str(old_i) + ") " + self.name_text.get(1.0, tk.END)
        test_name = re.sub(r'[\n]', "", test_name)
        count_q = int(self.count_text.get(1.0, tk.END))

        cursor.execute("UPDATE tests SET test_name=? WHERE test_name=?", (test_name, old_name))
        conn.commit()
        cursor.execute("UPDATE tests SET count_q=? WHERE test_name=?", (count_q, test_name))
        conn.commit()
        cursor.execute("DELETE  FROM tasks_with_variants WHERE test_name=?", [(old_name)])
        conn.commit()
        cursor.execute("DELETE  FROM tasks_with_answers WHERE test_name=?", [(old_name)])
        conn.commit()
        cursor.execute("DELETE  FROM variants WHERE test_name=?", [(old_name)])
        conn.commit()
        cursor.execute("DELETE  FROM tasks_with_questions WHERE test_name=?", [(old_name)])
        conn.commit()
        cursor.execute("DELETE FROM types WHERE test_name=?", [(old_name)])
        conn.commit()
        types = [(test_name, self.types[i]) for i in range(count_q)]
        cursor.executemany("INSERT INTO types(test_name, type) VALUES(?, ?);", types)

        tasks_with_answers = [(test_name, self.tasks[i], self.answers[i], self.errors[i])
                              for i in range(count_q) if self.types[i] == 1]
        cursor.executemany("INSERT INTO tasks_with_answers(test_name, task, answer, err) VALUES(?, ?, ?, ?);",
                           tasks_with_answers)
        conn.commit()
        tasks_with_variants = [(test_name, self.tasks[i], len(self.variants[i])) for i in range(count_q)
                               if self.types[i] == 0]
        cursor.executemany("INSERT INTO tasks_with_variants(test_name, task, count_variants) VALUES(?, ?, ?);",
                           tasks_with_variants)
        conn.commit()
        variants = []
        for i in range(count_q):
            if self.types[i] != 0:
                continue
            for j in range(len(self.variants[i])):
                variants.append((test_name, self.variants[i][j], self.flags[i][j]))
        cursor.executemany("INSERT INTO variants(test_name, variant, status) VALUES(?, ?, ?);", variants)
        conn.commit()
        tasks_with_questions = [(test_name, self.tasks[i],) for i in range(count_q) if self.types[i] == 2]
        cursor.executemany("INSERT INTO tasks_with_questions(test_name, task) VALUES(?, ?);", tasks_with_questions)
        conn.commit()
        App.clear_frame(self.master)
        self.destroy()

    def generate_constructor(self):
        tp = self.types[self.current - 1]
        if tp is not None:
            if tp == 0:
                count_vrs = len(self.variants[self.current - 1])
                txt = tk.Text(master=self.task_frame, font=base_font, wrap=tk.WORD, width=60, height=6)
                txt.insert(1.0, "Условие задания:\n\n" + self.tasks[self.current - 1])
                txt.grid(row=10, column=0, padx=(5, 0), pady=(10, 5), sticky="w", columnspan=2)
                fr = tk.Frame(master=self.task_frame, bg=light_green, highlightbackground=light_green,
                              highlightcolor=light_green, highlightthickness=3)
                fr.grid(row=11, column=0, sticky="w", columnspan=2)
                for i in range(count_vrs):
                    tx = tk.Text(master=fr, font=base_font, width=60, height=4)
                    tx.grid(row=i, column=0, padx=(5, 0), pady=(0, 5), sticky="w")
                    tx.insert(1.0, f"{i + 1}) " + self.variants[self.current - 1][i] + (
                        " +" if self.flags[self.current - 1][i] == 1 else " -"))
            elif tp == 1:
                txt = tk.Text(master=self.task_frame, font=base_font, wrap=tk.WORD, width=60, height=6)
                txt.insert(1.0, "Условие задания:\n\n" + self.tasks[self.current - 1])
                txt.grid(row=10, column=0, padx=(5, 0), pady=(10, 5), sticky="w", columnspan=2)

                fr = tk.Frame(master=self.task_frame, bg=light_green, highlightbackground=light_green,
                              highlightcolor=light_green, highlightthickness=3)
                fr.grid(row=11, column=0, sticky="w", columnspan=2)
                tx = tk.Text(master=fr, font=base_font, width=60, height=6)
                tx.grid(row=0, column=0, padx=(5, 0), pady=(0, 5), sticky="w")
                tx.insert(1.0, "Ответ: " + self.answers[self.current - 1])
                err_tx = tk.Text(master=fr, font=base_font, width=60, height=1)
                err_tx.grid(row=1, column=0, padx=(5, 0), pady=(0, 5), sticky="w")
                err_tx.insert(1.0, "Допустимая погрешность ответа в %: "+str(self.errors[self.current-1]))

            elif tp == 2:
                txt = tk.Text(master=self.task_frame, font=base_font, wrap=tk.WORD, width=60, height=6)
                txt.insert(1.0, "Условие задания:\n\n" + self.tasks[self.current - 1])
                txt.grid(row=10, column=0, padx=(5, 0), pady=(10, 5), sticky="w", columnspan=2)
        buttons_frame = tk.Frame(master=self.task_frame, highlightbackground=light_green,
                                 highlightcolor=light_green, highlightthickness=3)
        next_bt = tk.Button(master=buttons_frame, text="Вперед", font=base_font, command=self.go_next)
        previous_bt = tk.Button(master=buttons_frame, text="Назад", font=base_font, command=self.go_previous)
        next_bt.grid(row=0, column=1)
        previous_bt.grid(row=0, column=0)
        buttons_frame.grid(row=0, column=0, pady=(5, 20), padx=(5, 0), sticky="w")
        lb = tk.Label(master=self.task_frame, text=f"Вопрос №{self.current}", font=base_font)
        lb.grid(row=1, column=0, pady=(0, 10))
        save_bt = tk.Button(master=self.task_frame, text="Сохранить вопрос", command=self.save_task,
                            bg="light green", font=base_font)
        save_bt.grid(column=1, row=0, pady=(5, 20), padx=(0, 5), sticky="e")
        tk.Label(master=self.task_frame, text="Укажите тип задания", font=base_font).grid(row=2, column=0,
                                                                                          padx=(5, 0), sticky="w", )
        lbox = tk.Listbox(master=self.task_frame, width=50, height=3)
        lbox.grid(row=3, column=0, padx=(5, 0), pady=(0, 5))
        types = ["Задание с выбором правильных вариантов ответа", "Задание с числовым ответом",
                 "Задание с развёрнутым ответом"]
        for i in types:
            lbox.insert(tk.END, i)

        def make_variants(n):
            tk.Label(master=self.task_frame, text="Введите варианты ответа и укажите правильные", font=base_font).grid(
                row=8, column=0, padx=(5, 0), pady=(0, 5), sticky="w"
            )
            vr_frame = tk.Frame(master=self.task_frame, bg=light_green, highlightbackground=light_green,
                                highlightcolor=light_green, highlightthickness=3)
            vr_frame.grid(row=9, column=0, sticky="w")
            for i in range(n):
                tk.Label(text=f"{i + 1})", font=base_font, master=vr_frame, bg=light_green).grid(row=i, column=0,
                                                                                                 padx=(5, 0),
                                                                                                 pady=(5, 0),
                                                                                                 sticky="w")
                ent = tk.Text(master=vr_frame, width=30, height=2)
                ent.grid(row=i, column=1, sticky="w", padx=0, pady=(0, 5))
                self.current_variants_list.append(ent)
                var1 = tk.BooleanVar()
                var1.set(0)
                c1 = tk.Checkbutton(master=vr_frame, variable=var1, onvalue=1, offvalue=0, bg=light_green)
                c1.grid(row=i, column=2)
                self.current_flags_list.append(var1)

        def get_type():
            tp = lbox.curselection()[0]
            tk.Label(master=self.task_frame, font=base_font,
                     text="Напишите условие задания").grid(row=4, column=0, pady=(10, 5), padx=(5, 0), sticky="w")
            task_text = tk.Text(master=self.task_frame, wrap=tk.WORD, width=30, height=4)
            task_text.grid(row=5, column=0, pady=(0, 5), padx=(5, 0), sticky="w")
            self.current_task = task_text
            if tp == 0:
                self.current_type = 0
                tk.Label(master=self.task_frame, text="Число вариантов ответа", font=base_font).grid(
                    row=6, column=0, padx=(5, 0), pady=(10, 5), sticky="w")
                ent = tk.Entry(master=self.task_frame)
                ent.grid(row=7, column=0, padx=(5, 0), pady=(0, 5), sticky="w")
                bt = tk.Button(master=self.task_frame, text="Применить", font=base_font,
                               command=lambda: make_variants(int(ent.get())))
                bt.grid(row=6, column=1, padx=(0, 5), pady=(0, 5), sticky="e")
            elif tp == 1:
                self.current_type = 1
                tk.Label(master=self.task_frame,
                         text="Укажите правильный ответ,\nиспользуйте '.' в десятичных дробях",
                         font=base_font).grid(row=6, column=0, padx=(5, 0), pady=(10, 5), sticky="w")
                ent_ans = tk.Entry(master=self.task_frame)
                ent_ans.grid(row=7, column=0, padx=(5, 0), pady=(0, 5), sticky="w")
                self.current_answer = ent_ans
                tk.Label(master=self.task_frame, text="Задайте допустимую погрешность ответа (в %)",
                         font=base_font).grid(row=8, column=0, padx=(5, 0), pady=(10, 5), sticky="w")
                ent_err = tk.Entry(master=self.task_frame)
                ent_err.grid(row=9, column=0, padx=(5, 0), pady=(0, 5), sticky="w")
                self.current_err = ent_err
            elif tp == 2:
                self.current_type = 2

        tk.Button(master=self.task_frame, text="Применить", font=base_font, command=get_type).grid(
            row=2, column=1, padx=(0, 5), pady=(0, 5), sticky="e")
        self.task_frame.grid(row=1, column=2, columnspan=2)



    def save_task(self):
        if self.current_type == 0:

            self.types[self.current-1] = 0
            self.tasks[self.current-1] = self.current_task.get(1.0, tk.END)
            vrs = [self.current_variants_list[i].get(1.0, tk.END)
                             for i in range(len(self.current_variants_list))]
            self.variants[self.current-1] = vrs
            fgs = [int(self.current_flags_list[i].get()) for i in range(len(self.current_flags_list))]
            self.flags[self.current-1] = fgs
        elif self.current_type == 1:
            self.types[self.current-1] = 1
            self.tasks[self.current-1] = self.current_task.get(1.0, tk.END)
            self.answers[self.current-1] = self.current_answer.get()
            self.errors[self.current-1] = int(self.current_err.get())
        elif self.current_type == 2:
            self.types[self.current-1] = 2
            self.tasks[self.current-1] = self.current_task.get(1.0, tk.END)

    def go_next(self):
        if self.current == int(self.count_text.get(1.0, tk.END)):
            pass
        else:
            self.current += 1
            App.clear_frame(self.task_frame)

            self.current_type = None
            self.current_task = ""
            self.current_flags_list = []
            self.current_variants_list = []
            self.current_answer = ""
            self.current_err = 0

            self.generate_constructor()

    def go_previous(self):
        if self.current == 1:
            pass
        else:
            self.current -= 1
            App.clear_frame(self.task_frame)

            self.current_type = None
            self.current_task = ""
            self.current_flags_list = []
            self.current_variants_list = []
            self.current_answer = ""
            self.current_err = 0

            self.generate_constructor()


class newTest(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.master = master
        self.name_text = tk.Text(master=self, width=30, height=4, wrap=tk.WORD)
        self.count_text = tk.Text(master=self, width=10, height=1)
        self.task_frame = tk.Frame(master=self, bg=light_green, highlightbackground="green", highlightcolor="green",
                                   highlightthickness=3)


        self.current_type = None

        self.current_task = ""

        self.current_flags_list = []
        self.current_variants_list = []

        self.current_answer = ""
        self.current_err = 0

        self.types = [None for i in range(100)]
        self.tasks = [None for i in range(100)]

        self.variants = [None for i in range(100)]
        self.flags = [None for i in range(100)]

        self.answers = [None for i in range(100)]
        self.errors = [None for i in range(100)]

        self.current = 1
        self.grid()
        self.initUI()

    def initUI(self):
        tk.Label(text="Название работы", master=self,font=base_font).grid(row=0, column=0, padx=10, pady=10, sticky="n")
        self.name_text.grid(row=0, column=1, padx=10, pady=10, sticky="n")
        tk.Label(text="Количество вопросов\n(не больше 100)", master=self,font=base_font).grid(row=0, column=2, padx=10, pady=10, sticky="n")
        self.count_text.grid(row=0, column=3, padx=10, pady=10, sticky="n")
        tk.Button(text="Применить", master=self, command=self.generate_constructor,font=base_font).grid(row=0, column=4,
                                                                                                padx=10, pady=10,
                                                                                         sticky="n")
        tk.Button(text="Сохранить работу", bg="light green", master=self,font=base_font, command=self.save_test).grid(row=0, column=5,
                                                                                      padx=10, pady=10, sticky="n")

    def save_task(self):
        if self.current_type == 0:

            self.types[self.current-1] = 0
            self.tasks[self.current-1] = self.current_task.get(1.0, tk.END)
            vrs = [self.current_variants_list[i].get(1.0, tk.END)
                             for i in range(len(self.current_variants_list))]
            self.variants[self.current-1] = vrs
            fgs = [int(self.current_flags_list[i].get()) for i in range(len(self.current_flags_list))]
            self.flags[self.current-1] = fgs
        elif self.current_type == 1:
            self.types[self.current-1] = 1
            self.tasks[self.current-1] = self.current_task.get(1.0, tk.END)
            self.answers[self.current-1] = self.current_answer.get()
            self.errors[self.current-1] = int(self.current_err.get())
        elif self.current_type == 2:
            self.types[self.current-1] = 2
            self.tasks[self.current-1] = self.current_task.get(1.0, tk.END)



    def save_test(self):
        answer = mb.askokcancel(title="Сохранение", message="Сохранить работу? Нажмите OK, если уверены, "
                                        "что все задания заполнены полностью и верно")
        if answer:
            count_q = int(self.count_text.get(1.0, tk.END))
            if "tests.db" not in os.listdir():
                conn = sqlite3.connect("tests.db")
                cursor = conn.cursor()
                cursor.execute("""CREATE TABLE tests
                                              (id integer, test_name text, count_q integer)
                                           """)
                cursor.execute("""CREATE TABLE types (id integer primary key, test_name text, type integer)""")
                cursor.execute("""CREATE TABLE tasks_with_answers
                                              (id integer primary key, test_name text, task text, answer text, err real)
                                           """)
                cursor.execute("""CREATE TABLE tasks_with_variants
                                              (id integer primary key, test_name text, task text, count_variants integer)""")
                cursor.execute("""CREATE TABLE variants (id integer primary key, test_name text, variant text, status integer)""")
                cursor.execute("""CREATE TABLE tasks_with_questions (id integer primary key, test_name text, task text)""")
            conn = sqlite3.connect("tests.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tests;")
            if len(cursor.fetchall()) == 0:
                count_of_tests = 0
            else:
                cursor.execute("select count(*) from tests")
                count_of_tests = cursor.fetchone()[0]
            test_name = str(count_of_tests+1)+") "+self.name_text.get(1.0, tk.END)
            test_name = re.sub(r'[\n]', "", test_name)

            cursor.execute("INSERT INTO tests(id, test_name, count_q) VALUES(?, ?, ?);",
                           (count_of_tests+1, test_name, count_q))
            conn.commit()

            types = [(test_name, self.types[i]) for i in range(count_q)]
            cursor.executemany("INSERT INTO types(test_name, type) VALUES(?, ?);", types)


            tasks_with_answers = [(test_name, self.tasks[i], self.answers[i], self.errors[i])
                                  for i in range(count_q) if self.types[i] == 1]
            cursor.executemany("INSERT INTO tasks_with_answers(test_name, task, answer, err) VALUES(?, ?, ?, ?);", tasks_with_answers)
            conn.commit()
            tasks_with_variants = [(test_name, self.tasks[i], len(self.variants[i])) for i in range(count_q)
                                   if self.types[i] == 0]
            cursor.executemany("INSERT INTO tasks_with_variants(test_name, task, count_variants) VALUES(?, ?, ?);", tasks_with_variants)
            conn.commit()
            variants = []
            for i in range(count_q):
                if self.types[i] != 0:
                    continue
                for j in range(len(self.variants[i])):
                    variants.append((test_name, self.variants[i][j], self.flags[i][j]))
            cursor.executemany("INSERT INTO variants(test_name, variant, status) VALUES(?, ?, ?);", variants)
            conn.commit()
            tasks_with_questions = [(test_name, self.tasks[i], ) for i in range(count_q) if self.types[i] == 2]
            cursor.executemany("INSERT INTO tasks_with_questions(test_name, task) VALUES(?, ?);", tasks_with_questions)
            conn.commit()
            App.clear_frame(self.master)
            self.destroy()



    def go_next(self):
        if self.current == int(self.count_text.get(1.0, tk.END)):
            pass
        else:
            self.current += 1
            App.clear_frame(self.task_frame)

            self.current_type = None
            self.current_task = ""
            self.current_flags_list = []
            self.current_variants_list = []
            self.current_answer = ""
            self.current_err = 0

            self.generate_constructor()

    def go_previous(self):
        if self.current == 1:
            pass
        else:
            self.current -= 1
            App.clear_frame(self.task_frame)

            self.current_type = None
            self.current_task = ""
            self.current_flags_list = []
            self.current_variants_list = []
            self.current_answer = ""
            self.current_err = 0

            self.generate_constructor()

    def generate_constructor(self):
        tp = self.types[self.current-1]
        if tp is not None:
            if tp == 0:
                count_vrs = len(self.variants[self.current-1])
                txt = tk.Text(master=self.task_frame, font=base_font, wrap=tk.WORD, width=60, height=6)
                txt.insert(1.0, "Условие задания:\n\n"+self.tasks[self.current-1])
                txt.grid(row=10, column=0, padx=(5, 0), pady=(10, 5), sticky="w", columnspan=2)
                fr = tk.Frame(master=self.task_frame, bg=light_green, highlightbackground=light_green,
                              highlightcolor=light_green, highlightthickness=3)
                fr.grid(row=11, column=0, sticky="w", columnspan=2)
                for i in range(count_vrs):
                    tx = tk.Text(master=fr, font=base_font, width=60, height=4)
                    tx.grid(row=i, column=0, padx=(5, 0), pady=(0, 5), sticky="w")
                    tx.insert(1.0,  f"{i+1}) "+self.variants[self.current-1][i]+(" +" if self.flags[self.current-1][i] == 1 else " -"))
            elif tp == 1:
                txt = tk.Text(master=self.task_frame, font=base_font, wrap=tk.WORD, width=60, height=6)
                txt.insert(1.0, "Условие задания:\n\n" + self.tasks[self.current - 1])
                txt.grid(row=10, column=0, padx=(5, 0), pady=(10, 5), sticky="w", columnspan=2)

                fr = tk.Frame(master=self.task_frame, bg=light_green, highlightbackground=light_green,
                              highlightcolor=light_green, highlightthickness=3)
                fr.grid(row=11, column=0, sticky="w", columnspan=2)
                tx = tk.Text(master=fr, font=base_font, width=60, height=6)
                tx.grid(row=0, column=0, padx=(5, 0), pady=(0, 5), sticky="w")
                tx.insert(1.0, "Ответ: "+self.answers[self.current-1])
                err_tx = tk.Text(master=fr, font=base_font, width=60, height=1)
                err_tx.grid(row=1, column=0, padx=(5, 0), pady=(0, 5), sticky="w")
                err_tx.insert(1.0, "Допустимая погрешность ответа в %: " + str(self.errors[self.current - 1]))

            elif tp == 2:
                txt = tk.Text(master=self.task_frame, font=base_font, wrap=tk.WORD, width=60, height=6)
                txt.insert(1.0, "Условие задания:\n\n" + self.tasks[self.current - 1])
                txt.grid(row=10, column=0, padx=(5, 0), pady=(10, 5), sticky="w", columnspan=2)
        buttons_frame = tk.Frame(master=self.task_frame, highlightbackground=light_green, highlightcolor=light_green,
                                 highlightthickness=3)
        next_bt = tk.Button(master=buttons_frame, text="Вперед",font=base_font, command=self.go_next)
        previous_bt = tk.Button(master=buttons_frame, text="Назад",font=base_font, command=self.go_previous)
        next_bt.grid(row=0, column=1)
        previous_bt.grid(row=0, column=0)
        buttons_frame.grid(row=0, column=0, pady=(5, 20), padx=(5, 0), sticky="w")
        lb = tk.Label(master=self.task_frame, text=f"Вопрос №{self.current}", font=base_font)
        lb.grid(row=1, column=0, pady=(0, 10))
        save_bt = tk.Button(master=self.task_frame, text="Сохранить вопрос", command=self.save_task,
                            bg="light green", font=base_font)
        save_bt.grid(column=1, row=0, pady=(5, 20), padx=(0, 5), sticky="e")
        tk.Label(master=self.task_frame, text="Укажите тип задания", font=base_font).grid(row=2, column=0,
                                                                                     padx=(5, 0), sticky="w",)
        lbox = tk.Listbox(master=self.task_frame, width=50, height=3)
        lbox.grid(row=3, column=0, padx=(5, 0), pady=(0, 5))
        types = ["Задание с выбором правильных вариантов ответа", "Задание с числовым ответом",
                 "Задание с развёрнутым ответом"]
        for i in types:
            lbox.insert(tk.END, i)

        def make_variants(n):
            tk.Label(master=self.task_frame, text="Введите варианты ответа и укажите правильные", font=base_font).grid(
                row=8, column=0, padx=(5, 0), pady=(0, 5), sticky="w"
            )
            vr_frame = tk.Frame(master=self.task_frame, bg=light_green, highlightbackground=light_green,
                                highlightcolor=light_green, highlightthickness=3)
            vr_frame.grid(row=9, column=0, sticky="w")
            for i in range(n):
                tk.Label(text=f"{i+1})", font=base_font, master=vr_frame, bg=light_green).grid(row=i, column=0, padx=(5, 0),
                                                                               pady=(5, 0), sticky="w")
                ent = tk.Text(master=vr_frame, width=30, height=2)
                ent.grid(row=i, column=1, sticky="w", padx=0, pady=(0, 5))
                self.current_variants_list.append(ent)
                var1 = tk.BooleanVar()
                var1.set(0)
                c1 = tk.Checkbutton(master=vr_frame, variable=var1, onvalue=1, offvalue=0, bg=light_green)
                c1.grid(row=i, column=2)
                self.current_flags_list.append(var1)

        def get_type():
            tp = lbox.curselection()[0]
            tk.Label(master=self.task_frame, font=base_font,
                     text="Напишите условие задания").grid(row=4, column=0, pady=(10, 5), padx=(5, 0), sticky="w")
            task_text = tk.Text(master=self.task_frame, wrap=tk.WORD, width=30, height=4)
            task_text.grid(row=5, column=0, pady=(0, 5), padx=(5, 0), sticky="w")
            self.current_task = task_text
            if tp == 0:
                self.current_type = 0
                tk.Label(master=self.task_frame, text="Число вариантов ответа", font=base_font).grid(
                    row=6, column=0, padx=(5, 0), pady=(10, 5), sticky="w")
                ent = tk.Entry(master=self.task_frame)
                ent.grid(row=7, column=0, padx=(5, 0), pady=(0, 5), sticky="w")
                bt = tk.Button(master=self.task_frame, text="Применить", font=base_font,
                          command=lambda : make_variants(int(ent.get())))
                bt.grid(row=6, column=1, padx=(0, 5), pady=(0, 5), sticky="e")
            elif tp == 1:
                self.current_type = 1
                tk.Label(master=self.task_frame,
                         text="Укажите правильный ответ,\nиспользуйте '.' в десятичных дробях",
                         font=base_font).grid(row=6, column=0, padx=(5, 0), pady=(10, 5), sticky="w")
                ent_ans = tk.Entry(master=self.task_frame)
                ent_ans.grid(row=7, column=0, padx=(5, 0), pady=(0, 5), sticky="w")
                self.current_answer = ent_ans
                tk.Label(master=self.task_frame, text="Задайте допустимую погрешность ответа (в %)",
                         font=base_font).grid(row=8, column=0, padx=(5, 0), pady=(10,5), sticky="w")
                ent_err = tk.Entry(master=self.task_frame)
                ent_err.grid(row=9, column=0, padx=(5, 0), pady=(0, 5), sticky="w")
                self.current_err = ent_err
            elif tp == 2:
                self.current_type = 2
        tk.Button(master=self.task_frame, text="Применить", font=base_font, command=get_type).grid(
            row=2, column=1, padx=(0, 5), pady=(0, 5), sticky="e")
        self.task_frame.grid(row=1, column=2, columnspan=2)



class classList(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.initUI()

    def initUI(self):
        if "classes.db" not in os.listdir():
            tk.Label(master=self,
                     text="Список классов пуст.\n Добавьте класс в разделе 'Добавить новый'",
                     font=('Arial', 25)).grid(row=0, column=3, padx=10, pady=10)
        else:
            conn = sqlite3.connect("classes.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM classes;")
            classes = cursor.fetchall()
            classes = sorted(classes, key=lambda clas: [int(clas[0][:-1]), clas[0][-1]])
            count_classes = len(classes)
            listFrame = tk.Frame(master=self,)
            listFrame.grid()
            def find_ending(cnt):
                if cnt % 10 == 1:
                    return "ученик"
                elif (cnt % 10 >= 5 and cnt % 10 <= 9) or (cnt % 10 == 0):
                    return "учеников"
                else:
                    return "ученика"
            for i in range(count_classes):
                bt = tk.Button(master=listFrame, font=base_font, text=classes[i][0], bg="white", width=30)
                bt.grid(row=i, column=0, sticky="w")
                bt.bind("<Button-1>", self.showClas)
                tk.Label(master=listFrame, font=base_font, text=f"{classes[i][1]} {find_ending(classes[i][1])}").grid(
                    row=i, column=1, sticky="w", padx=(5, 0)
                )

    def showClas(self, event):
        class_name = event.widget.cget("text")
        App.clear_frame(self.master)
        clas = Clas(self.master, class_name)
        self.destroy()








class Clas(tk.Frame):
    def __init__(self, master, class_name):
        super().__init__(master)
        self.master = master
        self.class_name = class_name
        self.fr = tk.Frame(master=self.master)
        self.fr.grid(columnspan=4, row=2)
        self.count_entry = tk.Text(master=self.master, font=base_font, width=30, height=1)
        self.name_entry = tk.Text(master=self.master, font=base_font, width=30, height=1)
        self.current_count = 0
        self.names = []
        self.emails = []
        self.grid()
        self.initUI()

    def copy_to_clipboard(self, lst):
        l = [lst[i].get(1.0, tk.END) for i in range(len(lst))]
        l = sorted(l)
        r = tk.Tk()
        r.withdraw()
        r.clipboard_clear()
        r.clipboard_append("".join(l))
        r.update()

    def initUI(self):
        conn = sqlite3.connect("classes.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM classes WHERE name=?;", [self.class_name])
        count = cursor.fetchone()[1]
        cursor.execute("SELECT * FROM students WHERE class=?;", [self.class_name])
        students = cursor.fetchall()
        tk.Label(master=self.master, text="Количество учеников", font=base_font).grid(row=0, column=0, padx=10, pady=10)
        self.count_entry.insert(1.0, count)
        self.count_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        count_button = tk.Button(master=self.master, text="Применить", command=self.generate_table, font=base_font)
        count_button.grid(row=0, column=2, padx=10, pady=10, sticky="w")
        tk.Label(master=self.master, text="Имя класса", font=base_font).grid(row=0, column=3, padx=10, pady=10)
        self.name_entry.insert(1.0, self.class_name)
        self.name_entry.grid(row=0, column=4, padx=10, pady=10, sticky="w")
        save_button = tk.Button(master=self.master, text="Сохранить класс", bg="light green", command=self.load_list,
                                font=base_font)
        save_button.grid(row=0, column=5, padx=10, pady=10, sticky="w")
        tk.Label(master=self.master, text="ФИО ученика", font=base_font).grid(row=1, column=0)

        tk.Label(master=self.master, text="Email ученика", font=base_font).grid(row=1, column=2)

        students = sorted(students, key=lambda student: student[1])
        for i in range(count):
            name_text = tk.Text(master=self.fr, height=1, width=45, font=base_font)
            name_text.insert(1.0, students[i][1])
            name_text.grid(row=i, column=0, columnspan=2, sticky="ew", padx=(5, 0))
            email_text = tk.Text(master=self.fr, height=1, width=45, font=base_font)
            email_text.insert(1.0, students[i][2])
            email_text.grid(row=i, column=2, columnspan=2, sticky="ew", padx=(5, 0))
            self.names.insert(0, name_text)
            self.emails.insert(0, email_text)
        self.current_count = count
        tk.Button(master=self.master, text="Копировать ФИО", font=base_font,
                  command=lambda: self.copy_to_clipboard(self.names)).grid(
                  row=1, column=1, pady=(0, 10), sticky="w")
        tk.Button(master=self.master, text="Копировать адреса", font=base_font,
                  command=lambda: self.copy_to_clipboard(self.emails)).grid(
                  row=1, column=3, pady=(0, 10), sticky="w")

    def generate_table(self):
        count = int(self.count_entry.get(1.0, tk.END))
        if count > self.current_count:
            for i in range(count - self.current_count):
                name_text = tk.Text(master=self.fr, height=1, width=45, font=base_font)
                name_text.grid(row=self.current_count + i, column=0, columnspan=2, sticky="ew", padx=(5, 0))
                email_text = tk.Text(master=self.fr, height=1, width=45, font=base_font)
                email_text.grid(row=self.current_count + i, column=2, columnspan=2, sticky="ew", padx=(5, 0))
                self.names.insert(0, name_text)
                self.emails.insert(0, email_text)

            self.current_count = count
        elif count < self.current_count:
            for i in range(self.current_count - count):
                self.names[0].destroy()
                self.emails[0].destroy()
                self.names.pop(0)
                self.emails.pop(0)
            self.current_count = count


    def load_list(self):
        answer = mb.askokcancel(title="Сохранение", message="Сохранить класс? Нажмите OK, если уверены, "
                                                            "что все данные заполнены полностью и верно")
        if answer:
            conn = sqlite3.connect("classes.db")
            cursor = conn.cursor()
            class_name = self.name_entry.get(1.0, tk.END)
            class_name = re.sub(r"[\n]", "", class_name)
            count = int(self.count_entry.get(1.0, tk.END))
            cursor.execute("UPDATE classes SET name=? WHERE name=?;", (class_name, self.class_name))
            conn.commit()
            cursor.execute("UPDATE classes SET count=? WHERE name=?;", (count, class_name))
            conn.commit()
            cursor.execute("SELECT * FROM classes")

            cursor.execute("DELETE FROM students WHERE class=?", [(self.class_name)])
            conn.commit()
            st_data = [(class_name, re.sub(r"[\n]", "", self.names[i].get(1.0, tk.END)),
                        re.sub(r"[\n]", "", self.emails[i].get(1.0, tk.END))) for i in range(count)]
            cursor.executemany("INSERT INTO students VALUES (?,?,?)", st_data)
            conn.commit()

            App.clear_frame(self.master)
            self.destroy()






class newClass(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.fr = tk.Frame(master=self.master)
        self.fr.grid(columnspan=4, row=2)
        self.count_entry = tk.Text(master=self.master, width=30, height=1)
        self.name_entry = tk.Text(master=self.master, width=30, height=1)
        self.current_count = 0
        self.names = []
        self.emails = []
        self.grid()
        self.initUI()

    def generate_table(self):
        count = int(self.count_entry.get(1.0, tk.END))
        if count > self.current_count:
            for i in range(count-self.current_count):
                name_text = tk.Text(master=self.fr, height=1, width=40, font=base_font)
                name_text.grid(row=self.current_count+i, column=0, columnspan=2, sticky="ew", padx=(5, 0))
                email_text = tk.Text(master=self.fr, height=1, width=40, font=base_font)
                email_text.grid(row=self.current_count+i, column=2, columnspan=2, sticky="ew", padx=(5, 0))
                self.names.insert(0, name_text)
                self.emails.insert(0, email_text)

            self.current_count = count
        elif count < self.current_count:
            for i in range(self.current_count-count):
                self.names[0].destroy()
                self.emails[0].destroy()
                self.names.pop(0)
                self.emails.pop(0)
            self.current_count = count


    def load_list(self):
        conn = sqlite3.connect("classes.db")
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS classes
                                      (name text, count integer)
                                   """)
        cursor.execute("""CREATE TABLE IF NOT EXISTS students
                                      (class text, name text, email text)
                                   """)
        st_data = [(re.sub(r"[\n]", "", self.name_entry.get(1.0, tk.END)),
                          re.sub(r"[\n]", "", self.names[i].get(1.0, tk.END)),
                          re.sub(r"[\n]", "", self.emails[i].get(1.0, tk.END))) for i in range(len(self.names))]
        cl_data = [(re.sub(r"[\n]", "", self.name_entry.get(1.0, tk.END)), len(self.names))]

        cursor.executemany("INSERT INTO students VALUES (?,?,?)", st_data)
        cursor.executemany("INSERT INTO classes VALUES (?,?)", cl_data)
        conn.commit()
        App.clear_frame(self.master)
        self.destroy()


    def initUI(self):
        tk.Label(master=self.master, text="Количество учеников",font=base_font).grid(row=0, column=0, padx=10, pady=10)
        self.count_entry.grid(row=0, column=1, padx=10, pady=10)
        count_button = tk.Button(master=self.master, text="Применить", command=self.generate_table,font=base_font)
        count_button.grid(row=0, column=2, padx=10, pady=10)
        tk.Label(master=self.master, text="Имя класса",font=base_font).grid(row=0, column=3, padx=10, pady=10)
        self.name_entry.grid(row=0, column=4, padx=10, pady=10)
        save_button = tk.Button(master=self.master, text="Сохранить класс", bg="light green", command=self.load_list,font=base_font)
        save_button.grid(row=0, column=5, padx=10, pady=10)
        tk.Label(master=self.master, text="ФИО ученика", font=base_font).grid(row=1, column=0)
        tk.Label(master=self.master, text="Email ученика", font=base_font).grid(row=1, column=2)

class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self, width=1100, height=800)
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
    root.geometry("1200x800")

    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
