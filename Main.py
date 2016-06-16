from ReadCalData import *

CalibrationLogFolder = r'./log/' #TODO: change folder name of log files

'''
Usage:
1. put all log files text into array
2. call calc_all_calibration_param will get the result.
 return (MMDC_MPWLDECTRL0, MMDC_MPWLDECTRL1, MPDGCTRL0, MPDGCTRL1, MPRDDLCTL, MPWRDLCTL)
3. print_result can show the result
'''
def calculate_calibration_result():
        logfile_content_arr = []
        for logfile in os.listdir(CalibrationLogFolder):
            try:
                logfile_abs_path = CalibrationLogFolder + logfile
                if check_file(logfile_abs_path):
                    text = get_file_content(logfile_abs_path)
                    logfile_content_arr.append(text)
                else:
                    print '[Error] Check ',logfile,' Failed!'
            except:
                print '[Error] Can\'t open',logfile
                continue
        result = calc_all_calibration_param(logfile_content_arr)
        print_result(result)
calculate_calibration_result()
