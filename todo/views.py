from datetime import datetime
from tkinter import Tk, Frame, Entry, Label, Checkbutton, IntVar
from tkinter.constants import RIDGE, TOP, X, RIGHT, LEFT
from typing import List

from .logger import Business, Logger

MONTHS = ('янв', 'фев', 'мар', 'апр', 'май', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек')


class GuiForm:
    """
    Основное окно ввода информации
    """
    def __init__(self, file_name: str):
        self.logger = Logger(file_name)
        self._case_list = self.logger.load_from_files()
        self._unfinished_case_list = self._get_reversed_unfinished_case_list()
        self._create_window()
        self._create_widgets_entry()
        if self._unfinished_case_list:
            self._create_widgets_done()

    def _create_window(self):
        self.root = Tk()
        self.root.title('Что я делаю или сделал')
        self.root.iconbitmap('todo.ico')
        self.root.resizable(width=False, height=False)

    def _create_widgets_entry(self):
        now = datetime.now()
        self._edit_frame = Frame(self.root, relief=RIDGE, borderwidth=1)
        self._edit_frame.pack(side=TOP, fill=X)
        self._edit_date = Entry(self._edit_frame, width=10, font=f"Arial 12", borderwidth=1)
        self._edit_date.pack(side=LEFT)
        self._edit_date.insert(0, f'{now.strftime("%d.%m.%Y")}')
        self._edit_time = Entry(self._edit_frame, width=5, font=f"Arial 12", borderwidth=1)
        self._edit_time.insert(0, f'{now.strftime("%H:%M")}')
        self._edit_time.pack(side=LEFT)
        self._edit_case = Entry(self._edit_frame, width=40, font=f"Arial 12", borderwidth=1)
        self._edit_case.pack(side=LEFT)
        self._edit_case.bind('<KeyPress>', self._fedit_key_press)
        self._edit_case.focus_set()

    def _create_widgets_done(self):
        now = datetime.now()

        self._controls_list = []
        for case in self._unfinished_case_list:
            controls = {}
            controls['frame'] = Frame(self.root, relief=RIDGE, borderwidth=1)
            controls['frame'].pack(fill=X)

            controls['date_case'] = Label(controls['frame'], font=f"Arial 12", justify=LEFT,
                                          text=f'{case.time_begin} ({now.day:0>2}'
                                          f' {MONTHS[now.month - 1]}): {case.case[:50]}')
            controls['date_case'].pack(side=LEFT)
            controls['var'] = IntVar()
            controls['check'] = Checkbutton(controls['frame'], variable=controls['var'], relief=RIDGE, borderwidth=1)
            controls['check'].pack(side=RIGHT)
            controls['end_time'] = Entry(controls['frame'], width=5, font=f"Arial 12", borderwidth=1)
            controls['end_time'].insert(0, f'{now.strftime("%H:%M")}')
            controls['end_time'].pack(side=RIGHT)
            controls['end_date'] = Entry(controls['frame'], font=f"Arial 12", width=10, borderwidth=1)
            controls['end_date'].insert(0, f'{now.strftime("%d.%m.%Y")}')
            controls['end_date'].pack(side=RIGHT)

            self._controls_list.append(controls)

    def show_form(self):
        """
        Показ формы
        :return:
        """
        self.root.wm_geometry("+750+450")
        self.root.update_idletasks()
        self.root.mainloop()
        print(1)

    def _fedit_key_press(self, event):
        """
        Обработка нажатия Enter и Esc
        :param event: параметры события
        :return:
        """
        if event.keycode == 13:
            if self._edit_case.get():
                business = Business()
                business.date_begin = self._edit_date.get()
                business.time_begin = self._edit_time.get()
                business.case = self._edit_case.get()
                self._case_list.append(business)
                self.logger.write_to_file(self._case_list)
            exit(0)
        elif event.keycode == 27:
            exit(1)


    def _get_reversed_unfinished_case_list(self)-> List[Business]:
        """
        Возвращение списка незаконченных дел
        :return: список незаконченных дел
        """
        return list(reversed([case for case in self._case_list if not case.date_end]))
