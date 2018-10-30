import csv
import json
import remitparser


def main():
    xml = 'tbl2_test.xml'
    tb2 = remitparser.RemitTable2Parser(xml)
    doc = tb2.get_document()
    print(json.dumps(doc,indent=True))


if __name__ == '__main__':
    main()
