import re
from types import NoneType
from openpyxl import load_workbook
import library
from openpyxl import Workbook
import random
import requests

wb=load_workbook('PidorAndrei.xlsx')
tegi = open('tegi.txt', 'r')
text = ''
for line in (tegi):
    if line == '\n' :
            text = text + line
    else:
        text = text + line.replace("\n","")
text = re.findall('.+',text)
dict = {}
newstuff = {}
for i in range (len(text)):
    text[i]=re.findall ('[^,]+',text[i])
    newstuff = {text[i][0]:text[i]}
    dict.update(newstuff)
    dict_del=text[i][0]
    dict[dict_del].remove(dict_del)

cats = library.LinksCollector('links.txt')
catnames = []
resultdict = {}
for b in range (len(cats)):
        catnames.append(re.sub('https://www\.vidaxl\.com/g/\d+/','',cats[b]))
for l in range(len(cats)):
        link = cats[catnames.index(catnames[l])]
        results=(re.findall('\(.+ Results\)',requests.get(link).text))
        results[0]=re.sub(',',"",results[0])
        results =re.findall('\d+',results[0])
        results = results[0]
        newres = {catnames[l]:results}
        resultdict.update(newres)
for i in range (len(catnames)):
    wsx=wb.get_sheet_by_name(name=catnames[i])
    wsx['D1']= "Tags"
    print (resultdict[catnames[i]])
    for b in range (int(resultdict[catnames[i]])):
        randomina = ''
        if len(dict[catnames[i]])>= 13:
            randomika = random.sample(dict[catnames[i]],13)
            for i in range (len(randomika)):
                randomina = randomina + str(randomika[i])+','
            wsx['D'+str(b+2)]=randomina
        else:
            randomika = random.sample(dict[catnames[i]],len(dict[catnames[i]]))
            for i in range (len(randomika)):
                randomina = randomina + str(randomika[i])+','
            wsx['D'+str(b+2)]=randomina
    wb.save(filename='PidorAndreitags.xlsx')

#try:
    #randomtaginator = random.sample(dict['benches'],13)
    #print (randomtaginator)
#except:
    #print('too many tags for me')

