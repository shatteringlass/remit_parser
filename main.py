#! /usr/bin/env python3
import argparse
import csv
from remitparser import RemitParser


def main():
    parser = argparse.ArgumentParser(
        description='Parses REMIT Table1/Table2 XML into CSV files.')
    parser.add_argument('input', nargs='+', type=str,
                        help='The list of files to be parsed.')
    parser.add_argument('output', type=str,
                        help='The output CSV file to be produced.')
    args = parser.parse_args()

    # TODO: handle files/folders
    xml = args.input
    outfile = args.output
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
