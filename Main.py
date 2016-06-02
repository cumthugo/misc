from ReadCalData import *

CalibrationLogFolder = r'./log/' #TODO: change log files folder name

'''
Usage:
1. put all log files text into array
2. call calculate_all_calibration_parameter will get the result.
 return (MMDC_MPWLDECTRL0, MMDC_MPWLDECTRL1, MPDGCTRL0, MPDGCTRL1, MPRDDLCTL, MPWRDLCTL)
3. print_result can show the result
'''
def calculate_calibration_result():
        logfile_content_arr = []
        for logfile in os.listdir(CalibrationLogFolder):
            try:
                abs_logfile = CalibrationLogFolder + logfile
                if check_file(abs_logfile):
                    text = get_file_content(abs_logfile)
                    logfile_content_arr.append(text)
                else:
                    print 'Check ',logfile,' Failed!'
            except:
                print ' can\'t open',logfile
                continue
        result = calculate_all_calibration_parameter(logfile_content_arr)
        print_result(result)
calculate_calibration_result()
