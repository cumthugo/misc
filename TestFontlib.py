
from Fontlib import *
import unittest

class FontLibTestCase(unittest.TestCase):
    def testSimpleWidth(self):
        self.assertEqual(1,GetTextWidth('./VWThesis_MQB_Light_140425.TTF','./FZHT_GB18030.TTF',23,u'\u662F\u5426'))



if __name__ == '__main__':
    unittest.main()
