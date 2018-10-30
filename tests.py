import unittest

from remitparser import RemitParser
from remitparser import RemitTable1Parser
from remitparser import RemitTable2Parser


class TestStringMethods(unittest.TestCase):

    def test_namespace(self):
        self.assertEqual(RemitParser('./tbl2_test.xml')._xmlns,
                         {'tbl':'http://www.acer.europa.eu/REMIT/REMITTable2_V1.xsd'})


if __name__ == '__main__':
    unittest.main()
