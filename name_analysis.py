import re
import openpyxl


def numberGet(stri):
    match = re.search(r'\d+', stri)
    return match.group(0)


def clean_text(text):
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r"\\", "", text)
    text = re.sub(r"\'", "", text)
    text = re.sub(r"\"", "", text)
    text = re.sub(r'\w+\d+', "", text)
    text = re.sub(r"\w+\d+\w+", "", text)
    text = re.sub(r"\d+\w+", "", text)
    text = re.sub(r"\d+", "", text)
    text = text.strip().lower()
    filters = '!"\'#$%&()*+®Ø,-./:;<=>?@[\\]^_`{|}~\t\n'
    translate_dict = dict((c, " ") for c in filters)
    translate_map = str.maketrans(translate_dict)
    text = text.translate(translate_map)
    return text


def MERGESORT(array):
    if len(array) > 1:
        mid = len(array) // 2
        L = array[:mid]
        R = array[mid:]
        MERGESORT(L)
        MERGESORT(R)
        i = k = j = 0
        while i < len(L) and j < len(R):
            if int(numberGet(L[i])) > int(numberGet(R[j])):
                array[k] = L[i]
                i += 1
            else:
                array[k] = R[j]
                j += 1
            k += 1
        while i < len(L):
            array[k] = L[i]
            i += 1
            k += 1
        while j < len(R):
            array[k] = R[j]
            j += 1
            k += 1
    return array


wb = openpyxl.load_workbook(r'Python\\Test\\names.xlsx')
sheet = wb.active
all_the_words = ['']
for a in range(2, 24902):
    for i in clean_text(sheet['a%s' % a].value).split():
        if len(i) > 2:
            all_the_words.append('%s' % i)
    print('A', a, "total amount =", len(all_the_words))
unique_words = set(all_the_words)
counting_table = {}
all_the_words.pop(0)
for a in all_the_words:
    if a in counting_table:
        counting_table[a] = counting_table[a] + 1
    else:
        counting_table[a] = 1
result = ['']
count = 0
for a in counting_table:
    result.append('%s = %s\n' % (a, counting_table[a]))
result.pop(0)
result = MERGESORT(result)
file = open('names.txt', 'w', encoding='utf-8')
file.writelines(result)
file.close()
