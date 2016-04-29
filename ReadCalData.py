import re

class ReadFieldErrorException(Exception):pass

def get_text(text,start,end):
    #print 'start:',start,'*** end:',end
    ret = re.findall('('+start+'(.*\s*)*?)'+end,text)
    if ret:
        return ret[0][0]
    else:
        raise ReadFieldErrorException

def text_find(pat,text):
    ret = re.findall(pat,text)
    if ret:
        return ret[0]
    else:
        raise ReadFieldErrorException


folder_path = r'E:\private\python\Tools\\'


#check input file.
#fill field
#single calc result
#muti calc result
#output values


def get_Cal(text):
    ret = []
    for i in range(0x20):
        s ='result\[' + '%02X'%i + '\]=(0x[0-9A-F]*)'
        v = text_find(s,text)
        ret.append(v)
    return ret

def get_ReadCal(text):    
    read_cal_text = get_text(text,'Starting Read calibration','Byte 0')
    return get_Cal(read_cal_text)
    
def get_WriteCal(text):
    write_cal_text = get_text(text,'Starting Write calibration','Byte 0')
    return get_Cal(write_cal_text)

def get_Byte(text):
    ret = []
    byte_text = [get_text(text,'BYTE '+str(i),'BYTE') for i in range(3)]
    byte_text.append(get_text(text,'BYTE 3','DQS calibration'))
    for i in range(4):
        start_hc, start_abs = text_find('Start:\s*HC=(0x[0-9A-F]*) ABS=(0x[0-9A-F]*)',byte_text[i])       
        end_hc, end_abs = text_find('End:\s*HC=(0x[0-9A-F]*) ABS=(0x[0-9A-F]*)',byte_text[i])        
        ret.append({'start':[start_hc,start_abs],'end':[end_hc,end_abs]})
    return ret

def get_MMDC_MPWLDECTRL(i,text):
    return text_find('MMDC_MPWLDECTRL'+str(i)+'.*?= (0x[0-9A-F]*)',text)

def check_file(file_path):
    try:
        f = open(file_path)
        t = f.read().replace('\r\n','\n')
        ctrl0 = get_MMDC_MPWLDECTRL(0,t)
        ctrl1 = get_MMDC_MPWLDECTRL(1,t)
        byte = get_Byte(t)
        read_cat = get_ReadCal(t)
        write_cat = get_WriteCal(t)
        return True
    except:
        return False

import unittest

class CheckInputFileTestCase(unittest.TestCase):

    def testCorrectFile(self):
        self.failUnless(check_file(folder_path + '1.log'),'Correct file but check failed!')
    
    def testFileNotExist(self):
        self.failIf(check_file(folder_path + 'not_exist.log'),'File Not exist should return false!')   
    
    def testEmptyFile(self):
        self.failIf(check_file(folder_path + 'empty.log'),'Empty file should return false')

    def testCtrlError(self):
        self.failIf(check_file(folder_path + 'ctrl_error.log'),'Ctrl field error should return false')
    
    def testByteError(self):
        self.failIf(check_file(folder_path + 'byte_error.log'),'Byte field error should return false')

    def testReadCalError(self):
        self.failIf(check_file(folder_path + 'read_cal_error.log'),'Read Cal field error should return false')
    
    def testReadCalDataError(self):
        self.failIf(check_file(folder_path + 'read_cal_data_error.log'),'Read Cal field error should return false')

    def testWriteCalError(self):
        self.failIf(check_file(folder_path + 'write_cal_error.log'),'Write Cal field error should return false')
    
    def testWriteCalDataError(self):
        self.failIf(check_file(folder_path + 'write_cal_data_error.log'),'Write Cal field error should return false')

try:
    unittest.main()
except:
    pass


"""
    some experiments
"""

f = open(folder_path + '1.log','r')
file_text = f.read().replace('\r\n','\n')

byte_text = [get_text(file_text,'BYTE '+str(i),'BYTE') for i in range(3)]
byte_text.append(get_text(file_text,'BYTE 3','DQS calibration'))
#print byte_text
read_cal_text = get_text(file_text,'Starting Read calibration','Byte 0')
#print read_cal_text
write_cal_text = get_text(file_text,'Starting Write calibration','Byte 0')
#print write_cal_text



ctrl0 = text_find('MMDC_MPWLDECTRL0.*?= (0x[0-9A-F]*)',file_text)
ctrl1 = text_find('MMDC_MPWLDECTRL1.*?= (0x[0-9A-F]*)',file_text)
print 'MMDC_MPWLDECTRL0=',ctrl0
print 'MMDC_MPWLDECTRL1=',ctrl1

for i in range(4):
    start_hc, start_abs = text_find('Start:\s*HC=(0x[0-9A-F]*) ABS=(0x[0-9A-F]*)',byte_text[i])
    print 'Start:',start_hc, start_abs
    end_hc, end_abs = text_find('End:\s*HC=(0x[0-9A-F]*) ABS=(0x[0-9A-F]*)',byte_text[i])
    print 'End:',end_hc, end_abs

print '\nread:'
for i in range(0x20):
    s ='result\[' + '%02X'%i + '\]=(0x[0-9A-F]*)'
    v = text_find(s,read_cal_text)
    print '%02X'%(i*4),v

print '\nwrite:'
for i in range(0x20):
    s ='result\[' + '%02X'%i + '\]=(0x[0-9A-F]*)'
    v = text_find(s,write_cal_text)
    print '%02X'%(i*4),v
