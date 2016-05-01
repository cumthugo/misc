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

folder_path = r'./'

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

def get_file_context(file_path):
     f = open(file_path)
     return f.read().replace('\r\n','\n')

def check_file(file_path):
    try:
        t = get_file_context(file_path)
        ctrl0 = get_MMDC_MPWLDECTRL(0,t)
        ctrl1 = get_MMDC_MPWLDECTRL(1,t)
        byte = get_Byte(t)
        read_cat = get_ReadCal(t)
        write_cat = get_WriteCal(t)
        return True
    except:
        return False

def hc_abs_value(hc,abs):
    hc_v = int(hc,16)
    abs_v = int(abs,16)
    return (hc_v << 8) + abs_v

def calc_hc_abs(byte):
    start = byte['start']
    end = byte['end']
    start_hc_v = int(start[0],16)
    start_abs_v = int(start[1],16)
    end_hc_v = int(end[0],16)
    end_abs_v = int(end[1],16)
    mean = ((start_hc_v+end_hc_v)/2) << 8
    mean += (start_abs_v+end_abs_v)/2 
    end_half = ((end_hc_v-1) << 8) + end_abs_v
    final = max(mean,end_half)
    return final

def calc_DQS_cal(byte):
    b = []
    for i in range(4):
        b.append(calc_hc_abs(byte[i]))
    MPDG_ctrl0 = (b[1] << 16) + b[0]
    MPDG_ctrl1 = (b[3] << 16) + b[2]
    return "0x%08X"%MPDG_ctrl0, "0x%08X"%MPDG_ctrl1

 
def calc_cal_start_end(cal_arr,index):
    s=0;e=0
    last_value = '1'
    for i in range(len(cal_arr)):
        current_value = cal_arr[i][-(index+1)]
        if '0' == current_value and last_value == '1':
            s = i
        if '1' == current_value and last_value == '0':
            e = i-1
        last_value = current_value
    return s*4,e*4 

def calc_cal_value(cal_arr):
    ret = 0
    for i in range(4):
        start,end = calc_cal_start_end(cal_arr,i)
        mid = (start + end) / 2
        ret += mid << (8 * i)
    return "0x%08X"%ret


import unittest


#check input file.
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

#fill field
class CheckReadDataTestCase(unittest.TestCase):
    def testReadCtrlData(self):
        txt = get_file_context(folder_path + '1.log')
        ctrl0 = get_MMDC_MPWLDECTRL(0,txt)
        ctrl1 = get_MMDC_MPWLDECTRL(1,txt)
        self.assertEquals([ctrl0,ctrl1],['0x00000004','0x00150011'])
        
        byte = get_Byte(txt)
        self.assertEquals(byte[0]['start'],['0x02','0x10'])
        self.assertEquals(byte[0]['end'],['0x04','0x38'])

        self.assertEquals(byte[1]['start'],['0x02','0x08'])
        self.assertEquals(byte[1]['end'],['0x04','0x2C'])

        self.assertEquals(byte[2]['start'],['0x02','0x08'])
        self.assertEquals(byte[2]['end'],['0x04','0x2C'])

        self.assertEquals(byte[3]['start'],['0x01','0x68'])
        self.assertEquals(byte[3]['end'],['0x04','0x34'])

        read_cat = get_ReadCal(txt)
        for i in range(0,3):
            self.assertEqual(read_cat[i],'0x1111')
        self.assertEqual(read_cat[3],'0x1011')
        self.assertEqual(read_cat[4],'0x1001')
        self.assertEqual(read_cat[5],'0x1001')
        for i in range(6,0x18):
            self.assertEqual(read_cat[i],'0x0000')
        self.assertEqual(read_cat[0x18],'0x0110')
        self.assertEqual(read_cat[0x19],'0x0111')
        self.assertEqual(read_cat[0x1A],'0x0111')
        for i in range(0x1B,0x20):
            self.assertEqual(read_cat[i],'0x1111')

        #write cal
        write_cat = get_WriteCal(txt)
        for i in range(0,4):
            self.assertEqual(write_cat[i],'0x1111')
        self.assertEqual(write_cat[4],'0x0010')
        self.assertEqual(write_cat[5],'0x0010')
        for i in range(6,0x1A):
            self.assertEqual(write_cat[i],'0x0000')
        self.assertEqual(write_cat[0x1A],'0x0100')
        self.assertEqual(write_cat[0x1B],'0x1100')
        self.assertEqual(write_cat[0x1C],'0x1110')
        for i in range(0x1D,0x20):
            self.assertEqual(write_cat[i],'0x1111')


class CalcSingleResult(unittest.TestCase):
    def setUp(self):
        self.txt = get_file_context(folder_path + '1.log')

    def testCalcByte(self):
        byte = get_Byte(self.txt)
        self.assertEquals(hc_abs_value('0x03','0x38'),calc_hc_abs(byte[0]))
        self.assertEquals(hc_abs_value('0x03','0x2C'),calc_hc_abs(byte[1]))
        self.assertEquals(hc_abs_value('0x03','0x2C'),calc_hc_abs(byte[2]))
        self.assertEquals(hc_abs_value('0x03','0x34'),calc_hc_abs(byte[3]))

    def testQDSResult(self):
        byte = get_Byte(self.txt)
        self.assertEquals(('0x032C0338','0x0334032C'),calc_DQS_cal(byte))
    
    def testFindStartEnd(self):
        read_cat = get_ReadCal(self.txt)
        self.assertEquals((0x18,0x60),calc_cal_start_end(read_cat,0))
        self.assertEquals((0x10,0x5C),calc_cal_start_end(read_cat,1))
        self.assertEquals((0x0C,0x5C),calc_cal_start_end(read_cat,2))
        self.assertEquals((0x18,0x68),calc_cal_start_end(read_cat,3))

        write_cat = get_WriteCal(self.txt)
        self.assertEquals((0x10,0x70),calc_cal_start_end(write_cat,0))
        self.assertEquals((0x18,0x6C),calc_cal_start_end(write_cat,1))
        self.assertEquals((0x10,0x64),calc_cal_start_end(write_cat,2))
        self.assertEquals((0x10,0x68),calc_cal_start_end(write_cat,3))

    def testGetCalValue(self):
        read_cat = get_ReadCal(self.txt)
        self.assertEqual('0x4034363C',calc_cal_value(read_cat))

        write_cat = get_WriteCal(self.txt)
        self.assertEqual('0x3C3A4240',calc_cal_value(write_cat))
try:
    unittest.main()
except:
    pass


#single calc result
#muti calc result
#output values


"""
    some experiments
"""
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
"""
