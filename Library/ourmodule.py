import pickle
from tkinter import *
from tkinter import messagebox as mbox
import os
from math import inf


def byte(w, path1):
    """
    Функци считывания базы из двоичного файла
    Автор: Животов Глеб
    :param w: Словарь словарей базы данных
    :param path1: Путь к двоичному файлу
    :return: Словарь словарей базы данных
    """
    f = open(path1, "rb")
    w = pickle.load(f)
    f.close()
    return w


def update_output(listbox, w):
    """
    Функция обновления окна вывода
    Автор: Игуменова Марта
    :param listbox: Объект класса Multibox, который будет обновлён
    :param w: Словарь словарей который загрузится в listbox
    :return: None
    """
    listbox.delete(0, END)
    for a in w.keys():
        listbox.insert(END, (str(a), str(w[a]['name']), str(w[a]['year']), str(w[a]['dev']), str(w[a]['mass']),
                             str(w[a]['efmass']), str(w[a]['stages'])))




def summary(f, askentry):
    """
    Функция расчёта отклонений и записи результата в файл
    Автор: Миронюк Даниил
    :param f: Список - выборка записей, подходящих по параметру
    :param askentry: Объект класса Entry, из которого будет считано имя файла
    :return: None
    """
    outname = askentry.get()
    if outname == '':
        mbox.showerror("Отсутствует название", "Введите название файла")
        return
    keys = ["year", "mass", "efmass", "stages"]
    average = {}  # Словарь, содержащий средние значения клюей keys, его нужно вывести в файл вместе с записями
    kvadr = {}  # Словарь КВАДРАТОВ среднекважратичных отклонений от среднеарифметического, вывод в файл
    disp = {}  # Словарь дисперсии, вывод в файл
    k = len(f)
    if k == 0:
        for key in keys:
            average[key] = 0
            kvadr[key] = 0
            disp[key] = 0
    elif k == 1:
        for key in keys:
            s = 0
            kv = 0
            for node in f:
                s += float(node[key])
                kv += float(node[key])*float(node[key])
            average[key] = float(s)/k
            kvadr[key] = 0
            disp[key] = 0
    else:
        for key in keys:
            s = 0
            kv = 0
            for node in f.keys():
                s += float(f[node][key])
                kv += float(f[node][key])*float(f[node][key])
            average[key] = float(s)/k
            kvadr[key] = kv/k - average[key]*average[key]
            disp[key] = (kv - 2*average[key]*s + k*average[key]*average[key])/(k-1)
    outname += '.txt'
    path = os.getcwd()
    n = path.find("\Scripts")
    path1 = os.path.join(path[0:n] + "\Output", outname)
    fileout = open(path1, "w")
    for node in f.keys():
        print(f[node]['name'], f[node]['year'], f[node]['dev'], f[node]['mass'], f[node]['efmass'], f[node]['stages'],
              file=fileout)
    print("Средние значения", file=fileout)
    print("Год: ", average['year'], "Отклонение от среднего арифметического: ", kvadr['year']**0.5,
          "Дисперсия: ", disp['year'], file=fileout)
    print("Масса: ", average['mass'], "Отклонение от среднего арифметического: ", kvadr['mass']**0.5,
          "Дисперсия: ", disp['mass'], file=fileout)
    print("Эфективная масса: ", average['efmass'], "Отклонение от среднего арифметического: ", kvadr['efmass']**0.5,
          "Дисперсия: ", disp['efmass'], file=fileout)
    print("Ступени: ", average['stages'], "Отклонение от среднего арифметического: ", kvadr['stages']**0.5,
          "Дисперсия: ", disp['stages'], file=fileout)
    mbox.showinfo("Сохранено!", "Сохранение успешно")


def find_between(w, key, minnum=-float(inf), maxnum=float(inf)):
    """
    Автор: Животов Глеб
    Функция поиска записей, значение в поле key которых больше min и меньше max
    :param w: Словарь словарей с данными базы
    :param min: минимальное значение столбца
    :param max: максимальное значение столбца
    :param key: Ключ столбца, в котором происходит поиск
    :return: Список подходящих записей
    """
    if minnum > maxnum:
        temp = minnum
        minnum = maxnum
        maxnum = temp
    f = {}
    i = 0
    for a in w.keys():
        if (float(w[a][key]) >= minnum) & (float(w[a][key]) <= maxnum):
            f[str(i)] = w[a]
            i += 1
    return f

def find_name(w,name):
    """
    Автор: Миронюк Даниил
    Функция поиска записей с именем, введённым пользователем
    Получает на вход список словарей w
    Возвращает список ключей списка w
    """
    f = []
    for i in w.keys():
        if w[i]['name'] == name:
            f.append(w[i])
    return f

def add_node(w,new_name='',new_year='',new_dev='',new_mass='',new_efmass='',new_stages=''):
    """
    Функция добавления записи в словарь словарей
    Автор: Животов Глеб
    :param w: Словарь словарей базы данных
    :param new_name: Имя новой записи
    :param new_year: Год новой записи
    :param new_dev: Разработчик новой записи
    :param new_mass: Масса новой записи
    :param new_efmss: Эффективная масса новой записи
    :param new_stages: Количество ступеней новой записи
    :return: Изменённый словарь словарей базы данных
    """
    i=0
    while str(i) in w.keys():
        i += 1
    w[str(i)] = {
        "name": new_name,
        "year": new_year,
        "dev": new_dev,
        "mass": new_mass,
        "efmass": new_efmass,
        "stages": new_stages
    }
    return w

def change_node(w, key, cname='', cyear='', cdev='', cmass='', cefmass='', cstages=''):
    """
    Функция изменения существующей записи
    Автор: Миронюк Даниил
    :param w: Словарь словарей базы данных
    :param key: Ключ изменяемой записи
    :param cname: Новое имя
    :param cyear: Новый год
    :param cdev: Новый разработчик
    :param cmass: Новая масса
    :param cefmass: Новая эффективная масса
    :param cstages: Новое количество ступеней
    :return: Изменённый словарь словарей
    """
    if cname != '':
        w[str(key)]["name"] = cname
    if cyear != '':
        w[str(key)]["year"] = cyear
    if cdev != '':
        w[str(key)]["dev"] = cdev
    if cmass != '':
        w[str(key)]["mass"] = cmass
    if cefmass != '':
        w[str(key)]["efmass"] = cefmass
    if cstages != '':
        w[str(key)]["stages"] = cstages
    return w

def delete_node(w, key, multibox):
    """
    Функция удаления записи
    Автор: Игуменова Марта
    :param w: Словарь словарей базы данных
    :param key: Список полей записи, где 0 элемент - искомый ключ
    :param multibox: Объект класса Multilistbox, который будет обновлён после удаления
    :return: None
    """
    try:
        key = key[0]
    except IndexError:
        mbox.showerror("Отсутсвует выделение", "Не выбрана строка для удаления. Выберите и попробуйте снова")
        return
    w.pop(str(key))
    update_output(multibox, w)