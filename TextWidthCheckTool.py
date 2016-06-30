import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import xlrd
from xml.sax.handler import ContentHandler
from xml.sax import parse
import os
import Fontlib

#parameter config

#config text id and width xls file.
text_id_and_width_workbook = xlrd.open_workbook(r'./1.xls')
text_id_and_width_table = text_id_and_width_workbook.sheet_by_name(u'1')
text_id_colume_index = 2 #first colume A is 0, 2 means colume C
max_width_colume_index = 4
text_font_colume_index = 7

#config xml file
xml_file_path = r'./MIBG_GP_2217_M5_20160614/'
xml_languages_file =[r'Englisch_28USA29.xml',r'Chinese_CN.xml', r'Portugiesisch_28Brasilien29.xml', r'Russisch.xml', r'Spanisch_28Mexiko29.xml']

#config font file name
font_light_file = r'./VWThesis_MQB_Light_140425.ttf'
font_regular_file = r'./VWThesis_MQB_Regular_140425.TTF'
font_chinese_file = r'./FZHT_GB18030.TTF'

##############################################################################
#implementation below, please don't modify anything if you don't know, thanks.
##############################################################################
def read_text_id_and_max_width():
    text_info = {}
    for i in range(1,text_id_and_width_table.nrows):
        TextID = text_id_and_width_table.cell(i,text_id_colume_index).value.replace('.','_')
        if TextID[0:4] == r'LANG': #this is a filter, ignore some invalid text id
            text_info[TextID] = {}
            #print TextID
            text_info[TextID]['font'] = text_id_and_width_table.cell(i,text_font_colume_index).value[:-4] #:-4 means don't get the last 4 chars
            text_info[TextID]['size'] = int(text_id_and_width_table.cell(i,text_font_colume_index).value[-2:]) #-2: mean get the last 2 chars
            text_info[TextID]['maxPixel'] = int(text_id_and_width_table.cell(i,max_width_colume_index).value)
    return text_info


#read the output mode
def output_all_text():
    if len(sys.argv) < 2:
        return False
    return sys.argv[1] == 'all'

def check_width_which_larger_than_maxwidth(lang_table):
    text_id_width_info = read_text_id_and_max_width()
    for text_id in text_id_width_info:
        if text_id in lang_table:
            eng_font_name = font_regular_file
            if text_id_width_info[text_id]['font'] == u'VWThesis MIB Light':
                eng_font_name = font_light_file
            check_texts = lang_table[text_id].split('\\n')
            for text_line in check_texts:
                actual_width = Fontlib.GetTextWidth(eng_font_name,font_chinese_file,text_id_width_info[text_id]['size'],text_line)
                if output_all_text():
                    print text_id
                    print 'actual_width =',actual_width,' maxPixel =',text_id_width_info[text_id]['maxPixel'],' Text =',text_line, 'font =',text_id_width_info[text_id]['font'], 'size =', text_id_width_info[text_id]['size']
                elif actual_width > text_id_width_info[text_id]['maxPixel']:
                    print text_id
                    print 'actual_width =',actual_width,' maxPixel =',text_id_width_info[text_id]['maxPixel'],' Text =',text_line, 'font =',text_id_width_info[text_id]['font'], 'size =', text_id_width_info[text_id]['size']
                    break

class readTextTableHandler(ContentHandler):
    def __init__(self,arr):
        self.arr = arr
    def startElement(self,name,attrs):
        if name == 'LangID':
            self.arr[attrs['ID']] = attrs['Text']

def check_xml_text_width(xml_file):
    text_table = {}
    parse(xml_file_path + xml_file, readTextTableHandler(text_table))
    print '\n\n\nChecking ',xml_file
    check_width_which_larger_than_maxwidth(text_table)

for xml_filename in xml_languages_file:
    check_xml_text_width(xml_filename)
