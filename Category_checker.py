import openpyxl
import re


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


wb = openpyxl.load_workbook(filename='category_filling_imp.xlsx')
main_sheet = wb['Sheet1']
staP = input('start point')
endP = input('end point')
for a in range(int(staP), int(endP)):
    print('A', a)
    cell = main_sheet['e%s' % a].value
    path_elem = splitter(cell, ',')
    for i in path_elem:
        tmp = vaulter(i)
        for c in tmp:
            for_real_tho = False
            for b in path_elem:
                if c == b:
                    for_real_tho = True
                    break
            if for_real_tho is False:
                path_elem.append(c)
                print('in A', a, ' - ', c, 'appended')
    resul = ''
    for i in range(len(path_elem)):
        resul += path_elem[i] + ','
    resul = resul[:(len(resul)-1)]
    print(resul)
    main_sheet['e%s' % a] = resul
wb.save(filename='category_filling_imp.xlsx')
