from tkinter import *
import pickle
import os
from tkinter import messagebox as mbox
import sys
from math import inf

path = os.getcwd()
n = path.find("\Scripts")
path8 = os.path.join(path[0:n] + "\Scripts", "colors.txt")
path1 = os.path.join(path[0:n] + "\Data", "Rick.pic")  # ОП  до рикпик чтобы прога работала везде куда ее скачают
path2 = os.path.join(path[0:n] + "\Graphics",
                     "fon.png")  # ОП  до картинки фона чтобы прога работала везде куда ее скачают
path3 = os.path.join(path[0:n] + "\Graphics", "red.gif")  # ОП до картинки кнопки ред записи
path4 = os.path.join(path[0:n] + "\Graphics", "plus.gif")  # ОП до картинки кнопки доб записи
path5 = os.path.join(path[0:n] + "\Graphics", "del.gif")  # ОП до картинки кнопки удаление записи
path6 = os.path.join(path[0:n] + "\Graphics", "download.gif")  # ОП до картинки кнопки загрузки  бд
path7 = os.path.join(path[0:n] + "\Graphics", "save.gif")  # ОП до картинки кнопки сохранения бд
path9 = os.path.join(path[0:n] + "\Library")
path10 = os.path.join(path[0:n] + "\Graphics", "exit.gif")
sys.path.append(path9)

from ourmodule import *


# **********************************************************************************************************************


def colors(path8, length):
    """
    Функция считывания параметров интерфейса из файла
    Автор: Животов Глеб
    :param path8: Путь к текстовому файлу с параметрами
    :param length: Количество цветов
    :return: Список, состоящий из количества length цветов, названия шрифта и размера шрифта
    """
    a = []
    for i in range(length):
        a.append("white")
    f = open(path8, "r")
    i = 0
    for k in f:
        k = k.rstrip('\n')
        try:
            a[i] = str(k)
        except IndexError:
            a.append(str(k))
        i += 1
    f.close()
    return a


# **********************************************************************************************************************


a = []
a = colors(path8, 4)
butcolor = a[0]
bgcolor1 = a[1]
bgcolor2 = a[2]
bgcolor3 = a[3]
mainfont = (str(a[4]), int(a[5]))

# **********************************************************************************************************************


class MultiListbox(Frame):
    def __init__(self, master, lists):
        Frame.__init__(self, master)
        self.lists = []
        for l, w in lists:
            frame = Frame(self)
            frame.pack(side=LEFT, expand=YES, fill=BOTH)
            Label(frame, text=l, borderwidth=1, relief=RAISED, bg=bgcolor2, font=mainfont).pack(fill=X)
            lb = Listbox(frame, width=w, height = 30, borderwidth=0, selectborderwidth=0,
                         relief=FLAT, exportselection=FALSE, bg=bgcolor3, font=mainfont)
            lb.pack(expand=YES, fill=BOTH)
            self.lists.append(lb)
            lb.bind('<B1-Motion>', lambda e, s=self: s._select(e.y))
            lb.bind('<Button-1>', lambda e, s=self: s._select(e.y))
            lb.bind('<Leave>', lambda e: 'break')
            lb.bind('<B2-Motion>', lambda e, s=self: s._b2motion(e.x, e.y))
            lb.bind('<Button-2>', lambda e, s=self: s._button2(e.x, e.y))
            lb.bind('<Double-Button-1>', lambda e, s=self: print(self.get(self.curselection())[0]))
        frame = Frame(self)
        frame.pack(side=LEFT, fill=Y)
        Label(frame, borderwidth=1, relief=RAISED).pack(fill=X)
        sb = Scrollbar(frame, orient=VERTICAL, command=self._scroll)
        sb.pack(expand=YES, fill=Y)
        self.lists[0]['yscrollcommand'] = sb.set

    def _select(self, y):
        row = self.lists[0].nearest(y)
        self.selection_clear(0, END)
        self.selection_set(row)
        return 'break'

    def _button2(self, x, y):
        for l in self.lists:
            l.scan_mark(x, y)
        return 'break'

    def _b2motion(self, x, y):
        for l in self.lists:
            l.scan_dragto(x, y)
        return 'break'

    def _scroll(self, *args):
        for l in self.lists:
            try:
                l.yview(args[0], args[1], args[2])
            except IndexError:
                l.yview(args[0],args[1])

    def curselection(self):
        return self.lists[0].curselection()

    def delete(self, first, last=None):
        for l in self.lists:
            l.delete(first, last)

    def get(self, first, last=None):
        if first == ():
            return []
        result = []
        for l in self.lists:
            result.append(l.get(first, last))
        if last == first:
            return map([None] + result)
        return result

    def index(self, index):
        self.lists[0].index(index)

    def insert(self, index, *elements):
        for e in elements:
            i = 0
            for l in self.lists:
                l.insert(index, e[i])
                i = i + 1
        for l in self.lists:
            l.see(END)

    def size(self):
        return self.lists[0].size()

    def see(self, index):
        for l in self.lists:
            l.see(index)

    def selection_anchor(self, index):
        for l in self.lists:
            l.selection_anchor(index)

    def selection_clear(self, first, last=None):
        for l in self.lists:
            l.selection_clear(first, last)

    def selection_includes(self, index):
        return self.lists[0].selection_includes(index)

    def selection_set(self, first, last=None):
        for l in self.lists:
            l.selection_set(first, last)

# **********************************************************************************************************************


def load_base_button():
    """
    Функция, вызываемая при нажатии кнопки загрузки. Вынужденное использование глобальной переменной из-за особенностей
    вызова функции при нажатии кнопки. Загружает базу данных из двоичного файла в оперативную память.
    Автор: Игуменова Марта
    :return: None
    """
    global w
    w = byte(w, path1)
    update_output(multibox, w)


# **********************************************************************************************************************


def open_w_summary(f, bgcolor1, bgcolor3, mainfont, window):
    """
    Функция, вызываемая при нажатии кнопки подведения итого. Создаёт диалоговое с возможностью задания имени выходного
    файла
    Автор: Миронюк Даниил
    :param f: Список - выборка записей, подходящих по параметру
    :param bgcolor1: Цвет фона 1
    :param bgcolor3: Цвет фона 2
    :param mainfont: Список - Название шрифта и размер
    :return: None
    """
    askwindow = Toplevel(window)
    askwindow.config(bg=bgcolor3)
    askwindow.title("Сохранение файла")
    asklabel = Label(askwindow, text = "Введите название файла", bg=bgcolor3, font=mainfont)
    asklabel.grid(row=0)
    askentry = Entry(askwindow)
    askentry.grid(row=1)
    askentry.insert(0, "saved")
    askbutton = Button(askwindow, text="Сохранить файл", bg=bgcolor1, font=mainfont)
    askbutton.bind("<Button-1>", lambda e: summary(f, askentry))
    askbutton.grid(row=2, sticky=EW)
    quitbut1 = Button(askwindow, text="Выход", command=askwindow.destroy, bg=bgcolor1, font=mainfont)
    quitbut1.grid(row=3, columnspan=1, sticky=EW)

    askwindow.mainloop()


# **********************************************************************************************************************

# **********************************************************************************************************************

# **********************************************************************************************************************


def open_w_findbetween(w, bgcolor1, bgcolor2, bgcolor3, mainfont):
    """
    Функция, вызываемая при нажатии кнопки "Найти в диапазоне". Создаёт окно для ввода интересующих данных и запуска функции
    поиска записей со значением выбранного поля в заданном диапазоне
    Автор: Игуменова Марта
    :param w: Словарь словарей базы данных
    :param bgcolor1: Цвет фона 1
    :param bgcolor2: Цвет фона 2
    :param bgcolor3: Цвет фона 3
    :param mainfont: Список - Название шрифта, размер шрифта
    :return: None
    """
    betweenwind = Toplevel(root)
    betweenwind.config(bg=bgcolor3)
    betweenwind.title("Найти записи меньше опредленого значения")
    message = Label(betweenwind, text="Выберете интересующий ключ и диапазон", bg=bgcolor3, font=mainfont)
    message.grid(row=0, column=0, columnspan=3)
    ot = Label(betweenwind, text="От", bg=bgcolor3, font=mainfont)
    ot.grid(row=1, column=0)
    edit1 = Entry(betweenwind)
    edit1.grid(row=1, column=1)
    edit1.insert(0, '0')
    do = Label(betweenwind, text="До", bg=bgcolor3, font=mainfont)
    do.grid(row=2, column=0)
    edit2 = Entry(betweenwind)
    edit2.grid(row=2, column=1)
    edit2.insert(0, "0")
    kluchi = ["Год", "Масса", "Эф. масса", "Ступени"]
    kluch = StringVar()
    kluch.set(kluchi[0])
    opt = OptionMenu(betweenwind, kluch, *kluchi)
    opt.config(bg=bgcolor2)
    opt.grid(row=3, column=0, columnspan=3, sticky=NSEW)

    def start(w, bgcolor1, bgcolor2, bgcolor3, mainfont):
        """

        :param w:
        :return:
        """
        try:
            num1 = int(edit1.get())
            num2 = int(edit2.get())
        except ValueError or TypeError:
            mbox.showerror("Неверный ввод", "Введено неверное значение.")
            return
        start_function.grid_remove()
        opt.grid_remove()
        edit1.grid_remove()
        edit2.grid_remove()
        ot.grid_remove()
        do.grid_remove()
        message.grid_remove()
        key = kluch.get()
        if key == "Год":
            key = "year"
        elif key == "Масса":
            key = "mass"
        elif key == "Эф. масса":
            key = "efmass"
        elif key == "Ступени":
            key = "stages"
        f = find_between(w, key, num1, num2)
        label = Label(betweenwind, text="Записи с параметром " + str(key) + " от " + str(num1) + " до " + str(num2), bg=bgcolor3, font=mainfont)
        label.grid(row=0)
        itogo = Button(betweenwind, text="Подвести итоги", bg=bgcolor2, font=mainfont)
        itogo.grid(row=14, column=0, sticky=NSEW)
        itogo.bind("<Button-1>", lambda e: open_w_summary(f, bgcolor1, bgcolor3, mainfont, betweenwind))
        multibox = MultiListbox(betweenwind, (("Название", 17), ("Год", 17), ('Разработчик', 17), ('Масса', 17),
                                     ('Эфф. масса', 17), ('Ступени', 17)))
        multibox.grid(row=2)
        for i in f:
            multibox.insert(END, (str(i['name']), str(i['year']), str(i['dev']), str(i['mass']),
                                  str(i['efmass']), str(i['stages'])))
        quitbut1.grid(row=15, sticky=EW)

    start_function = Button(betweenwind, text="Старт", bg=bgcolor1, font=mainfont)
    start_function.bind("<Button-1>", lambda e: start(w, bgcolor1, bgcolor2, bgcolor3, mainfont))
    start_function.grid(row=4, column=0, sticky=NSEW, columnspan=3)
    quitbut1 = Button(betweenwind, text="Выход", command=betweenwind.destroy, font=mainfont, bg=bgcolor2)
    quitbut1.grid(row=3, columnspan=3, sticky=EW)
    betweenwind.mainloop()


# **********************************************************************************************************************


def open_w_findname(w, bgcolor1, bgcolor2, bgcolor3, mainfont):
    """
    Функция, вызываемая при нажатии кнопки "Поиск по имени". Создаёт окно для ввода интересующих данных и запуска функции
    поиска записей с заданным именем
    Автор: Животов Глеб
    :param w: Словарь словарей базы данных
    :param bgcolor1: Цвет фона 1
    :param bgcolor2: Цвет фона 2
    :param bgcolor3: Цвет фона 3
    :param mainfont: Список - Название шрифта, размер шрифта
    :return: None
    """
    findname= Toplevel(root)
    findname.config(bg=bgcolor3)
    findname.title("Найти записи c именем")
    message = Label(findname, text="Введите имя", bg=bgcolor3, font=mainfont)
    message.grid(row=0, column=0, sticky=NSEW)
    edit = Entry(findname)
    edit.grid(row=1, column=0, sticky=NSEW)

    def start(w, bgcolor1, bgcolor2, bgcolor3, mainfont):
        """

        :param w:
        :return:
        """
        name = edit.get()
        start_function.grid_remove()
        edit.grid_remove()
        message.grid_remove()
        f = find_name(w, name)
        label = Label(findname, text="Записи с именем " + str(name), bg=bgcolor3, font=mainfont)
        label.grid(row=0)
        itogo = Button(findname, text="Подвести итоги", bg=bgcolor2, font=mainfont)
        itogo.grid(row=14, column=0, sticky=NSEW)
        itogo.bind("<Button-1>", lambda e: open_w_summary(f, bgcolor1, bgcolor3, mainfont, findname))
        multibox = MultiListbox(findname, (("Название", 17), ("Год", 17), ('Разработчик', 17), ('Масса', 17),
                                     ('Эфф. масса', 17), ('Ступени', 17)))
        multibox.grid(row=2)
        for i in f:
            multibox.insert(END, (str(i['name']), str(i['year']), str(i['dev']), str(i['mass']),
                                  str(i['efmass']), str(i['stages'])))
        quitbut1.grid(row=15, sticky=EW)

    start_function = Button(findname, text="Старт", bg=bgcolor1, font=mainfont)
    start_function.grid(row=3, column=0, sticky=NSEW)
    start_function.bind("<Button-1>", lambda e: start(w, bgcolor1, bgcolor2, bgcolor3, mainfont))
    quitbut1 = Button(findname, text="Выход", command=findname.destroy, font=mainfont, bg=bgcolor2)
    quitbut1.grid(row=4, columnspan=3, sticky=EW)
    findname.mainloop()


# **********************************************************************************************************************


def click_add_node(w, namee, yeare, deve, masse, efmasse, stagese, multibox):
    """
    Функция, вызываемая при нажатии кнопки добавления новой записи. Считывает данные из полей и запускает функцию
    добавления записи
    Автор: Миронюк Даниил
    :param w: Словарь словарей базы данных
    :param namee: Объект класса Entry, содержащий новое имя
    :param yeare: Объект класса Entry, содержащий новый год
    :param deve: Объект класса Entry, содержащий нового разработчик
    :param masse: Объект класса Entry, содержащий новую массу
    :param efmasse: Объект класса Entry, содержащий новую эффективную массу
    :param stagese: Объект класса Entry, содержащий новое количество степеней
    :param multibox: Объект класса Multilistbox, который будет обновлён после добавления записи
    :return: None
    """
    name = namee.get()
    year = yeare.get()
    dev = deve.get()
    mass = masse.get()
    efmass = efmasse.get()
    stages = stagese.get()
    if name == '' or year == '' or dev == '' or mass == '' or efmass == '' or stages == '':
        mbox.showerror("Пустые поля", "Заполните поля перед добавлением записи")
        return
    add_node(w, name, year, dev, mass, efmass, stages)
    update_output(multibox, w)
    namee.delete(0, END)
    yeare.delete(0, END)
    deve.delete(0, END)
    masse.delete(0, END)
    efmasse.delete(0, END)
    stagese.delete(0, END)

# **********************************************************************************************************************


def click_change_node(w, namee, yeare, deve, masse, efmasse, stagese, multibox, key):
    """
    Функция, вызываемая при нажатии кнопки изменения записи. Считывает данные полей и запускает функцию изменения записи
    Автор: Животов Глеб
    :param w: Словарь словарей базы данных
    :param namee: Объект класса Entry, содержащий новое имя
    :param yeare: Объект класса Entry, содержащий новый год
    :param deve: Объект класса Entry, содержащий нового разработчик
    :param masse: Объект класса Entry, содержащий новую массу
    :param efmasse: Объект класса Entry, содержащий новую эффективную массу
    :param stagese: Объект класса Entry, содержащий новое количество степеней
    :param multibox: Объект класса Multilistbox, который будет обновлён после добавления записи
    :param key: Список полей записи, где 0 элемент - искомый ключ
    :return: None
    """
    try:
        key = key[0]
    except IndexError:
        mbox.showerror("Отсутсвует выделение", "Не выбрана строка для редактирования. Выберите и попробуйте снова")
        return
    name = namee.get()
    year = yeare.get()
    dev = deve.get()
    mass = masse.get()
    efmass = efmasse.get()
    stages = stagese.get()
    if name == '' or year == '' or dev == '' or mass == '' or efmass == '' or stages == '':
        mbox.showerror("Пустые поля", "Заполните поля перед редактированием записи")
        return
    change_node(w, key, name, year, dev, mass, efmass, stages)
    update_output(multibox, w)
    namee.delete(0, END)
    yeare.delete(0, END)
    deve.delete(0, END)
    masse.delete(0, END)
    efmasse.delete(0, END)
    stagese.delete(0,END)

# **********************************************************************************************************************


def filter_summary(f, bgcolor1, bgcolor2, bgcolor3, mainfont, filter_top):
    filter_summary_window = Toplevel(filter_top)
    summary_message = Label(filter_summary_window, text="Результаты выборки по фильтру: ")
    summary_message.grid(row=0, sticky=NSEW)
    summary_multibox = MultiListbox(filter_summary_window, (("Название", 17), ("Год", 17), ('Разработчик', 17),
                                                            ('Масса', 17), ('Эфф. масса', 17), ('Ступени', 17)))
    summary_multibox.grid(row=1, sticky=NSEW)
    for i in f.keys():
        summary_multibox.insert(END, (f[i]["name"], f[i]["year"], f[i]["dev"], f[i]["mass"], f[i]["efmass"],
                                      f[i]["stages"]))
    output_button = Button(filter_summary_window, text="Подвести итоги")
    output_button.grid(row=2, sticky=NSEW)
    output_button.bind("<Button-1>", lambda e: open_w_summary(f, bgcolor1, bgcolor3, mainfont, filter_summary_window))


def filter_start_click(w, bgcolor1, bgcolor2, bgcolor3, mainfont, year_from_entry, year_to_entry,
                       mass_from_entry, mass_to_entry, efmass_from_entry, efmass_to_entry,
                       stages_from_entry, stages_to_entry, filter_top):
    from_values = []
    tempyear = year_from_entry.get()
    from_values.append(tempyear)
    tempyear = mass_from_entry.get()
    from_values.append(tempyear)
    tempyear = efmass_from_entry.get()
    from_values.append(tempyear)
    tempyear = stages_from_entry.get()
    from_values.append(tempyear)
    for i in range(len(from_values)):
        if from_values[i] == '':
            from_values[i] = -float(inf)
        else:
            try:
                from_values[i] = float(from_values[i])
            except ValueError:
                mbox.showerror("Ошибка!", "Введите верный тип данных")
    to_values = []
    tempyear = year_to_entry.get()
    to_values.append(tempyear)
    tempyear = mass_to_entry.get()
    to_values.append(tempyear)
    tempyear = efmass_to_entry.get()
    to_values.append(tempyear)
    tempyear = stages_to_entry.get()
    to_values.append(tempyear)
    for i in range(len(to_values)):
        if to_values[i] == '':
            to_values[i] = float(inf)
        else:
            try:
                to_values[i] = float(to_values[i])
            except ValueError:
                mbox.showerror("Ошибка!", "Введите верный тип данных")
    editable = w
    keys = ["year", "mass", "efmass", "stages"]
    for i in range(4):
        editable = find_between(editable, keys[i], from_values[i], to_values[i])
    filter_summary(editable, bgcolor1, bgcolor2, bgcolor3, mainfont, filter_top)


def filter_window(w, bgcolor1, bgcolor2, bgcolor3, mainfont):
    filter_top = Toplevel(root)
    for x in range(5):
        filter_top.grid_columnconfigure(x, weight=1)
    filter_top.grid_columnconfigure(2, weight=4)
    filter_top.grid_columnconfigure(4, weight=4)
    for y in range(8):
        filter_top.grid_rowconfigure(y, weight=1)
    filter_top.config(bg=bgcolor3)
    filter_top.title("Поиск по фильтру")
    filter_message = Label(filter_top, text="Введите значения для поиска по фильтрам", bg=bgcolor3, font=mainfont)
    filter_message.grid(row=0, column=0, columnspan=5, sticky=NSEW)
    year_label = Label(filter_top, text="Год:", bg=bgcolor3, font=mainfont)
    year_label.grid(row=1, column=0, sticky=N+S+W)
    year_from_label = Label(filter_top, text="От", bg=bgcolor3, font=mainfont)
    year_from_label.grid(row=1, column=1, sticky=NSEW)
    year_from_entry = Entry(filter_top)
    year_from_entry.grid(row=1, column=2, sticky=NSEW)
    year_to_label = Label(filter_top, text="До", bg=bgcolor3, font=mainfont)
    year_to_label.grid(row=1, column=3, sticky=NSEW)
    year_to_entry = Entry(filter_top)
    year_to_entry.grid(row=1, column=4, sticky=NSEW)
    mass_label = Label(filter_top, text="Масса:", bg=bgcolor3, font=mainfont)
    mass_label.grid(row=3, column=0, sticky=N+S+W)
    mass_from_label = Label(filter_top, text="От", bg=bgcolor3, font=mainfont)
    mass_from_label.grid(row=3, column=1, sticky=NSEW)
    mass_from_entry = Entry(filter_top)
    mass_from_entry.grid(row=3, column=2, sticky=NSEW)
    mass_to_label = Label(filter_top, text="До", bg=bgcolor3, font=mainfont)
    mass_to_label.grid(row=3, column=3, sticky=NSEW)
    mass_to_entry = Entry(filter_top)
    mass_to_entry.grid(row=3, column=4, sticky=NSEW)
    efmass_label = Label(filter_top, text="Эффективная масса:", bg=bgcolor3, font=mainfont)
    efmass_label.grid(row=4, column=0, sticky=N+S+W)
    efmass_from_label = Label(filter_top, text="От", bg=bgcolor3, font=mainfont)
    efmass_from_label.grid(row=4, column=1, sticky=NSEW)
    efmass_from_entry = Entry(filter_top)
    efmass_from_entry.grid(row=4, column=2, sticky=NSEW)
    efmass_to_label = Label(filter_top, text="До", bg=bgcolor3, font=mainfont)
    efmass_to_label.grid(row=4, column=3, sticky=NSEW)
    efmass_to_entry = Entry(filter_top)
    efmass_to_entry.grid(row=4, column=4, sticky=NSEW)
    stages_label = Label(filter_top, text="Ступени:", bg=bgcolor3, font=mainfont)
    stages_label.grid(row=5, column=0, sticky=N+S+W)
    stages_from_label = Label(filter_top, text="От", bg=bgcolor3, font=mainfont)
    stages_from_label.grid(row=5, column=1, sticky=NSEW)
    stages_from_entry = Entry(filter_top)
    stages_from_entry.grid(row=5, column=2, sticky=NSEW)
    stages_to_label = Label(filter_top, text="До", bg=bgcolor3, font=mainfont)
    stages_to_label.grid(row=5, column=3, sticky=NSEW)
    stages_to_entry = Entry(filter_top)
    stages_to_entry.grid(row=5, column=4, sticky=NSEW)
    start_button = Button(filter_top, text="Поиск", bg=bgcolor2, font=mainfont)
    start_button.grid(row=6, columnspan=5, sticky=NSEW)
    start_button.bind("<Button-1>", lambda e: filter_start_click(w, bgcolor1, bgcolor2, bgcolor3, mainfont,
                                                                 year_from_entry, year_to_entry,
                                                                 mass_from_entry, mass_to_entry,
                                                                 efmass_from_entry, efmass_to_entry, stages_from_entry,
                                                                 stages_to_entry, filter_top))
    exit_button = Button(filter_top, text="Выход", bg=bgcolor2, font=mainfont)
    exit_button.grid(row=7, columnspan=5, sticky=NSEW)
# **********************************************************************************************************************


def open_w_save(w, path1):
    """
    Автор: Игуменова Марта
    Функция сохранения словаря словарей в двоичный файл
    :param w: Словарь словарей базы данных
    :param path1: Путь к двоичному файлу
    :return: None
    """
    ans = mbox.askokcancel("Сохранить базу данных?", "Двоичный файл будет изменён. Вы уверены?")
    if ans:
        f = open(path1, "wb")
        pickle.dump(w, f)
        f.close()


# **********************************************************************************************************************



# **********************************************************************************************************************



w ={}



root = Tk()
root.title("STAR BASE BIZARU ADVENTURES VER. 08.06")
img_change = PhotoImage(file=path3)
img_plus = PhotoImage(file=path4)
img_del = PhotoImage(file=path5)
img_load = PhotoImage(file=path6)
img_save = PhotoImage(file=path7)
img_rip_lil_pip = PhotoImage(file=path10)
filename = PhotoImage(file=path2)
background_label = Label(root, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

multiframe = Frame(root)
multiframe.grid(row=0, column=1, columnspan=8)

editframe = Frame(root, bg=bgcolor1)
editframe.grid(row=0, column=10, rowspan=33)

picbuttonframe = Frame(root)
picbuttonframe.grid(row=0, column=0, rowspan=33)

multibox = MultiListbox(multiframe, (("ID", 5), ("Название", 17), ("Год", 17), ('Разработчик', 17), ('Масса', 17),
                                     ('Эфф. масса', 17), ('Ступени', 17)))
multibox.pack()
filterbut = Button(picbuttonframe, text='Фильтр')
filterbut.grid(row=3)
filterbut.bind("<Button-1>", lambda e: filter_window(w, bgcolor1, bgcolor2, bgcolor3, mainfont))
namebut = Button(picbuttonframe, text='Поиск по имени')
namebut.grid(row=4)
namebut.bind("<Button-1>", lambda e: open_w_findname(w, bgcolor1, bgcolor2, bgcolor3, mainfont))
namel = Label(editframe, text="Название", bg=bgcolor1, font=mainfont)
namel.grid(row=0, column=0)
namee = Entry(editframe, bg=bgcolor1)
namee.grid(row=1, column=0)
yearl = Label(editframe, text="Год", bg=bgcolor1, font=mainfont)
yearl.grid(row=2, column=0)
yeare = Entry(editframe, bg=bgcolor1)
yeare.grid(row=3, column=0)
devl = Label(editframe, text="Разработчик", bg=bgcolor1, font=mainfont)
devl.grid(row=4, column=0)
deve = Entry(editframe, bg=bgcolor1)
deve.grid(row=5, column=0)
massl = Label(editframe, text="Масса", bg=bgcolor1, font=mainfont)
massl.grid(row=6, column=0)
masse = Entry(editframe, bg=bgcolor1)
masse.grid(row=7, column=0)
efmassl = Label(editframe, text="Эффективная масса", bg=bgcolor1, font=mainfont)
efmassl.grid(row=8, column=0)
efmasse = Entry(editframe, bg=bgcolor1)
efmasse.grid(row=9, column=0)
stagesl = Label(editframe, text="Количество ступеней", bg=bgcolor1, font=mainfont)
stagesl.grid(row=10, column=0)
stagese = Entry(editframe, bg=bgcolor1)
stagese.grid(row=11, column=0)

LoadBaseBut = Button(picbuttonframe, image=img_load)
LoadBaseBut.grid(row=5, column=0)
LoadBaseBut.bind("<Button-1>", lambda e: load_base_button())
ChangeButton=Button(picbuttonframe, image=img_change)
ChangeButton.grid(row=6, column=0)
ChangeButton.bind("<Button-1>", lambda e: click_change_node(w, namee, yeare, deve, masse, efmasse, stagese, multibox,
                                                            multibox.get(multibox.curselection())))
AddButton = Button(picbuttonframe, image=img_plus)
AddButton.grid(row=7, column=0)
AddButton.bind("<Button-1>", lambda e: click_add_node(w, namee, yeare, deve, masse, efmasse, stagese, multibox))
DelButton = Button(picbuttonframe, image=img_del)
DelButton.grid(row=8, column=0)
DelButton.bind("<Button-1>", lambda e: delete_node(w, multibox.get(multibox.curselection()), multibox))
SaveButton = Button(picbuttonframe, image=img_save)
SaveButton.grid(row=9, column=0)
SaveButton.bind("<Button-1>", lambda e: open_w_save(w, path1))


update_output(multibox, w)

quitbut = Button(picbuttonframe,command=root.destroy, image=img_rip_lil_pip)
quitbut.grid(row=10)


root.mainloop()
