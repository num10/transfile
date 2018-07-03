#!/usr/bin/ python
# -*- coding: UTF-8 -*-

import urllib.request
import hashlib
import sys

typ = sys.getfilesystemencoding()

def translate(querystr, to_l="zh", from_l="en"):
    C_agent = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.165063 Safari/537.36 AppEngine-Google."}
    flag = 'class="t0">'

    tarurl = "http://translate.google.cn/m?hl=%s&sl=%s&q=%s \
        " % (to_l, from_l, querystr.replace(" ", "+"))
    request = urllib.request.Request(tarurl, headers=C_agent)
    page = str(urllib.request.urlopen(request).read().decode())
    target = page[page.find(flag) + len(flag):]
    target = target.split("<")[0]
    return target

def translatefile(path):
    md5 = hashlib.md5()
    md5.update(path.encode('utf8'))
    filename = md5.hexdigest()
    wordfilename = filename + '.doc'

    strread=''
    with open(path,'r') as file:
        for char in file.read():
            if char=='\n':
                with open('/home/shihao/project/transfile/app/downloads/'+filename+'.doc', 'a') as f:
                    f.write(translate(strread)+'\n')
                strread=''
            else:
                strread += char
    return wordfilename


