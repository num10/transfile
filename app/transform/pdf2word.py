#!/usr/bin/ python
# -*- coding: UTF-8 -*-

'''PDF文件转换成WORD文件'''


import sys
import importlib
from config import basedir

importlib.reload(sys)

from pdfminer.pdfparser import PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
import hashlib

def pdf2word(path):
    md5 = hashlib.md5()
    md5.update(path.encode('utf8'))
    filename = md5.hexdigest()
    wordfilename = filename + '.doc'

    fp = open(path, 'rb')
    praser = PDFParser(fp)
    doc = PDFDocument()
    praser.set_document(doc)
    doc.set_parser(praser)
    doc.initialize()

    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        for page in doc.get_pages():
            interpreter.process_page(page)
            layout = device.get_result()
            for x in layout:
                if (isinstance(x, LTTextBoxHorizontal)):
                    with open(basedir+'/app/downloads/'+filename+'.doc', 'a') as f:
                        results = x.get_text()
                        f.write(results + '\n')
    return wordfilename
