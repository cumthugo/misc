import re
folder_path = r'E:\private\python\Tools'
f = open(folder_path + '\\1.log','r')
file_text = f.read().replace('\r\n','\n')
lines = file_text.split('\n')
for line in lines:
    m = re.match(' +MMDC_MPWLDECTRL0.*= (.+)',line)
    if m:
        print m.group(1)
        break

def get_text(text,start,end):
    #print 'start:',start,'*** end:',end
    ret = re.findall('('+start+'(.*\s*)*?)'+end,text)
    if ret:
        return ret[0][0]
    else:
        return []

byte_text = [get_text(file_text,'BYTE '+str(i),'BYTE') for i in range(3)]
byte_text.append(get_text(file_text,'BYTE 3','DQS calibration'))
#print byte_text
read_cal_text = get_text(file_text,'Starting Read calibration','Byte 0')
#print read_cal_text
write_cal_text = get_text(file_text,'Starting Write calibration','Byte 0')
print write_cal_text


def txt_find(pat,text):
    ret = re.findall(pat,text)
    if ret:
        return ret[0]
    else:
        return []
for i in range(4):
    start_hc, start_abs = txt_find('Start:\s*HC=(0x[0-9A-F]*) ABS=(0x[0-9A-F]*)',byte_text[i])
    print 'Start:',start_hc, start_abs
    end_hc, end_abs = txt_find('End:\s*HC=(0x[0-9A-F]*) ABS=(0x[0-9A-F]*)',byte_text[i])
    print 'End:',end_hc, end_abs

