import daneTechniczneBosch
from bs4 import BeautifulSoup
import requests
import urllib.request
import time
import openpyxl
import re


wb = openpyxl.load_workbook(filename='test_1.xlsx')
sheet_m = wb['sheet']
sheet2 = wb['Sheet1']
staP = input('start point.. ')
endP = input('end point.. ')
count = 1
for a in range(int(endP)-int(staP)):
    try:
        sku = (sheet_m['a%s' % str(a+int(staP))].value)
        print(sku)
        if daneTechniczneBosch.count_table(sku) == 1:
            daneTech = ['']
            # tech info insertion
            sheet2['a%s' % str(a+int(staP))].value = sku
            val = ''
            daneTechh = daneTechniczneBosch.daneTechReturnCat_os(sku)
            for c in range(1, len(daneTechh)):
                val += (daneTechh[c] + "\n")
            sheet2['b%s' % str(a+int(staP))].value = val
            add = ''
            regex = re.compile(':\s\d+')
            for m in daneTechh:
                if regex.findall(m) == []:
                    continue
                tmp = (regex.findall(m))
                for i in range(len(tmp)):
                    tmp[i] = tmp[i].replace(': ', '')
                    add += " " + tmp[i] + "x"
                add = add[:-1]
            # picture insertion
            sheet_m['v%s' % str(a+int(staP))].value = daneTechniczneBosch.PictureGet_os(sku)
            # name insertion
            val = (daneTechniczneBosch.nameGet(sku))
            sheet_m['g%s' % str(a+int(staP))].value = val + add
            print(str(a+int(staP)), " - ", sku, " done")
        elif daneTechniczneBosch.count_table(sku) == 0:
            sheet_m['g%s' % str(a+int(staP))].value = 'nie ma strony'
            print(str(sku), 'nie ma strony')
        if count % 20 == 0:
            wb.save('test_1.xlsx')
            print(count, '!!SAVED!!')
        time.sleep(3)
        print("count=", str(a+int(staP)))
        count += 1
    except: 
        sheet_m['g%s' % str(a+int(staP))].value = ('error')
        count += 1
        print(sku, " - error occured")
wb.save('test_1.xlsx')
print('All done, final save')
