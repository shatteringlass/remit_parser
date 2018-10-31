import csv
from remitparser import RemitParser


def main():
    # TODO: handle files/folders
    xml = ['tbl2_test.xml']
    outfile = './tbl2_test.csv'
    rows = list()
    for _x in xml:
        p = RemitParser(_x)
        doc = p.get_document()
        rows.extend(doc)
    to_csv(rows, outfile)


def to_csv(rows, filename):
    with open(filename, 'w', newline='\n') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        while rows:
            writer.writerow(rows.pop())


if __name__ == '__main__':
    main()
