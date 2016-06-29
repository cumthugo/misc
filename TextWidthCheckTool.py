import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import xlrd
import string
from xml.sax.handler import ContentHandler
from xml.sax import parse
import sys,os
import Fontlib

#parameter config

#config text id and width xls file.
text_id_and_width_workbook = xlrd.open_workbook(r'./1.xls')
text_id_and_width_table = text_id_and_width_workbook.sheet_by_name(u'1')
text_id_colume_index = 2 #first colume A is 0, 2 means colume C
max_width_colume_index = 4
text_font_colume_index = 7

#config xml file 
xml_file_path = './MIBG_GP_2217_M5_20160614'
xml_languages_file =['/Englisch_28USA29.xml','/Chinese_CN.xml', '/Portugiesisch_28Brasilien29.xml', '/Russisch.xml', '/Spanisch_28Mexiko29.xml'] 

#config font file name
font_light_file = './unittest/VWThesis_MQB_Light_140425.ttf'
font_regular_file = './unittest/VWThesis_MQB_Regular_140425.TTF'
font_chinese_file = './unittest/FZHT_GB18030.TTF'

textInfo = {}
for i in range(1,text_id_and_width_table.nrows):
    TextID = text_id_and_width_table.cell(i,text_id_colume_index).value.replace('.','_')
    if TextID[0:4] == 'LANG':
        textInfo[TextID] = {}
        #print TextID
        textInfo[TextID]['font'] = text_id_and_width_table.cell(i,text_font_colume_index).value[:-4]
        textInfo[TextID]['size'] = int(text_id_and_width_table.cell(i,text_font_colume_index).value[-2:])
        textInfo[TextID]['maxPixel'] = int(text_id_and_width_table.cell(i,max_width_colume_index).value)



def checkwidth(lang_table):
    for k in textInfo:
        if k in lang_table:
            eng_font_name = font_regular_file
            if textInfo[TextID]['font'] == u'VWThesis MIB Light':
                eng_font_name = font_light_file 
            check_texts = lang_table[k].split('\\n')
            for t in check_texts:
                actual_width = Fontlib.GetTextWidth(eng_font_name,font_chinese_file,textInfo[k]['size'],t)
                if actual_width > textInfo[k]['maxPixel']:
                    print k
                    print 'actual_width =',actual_width,' maxPixel =',textInfo[k]['maxPixel'],' Text =',t
                    break

class readTextTableHandler(ContentHandler):
    def __init__(self,arr):
        self.arr = arr
    def startElement(self,name,attrs):
        if name == 'LangID':
            self.arr[attrs['ID']] = attrs['Text']

English_text_table = {}
Chinese_text_table = {}
Brasilien_text_table = {}
Russisch_text_table = {}
Mexiko_text_table = {}

parse(xml_file_path + r'/Englisch_28USA29.xml',readTextTableHandler(English_text_table))
parse(xml_file_path + r'/Chinese_CN.xml',readTextTableHandler(Chinese_text_table))
parse(xml_file_path + r'/Portugiesisch_28Brasilien29.xml',readTextTableHandler(Brasilien_text_table))
parse(xml_file_path + r'/Russisch.xml',readTextTableHandler(Russisch_text_table))
parse(xml_file_path + r'/Spanisch_28Mexiko29.xml',readTextTableHandler(Mexiko_text_table))


print 'Checking English ...'
checkwidth(English_text_table)

print '\n\n\nChecking Chinese ...'
checkwidth(Chinese_text_table)

print '\n\n\nChecking Brasilien ...'
checkwidth(Brasilien_text_table)

print '\n\n\nChecking Russisch ...'
checkwidth(Russisch_text_table)

print '\n\n\nChecking Mexiko ...'
checkwidth(Mexiko_text_table)

