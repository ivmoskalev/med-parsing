import re
import datetime

from string import punctuation

from config import TABLES_HEADERS, TABLES_TITLES
from textprocessing import date_processing, table_title_clean
from tableheader import get_current_header


def cell_value_operate(value):
    value = value.replace(' ', '')
    value = re.sub(r'[-]+', '-', value)
    if value == '' or value == '-':
        result = 0
    else:
        match = re.search(r'(\d)', value)
        if match:
            try:
                result = float(value)
            except:
                result = value
        else:
            result = value
    

    return result

def generate_empty_table_data():
    result = {}
    for table, cells in TABLES_HEADERS.items():
        result[table] = {}
        for cell in cells:
            result[table][cell] = None

    return result

def get_table_data(table, table_data, entrance_date):
    for i in range(1,len(table.rows)):
        if table.rows[i].cells[0].text:
            test_date = get_test_date(table.rows[i].cells[0].text, entrance_date.year)
            if test_date and test_date >= entrance_date:

                header = get_current_header(table)
                # print(header)
                for k in range(len(table.rows[i].cells)):
                    table_key = header[k]
                    table_data_keys = table_data.keys()
                    if table_key in table_data_keys:
                        # table_key = table.rows[0].cells[k].text.lower().replace(' ', '')
                        # for p in punctuation:
                        #     table_key = table_key.replace(p, '')
                        if k == 0:
                            table_data[table_key] = test_date
                        else:
                            cell_value = cell_value_operate(table.rows[i].cells[k].text)
                            table_data[table_key] = cell_value
                return table_data

    return table_data

def get_test_date(date_str, year):
    date = date_processing(date_str)
    if not date:
        date = add_year(date_str, year)
    
    return date

def add_year(date_str, year):
    date_str = date_str.replace('/', '.').replace(' ', '')
    match = re.search(r'(\d+\.\d+)', date_str)
    if match:
        d = int(match.group(1).split('.')[0])
        m = int(match.group(1).split('.')[1])
        try:
            date = datetime.date(int(year), m, d)
        except ValueError:
            date = None
    else:
        date = None   
    return date
