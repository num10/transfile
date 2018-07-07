#!/usr/bin/ python
# -*- coding: UTF-8 -*-

from PIL import Image
import pytesseract
import hashlib
from config import basedir


def pic2word(path):
    md5 = hashlib.md5()
    md5.update(path.encode('utf8'))
    filename = md5.hexdigest()
    wordfilename = filename+'.doc'

    text=pytesseract.image_to_string(Image.open(path),lang='chi_sim')
    with open(basedir+'/app/downloads/'+filename+'.doc', 'a') as file:
        file.write(text)
    return wordfilename
