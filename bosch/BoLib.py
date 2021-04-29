import os
from bs4 import BeautifulSoup
import requests
import urllib.request
import pandas as pd
import time
import inspect
from io import StringIO
from html.parser import HTMLParser
import openpyxl
import re



def sku_2_page_bosch(sku):
    URL = 'https://www.bosch-professional.com/pl/pl/searchfrontend/'
    payload = {'q': sku}
    page = requests.get(URL, params=payload)
    return page


def count_table(sku):
    page = sku_2_page_bosch(sku)
    content = page.text
    number = content.count('<table')
    if number == 1:
        return 1
    elif number == 0:
        return 0
    else:
        return 6


def CategoryGet_os(sku):
    daneTech = []
    page = sku_2_page_bosch(sku)
    content = page.text
    soup = BeautifulSoup(content, "html.parser")
    temp = soup.find("tr", id=sku)
    temp = temp.find("div")
    url = temp['data-ajax-src']
    page = requests.get(url)
    content = page.text
    soup = BeautifulSoup(content, "html.parser")
    temp = soup.div.find_all('table')
    daneTech = temp[1].find_all('tr')
    daneTechF = ['']
    count = 0
    for a in daneTech:
        if count == 0:
            count += 1
            continue
        sp_co = 0
        daneTechF.append('')
        for b in a.text:
            if (ord(b) != 10):
                daneTechF[count] += (b)
            elif sp_co == 1:
                daneTechF[count] += (" : ")
                sp_co += 1
            else:
                sp_co += 1
        count += 1
    return daneTechF


def CategoryGet_instr(sku):
    daneTech = ['']
    val = ''
    page = sku_2_page_bosch(sku)
    content = page.text
    soup = BeautifulSoup(content, "html.parser")
    temp = soup.find('div', class_="col-lg-8 col-xs-12")
    temp = temp.find_all('td')
    count = 2
    for x in temp:
        if count % 2 == 0:
            daneTech.append(temp[temp.index(x)].get_text())
        daneTech[temp.index(x)]=daneTech[temp.index(x)].replace('\xa0', '') 
    for c in range(1,len(daneTech)-1,2):
        val += str(daneTech[c]) + ' : ' + str(daneTech[c+1]) + '\n'
    return val


def PictureGet_os(sku):
    page = sku_2_page_bosch(sku)
    Pic = ([''])
    Picture = dict()
    content = page.text
    soup = BeautifulSoup(content, "html.parser")
    temp = soup.find("tr", id=sku)
    temp = temp.find("div")
    url = temp['data-ajax-src']
    page = requests.get(url)
    content = page.text
    soup = BeautifulSoup(content, "html.parser")
    Picture = soup.find('img', class_='media-gallery-img lazyload')
    Pic[0] = (Picture['data-src'])
    return Pic[0]


def PictureGet_instr(sku):
    page = sku_2_page_bosch(sku)
    Pic = ([''])
    Picture = dict()
    content = page.text
    soup = BeautifulSoup(content, "html.parser")
    temp = soup.find("div", id= "m-media-gallery-1")
    Picture = temp.find('img', class_='media-gallery-img lazyload')
    Pic[0] = (Picture['data-src'])
    return Pic[0]


def descrGet_os(sku):
    page = sku_2_page_bosch(sku)
    temp = ['']
    name = ['']
    content = page.text
    soup = BeautifulSoup(content, "html.parser")
    temp = soup.find("div", class_="m-product_hightlights__description")
    temp = temp.find_all('p')
    for a in range(len(temp)):
        name[0] += temp[a].text
    return name


def descrGet_instr(sku):
    page = sku_2_page_bosch(sku)
    temp = ['']
    name = ['']
    content = page.text
    soup = BeautifulSoup(content, "html.parser")
    temp = soup.find("ul", class_="m-product_hightlights__list")
    temp = temp.find_all('li')
    for a in range(len(temp)):
        name[0] += temp[a].text
    return name


def nameGet(sku):
    page = sku_2_page_bosch(sku)
    temp = ''
    content = page.text
    soup = BeautifulSoup(content, "html.parser")
    temp = soup.find("h1", class_="headline hl1")
    temp = temp.text
    temp += " Bosch"
    return temp


def nameGet_instr(sku):
     page = sku_2_page_bosch(sku)
     temp = ''
     content = page.text
     soup = BeautifulSoup(content, "html.parser")
     temp = soup.find("h1", class_="headline hl1")
     red = temp.find("span")
     red=red.text
     temp = temp.text
     temp=temp.replace(red, "")
     temp = temp.strip() + " Bosch"
     return temp


def splitter(string, ch):
    el_co = 0
    elem = ['']
    for a in string:
        if a != ch:
            elem[el_co] += a
        else:
            el_co += 1
            elem.append('')
    return elem


def vaulter(curre):
    vault = ['']
    tmp = splitter(curre, '/')
    vault[0] = tmp[0]
    for i in range(1, len(tmp)-1):
        vault.append(vault[i-1] + '/' + tmp[i])
    return vault


def ospsz_get(file):
    wb = openpyxl.load_workbook(filename=file)
    sheet_m = wb['sheet']
    sheet2 = wb['Sheet1']
    x = False
    while x == False:
        yeno = input('sleep? (y/n)')
        if (yeno == 'y') or (yeno == 'n'):
            x = True
        else:
            print('bruh')
    staP = input('start point.. ')
    endP = input('end point.. ')
    count = 1
    for a in range(int(endP)-int(staP)):
        try:
            sku = (sheet_m['a%s' % str(a+int(staP))].value)
            print(sku)
            if count_table(sku) == 1:
                # tech info insertion
                sheet2['a%s' % str(a+int(staP))].value = sku
                val = ''
                daneTechh = CategoryGet_os(sku)
                for c in range(1, len(daneTechh)):
                    val += (daneTechh[c] + "\n")
                sheet2['b%s' % str(a+int(staP))].value = val
                add = ''
                regex = re.compile(r':\s\d+')
                for m in daneTechh:
                    if regex.findall(m) == []:
                        continue
                    tmp = (regex.findall(m))
                    for i in range(len(tmp)):
                        tmp[i] = tmp[i].replace(': ', '')
                        add += " " + tmp[i] + "x"
                    add = add[:-1]
                # picture insertion
                sheet_m['v%s' % str(a+int(staP))].value = PictureGet_os(sku)
                # description insertion
                sheet_m['b%s' % str(a+int(staP))].value = str(descrGet_os(sku)[0])
                # name insertion
                val = (nameGet(sku))
                sheet_m['g%s' % str(a+int(staP))].value = val + add
                print(str(a+int(staP)), " - ", sku, " done")
            elif count_table(sku) == 0:
                sheet_m['g%s' % str(a+int(staP))].value = 'nie ma strony'
                print(str(sku), 'nie ma strony')
            if count % 20 == 0:
                wb.save('test_1.xlsx')
                print(count, '!!SAVED!!')
            print("count=", str(a+int(staP)))
            count += 1
            if yeno == 'y':
                time.sleep(3)
        except: 
            sheet_m['g%s' % str(a+int(staP))].value = ('error')
            count += 1
            print(sku, " - error occured")
    wb.save(file)
    print('All done, final save')


def tool_get(file)
    wb = openpyxl.load_workbook(filename = file)
    sheet1 = wb['sheet']
    sheet2 = wb['Sheet1']
    start = input("Start from ...")
    end = input("End on ...")
    x = False
    while x == False:
        yeno = input('sleep? (y/n)')
        if (yeno == 'y') or (yeno == 'n'):
            x = True
        else:
            print('bruh')
    for x in range(abs(int(start) - int(end))):
        try:
            sku = (sheet1["A%s" % str(x + int(start))].value)
            count = 0
            if count_table(sku) == 0:
                print (str(sku) + "not found")
            elif count_table(sku) > 0:
                descr = str(descrGet(sku)[0])
                pic = PictureGet(sku)
                daneTech = daneTechReturnCat(sku)
                name = str(nameGet(sku))
                sheet2['a%s' % str(a + int(start))].value = sku
                sheet2["B%s" % str(x + int(start))].value = daneTech
                sheet1["v%s" % str(x + int(start))].value = pic
                sheet1["D%s" % str(x + int(start))].value = descr
                sheet1["G%s" % str(x + int(start))].value = name
                count += 1
                print(sku + "DONE, next")
            if count % 5 == 0:
                wb.save(file)
                print ("Saved on " + sku)
        except:
            print(sku + " errored")
    if yeno == 'y':
        time.sleep(2)
    wb.save(file)

# table-based goods are working fine
# tools and stuff gotta be evaluated
