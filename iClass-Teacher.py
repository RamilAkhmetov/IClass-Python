import tkinter as tk
from tkinter import ttk
#import time
import re
import os
import sqlite3
import pathlib
from tkinter import messagebox as mb
from tkinter import filedialog as fl
import shutil
from collections import Counter
import imaplib
import email
import base64



light_green = "#C4F4CE"
light_yellow = "#F5EBCF"
base_font = ("Arial", 10)
weight = "bold"
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
        testsMenu.add_command(label="Результаты", command=self.showResults)
        testsMenu.add_command(label="Загрузить результат", command=self.loadResult)
        menubar.add_cascade(label="Проверочные работы", menu=testsMenu)
        # emailMenu = tk.Menu(menubar)
        # emailMenu.add_command(label="Данные авторизации", command=self.emailData)
        # emailMenu.add_command(label="Отправить работу", command=self.sendTest)
        # emailMenu.add_command(label="Результаты", command=self.getResult)
        # menubar.add_cascade(label="Email", menu=emailMenu)
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

    def showResults(self):
        self.clear_frame(self.frame)
        results = Results(self.frame)

    def loadResult(self):
        self.clear_frame(self.frame)
        loader = loadResult(self.frame)

    def createClass(self):
        self.clear_frame(self.frame)
        newclass = newClass(self.frame)

    def createTest(self):
        self.clear_frame(self.frame)
        newtest = newTest(self.frame)

    def emailData(self):
        self.clear_frame(self.frame)
        emaildata = EmailData(self.frame)

    def sendTest(self):
        self.clear_frame(self.frame)
        sendtest = SendTest(self.frame)

    def getResult(self):
        self.clear_frame(self.frame)
        getresults = GetResults(self.frame)

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
        tk.Label(master=self.master, font=heading_font, text="1. Создание новой работы").grid(
            row=0, column=0, sticky="w", padx=(0, 0))
        paragraph_1 = """1. Для создания новой работы откройте в панели меню раздел “Проверочные работы”. 
2. Далее откройте “Создать новую работу”. 
3. В открывшемся конструкторе заполните поля названия работы и количества вопросов.
4. Кликнете на кнопку “Применить”.
5. В появившемся окне выберите тип задания из списка.
6. Кликнете на кнопку “Применить” в малом окне.
7. Заполните данные о задании.
8. Сохраните задание, нажав на кнопку “Сохранить вопрос”
9. Вы может перемещаться между заданиями теста кнопками “Вперед” и “Назад”.
10. Сохраните работу кнопкой “Сохранить работу”.
"""
        tk.Label(master=self.master, font=manual_font, text=paragraph_1, wraplength=900, justify="left").grid(
            row=1, column=0, sticky="w", padx=(0, 0)
        )

        tk.Label(master=self.master, font=heading_font, text="2. Редактирование работы").grid(
            row=2, column=0, sticky="w", padx=(0, 0))
        paragraph_2 = """1. Для редактирования работы откройте раздел меню “Проверочные работы” -> “Показать”. 
2. Из появившегося списка выберите нужную работу и нажмите кнопку “Просмотреть/Редактировать”.
3. Внесите необходимые изменения.
4. Сохраняйте изменения в заданиях кнопкой “Сохранить вопрос”.
5. Сохраните работу кнопкой “Сохранить работу”.
"""
        tk.Label(master=self.master, font=manual_font, text=paragraph_2, wraplength=900, justify="left").grid(
            row=3, column=0, sticky="w", padx=(0, 0)
        )
        tk.Label(master=self.master, font=heading_font, text="3. Заполнение данных класса").grid(
            row=4, column=0, sticky="w", padx=(0, 0))
        paragraph_3 = """1. Откройте раздел “Мои классы” -> “Создать новый”.
2. В появившемся разделе заполните поля названия класса (номер и
литера; например, “11В”). 
3. Нажмите кнопку “Применить”.
4. Вы можете вставить столбец с ФИО учеников или из email-адресов из
буфера обмена, нажав на кнопку “Вставить из буфера”.
5. Сохраните класс кнопкой “Сохранить класс”

        """
        tk.Label(master=self.master, font=manual_font, text=paragraph_3, wraplength=900, justify="left").grid(
            row=5, column=0, sticky="w", padx=(0, 0)
        )
        tk.Label(master=self.master, font=heading_font, text="4. Редактирование данных класса").grid(
            row=6, column=0, sticky="w", padx=(0, 0))
        paragraph_4 = """1. Откройте раздел “Мои классы” -> “Показать”.
2. В появившемся разделе Вы увидите список созданных классов. Выберите нужный и кликнете на его название.
3. Внесите необходимые изменения в данные класса.
4. Сохраните изменения, нажав на кнопку “Сохранить класс”.

                """
        tk.Label(master=self.master, font=manual_font, text=paragraph_4, wraplength=900, justify="left").grid(
            row=7, column=0, sticky="w", padx=(0, 0)
        )

        tk.Label(master=self.master, font=heading_font, text="5. Загрузка результата ученика").grid(
            row=8, column=0, sticky="w", padx=(0, 0))
        paragraph_5 = """1. Откройте раздел меню “Проверочные работы” -> “Загрузить результат”.
 2. В появившемся окне проводника найдите скачанный файл с результатом ученика, выберите его и нажмите “Открыть”.

                        """
        tk.Label(master=self.master, font=manual_font, text=paragraph_5, wraplength=900, justify="left").grid(
            row=9, column=0, sticky="w", padx=(0, 0)
        )

        tk.Label(master=self.master, font=heading_font, text="6. Просмотр и проверка работ учащихся").grid(
            row=10, column=0, sticky="w", padx=(0, 0))
        paragraph_6 = """1. Откройте раздел “Проверочные работы” -> “Результаты”.
	Вам откроется список проверочных работ, для которых загружен результат хотя бы одного ученика. 
2. Выберите нужную работу и кликнете “Показать результаты по классам”.
	Вам откроется список классов, ученики которых прислали результат по данной работе.
3. Выберите нужный класс и кликнете “Показать результаты учеников”.
Вам откроется список учеников выбранного класса. Для каждого
ученика указан статус проверки: “Оценка: ”для ученика с результатом или “Результат ещё не получен”.
4. Выберите ученика с результатом. Кликнете на кнопку “Работа ученика”.
Вам откроется окно с тестовой работой ученика. Для каждого задания
показано условие. Для задания с выбором правильных вариантов ответа приводится количество правильных и ложных ответов, данных учеником, а также правильных ответов за задание. 
Для задания с числовым ответом показаны правильный ответ на задачу, ответ ученика и рассчитанная погрешность ответа ученика. Для задания с развернутым ответом показано текстовое поле с ответом ученика.
5. Для каждого задания укажите максимальное количество баллов за задание и количество баллов, набранных учеником.
6. По окончании проверки нажмите “Закончить проверку”.
Откроется окно с информацией о сумме набранных учеником баллов и их процентном отношении к максимальному количеству баллов за тест.
7. Выберите оценку по пятибалльной шкале из списка и нажмите “Сохранить оценку”. """
        tk.Label(master=self.master, font=manual_font, text=paragraph_6, wraplength=900, justify="left").grid(
            row=11, column=0, sticky="w", padx=(0, 0)
        )




class EmailData(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.login = None
        self.password = None
        self.today = None

        self.grid()
        self.initUI()


    def initUI(self):
        if "Email.txt" in os.listdir():
            file = open("Email.txt")
            login, password = file.readlines()
            file.close()
        else:
            login = ""
            password = ""

        fr = tk.Frame(master=self, highlightbackground=light_green,
                      highlightthickness=3, highlightcolor=light_green, bg=light_yellow)
        fr.grid(sticky="news", pady=(200, 10))
        tk.Label(master=fr, text="Мой аккаунт Gmail", font=base_font, bg=light_yellow).grid(row=0, column=0, padx=(10, 0),
                                                                                     pady=(10, 0), sticky="w")
        save_bt = tk.Button(master=fr, font=base_font, text="Сохранить", bg="light green")
        save_bt.config(command=self.save)
        save_bt.grid(row=0, column=1, sticky="e", padx=(200, 10), pady=(10, 0))
        tk.Label(master=fr, text="Логин", font=base_font, bg=light_yellow).grid(row=1, column=0, padx=(10, 0),
                                                                              pady=(30, 0), sticky="w")
        self.login = tk.Text(master=fr, font=base_font, relief=tk.RAISED, width=50, height=1)
        self.login.insert(1.0, login)
        self.login.grid(row=1, column=1, padx=(200, 10), sticky="e", pady=(30, 0))
        tk.Label(master=fr, font=base_font, bg=light_yellow, text="Пароль").grid(row=2, column=0, padx=(10, 0),
                                                                                pady=(30, 10), sticky="w")
        self.password = tk.Text(master=fr, font=base_font, relief=tk.RAISED, width=50, height=1)
        self.password.insert(1.0, password)
        self.password.grid(row=2, column=1, padx=(200, 10), sticky="e", pady=(30, 10))

    def save(self):
        login = self.login.get(1.0, tk.END)
        password = self.password.get(1.0, tk.END)
        login = re.sub(r"[\n]", "", login)
        password = re.sub(r"[\n]", "", password)
        file = open("Email.txt", "w")
        file.writelines([login + "\n", password])
        file.close()

class SendTest(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

    def initUI(self):
        pass

class GetResults(tk.Frame):
    def __init__(self, master):
        super().__init__(master)


        self.encoded_mails = []
        self.uids = []
        self.grid()
        self.initUI()

    def initUI(self):
        try:
            with open("Email.txt") as file:
                login, password = file.readlines()
            print(login, password)
            mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)

            mail.login(login, password)
            mail.select('inbox')
            result, data = mail.uid('search', None, 'UNSEEN')
            ids_list = data[0].split()

            mails = []
            c = 0
            for i in ids_list:
                result, data = mail.uid(u'fetch', i, u"(RFC822)")
                mail.store(i, '+FLAGS', '\\SEEN')
                raw_email = data[0][1]
                raw_email_string = raw_email.decode('utf-8')
                file = open(f"письмо{c}.txt", "w")
                file.write(raw_email_string)
                file.close()
                c += 1
                email_message = email.message_from_string(raw_email_string)
                raw_subject = email_message['Subject']
                try:
                    subject = base64.b64decode(raw_subject.split('?')[3]).decode("utf-8")
                    if subject == "iClass - Учебное приложение":
                        self.uids.append(i)
                        self.encoded_mails.append(email_message)
                except Exception:
                    continue


        except imaplib.socket.gaierror:
            mb.showerror(title="Ошибка", message="Нет подключения к интернету")

    def save_mails(self):
        for i in range(len(self.encoded_mails)):
            email_message = self.encoded_mails[i]

            # if email_message.is_multipart():
            #     for payload in email_message.get_payload():
            #         body = payload.get_payload(decode=True)
            #         if body == None:
            #             continue
            #         print(body)
            #         print(base64.b64decode(body))
            #         f = open("письмо.txt", "w")
            #         f.write(body)
            #         print(body)



class Results(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.names = []

        self.initUI()
        self.grid()

    def initUI(self):
        if "Результаты" not in os.listdir():
            os.makedirs("Результаты")
        if len(os.listdir("Результаты")) == 0:

            tk.Label(master=self,
                     text="Список результатов пуст.\n Добавьте результаты в разделе 'Загрузить результат'",
                     font=('Arial', 25)).pack(padx=10, pady=10)

        else:
            all_results = os.listdir("Результаты")
            all_results.sort(key=lambda f: os.path.getmtime(os.path.join(os.getcwd()+"\Результаты", f)))

            all_results = all_results[::-1]

            all_results = [all_results[i].split("(")[0] for i in range(len(all_results))]
            results = list(Counter(all_results))
            count = len(results)


            for i in range(count):
                row = tk.Frame(master=self, bg="white", highlightbackground=light_green, highlightthickness=3,
                               highlightcolor=light_green)
                row.grid(sticky="ew")
                lb = tk.Label(master=row, font=base_font, text=str(i+1)+") "+results[i], bg="white", wraplength=300)
                self.names.append(results[i])
                lb.pack(side=tk.LEFT, padx=(20, 0), fill=tk.X)
                bt = tk.Button(master=row, font=base_font, text="Показать результаты по классам")
                bt.configure(command=lambda button=bt: self.showResult(button.master))
                bt.pack(side=tk.RIGHT, padx=(600, 0), fill=tk.X)

    def showResult(self, master):
        gi = master.grid_info()['row']
        name = self.names[gi]
        name = re.sub(r'["]', '', name)
        App.clear_frame(self.master)
        classresult = classResult(self.master, name)
        self.destroy()


class classResult(tk.Frame):
    def __init__(self, master, name):
        super().__init__(master)

        self.master = master
        self.name = name
        self.full_name = ""
        self.classes = dict()
        self.initUI()
        self.grid()

    def initUI(self):
        conn = sqlite3.connect(f"tests/{self.name}.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM name;")
        self.full_name = cursor.fetchone()[0]
        conn.close()
        tk.Label(master=self, text=self.full_name, font=heading_font, bg="white").grid()
        for file_path in os.listdir("Результаты"):
            if file_path.split(sep="(")[0].split(sep="/")[-1] != self.name:
                continue
            file = open(f"Результаты/{file_path}")
            fio = file.readline()[:-1]
            klas = file.readline()[:-1]
            if klas in self.classes.keys():
                self.classes[f"{klas}"] += 1
            else:
                self.classes[f"{klas}"] = 1
        conn = sqlite3.connect("classes.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM classes")
        classes_data = cursor.fetchall()
        clases = {classes_data[i][0]: classes_data[i][1] for i in range(len(classes_data))}

        for i in range(len(self.classes)):
            row = tk.Frame(master=self, bg="white", highlightbackground=light_green, highlightthickness=3,
                           highlightcolor=light_green)
            row.grid(sticky="ew", row=i+1)
            lb = tk.Label(master=row, font=base_font, text=list(self.classes.keys())[i], bg="white", wraplength=300)
            lb.pack(side=tk.LEFT, padx=(20, 0), fill=tk.X)
            bt = tk.Button(master=row, font=base_font, text="Показать результаты учеников")
            bt.configure(command=lambda button=bt: self.showResult(button.master, list(clases.values())[i]))
            bt.pack(side=tk.RIGHT, padx=(400, 0), fill=tk.X)
            tk.Label(master=row, bg="white", font=base_font,
                     text=f"Есть результат от {list(self.classes.values())[i]} "
                          f"из {clases[list(self.classes.keys())[i]]}").pack(side=tk.LEFT, padx=(20, 0))

    def showResult(self, master, class_count):
        gi = master.grid_info()['row']

        class_name = list(self.classes.keys())[gi-1]
        class_name = re.sub(r'["]', '', class_name)
        App.clear_frame(self.master)
        studentsresult = studentsResults(self.master, class_name, class_count, self.name, self.full_name)
        self.destroy()


class studentsResults(tk.Frame):
    def __init__(self, master, class_name, class_count, short_test_name, full_test_name):
        super().__init__(master)

        self.master = master
        self.class_name = class_name
        self.class_count = class_count
        self.short_test_name = short_test_name
        self.full_test_name = full_test_name
        self.results = []
        self.students_with_result = []
        self.marks = ["\n" for i in range(self.class_count)]
        self.initUI()
        self.grid()

    def initUI(self):

        tk.Label(master=self, text=self.class_name, font=heading_font, bg="white",
                 ).grid(row=0, column=1, pady=(10, 30))
        tk.Label(master=self, text=self.full_test_name, font=heading_font, bg="white",
                 wraplength=300).grid(row=0, column=2, pady=(10, 30))
        tk.Button(master=self, text="Копировать столбец оценок", bg="light green", command=self.copyMarks).grid(
            row=0, column=0, sticky="e", pady=(10, 30)
        )

        for file_path in os.listdir("Результаты"):
            if file_path.split(sep="(")[0].split(sep="/")[-1] != self.short_test_name:
                continue
            file = open(f"Результаты/{file_path}")
            fio = file.readline()[:-1]
            klas = file.readline()[:-1]
            if klas == self.class_name:
                self.students_with_result.append(fio)
                data = file.readlines()
                data = [data[i][:-1] for i in range(len(data))]
                self.results.append(data)
            file.close()
        if "marks.db" in os.listdir():

            cnn = sqlite3.connect("marks.db")
            curs = cnn.cursor()
            f = True
        else:
            f = False
        conn = sqlite3.connect("classes.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE class=?", (self.class_name,))
        classes_data = cursor.fetchall()
        conn.close()
        all_students = [classes_data[i][1] for i in range(len(classes_data))][::-1]
        for i in range(len(all_students)):
            row = tk.Frame(master=self, bg="white", highlightbackground=light_green, highlightthickness=3,
                           highlightcolor=light_green)
            row.grid(sticky="ew", row=i+1)
            lb = tk.Label(master=row, font=base_font, text=all_students[i], bg="white", wraplength=300)
            lb.pack(side=tk.LEFT, padx=(20, 0), fill=tk.X)
            if all_students[i] in self.students_with_result:
                index = self.students_with_result.index(all_students[i])
                if f:
                    curs.execute("SELECT * FROM marks WHERE test_name=? AND class=? AND student=?",
                                 (self.full_test_name, self.class_name, all_students[i]))
                    res = curs.fetchall()
                else:
                    res = []
                if len(res) == 0:
                    mark = "\n"
                else:
                    mark = res[0][-1]

                l = tk.Label(master=row, bg="white", text="Оценка: "+str(mark))
                l.pack(side=tk.RIGHT, padx=(10, 0), fill=tk.X)
                if mark == 5:
                    l.config(fg="green")
                elif mark == 4:
                    l.config(fg="blue")
                elif mark == 3:
                    l.config(fg="yellow")
                elif mark == 2:
                    l.config(fg="red")
                elif mark == 1:
                    l.config(fg="red")
                self.marks[i] = str(mark)+"\n"
                bt = tk.Button(master=row, font=base_font, text="Работа ученика", bg="light green")
                bt.configure(command=lambda button=bt: self.showResult(button.master, index))
                bt.pack(side=tk.RIGHT, padx=(20, 0), fill=tk.X)
            else:
                tk.Label(master=row, fg="red", bg="white", text="Результат ещё не получен").pack(
                    side=tk.RIGHT, padx=(400, 0), fill=tk.X)

    def showResult(self, master, index):

        student = self.students_with_result[index]

        App.clear_frame(self.master)
        result = Result(self.master, self.short_test_name,
                                        self.full_test_name, self.class_name, student, self.results[index][1:])
        self.destroy()

    def copyMarks(self):
        l = [self.marks[i] for i in range(self.class_count)]
        r = tk.Tk()
        r.withdraw()
        r.clipboard_clear()
        r.clipboard_append("".join(l))
        r.update()
        r.destroy()


class Result(tk.Frame):
    def __init__(self, master, short_test_name, full_test_name, class_name, student_name, result):
        super().__init__(master)

        self.short_test_name = short_test_name
        self.full_test_name = full_test_name
        self.class_name = class_name
        self.count_q = 0
        self.student_name = student_name
        self.result = result

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

        self.marks = ["" for i in range(1000)]
        self.max_points = ["" for i in range(1000)]
        self.types = [None for i in range(1000)]
        self.tasks = [None for i in range(1000)]

        self.variants = [None for i in range(1000)]
        self.flags = [None for i in range(1000)]

        self.answers = [None for i in range(1000)]
        self.errors = [None for i in range(1000)]

        self.current = 1

        self.final_mark = None

        self.initUI()
        self.grid()

    def initUI(self):

        conn = sqlite3.connect("tests.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tests WHERE test_name=?", [(self.full_test_name)])
        data = cursor.fetchone()
        i, name, self.count_q = data

        cursor.execute("SELECT * FROM types WHERE test_name=?;", [(self.full_test_name)])
        types = cursor.fetchall()
        cursor.execute("SELECT * FROM tasks_with_answers WHERE test_name=?;", [(self.full_test_name)])
        tasks_with_answers = cursor.fetchall()
        cursor.execute("SELECT * FROM tasks_with_variants WHERE test_name=?;", [(self.full_test_name)])
        tasks_with_variants = cursor.fetchall()
        cursor.execute("SELECT * FROM variants WHERE test_name=?;", [(self.full_test_name)])
        variants = cursor.fetchall()
        cursor.execute("SELECT * FROM tasks_with_questions WHERE test_name=?;", [(self.full_test_name)])
        tasks_with_questions = cursor.fetchall()
        if "marks.db" in os.listdir():
            cnn = sqlite3.connect("marks.db")
            curs = cnn.cursor()
            f = True
        else:
            f = False
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
                self.current_tsk_a += 1
            elif types[i][2] == 2:
                self.types[i] = 2
                self.tasks[i] = tasks_with_questions[self.current_tsk_q][2]
                self.current_tsk_q += 1
            if f:
                curs.execute("SELECT * FROM points WHERE test_name=? AND class=? AND student=? AND task=?",
                             (self.full_test_name, self.class_name, self.student_name, i + 1))
                rs = curs.fetchall()
            else:
                rs = ""

            if len(rs) == 0:
                if f:
                    curs.execute("SELECT * FROM points WHERE test_name=? AND class=? AND task=?",
                                 (self.full_test_name, self.class_name, i + 1))
                    res = curs.fetchall()
                else:
                    res = ""
                if len(res) == 0:
                    self.max_points[i] = ""
                    self.marks[i] = ""
                else:
                    self.max_points[i] = res[0][-2]
                    self.marks[i] = ""
            else:
                self.max_points[i] = rs[0][-2]
                self.marks[i] = rs[0][-1]



        if f:
            curs.execute("SELECT * FROM marks WHERE test_name=? AND class=? AND student=?",
                         (self.full_test_name, self.class_name, self.student_name))
            res = curs.fetchall()
        else:
            res = ""
        if len(res) == 0:
            mark = ""
        else:
            mark = res[0][-1]







        first = tk.Frame(master=self)
        first.grid(row=0, column=0, sticky="w")
        tk.Label(master=first, font=base_font, text="Работа по теме").grid(
            row=0, column=0, padx=(20, 0), pady=(20, 0), sticky='w')
        tk.Label(master=first, font=heading_font, bg="white",
                 text=self.full_test_name, wraplength=200).grid(
            row=1, column=0, padx=(20, 0), pady=(20, 0), sticky="s"
        )
        tk.Label(master=first, font=base_font, text="Количество вопросов").grid(
            row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="w"
        )
        tk.Label(master=first, font=heading_font, bg="white", text=self.count_q).grid(
            row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="w"
        )
        second = tk.Frame(master=self)
        second.grid(row=0, column=1, sticky="w")
        tk.Label(master=second, font=base_font, text="ФИО ученика").grid(
            row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="w")
        tk.Label(master=second, font=heading_font, bg="white",
                 text=self.student_name, wraplength=200).grid(
            row=1, column=0, padx=(20, 0), pady=(20, 0), sticky="w"
        )
        tk.Label(master=second, text="Класс", font=base_font).grid(
            row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="w"
        )
        tk.Label(master=second, font=heading_font, bg="white",
                 text=self.class_name, wraplength=200).grid(
            row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="w"
        )
        tk.Label(master=second, text="Оценка", font=base_font).grid(
            row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="w"
        )
        tk.Label(master=second, font=heading_font, bg="white",
                 text="Не проверено" if mark == "" else mark, wraplength=200).grid(
            row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="w"
        )
        save_bt = tk.Button(master=second, text="Закончить проверку",
                            command=self.save_work,
                            bg="light green", font=base_font)
        save_bt.grid(column=2, row=0, pady=(40, 0), padx=(100, 5), sticky="w")


        self.generate_task()


    def generate_task(self):
        self.task_frame.grid(row=2, column=0, pady=(100, 5), columnspan=3)
        buttons_frame = tk.Frame(master=self.task_frame, highlightbackground=light_green,
                                 highlightcolor=light_green, highlightthickness=3)
        next_bt = tk.Button(master=buttons_frame, text="Вперед", font=base_font, command=self.go_next)
        previous_bt = tk.Button(master=buttons_frame, text="Назад", font=base_font, command=self.go_previous)
        next_bt.grid(row=0, column=1)
        previous_bt.grid(row=0, column=0)
        buttons_frame.grid(row=0, column=0, pady=(5, 20), padx=(5, 0), sticky="w")
        lb = tk.Label(master=self.task_frame, text=f"Вопрос №{self.current}", font=base_font)
        lb.grid(row=0, column=1, pady=(0, 10), padx=(5, 0), sticky="w")
        mark_fr = tk.Frame(master=self.task_frame, bg=light_green)
        mark_fr.grid(row=1, column=0, columnspan=2, sticky="w")
        tk.Label(master=mark_fr, font=base_font, text="Максимум баллов за задание", bg=light_green).grid(
            row=0, column=0, padx=(5, 0), pady=(5, 20), sticky="w"
        )
        max_txt = tk.Text(master=mark_fr, font=base_font, wrap=tk.WORD, width=10, height=1)
        max_txt.insert(1.0, self.max_points[self.current - 1])
        max_txt.grid(row=0, column=1, padx=(5, 0), pady=(5, 20), sticky="w")
        tk.Label(master=mark_fr, font=base_font, text="Оценка задания в баллах", bg=light_green).grid(
            row=1, column=0, padx=(5, 0), pady=(5, 20), sticky="w"
        )
        mark_txt = tk.Text(master=mark_fr, font=base_font, wrap=tk.WORD, width=10, height=1)
        mark_txt.insert(1.0, self.marks[self.current-1])
        mark_txt.grid(row=1, column=1, padx=(5, 0), pady=(5, 20), sticky="w")
        save_bt = tk.Button(master=self.task_frame, text="Сохранить оценку\nзадания", command=lambda: self.save_mark(int(mark_txt.get(1.0, tk.END)), int(max_txt.get(1.0, tk.END))),
                            bg="light green", font=base_font)
        save_bt.grid(column=2, row=0, pady=(5, 20), padx=(0, 5), sticky="e")
        tk.Label(master=self.task_frame, text="Условие задания", bg=light_green, font=base_font).grid(
            row=2, column=0, padx=(5, 0), pady=(5, 20), sticky="w"
        )
        txt = tk.Text(master=self.task_frame, font=base_font, wrap=tk.WORD, width=40, height=6)
        txt.insert(1.0,  self.tasks[self.current - 1])
        txt.grid(row=2, column=1, padx=(5, 0), pady=(5, 20), sticky="w")
        tp = self.types[self.current - 1]
        if tp is not None:
            if tp == 0:
                n = len(self.variants[self.current - 1])
                vr_frame = tk.Frame(master=self.task_frame, bg=light_green, highlightbackground=light_green,
                                    highlightcolor=light_green, highlightthickness=3)
                vr_frame.grid(row=3, column=0, sticky="w")
                if self.result[self.current - 1] is not None:
                    flg_list = self.result[self.current - 1].split(sep="=")[0].split(sep=":")[-1].split()
                else:
                    flg_list = [0 for i in range(n)]
                count_of_corrects = self.flags[self.current - 1].count(1)
                count_of_correct_ans = 0
                count_of_wrong_ans = 0
                for i in range(n):

                    tk.Label(text=f"{i + 1})", font=base_font, master=vr_frame, bg=light_green).grid(
                        row=i, column=0, padx=(5, 0), pady=(5, 0), sticky="w")
                    lb = tk.Label(master=vr_frame, font=base_font,
                                  text=self.variants[self.current - 1][i], wraplength=200, bg="white")
                    lb.grid(
                        row=i, column=1, padx=(5, 0), pady=(5, 0), sticky="w"
                    )

                    #corrects = len([self.variants[i][j] for j in range(n) if self.flags[i][j] == 1])

                    if flg_list[i] == "0" and self.flags[self.current-1][i] == 0:
                        pass
                    elif flg_list[i] == '0' and self.flags[self.current-1][i] == 1:
                        lb.config(bg="light green")
                    elif flg_list[i] == '1' and self.flags[self.current-1][i] == 0:
                        count_of_wrong_ans += 1
                        lb.config(bg="red")
                    else:
                        count_of_correct_ans += 1
                        lb.config(bg="light green")
                    var1 = tk.BooleanVar()
                    var1.set(flg_list[i])
                    c1 = tk.Checkbutton(master=vr_frame, variable=var1, onvalue=1, offvalue=0, bg=light_green)
                    c1.grid(row=i, column=2)
                    message = f"Всего вариантов ответа: {n}\n" \
                              f"Всего правильных вариантов ответа: {count_of_corrects}\n" \
                              f"Число данных правильных вариантов ответа: {count_of_correct_ans}\n" \
                              f"Число данных ошибочных вариантов ответа: {count_of_wrong_ans}"

                    txt = tk.Text(master=self.task_frame, wrap=tk.WORD,
                                  width=60, height=4)
                    txt.insert(1.0, message)
                    txt.grid(row=3, column=1, padx=(10, 5), pady=(10, 0))
                    self.current_flags_list.append(var1)

            elif tp == 1:
                fr = tk.Frame(master=self.task_frame, bg=light_green, highlightbackground=light_green,
                              highlightcolor=light_green, highlightthickness=3)
                fr.grid(row=11, column=0, sticky="w", columnspan=2)
                tk.Label(master=self.task_frame, text="Правильный ответ", font=base_font, bg=light_green).grid(
                    row=3, column=0, padx=(5, 0), pady=(5, 0), sticky="w"
                )
                tk.Label(master=self.task_frame, text="Ответ ученика", font=base_font, bg=light_green).grid(
                    row=4, column=0, padx=(5, 0), pady=(5, 0), sticky="w"
                )
                correct_tx = tk.Text(master=self.task_frame, font=base_font, width=6, height=1, wrap=tk.WORD)
                correct_tx.grid(row=3, column=1, padx=(5, 0), pady=(0, 5), sticky="w")
                correct_tx.insert(1.0, self.answers[self.current - 1])
                ans_tx = tk.Text(master=self.task_frame, font=base_font, width=6, height=1, wrap=tk.WORD)
                ans_tx.grid(row=4, column=1, padx=(5, 0), pady=(0, 5), sticky="w")
                ans_tx.insert(1.0, self.result[self.current - 1].split(sep=":")[-1])
                err_tx = tk.Text(master=fr, font=base_font, width=60, height=1)
                err_tx.grid(row=5, column=0, padx=(5, 0), pady=(0, 5), sticky="w")
                err_tx.insert(1.0, "Допустимая погрешность ответа в %: " + str(self.errors[self.current - 1]))
                ans_err = tk.Text(master=fr, font=base_font, width=60, height=1)
                ans_err.grid(row=6, column=0, padx=(5, 0), pady=(0, 5), sticky="w")
                try:
                    err = (abs(float(self.result[self.current - 1].split(sep=":")[-1])-float(self.answers[self.current-1]))/float(self.answers[self.current-1])*100)
                except ZeroDivisionError:
                    err = "Infinity"
                ans_err.insert(1.0, "Погрешность ответа ученика в %: " + str(err))

            elif tp == 2:
                tk.Label(master=self.task_frame, text="Ответ ученика", font=base_font, bg=light_green).grid(
                    row=3, column=0, padx=(5, 0), pady=(5, 0), sticky="w"
                )
                txt = tk.Text(master=self.task_frame, font=base_font, wrap=tk.WORD, width=60, height=6)
                txt.insert(1.0, self.result[self.current - 1].split(sep=":")[-1])
                txt.grid(row=3, column=1, padx=(5, 0), pady=(10, 5), sticky="w", columnspan=2)
        buttons_frame = tk.Frame(master=self.task_frame, highlightbackground=light_green,
                                 highlightcolor=light_green, highlightthickness=3)
        next_bt = tk.Button(master=buttons_frame, text="Вперед", font=base_font, command=self.go_next)
        previous_bt = tk.Button(master=buttons_frame, text="Назад", font=base_font, command=self.go_previous)
        next_bt.grid(row=0, column=1)
        previous_bt.grid(row=0, column=0)
        buttons_frame.grid(row=0, column=0, pady=(5, 20), padx=(5, 0), sticky="w")

    def save_mark(self, mark, max_point):
        self.marks[self.current-1] = mark
        self.max_points[self.current-1] = max_point

    def go_next(self):
        if self.current == self.count_q:
            pass
        else:
            self.current += 1
            App.clear_frame(self.task_frame)


            self.generate_task()

    def go_previous(self):
        if self.current == 1:
            pass
        else:
            self.current -= 1
            App.clear_frame(self.task_frame)

            self.current_flags_list = []
            self.current_answer = ""
            self.current_ans = ""

            self.generate_task()

    def save_work(self):
        answer = mb.askokcancel(title="Сохранение", message="Сохранить проверку? Нажмите OK, если уверены, "
                                                            "что все оценки заполнены полностью")
        if answer:

            App.clear_frame(self.task_frame)
            sum_max = sum(self.max_points[:self.count_q])
            sum_result = sum(self.marks[:self.count_q])

            tk.Label(master=self.task_frame, font=base_font,
                     text="Максимальное количество баллов", bg=light_green).grid(
                row=0, column=0, padx=(5, 0), pady=(5, 0), sticky="w")
            tk.Label(master=self.task_frame, font=heading_font,
                     text=sum_max, bg=light_green).grid(
                row=0, column=1, padx=(5, 0), pady=(5, 0), sticky="w")
            tk.Label(master=self.task_frame, font=base_font,
                     text="Количество баллов ученика", bg=light_green).grid(
                row=1, column=0, padx=(5, 0), pady=(5, 0), sticky="w")
            tk.Label(master=self.task_frame, font=heading_font,
                     text=sum_result, bg=light_green).grid(
                row=1, column=1, padx=(5, 0), pady=(5, 0), sticky="w")
            tk.Label(master=self.task_frame, font=base_font,
                     text="Доля набранных баллов от максимума, %", bg=light_green).grid(
                row=2, column=0, padx=(5, 0), pady=(5, 0), sticky="w")
            tk.Label(master=self.task_frame, font=heading_font,
                     text=sum_result/sum_max*100, bg=light_green).grid(
                row=2, column=1, padx=(5, 0), pady=(5, 0), sticky="w")
            tk.Label(master=self.task_frame, text="Оценка по пятибальной шкале", font=base_font, bg=light_green).grid(
                row=3, column=0, padx=(5, 0), pady=(5, 0), sticky="w"
            )
            lbox = tk.Listbox(master=self.task_frame, width=2, height=5)
            lbox.grid(row=3, column=1, padx=(5, 0), pady=(0, 5), sticky="w")
            types = [i for i in range(1, 6)]
            for i in types:
                lbox.insert(tk.END, i)

            save_bt = tk.Button(master=self.task_frame, text="Сохранить оценку",
                                command=lambda: self.load_marks(lbox.curselection()[0]+1),
                                bg="light green", font=base_font)
            save_bt.grid(column=2, row=0, pady=(5, 0), padx=(40, 5), sticky="e")



    def load_marks(self, mark):

        answer = mb.askokcancel(title="Сохранение", message="Сохранить оценку? Нажмите OK, если выбрали оценку")
        if answer:
            App.clear_frame(self.master)
            cnn = sqlite3.connect("marks.db")
            curs = cnn.cursor()
            curs.execute("CREATE TABLE IF NOT EXISTS marks(test_name text, class text, student text, mark integer);")
            cnn.commit()
            curs.execute("SELECT * FROM marks WHERE test_name=? AND class=? AND student=?",
                         (self.full_test_name, self.class_name, self.student_name))
            if len(curs.fetchall()) == 0:
                curs.execute("INSERT INTO marks(test_name, class, student, mark) VALUES(?, ?, ?, ?)",
                             (self.full_test_name, self.class_name, self.student_name, mark))
                cnn.commit()
            else:
                curs.execute("UPDATE marks SET mark=? WHERE test_name=? AND class=? AND student=?",
                             (mark, self.full_test_name, self.class_name, self.student_name))
                cnn.commit()
            curs.execute("CREATE TABLE IF NOT EXISTS points(test_name text, class text, student text, task integer, max integer, score integer);")
            cnn.commit()
            curs.execute("SELECT * FROM points WHERE test_name=? AND class=? AND student=?",
                         (self.full_test_name, self.class_name, self.student_name))
            points_rows = [(self.full_test_name, self.class_name, self.student_name, i+1, self.max_points[i], self.marks[i])
                           for i in range(self.count_q)]
            if len(curs.fetchall()) == 0:
                curs.executemany("INSERT INTO points(test_name, class, student, task, max, score) VALUES(?, ?, ?, ?, ?, ?)",
                             points_rows)
                cnn.commit()
            else:
                for i in range(self.count_q):
                    curs.execute("DELETE FROM points WHERE WHERE test_name=? AND class=? AND student=? AND task=?",
                                 (self.full_test_name, self.class_name, self.student_name, i+1))
                    cnn.commit()
                    curs.execute(
                        "INSERT INTO points(test_name, class, student, task, max, score) VALUES(?, ?, ?, ?, ?, ?)",
                        points_rows[i])
                    cnn.commit()












class loadResult(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.initUI()

    def initUI(self):
        file_path = fl.askopenfilename()
        if "Результаты" not in os.listdir():
            os.makedirs("Результаты")
        if file_path in os.listdir("Результаты"):
            pass
        else:
            file_name = list(file_path.split(sep="/"))[-1]
            if file_name != "":
                file = open(f"Результаты/{file_name}", "w+")
                file.close()
                shutil.copyfile(file_path, f"Результаты/{file_name}")
        App.clear_frame(self.master)
        self.destroy()




class testList(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.show_bts = []
        self.file_bts = []
        self.names = []

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
            data = data[::-1]
            tests_count = len(data)
            self.names = [data[i][1] for i in range(tests_count)]

            for i in range(tests_count):
                test_frame = tk.Frame(master=self, bg="white",
                                  highlightbackground=light_green, highlightthickness=3,
                                  highlightcolor=light_green)
                test_frame.grid(row=i, sticky="ew")
                tk.Label(master=test_frame, font=base_font, bg="white", wraplength=600, justify="left",
                         text=str(i+1)+") "+ data[i][1], ).pack(side=tk.LEFT, padx=(5, 0), pady=0)


                fl_bt = tk.Button(master=test_frame, font=base_font,
                          text=f"Выгрузить файл", )
                fl_bt.configure(command=lambda button=fl_bt: self.uploadButton(button.master))
                fl_bt.pack(side=tk.RIGHT, padx=(0, 50))
                #fl_bt.bind(f"<Button-1>", self.on_click_fl_bt)
                sh_bt = tk.Button(master=test_frame, font=base_font,
                          text=f"Просмотреть/редактировать")
                sh_bt.configure(command=lambda button=sh_bt: self.testButton(button.master))
                sh_bt.pack(side=tk.RIGHT, padx=(200, 0))
                #sh_bt.bind(f"<Button-1>", self.on_click_sh_bt)

    def uploadButton(self, master):
        gi = master.grid_info()['row']
        self.uploadFile(self.names[gi])

    def testButton(self, master):
        gi = master.grid_info()['row']
        self.showTest(self.names[gi])


    def on_click_fl_bt(self, event):
        button_text = event.widget.cget("text")
        bt_ind = list(button_text.split())[-1][-1]
        self.uploadFile(bt_ind)

    def on_click_sh_bt(self, event):
        button_text = event.widget.cget("text")
        bt_ind = list(button_text.split())[-1][-1]
        self.showTest(bt_ind)

    def showTest(self, name):
        App.clear_frame(self.master)
        test = Test(self.master, name)
        self.destroy()


    def uploadFile(self, name):

        conn = sqlite3.connect("tests.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tests WHERE test_name=?", [(name)])
        i, name, count_q = cursor.fetchone()
        if "tests" not in os.listdir():
            os.makedirs("tests")
        test_name = name[:100]
        test_name = re.sub(r'[/\\?%*:|"<>.,]', "", test_name)
        test_name = re.sub(r'[\n]', "", test_name)

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

        conn.close()

        test_path = str(pathlib.Path().resolve())+f"\\tests\\{test_name}.db"

        if test_path in os.listdir(r'tests'):
            os.remove(test_path)
        cnn = sqlite3.connect(test_path)
        curs = cnn.cursor()
        curs.execute("CREATE TABLE IF NOT EXISTS count_q(count integer);")
        cnn.commit()
        curs.execute("CREATE TABLE IF NOT EXISTS name(name text);")
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
        cnn.commit()
        curs.execute("INSERT INTO name(name) VALUES(?);",
                     (name,))
        cnn.commit()
        curs.executemany("INSERT INTO types(test_name, type) VALUES(?, ?);",
                         types)
        cnn.commit()
        curs.executemany("INSERT INTO tasks_with_answers(test_name, task, answer, err) VALUES(?, ?, ?, ?);",
                           tasks_with_answers)
        cnn.commit()
        curs.executemany("INSERT INTO tasks_with_variants(test_name, task, count_variants) VALUES(?, ?, ?);",
                           tasks_with_variants)
        cnn.commit()
        curs.executemany("INSERT INTO tasks_with_questions(test_name, task) VALUES(?, ?);", tasks_with_questions)
        cnn.commit()
        curs.executemany("INSERT INTO variants(test_name, variant, status) VALUES(?, ?, ?);", variants)
        cnn.commit()





class Test(tk.Frame):
    def __init__(self, master, test_name):
        super().__init__(master)
        self.master = master
        self.test_name = test_name
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

        self.types = [None for i in range(1000)]
        self.tasks = [None for i in range(1000)]

        self.variants = [None for i in range(1000)]
        self.flags = [None for i in range(1000)]

        self.answers = [None for i in range(1000)]
        self.errors = [None for i in range(1000)]

        self.current = 1


        self.grid()
        self.initUI()

    def initUI(self):
        conn = sqlite3.connect("tests.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tests WHERE test_name=?", [(self.test_name)])
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
                self.current_tsk_a += 1
            elif types[i][2] == 2:
                self.types[i] = 2
                self.tasks[i] = tasks_with_questions[self.current_tsk_q][2]
                self.current_tsk_q += 1


        tk.Label(text="Название работы", master=self, font=base_font).grid(
            row=0, column=0, padx=10, pady=10, sticky="n")
        self.name_text.grid(row=0, column=1, padx=10, pady=10, sticky="n")
        self.name_text.insert(1.0, name)
        tk.Label(text="Количество вопросов\n(не больше 1000)", master=self, font=base_font).grid(
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
        test_name = self.name_text.get(1.0, tk.END)
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
                    tx = tk.Text(master=fr, font=base_font, width=60, height=4, wrap=tk.WORD)
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

        self.types = [None for i in range(1000)]
        self.tasks = [None for i in range(1000)]

        self.variants = [None for i in range(1000)]
        self.flags = [None for i in range(1000)]

        self.answers = [None for i in range(1000)]
        self.errors = [None for i in range(1000)]

        self.current = 1
        self.grid()
        self.initUI()

    def initUI(self):
        tk.Label(text="Название работы", master=self,font=base_font).grid(row=0, column=0, padx=10, pady=10, sticky="n")
        self.name_text.grid(row=0, column=1, padx=10, pady=10, sticky="n")
        tk.Label(text="Количество вопросов\n(не больше 1000)", master=self,font=base_font).grid(row=0, column=2, padx=10, pady=10, sticky="n")
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
            vrs = [self.current_variants_list[i].get(1.0, tk.END)[:-1]
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
            test_name = self.name_text.get(1.0, tk.END)
            test_name = re.sub(r'[\n]', "", test_name)
            test_name = re.sub(r"""["']""", "", test_name)

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
                    tx = tk.Text(master=fr, font=base_font, width=60, height=4, wrap=tk.WORD)
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
                ent = tk.Text(master=vr_frame, width=30, height=2, wrap=tk.WORD)
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
        r.destroy()

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
            class_name = class_name.upper()
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
        st_data = [(re.sub(r"[\n]", "", self.name_entry.get(1.0, tk.END)).upper(),
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
        tk.Label(master=self.master, text="ФИО ученика", font=base_font).grid(row=1, column=0, padx=(10, 0))
        paste_names_button = tk.Button(master=self.master, text="Вставить\nиз буфера",
                                       command=lambda: self.paste_from_clipboard(1))
        paste_names_button.grid(row=1, column=1, padx=(10, 0), sticky="w")
        tk.Label(master=self.master, text="Email ученика", font=base_font).grid(row=1, column=2, padx=(10, 0))
        paste_emails_button = tk.Button(master=self.master, text="Вставить\nиз буфера",
                                       command=lambda: self.paste_from_clipboard(2))
        paste_emails_button.grid(row=1, column=3, padx=(10, 0), sticky="w")

    def paste_from_clipboard(self, tp):

        r = tk.Tk()
        r.withdraw()
        data = r.clipboard_get().split(sep="\n")
        
        if tp == 1:
            count = len(self.names) if len(self.names) < len(data) else len(data)
            names_count = len(self.names)
            if count == 0:
                return
            else:
                for i in range(count):
                    self.names[names_count-i-1].delete(1.0, tk.END)
                    self.names[names_count-i-1].insert(1.0, data[i])

        else:
            count = len(self.emails) if len(self.emails) < len(data) else len(data)
            emails_count = len(self.emails)

            if count == 0:
                return
            else:
                for i in range(count):
                    self.emails[emails_count-1-i].delete(1.0, tk.END)
                    self.emails[emails_count-1-i].insert(1.0, data[i])






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
