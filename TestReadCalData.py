from ReadCalData import *

import unittest
folder_path = r'./'
unittest_folder = r'./unittest/'

#check input file.
class CheckInputFileTestCase(unittest.TestCase):

    def testCorrectFile(self):
        self.failUnless(check_file(unittest_folder + '1.log'),'Correct file but check failed!')
    
    def testFileNotExist(self):
        self.failIf(check_file(unittest_folder + 'not_exist.log'),'File Not exist should return false!')
    
    def testEmptyFile(self):
        self.failIf(check_file(unittest_folder + 'empty.log'),'Empty file should return false')

    def testCtrlError(self):
        self.failIf(check_file(unittest_folder + 'ctrl_error.log'),'Ctrl field error should return false')
    
    def testByteError(self):
        self.failIf(check_file(unittest_folder + 'byte_error.log'),'Byte field error should return false')

    def testReadCalError(self):
        self.failIf(check_file(unittest_folder + 'read_cal_error.log'),'Read Cal field error should return false')
    
    def testReadCalDataError(self):
        self.failIf(check_file(unittest_folder + 'read_cal_data_error.log'),'Read Cal field error should return false')

    def testWriteCalError(self):
        self.failIf(check_file(unittest_folder + 'write_cal_error.log'),'Write Cal field error should return false')
    
    def testWriteCalDataError(self):
        self.failIf(check_file(unittest_folder + 'write_cal_data_error.log'),'Write Cal field error should return false')

#read field data
class CheckReadDataTestCase(unittest.TestCase):
    def testReadCtrlData(self):
        log_content = get_file_content(unittest_folder + '1.log')
        ctrl_value = get_MMDC_MPWLDECTRL(log_content)

        self.assertEquals(ctrl_value,('0x00000004','0x00150011'))
        
        byte_arr = get_byte(log_content)
        self.assertEquals(byte_arr[0][0],calc_hc_abs_value('0x02','0x10')) #start
        self.assertEquals(byte_arr[0][1],calc_hc_abs_value('0x04','0x38')) #end

        self.assertEquals(byte_arr[1][0],calc_hc_abs_value('0x02','0x08'))
        self.assertEquals(byte_arr[1][1],calc_hc_abs_value('0x04','0x2C'))

        self.assertEquals(byte_arr[2][0],calc_hc_abs_value('0x02','0x08'))
        self.assertEquals(byte_arr[2][1],calc_hc_abs_value('0x04','0x2C'))

        self.assertEquals(byte_arr[3][0],calc_hc_abs_value('0x01','0x68'))
        self.assertEquals(byte_arr[3][1],calc_hc_abs_value('0x04','0x34'))

        read_cal = get_read_cal(log_content)
        for i in range(0x00,0x03):
            self.assertEqual(read_cal[i],'0x1111')
        self.assertEqual(read_cal[0x03],'0x1011')
        self.assertEqual(read_cal[0x04],'0x1001')
        self.assertEqual(read_cal[0x05],'0x1001')
        for i in range(0x06,0x18):
            self.assertEqual(read_cal[i],'0x0000')
        self.assertEqual(read_cal[0x18],'0x0110')
        self.assertEqual(read_cal[0x19],'0x0111')
        self.assertEqual(read_cal[0x1A],'0x0111')
        for i in range(0x1B,0x20):
            self.assertEqual(read_cal[i],'0x1111')

        write_cal = get_write_cal(log_content)
        for i in range(0x00,0x04):
            self.assertEqual(write_cal[i],'0x1111')
        self.assertEqual(write_cal[0x04],'0x0010')
        self.assertEqual(write_cal[0x05],'0x0010')
        for i in range(0x06,0x1A):
            self.assertEqual(write_cal[i],'0x0000')
        self.assertEqual(write_cal[0x1A],'0x0100')
        self.assertEqual(write_cal[0x1B],'0x1100')
        self.assertEqual(write_cal[0x1C],'0x1110')
        for i in range(0x1D,0x20):
            self.assertEqual(write_cal[i],'0x1111')

#single calculation
class CalcSingleResult(unittest.TestCase):
    def setUp(self):
        self.log_content = get_file_content(unittest_folder + '1.log')

    def testCalcByte(self):
        byte_arr = get_byte(self.log_content)
        self.assertEquals(calc_hc_abs_value('0x03','0x38'),calc_hc_abs_final(byte_arr[0]))
        self.assertEquals(calc_hc_abs_value('0x03','0x2C'),calc_hc_abs_final(byte_arr[1]))
        self.assertEquals(calc_hc_abs_value('0x03','0x2C'),calc_hc_abs_final(byte_arr[2]))
        self.assertEquals(calc_hc_abs_value('0x03','0x34'),calc_hc_abs_final(byte_arr[3]))

    def testQDSResult(self):
        byte_arr = get_byte(self.log_content)
        self.assertEquals(('0x032C0338','0x0334032C'),get_DQS(byte_arr))
    
    def testFindStartEnd(self):
        read_cal = get_read_cal(self.log_content)
        self.assertEquals((0x18,0x60),calc_calibration_start_end(read_cal,0))
        self.assertEquals((0x10,0x5C),calc_calibration_start_end(read_cal,1))
        self.assertEquals((0x0C,0x5C),calc_calibration_start_end(read_cal,2))
        self.assertEquals((0x18,0x68),calc_calibration_start_end(read_cal,3))

        write_cal = get_write_cal(self.log_content)
        self.assertEquals((0x10,0x70),calc_calibration_start_end(write_cal,0))
        self.assertEquals((0x18,0x6C),calc_calibration_start_end(write_cal,1))
        self.assertEquals((0x10,0x64),calc_calibration_start_end(write_cal,2))
        self.assertEquals((0x10,0x68),calc_calibration_start_end(write_cal,3))

    def testGetCalValue(self):
        read_cal = get_read_cal(self.log_content)
        self.assertEqual('0x4034363C',calc_calibration([read_cal]))

        write_cal = get_write_cal(self.log_content)
        self.assertEqual('0x3C3A4240',calc_calibration([write_cal]))


class Calc2SampleResult(unittest.TestCase):
    def setUp(self):
        self.data_txt_1 = get_file_content(unittest_folder + '1.log')
        self.data_txt_2 = get_file_content(unittest_folder + '2.log')

    def testMPWLDE(self):
        file1_ctrl_value = get_MMDC_MPWLDECTRL(self.data_txt_1)
        file2_ctrl_value = get_MMDC_MPWLDECTRL(self.data_txt_2)
        ctrl_list = [file1_ctrl_value,file2_ctrl_value]
        self.assertEquals(('0x00020007','0x00170010'),calc_MPWLDECTRL(ctrl_list))

    def testCalcByte(self):
        file1_byte = get_byte(self.data_txt_1)
        file2_byte = get_byte(self.data_txt_2)
        bytes = [file1_byte,file2_byte]
        self.assertEqual(('0x032C0338','0x0330032C'),calc_DQS_cals(bytes))

    def testCalcCalValue(self):
        file1_read_cal = get_read_cal(self.data_txt_1)
        file2_read_cal = get_read_cal(self.data_txt_2)
        cals = [file1_read_cal,file2_read_cal]
        self.assertEqual('0x40323638',calc_calibration(cals))

        file1_write_cal = get_write_cal(self.data_txt_1)
        file2_write_cal = get_write_cal(self.data_txt_2)
        cals = [file1_write_cal,file2_write_cal]
        self.assertEqual('0x383A4440',calc_calibration(cals))

class CalcMutiResult(unittest.TestCase):
    def setUp(self):
        self.data_txt_1 = get_file_content(folder_path + "log/ddr_calibration_20160427-10'8'3_Radio1_tmp85_1.log")
        self.data_txt_2 = get_file_content(folder_path + "log/ddr_calibration_20160427-11'46'37_Radio3_tmp85_1.log")
        self.data_txt_3 = get_file_content(folder_path + "log/ddr_calibration_20160427-11'49'53_Radio3_tmp85_2.log")

    def test3Samples(self):
        file_text = [self.data_txt_1,self.data_txt_2,self.data_txt_3]
        self.assertEqual(['0x00020008','0x0018000F','0x032C0338','0x0330032C','0x40323638','0x383A4440'],calc_all_calibration_param(file_text))

try:
    unittest.main()
except:
    pass

