#!/usr/bin/python3

import csv
import getopt
import os
import sys


def main(argv):
    input_file = ''
    output_dir = 'output'

    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["inputFile=", "outputDir="])
    except getopt.GetoptError:
        print_help(2)
    for opt, arg in opts:
        if opt == '-h':
            print_help()
        elif opt in ("-i", "--inputFile"):
            input_file = arg
        elif opt in ("-o", "--outputDir"):
            output_dir = arg

    if input_file == '':
        print_help(2)
    split(input_file, output_dir)


def print_help(exit_code=0):
    print('splitcsv.py -i <inputFile> -o <outputDir> (default: output/)')
    sys.exit(exit_code)


def remove(filename):
    if os.path.exists(filename):
        os.remove(filename)


def data_file(i, target_dir):
    return f'{target_dir}/data_{i + 1}.csv'


def split(filepath, target_dir):
    column_set = [2, 2, 2]
    os.makedirs(os.path.dirname(target_dir + '/'), exist_ok=True)

    for fIndex in range(len(column_set)):
        remove(data_file(fIndex, target_dir))

    with open(filepath, 'r') as mainFile:
        reader = csv.reader(mainFile, delimiter=',')
        for row in reader:
            read_columns = 0
            for i in range(len(column_set)):
                f = open(data_file(i, target_dir), 'a')
                w = csv.writer(f, delimiter=',')
                w.writerow(row[read_columns:read_columns + column_set[i]])
                read_columns += column_set[i]
                f.close()


if __name__ == '__main__':
    main(sys.argv[1:])
