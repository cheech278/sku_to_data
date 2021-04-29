import BoLib
from bs4 import BeautifulSoup
import requests
import urllib.request
import time
import openpyxl
import re

wb = openpyxl.load_workbook(filename='test_1.xlsx')
sheet1 = wb['sheet']
sheet2 = wb['Sheet1']
start = input("Start from ...")
end = input("End on ...")
for x in range(abs(int(start) - int(end))):
    sku = (sheet1["A%s" % str(x + int(start))].value)
    print(sku)
    if BoLib.count_table(sku) == 0:
        print (str(sku) + "not found")
    elif BoLib.count_table(sku) > 0:
        descr = str(BoLib.descrGet_instr(sku)[0])
        pic = BoLib.PictureGet_instr(sku)
        daneTech = BoLib.daneTechReturnCat(sku)
        val = ''
        name = str(BoLib.nameGet_instr(sku))
        for c in range(1,len(daneTech)-1,2):
            val+=str(daneTech[c]) + ' : ' + str(daneTech[c+1]) + '\n'
        sheet1["B%s" % str(x+int(start))].value = val
        sheet1["C%s" % str(x+int(start))].value = pic
        sheet1["D%s" % str(x+int(start))].value = descr
        sheet1["G%s" % str(x+int(start))].value = name
    
wb.save("test_1.xlsx")
        