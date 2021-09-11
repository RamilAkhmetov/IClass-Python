import tkinter as tk
from tkinter import ttk


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
        classesMenu.add_command(label="Показать", command=self.showTests)
        classesMenu.add_command(label="Загрузить новую", command=self.downloadNewTest)
        menubar.add_cascade(label="Проверочные работы", menu=classesMenu)

    def showTests(self):
        pass

    def downloadNewTest(self):
        pass

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