from Fontlib import *
import unittest

class FontLibTestCase(unittest.TestCase):
    def testSimpleWidth(self):
        self.assertEqual(1,GetTextWidth('./unittest/VWThesis_MQB_Regular_140425.TTF','./unittest/FZHT_GB18030.TTF',15,u"Emergency call"))



if __name__ == '__main__':
    unittest.main()
