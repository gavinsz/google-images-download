#coding=utf8
import codecs
from langconv import *

diff = codecs.open('diff.txt', 'w', 'utf-8', errors='ignore')
f = codecs.open('star-uc.txt', 'r', 'utf-8')
list_uc = []
line = f.readline() 
while line !='':
    line = line.strip('\r\n')
    list_uc.append(line)
    line = f.readline()

f.close()

f = codecs.open('明星-modify.txt', 'r', 'utf-8')
line = f.readline()
while line !='':
    tmp = line
    line = line.strip('\n')
    #转换繁体到简体
    line = Converter('zh-hans').convert(line)
    if line not in list_uc:
        diff.write(line+'\n')
        print(tmp, '=====>', line)

    line = f.readline()

f.close()
diff.close()


