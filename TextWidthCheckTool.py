import xlrd
import string
from xml.sax.handler import ContentHandler
from xml.sax import parse
import sys,os
import Fontlib

text_id_and_width_workbook = xlrd.open_workbook(r'./1.xls')
text_id_and_width_table = text_id_and_width_workbook.sheet_by_name(u'1')
text_id_colume_index = 2 #first colume A is 0, 2 means colume C
max_width_colume_index = 4
text_font_colume_index = 7

xml_file_path = r'./MIBG_GP_2217_M5_20160614'

textInfo = {}

for i in range(1,text_id_and_width_table.nrows):
    TextID = text_id_and_width_table.cell(i,text_id_colume_index).value.replace('.','_')
    if TextID[0:4] == 'LANG':
        textInfo[TextID] = {}
        #print TextID
        textInfo[TextID]['font'] = text_id_and_width_table.cell(i,text_font_colume_index).value[:-4]
        textInfo[TextID]['size'] = int(text_id_and_width_table.cell(i,text_font_colume_index).value[-2:])
        textInfo[TextID]['maxPixel'] = int(text_id_and_width_table.cell(i,max_width_colume_index).value)

class readTextTableHandler(ContentHandler):
    def __init__(self,arr):
        self.arr = arr
    def startElement(self,name,attrs):
        if name == 'LangID':
            self.arr[attrs['ID']] = attrs['Text']#.decode('gb18030')

English_text_table = {}
Chinese_text_table = {}

parse(xml_file_path + r'/Englisch_28USA29.xml',readTextTableHandler(English_text_table))
parse(xml_file_path + r'/Chinese_CN.xml',readTextTableHandler(Chinese_text_table))

def checkwidth(lang_table):
    for k in textInfo:
        if k in lang_table:
            eng_font_name = './unittest/VWThesis_MQB_Regular_140425.TTF'
            if textInfo[TextID]['font'] == u'VWThesis MIB Light':
                eng_font_name = './unittest/VWThesis_MQB_Light_140425.ttf'
            check_texts = lang_table[k].split('\\n')
            for t in check_texts:
                actual_width = Fontlib.GetTextWidth(eng_font_name,'./unittest/FZHT_GB18030.TTF',textInfo[k]['size'],t)
                if actual_width > textInfo[k]['maxPixel']:
                    print k
                    print 'actual_width =',actual_width,' maxPixel =',textInfo[k]['maxPixel'],' Text ='#,lang_table[k].decode('gb18030')
                    break

#print Chinese_text_table
print 'Checking English ...'
checkwidth(English_text_table)
print 'Checking Chinese ...'
checkwidth(Chinese_text_table)
