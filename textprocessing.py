import re
import string
import datetime

from config import DISEAS_DICT


def sublist(sublist, lst):
    sublist_len = len(sublist)
    k=0
    # s=None

    if (sublist_len > len(lst)):
        return False
    elif (sublist_len == 0):
        return True

    for x in sublist:
        if x in lst:
            k += 1
            if k == sublist_len:
                return True

    # for x in lst:
    #     if x == sublist[k]:
    #         if (k == 0): s = x
    #         elif (x != s): s = None
    #         k += 1
    #         if k == sublist_len:
    #             return True
    #     elif k > 0 and sublist[k-1] != s:
    #         k = 0

    return False

def clear_diseas(diseas):
    bronh = ['d0', 'd2', 'd4', 'd20', 'd23']
    pnev = ['d9', 'd10']
    if any(x == 1 for x in [diseas[k] for k in bronh]):
        diseas['d1'] = 0
    if any(x == 1 for x in [diseas[k] for k in pnev]):
        diseas['d11'] = 0

    return diseas

def diseas_matcher(diagnosis):
    temp_str = diagnosis
    for char in string.punctuation:
        temp_str = temp_str.replace(char, ' ')
    temp_str = re.sub(' +', ' ', temp_str.lower())
    # tokens = temp_str.split(' ')
    tokens = temp_str
    diseas_match = {}

    for k in DISEAS_DICT.keys():
        if sublist(DISEAS_DICT[k], tokens):
            diseas_match['d'+str(k)] = 1
        else:
            diseas_match['d'+str(k)] = 0

    diseas = clear_diseas(diseas_match)

    return diseas


def get_patient_id(paragraph):
    # result = paragraph.split('№')[1].strip()
    result = paragraph.split(':')
    if len(result) > 1:
        return result[1].strip()
    else:
        return f'!!!!!!!!!!!!WARNING!!!!!!!!!!!!  {paragraph}'

"""
Попытка восстановить дату, полученную в 
результате опечатки
Обработаны случаи:
    1. ХХХХ.ХХ
    2. ХХ.ХХХХ
    3. исключение 01.01.2050
"""
def repair_date(bad_date):
    if len(bad_date[0]) == 4:
        repaired_date = '.'.join([bad_date[0][:2], bad_date[0][2:], bad_date[1]])
    elif len(bad_date[1]) == 4 or len(bad_date[1]) == 6:
        repaired_date = '.'.join([bad_date[0], bad_date[1][:2], bad_date[1][2:]])
    else:
        repaired_date = '01.01.2050'
    return repaired_date.split('.') 

"""
Конвертирует строку в дату
"""
def date_processing(datestring):
    datestring = datestring.replace('/', '.').replace(' ', '')
    datestring = datestring.replace(',', '.').replace('..', '.')
    match = re.search(r'(\d+\.\d+\.\d+)', datestring)
    if match:
        date_split = match.group(1).split('.')
        if len(date_split) == 3:
            year = date_split[2]
        elif len(date_split) == 2:
            date_split = repair_date(date_split)
            year = date_split[2]
        else:
            return None
        date_str = '.'.join(date_split)
        if len(year) == 4:
            try:
                return datetime.datetime.strptime(date_str, "%d.%m.%Y").date()
            except ValueError:
                return None
        else:
            try:
                return datetime.datetime.strptime(date_str, "%d.%m.%y").date()
            except ValueError:
                return None
    else:
        return None

"""
Получение возраста из текста
Обработка случав:
    1. число слово число
    2. число 
        2.1. есть символы 'г', 'л' (год, лет и т.д.)
        2.2. есть символ 'м' (месяц)
        2.3. исключение возраст 9999
    3. исключение возраст 7777
"""
def get_age(paragraph):
    result = 0
    text = paragraph.split(':')[1].replace(' ', '')
    match = re.search(r'(\d+)\D+(\d+)', text)
    if match:
        result += (int(match.group(1)) * 12 + int(match.group(2)))
    else:
        match = re.search(r'(\d+)', text)
        if match:
            if re.search(r'([гл])', text):
                result += int(match.group(1)) * 12
            elif re.search(r'([м])', text):
                result += int(match.group(1))
            else:
                result += 9999
        else:
            result += 7777

    return result

"""
Получение даты рождения из текста
Если даты нет, то попытка получить возраст
"""
def get_patient_birth_date(paragraph):
    birth_date = date_processing(paragraph)
    if not birth_date:
        birth_date = get_age(paragraph)
    return birth_date

"""
Получение адрса (текст после ':')
"""

def get_patient_adress(paragraph):
    return paragraph.split(':')[1].strip()

"""
Получение примерной даты рождения из даты поступления
и возраста в месяцах
"""
def approx_birth_date(date, delta):
    month = ((date.month - delta - 1) % 12) + 1
    year = date.year + ((date.month - delta - 1) // 12)
    day = 15
    return date.replace(day=day, month=month, year=year)

"""
Очистка текста для распознавания заколовка таблицы
Удаляет все цифры и некоторые символы пунктуации ',@'?.$%'
переводит текст в нижний регистр и убирает лишние пробелы
"""
def table_title_clean(text):
    return re.sub(r'[,@\'?\.$%_\d]', '', text).lower().strip()

"""
Очистка текста для работы с именами колонок
Удаляет все не текстовые символы переводит текст в 
нижний регистр и убирает пробелы
"""
def table_header_clean(text):
    return re.sub(r'\W', '', text).lower().strip()