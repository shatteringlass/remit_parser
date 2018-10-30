import csv

from remitparser import RemitTable1Parser
from remitparser import RemitTable2Parser


def main():
    # TODO: handle files/folders
    xml = ['tbl2_test.xml']
    rows = list()
    for _x in xml:
        rows.extend(RemitTable2Parser(_x).get_document())
    to_csv(rows, './tbl2_test.csv')


def to_csv(rows, filename):
    with open(filename, 'w', newline='\n') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        while rows:
            writer.writerow(rows.pop())


if __name__ == '__main__':
    main()
