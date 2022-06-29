import requests
import re
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl import load_workbook
import library
import time

start = time.time()

catnames =[]
cats=library.LinksCollector('links.txt')
for b in range (len(cats)):
        catnames.append(re.sub('https://www\.vidaxl\.com/g/\d+/','',cats[b]))
for l in range(len(cats)):
        link = cats[catnames.index('benches')]
        results=(re.findall('\(.+ Results\)',requests.get(link).text))
        results[0]=re.sub(',',"",results[0])
        results =re.findall('\d+',results[0])
end = time.time()
total_time = end - start
print("\n"+ str(total_time))


print (results)