import os
from bs4 import BeautifulSoup
import requests
import urllib.request
import pandas as pd
import time
import inspect
from io import StringIO
from html.parser import HTMLParser


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


# evaluation needed


def daneTechReturnCat(sku):
    daneTech = ['']
    page = sku_2_page_bosch(sku)
    content = page.text
    soup = BeautifulSoup(content, "html.parser")
    temp = soup.find('div', class_="col-lg-8 col-xs-12")
    temp = temp.find_all('td')
    count = 1
    for a in temp:
        if count % 2 == 0:
            daneTech[0] += (a[0], " : ")
            count += 1
        else:
            daneTech[0] += (a[0], "\n")
            count += 1
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


# ready (?)


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


# ready


def nameGet(sku):
    page = sku_2_page_bosch(sku)
    temp = ''
    name = ''
    content = page.text
    soup = BeautifulSoup(content, "html.parser")
    temp = soup.find("h1", class_="headline hl1")
    temp = temp.text
    temp += " Bosch"
    return temp


# table-based goods are working fine
# tools and stuff aren't developed
