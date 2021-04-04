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


# ready


def sku_2_page_bosch(sku):
    URL = 'https://www.bosch-professional.com/pl/pl/searchfrontend/'
    payload = {'q': sku}
    page = requests.get(URL, params=payload)
    return page


# ready


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


# seems ready


def daneTechReturnCat_os(sku):
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


# vrode ready


def daneTechReturnCat(sku):
    daneTech = ['']
    page = sku_2_page_bosch(sku)
    content = page.text
    soup = BeautifulSoup(content, "html.parser")
    temp = soup.find('div', class_="col-lg-8 col-xs-12")
    temp = temp.find_all('td')
    count=2
    for x in temp:
        if count % 2 ==0:
         daneTech.append(temp[temp.index(x)].get_text())
         daneTech[temp.index(x)]=daneTech[temp.index(x)].replace('\xa0', '') 
    return daneTech


# legacy function


def daneTechReturnVal_os(sku):
    daneTech = []
    page = sku_2_page_bosch(sku)
    content = page.text
    soup = BeautifulSoup(content, "html.parser")
    daneTech = soup.table.find('tr', id=sku)
    return daneTech


# ready

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

#ready
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

# ready


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

# ready


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


#instruments functions


# ready(not tested as a function) 


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


# ready(not tested as a function) 


def vaulter(curre):
    vault = ['']
    tmp = splitter(curre, '/')
    vault[0] = tmp[0]
    for i in range(1, len(tmp)-1):
        vault.append(vault[i-1] + '/' + tmp[i])
    return vault


# ready(not tested as a function) 


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
                daneTechh = daneTechReturnCat_os(sku)
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


# table-based goods are working fine
# tools and stuff aren't developed
