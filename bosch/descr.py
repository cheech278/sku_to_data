import BoLib
from bs4 import BeautifulSoup
import requests
import urllib.request
import time
import openpyxl
import re


wb = openpyxl.load_workbook(filename='bruh.xlsx')
sheet_m = wb['Arkusz1']
staP = input('start point.. ')
endP = input('end point.. ')
count = 1
for a in range(int(endP)):
    try:
        sku = (sheet_m['a%s' % str(a+int(staP))].value)
        if BoLib.count_table(sku) == 1:
            sheet_m['b%s' % str(a+int(staP))].value = str(BoLib.descrGet_os(sku)[0])
            print(sku, " is done")
            print(count, "/", str(int(endP)))
        elif BoLib.count_table(sku) == 0:
            sheet_m['g%s' % str(a+int(staP))].value = 'nie ma strony'
            print(str(sku), 'nie ma strony')
        if count % 20 == 0:
            wb.save('test_1.xlsx')
            print(count, '!!SAVED!!')
        print("count=", str(a+int(staP)))
        count += 1
    except: 
        sheet_m['g%s' % str(a+int(staP))].value = ('error')
        count += 1
        print(sku, " - error occured")
wb.save('bruh.xlsx')
print('All done, final save')
