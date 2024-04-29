import re
from os import listdir
import json
import os

def clearTextInFile(path='') -> list:
    """
    Метод получает в параметр путь до файла 'blacklist.txt', или если он есть в проекте читает этот файл и оставляет все ссылки в 'result.txt' 
    """
    url = "blacklist.txt"
    if path:
        url = path
    listurl = []
    for i in open(url,'r', encoding='utf-8').read().split('\n'):
        line = i.replace(' ','')
        if i:
            if line[0] == '#':
                continue
            else:
                newurl = ''
                for j in line:
                    if j == '#':
                        break
                    else:
                        newurl+=j
                listurl.append(newurl)
    return listurl

def blackurlInText(text:str) -> bool:
    """
    Метод, который ищет ссылки в тексте и проверяет их на содержание запрещенных ссылок
    """
    for i in re.findall(r'https://\S+', text):
        for j in open('blacklist.txt','r', encoding='utf-8').read().split('\n'):
            if re.match(fr'{j}',i):
                return True
    return False

if __name__ == '__main__':
    result = ''
    for i in listdir('xacaton'):
        for j in listdir('xacaton\\'+str(i)):
            for d in listdir('xacaton\\'+i+'\\'+j):
                for c in listdir('xacaton\\'+i+'\\'+j+'\\'+d):
                    for b in listdir('xacaton\\'+i+'\\'+j+'\\'+d+'\\'+c):
                        result+='xacaton\\'+i+'\\'+j+'\\'+d+'\\'+c+'\\'+b+' - '+str(blackurlInText(json.loads(open('xacaton\\'+i+'\\'+j+'\\'+d+'\\'+c+'\\'+b,'r',encoding='utf-8').read())['text']))+'\n'
    open('resulttest.txt','w').write(result)
