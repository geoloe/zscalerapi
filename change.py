import openpyxl
import os
import random
import string

def genPSK():
    length = 64
    psk = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=length))
    return psk

def something(arg, filename):

    path = "/home/nea/zscaler/files/"
    new_name = "test_new.xlsx"
    xfile = openpyxl.load_workbook(path + 'test.xlsx')
    print(arg)
    new_name = filename
    if(arg == 'slcc'):
        sheet = xfile.get_sheet_by_name('Tabelle1')
        sheet['E1'] = genPSK()
    elif(arg == 'branch'):
        sheet = xfile.get_sheet_by_name('Tabelle1')
        sheet['D1'] = genPSK()
    else:
        sheet = xfile.get_sheet_by_name('Tabelle1')
        sheet['A1'] = genPSK()
    print(path + new_name)
    xfile.save(path + new_name)
    print(path)
    return new_name