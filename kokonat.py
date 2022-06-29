import library
import re
from openpyxl import Workbook


cats = library.LinksCollector('links.txt')
catnames = []
library.CreateWB('PidorAndrei.xlsx')
for b in range (len(cats)):
        catnames.append(re.sub('https://www\.vidaxl\.com/g/\d+/','',cats[b]))
for i in range (len(catnames)):
    library.SkuCollector(catnames[i],'PidorAndrei.xlsx' )
    print (catnames[i])