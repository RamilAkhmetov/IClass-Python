import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import filedialog as fl
import os
import shutil
import sqlite3
import pathlib
import re

import base64

light_green = "#C4F4CE"
light_yellow = "#F5EBCF"
base_font = ("Arial", 10)


class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.Scrollable_frame = ScrollableFrame(master)
        self.frame = self.Scrollable_frame.scrollable_frame
        self.frame.grid(sticky="news")
        self.Scrollable_frame.pack()
        self.master = master
        self.initUI()

    def initUI(self):
        self.master.title("iClass")
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)
        studentsInfo = tk.Menu(menubar)
        studentsInfo.add_command(label="Личные данные", command=self.showProfile)
        menubar.add_cascade(label="Мой профиль", menu=studentsInfo)
        classesMenu = tk.Menu(menubar)
        classesMenu.add_command(label="Загрузить новую", command=self.downloadNewTest)
        classesMenu.add_command(label="Новые работы", command=self.showTests)
        classesMenu.add_command(label="Пройденные работы", command=self.showResults)
        menubar.add_cascade(label="Проверочные работы", menu=classesMenu)
        manualMenu = tk.Menu(menubar)
        manualMenu.add_command(label="Показать", command=self.showManual)
        menubar.add_cascade(label="Руководство пользователя", menu=manualMenu)

    @staticmethod
    def clear_frame(frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def showProfile(self):
        App.clear_frame(self.frame)
        profile = Profile(self.frame)

    def showTests(self):
        App.clear_frame(self.frame)
        tests = TestsList(self.frame)

    def showResults(self):
        App.clear_frame(self.frame)
        results = Results(self.frame)

    def downloadNewTest(self):
        App.clear_frame(self.frame)
        dowloader = TestLoader(self.frame)

    def showManual(self):
        pass


class Profile(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.fio = None
        self.clas = None

        self.grid(sticky="nsew")
        self.initUI()

    def initUI(self):
        if "Мои данные.txt" in os.listdir():
            file = open("Мои данные.txt")
            fio, klas = file.readlines()
            file.close()
        else:
            fio = ""
            klas = ""

        fr = tk.Frame(master=self, highlightbackground=light_green,
                      highlightthickness=3, highlightcolor=light_green, bg=light_yellow)
        fr.grid(sticky="news", pady=(200, 10))
        tk.Label(master=fr, text="Мои данные", font=base_font, bg=light_yellow).grid(row=0, column=0, padx=(10, 0),
                                                                                pady=(10, 0), sticky="w")
        save_bt = tk.Button(master=fr, font=base_font, text="Сохранить", bg="light green")
        save_bt.config(command=self.save)
        save_bt.grid(row=0, column=1, sticky="e", padx=(200, 10), pady=(10, 0))
        tk.Label(master=fr, text="ФИО", font=base_font, bg=light_yellow).grid(row=1, column=0, padx=(10, 0),
                                                                         pady=(30, 0), sticky="w")
        self.fio = tk.Text(master=fr, font=base_font, relief=tk.RAISED, width=50, height=1)
        self.fio.insert(1.0, fio)
        self.fio.grid(row=1, column=1, padx=(200, 10), sticky="e", pady=(30, 0))
        tk.Label(master=fr, font=base_font, bg=light_yellow, text="Класс").grid(row=2, column=0, padx=(10, 0),
                                                                                pady=(30, 10), sticky="w")
        self.clas = tk.Text(master=fr, font=base_font, relief=tk.RAISED, width=10, height=1)
        self.clas.insert(1.0, klas)
        self.clas.grid(row=2, column=1, padx=(200, 10), sticky="e", pady=(30, 10))

    def save(self):
        fio = self.fio.get(1.0, tk.END)
        klas = self.clas.get(1.0, tk.END)
        klas = klas.upper()
        fio = re.sub(r"[\n]", "", fio)
        klas = re.sub(r"[\n]", "", klas)
        file = open("Мои данные.txt", "w")
        file.writelines([fio+"\n", klas])
        file.close()


class TestLoader(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.initUI()

    def initUI(self):
        file_path = fl.askopenfilename()
        if "My tests" not in os.listdir():
            os.makedirs("My tests")
        if file_path in os.listdir("My tests"):
            pass
        else:
            file_name = list(file_path.split(sep="/"))[-1]
            if file_name != "":
                file = open(f"My tests/{file_name}", "w+")
                file.close()
                shutil.copyfile(file_path, f"My tests/{file_name}")
        App.clear_frame(self.master)
        self.destroy()


class TestsList(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.names = []


        self.grid()
        self.initUI()

    def initUI(self):
        if "My tests" not in os.listdir():
            os.makedirs("My tests")
        if len(os.listdir("My tests")) == 0:
            tk.Label(master=self,
                     text="Список работ пуст.\n Добавьте проверочную работу \n в разделе 'Загрузить новую работу'",
                     font=('Arial', 25)).pack(padx=10, pady=10)
        else:
            tests = os.listdir("My tests")

            tests = [tests[i].split(".")[0] for i in range(len(tests))]
            tests_count = len(tests)
            results = os.listdir("Results")
            results = [results[i].split("(")[0] for i in range(len(results))]

            unfinished_tests_count = len(tests)

            names = []
            for i in range(tests_count):

                if tests[i] in results:
                    unfinished_tests_count -= 1
                    continue

                names.append(tests[i])
            if unfinished_tests_count == 0:
                tk.Label(master=self,
                         text="Новых работ нет",
                         font=('Arial', 25)).pack(padx=10, pady=10)
            for i in range(unfinished_tests_count):
                row = tk.Frame(master=self, bg="white", highlightbackground=light_green, highlightthickness=3,
                                  highlightcolor=light_green)
                row.grid(sticky="ew")
                lb = tk.Label(master=row, font=base_font, text=names[i], bg="white", wraplength=600)
                self.names.append(lb['text'])
                lb.pack(side=tk.LEFT, padx=(20, 0), fill=tk.X)
                bt = tk.Button(master=row, font=base_font, text="Начать")
                bt.configure(command=lambda button=bt: self.startTest(button.master))
                bt.pack(side=tk.RIGHT, padx=(200, 0), fill=tk.X)

    def startTest(self, master):
        if "Мои данные.txt" not in os.listdir():
            err = mb.showerror(title="Ошибка", message="Личные данные не заполенены. "
                                                       "Введите их в разделе 'Мой профиль'->'Личные данные'")
            return
        gi = master.grid_info()['row']
        name = self.names[gi]
        name = re.sub(r'["]', '', name)
        App.clear_frame(self.master)
        test = Test(self.master, name)


class Results(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.names = []
        self.grid()
        self.initUI()

    def initUI(self):
        if "Results" not in os.listdir():
            os.makedirs("Results")
        if len(os.listdir("Results")) == 0:
            tk.Label(master=self,
                     text="Список пройденных работ пуст",
                     font=('Arial', 25)).pack(padx=10, pady=10)

        else:
            results = os.listdir("Results")
            results = [results[i].split(".")[0] for i in range(len(results))]

            count = len(results)
            for i in range(count):
                row = tk.Frame(master=self, bg="white", highlightbackground=light_green, highlightthickness=3,
                               highlightcolor=light_green)
                row.grid(sticky="ew")
                lb = tk.Label(master=row, font=base_font, text=results[i].split(sep="(")[0], bg="white", wraplength=300)
                self.names.append(lb['text'])
                lb.pack(side=tk.LEFT, padx=(20, 0), fill=tk.X)
                bt = tk.Button(master=row, font=base_font, text="Показать результат")
                bt.configure(command=lambda button=bt: self.showResult(button.master))
                bt.pack(side=tk.RIGHT, padx=(600, 0), fill=tk.X)

    def showResult(self, master):
        gi = master.grid_info()['row']
        name = self.names[gi]
        name = re.sub(r'["]', '', name)
        App.clear_frame(self.master)
        result = Result(self.master, name)
        self.destroy()


class Result(tk.Frame):
    def __init__(self, master, name):
        super().__init__(master)
        self.master = master
        self.name = name
        self.task_frame = tk.Frame(master=self, bg=light_green, highlightbackground="green", highlightcolor="green",
                                   highlightthickness=3)
        self.grid()
        self.initUI()


    def initUI(self):

        with open(f"Results/{self.name}.txt", "r") as file:
            data = file.read()
        data = data.split(sep="\n")[:-1]
        count = int(data[2])

        tk.Label(master=self, text="Работа по теме", font=base_font).grid(row=0, column=0, padx=(30, 0), sticky="n")
        tk.Label(master=self, text=self.name, font=base_font, bg="white", wraplength=400).grid(row=0, column=1, padx=(10, 0),
                                                                               sticky="n")
        tk.Label(master=self, text="Количество вопросов", font=base_font).grid(row=0, column=2, padx=(200, 0),
                                                                               sticky="n")
        tk.Label(master=self, text=str(count), font=base_font, bg="white").grid(row=0, column=3, padx=(10, 0),
                                                                                       sticky="n")
        self.task_frame.grid(row=1, column=1, columnspan=2, pady=(100, 0), sticky="ew")
        for i in range(count):
            fr = tk.Frame(master=self.task_frame, bg=light_green)
            fr.grid(row=i, column=0, columnspan=3)
            l = tk.Label(master=fr, text=f"Вопрос №{i + 1}", font=base_font, bg=light_green)
            l.grid(
                row=0, column=0, pady=(5, 0), padx=(5, 30), sticky="w")
            line = data[i+3]
            if line[0] == '0':
                points, maxs = line[2:].split(sep="=")[1].split(sep="_")
                tk.Label(master=fr, text=f"Ваш результат: {points} из {maxs}", font=base_font, bg="white").grid(
                    row=0, column=1, pady=(5, 0), padx=(5, 0), sticky="w")
            elif line[0] == '1':
                tk.Label(master=fr, text="Ваш ответ:", font=base_font, bg=light_green).grid(
                    row=0, column=1, pady=(5, 0), padx=(5, 0), sticky="w")
                tk.Label(master=fr, text=line.split(sep=":")[1], font=base_font, bg="white"
                         ).grid(row=0, column=2, padx=(5, 0), pady=(5, 0), sticky="w")
            else:
                tk.Label(master=fr, text="Ваш ответ:", font=base_font, bg=light_green).grid(
                    row=0, column=1, pady=(5, 0), padx=(5, 0), sticky="w")
                tk.Label(master=fr, text=line.split(sep=":")[1], font=base_font, bg="white"
                         ).grid(row=0, column=2, padx=(5, 0), pady=(5, 0), sticky="w")











class Test(tk.Frame):
    def __init__(self, master, name):
        super().__init__(master)
        self.master = master
        self.name = name
        self.task_frame = tk.Frame(master=self, bg=light_green, highlightbackground="green", highlightcolor="green",
                                   highlightthickness=3)
        self.count_q = 0
        self.current = 1
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
        self.current_ans = ""

        self.results = [None for i in range(1000)]

        self.types = [None for i in range(1000)]
        self.tasks = [None for i in range(1000)]

        self.variants = [None for i in range(1000)]
        self.flags = [None for i in range(1000)]

        self.answers = [None for i in range(1000)]
        self.errors = [None for i in range(1000)]

        self.grid()
        self.initUI()

    def initUI(self):
        conn = sqlite3.connect("My tests/"+self.name+".db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM count_q")
        self.count_q = cursor.fetchone()[0]
        cursor.execute("SELECT * FROM name")
        name = cursor.fetchone()[0]
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
        for i in range(self.count_q):
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

        tk.Label(master=self, text="Работа по теме", font=base_font).grid(row=0, column=0, padx=(30, 0), sticky="n")
        tk.Label(master=self, text=name, font=base_font, bg="white", wraplength=400).grid(
            row=0, column=1, padx=(10, 0), sticky="n")
        tk.Label(master=self, text="Количество вопросов", font=base_font).grid(row=0, column=2, padx=(30, 0), sticky="n")
        tk.Label(master=self, text=str(self.count_q), font=base_font, bg="white").grid(row=0, column=3, padx=(10, 0), sticky="n")
        tk.Button(master=self, text="Закончить работу", bg="light green", command=lambda: self.save_result()).grid(
            row=0, column=4, padx=(30, 0), sticky="n"
        )
        self.generate_test()

    def generate_test(self):
        self.task_frame.grid(row=1, column=1, columnspan=2, pady=(100, 0), sticky="ew")
        tk.Label(master=self.task_frame, text=f"Вопрос №{self.current}", font=base_font).grid(
            row=1, column=0, pady=(0, 10))
        buttons_frame = tk.Frame(master=self.task_frame, highlightbackground=light_green,
                                 highlightcolor=light_green, highlightthickness=3)
        buttons_frame.grid(row=0, column=0, pady=(5, 20), padx=(5, 0), sticky="w")
        next_bt = tk.Button(master=buttons_frame, text="Вперед", font=base_font, command=self.go_next)
        previous_bt = tk.Button(master=buttons_frame, text="Назад", font=base_font, command=self.go_previous)
        next_bt.grid(row=0, column=1)
        previous_bt.grid(row=0, column=0)
        tk.Button(master=self.task_frame, text="Сохранить ответ",
                  font=base_font, bg="light green", command=self.save_answer).grid(
            row=0, column=1, padx=(0, 5), pady=(5, 20), sticky="e"
        )
        task_txt = tk.Text(master=self.task_frame, font=base_font, width=80, height=5, wrap=tk.WORD)
        task_txt.insert(1.0, self.tasks[self.current-1])
        task_txt.grid(row=2, column=0, padx=(5, 5), pady=(10, 0), sticky="e")

        if self.types[self.current-1] == 0:
            n = len(self.variants[self.current-1])
            vr_frame = tk.Frame(master=self.task_frame, bg=light_green, highlightbackground=light_green,
                                highlightcolor=light_green, highlightthickness=3)
            vr_frame.grid(row=3, column=0, sticky="w")
            if self.results[self.current-1] is not None:
                flg_list = self.results[self.current-1]
            else:
                flg_list = [0 for i in range(n)]
            for i in range(n):
                tk.Label(text=f"{i + 1})", font=base_font, master=vr_frame, bg=light_green).grid(
                    row=i, column=0, padx=(5, 0), pady=(5, 0), sticky="w")
                tk.Label(master=vr_frame, font=base_font, text=self.variants[self.current-1][i], bg="white").grid(
                    row=i, column=1, padx=(5, 0), pady=(5, 0), sticky="w"
                )
                var1 = tk.BooleanVar()
                var1.set(flg_list[i])
                c1 = tk.Checkbutton(master=vr_frame, variable=var1, onvalue=1, offvalue=0, bg=light_green)
                c1.grid(row=i, column=2)
                self.current_flags_list.append(var1)
        elif self.types[self.current-1] == 1:
            tk.Label(master=self.task_frame, font=base_font,
                     text=f"Допустимая погрешность: {self.errors[self.current-1]} %").grid(
                row=3, column=0, sticky="w", padx=(5, 0), pady=(5, 0)
            )
            tk.Label(master=self.task_frame, font=base_font, text="Ваш ответ:").grid(
                row=4, column=0, padx=(5, 0), pady=(5, 0), sticky="w")
            if self.results[self.current-1] is not None:
                an = self.results[self.current-1]
            else:
                an = ""
            answer = tk.Text(master=self.task_frame, font=base_font, width=80, height=5)
            answer.insert(1.0, an)
            answer.grid(row=5, column=0, padx=(5, 0), pady=(5, 5), sticky="w")
            self.current_answer = answer
        else:
            tk.Label(master=self.task_frame, font=base_font, text="Ваш ответ:").grid(
                row=4, column=0, padx=(5, 0), pady=(5, 0), sticky="w")
            if self.results[self.current-1] is not None:
                an = self.results[self.current-1]
            else:
                an = ""
            ans = tk.Text(master=self.task_frame, font=base_font, width=80, height=5)
            ans.insert(1.0, an)
            ans.grid(row=5, column=0, padx=(5, 0), pady=(5, 5), sticky="w")
            self.current_ans = ans

    def save_answer(self):
        if self.types[self.current - 1] == 0:
            fgs = [int(self.current_flags_list[i].get()) for i in range(len(self.current_flags_list))]
            self.results[self.current - 1] = fgs
        elif self.types[self.current - 1] == 1:
            self.results[self.current - 1] = self.current_answer.get(1.0, tk.END)
        else:
            self.results[self.current - 1] = self.current_ans.get(1.0, tk.END)

    def go_next(self):
        if self.current == self.count_q:
            pass
        else:
            self.current += 1
            App.clear_frame(self.task_frame)

            self.current_flags_list = []
            self.current_answer = ""
            self.current_ans = ""

            self.generate_test()




    def go_previous(self):
        if self.current == 1:
            pass
        else:
            self.current -= 1
            App.clear_frame(self.task_frame)

            self.current_flags_list = []
            self.current_answer = ""
            self.current_ans = ""

            self.generate_test()

    def save_result(self):
        answer = mb.askokcancel(title="Сохранение", message="Сохранить работу? Нажмите OK, если уверены, "
                                                            "что все ответы заполнены полностью и сохранены")
        if answer:
            App.clear_frame(self.task_frame)
            for i in range(self.count_q):
                fr = tk.Frame(master=self.task_frame, bg=light_green)
                fr.grid(row=i, column=0, columnspan=2)
                l = tk.Label(master=fr, text=f"Вопрос №{i+1}", font=base_font, bg=light_green)
                l.grid(
                    row=0, column=0, pady=(5, 0), padx=(5, 0))

                if self.types[i] == 0:
                    n = len(self.variants[i])
                    vr_frame = tk.Frame(master=fr, bg=light_green, highlightbackground=light_green,
                                        highlightcolor=light_green, highlightthickness=3)
                    vr_frame.grid(row=1, column=0, sticky="w")
                    points = 0
                    corrects = len([self.variants[i][j] for j in range(n) if self.flags[i][j] == 1])
                    for j in range(n):
                        tk.Label(text=f"{j + 1})", font=base_font, master=vr_frame, bg=light_green).grid(
                            row=j, column=0, padx=(5, 0), pady=(5, 0), sticky="w")
                        lb = tk.Label(master=vr_frame, font=base_font, text=self.variants[i][j], bg=light_green)
                        lb.grid(
                            row=j, column=1, padx=(5, 0), pady=(5, 0), sticky="w"
                        )
                        if self.results[i][j] == 0 and self.flags[i][j] == 0:
                            pass
                        elif self.results[i][j] == 0 and self.flags[i][j] == 1:
                            lb.config(bg="light green")
                        elif self.results[i][j] == 1 and self.flags[i][j] == 0:
                            points -= 1
                            lb.config(bg="red")
                        else:
                            points += 1
                            lb.config(bg="light green")
                    res_label = tk.Label(master=fr, bg=light_green, text=f"{points} из {corrects} баллов")
                    res_label.grid(row=0, column=1, padx=(50, 0), pady=(5, 0))
                else:
                    tk.Label(master=fr, text="Задания с письменным ответом проверяются учителем",
                             bg=light_green).grid(
                        row=1, column=0, padx=(5, 0), pady=(5, 0), sticky="w"
                    )
                    tk.Label(master=fr, text="Ваш ответ:", bg=light_green).grid(
                        row=2, column=0, padx=(5, 0), pady=(5, 0), sticky="w"
                    )
                    tk.Label(master=fr, text=self.results[i], bg=light_green).grid(
                        row=3, column=0, padx=(5, 0), pady=(5, 0), sticky="w"
                    )

            if "Results" not in os.listdir():
                os.makedirs("Results")
            str_results = []
            encrypted_str_results = []
            key = self.name[::-1]

            for i in range(self.count_q):
                if self.types[i] == 0:
                    lin = " ".join(list(map(str, self.results[i])))+f"={points}_{corrects}"+"\n"
                    lin = str(self.types[i])+":"+lin
                    line = lin.encode("utf8")

                    encrypted_line = base64.b64encode(line)
                    #encrypted_line = encrypted_line.decode("utf8")
                    #encrypted_line = cryptocode.encrypt(line, key)
                elif self.types[i] == 1:
                    lin = str(self.types[i])+":"+self.results[i]
                    line = lin.encode("utf8")

                    encrypted_line = base64.b64encode(line)
                    #encrypted_line = encrypted_line.decode("utf8")
                    #encrypted_line = cryptocode.encrypt(line, key)
                else:
                    lin = str(self.types[i])+":"+self.results[i]
                    line = lin.encode("utf8")

                    encrypted_line = base64.b64encode(line)
                    #encrypted_line = encrypted_line.decode("utf8")
                    #encrypted_line = cryptocode.encrypt(line)
                str_results.append(lin)
                encrypted_str_results.append(encrypted_line)
            encrypted_str_results.insert(0, base64.b64encode((str(self.count_q)+"\n").encode("utf8")))

            with open("Мои данные.txt") as file:
                fio, klas = file.readlines()

            str_results.insert(0, str(self.count_q)+"\n")
            str_results.insert(0, klas+"\n")
            str_results.insert(0, fio)
            file = open(f"Results/{self.name}({fio[:-1]}).txt", "w")
            file.writelines(str_results)
            file.close()
            """
            conn = sqlite3.connect(f"Results/{self.name}.db")
            curs = conn.cursor()

            curs.execute("CREATE TABLE inf (name text, count_q integer)")
            curs.execute("CREATE TABLE types (id integer primary key, type integer)")
            curs.execute("CREATE TABLE answers
                                                          (answer text)
                                                       ")
            curs.execute("CREATE TABLE tasks_with_variants
                                                          (id integer primary key, count_variants integer)")
            curs.execute(
                "CREATE TABLE variants (id integer primary key, variant text, status integer)")
            curs.execute("CREATE TABLE tasks_with_questions (id integer primary key, answer text)")
            conn.commit()
            curs.execute("INSERT INTO inf(name, count_q) VALUES(?, ?)", (self.name, self.count_q))
            answers = []
            curs.executemany("INSERT INTO tasks_with_answers()")
            """
            











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