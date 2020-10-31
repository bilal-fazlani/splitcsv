#!/usr/bin/python3

import csv
import getopt
import os
import sys
import math
import pathlib


def main(argv):
    input_file = ''
    output_dir = 'output'
    split_pattern = ''
    batch_size = ''

    try:
        opts, args = getopt.getopt(argv, "hi:o:p:b:", ["inputFile=", "outputDir=", "splitPattern=", "batchSize="])
    except getopt.GetoptError:
        print_help(2)
    for opt, arg in opts:
        if opt == '-h':
            print_help()
        elif opt in ("-i", "--inputFile"):
            input_file = arg
        elif opt in ("-o", "--outputDir"):
            output_dir = arg
        elif opt in ("-p", "--splitPattern"):
            split_pattern = arg
        elif opt in ("-b", "--batchSize"):
            batch_size = arg

    if input_file == '':
        print("please specify input file")
        print_help(2)

    if (split_pattern == '') & (batch_size == ''):
        print("please specify split pattern or batch size")
        print_help(2)

    file = pathlib.Path(input_file)
    if not file.exists():
        print("input file does not exist")
        sys.exit(1)

    if split_pattern != '':
        sp = list(map(int, split_pattern.split(',')))
        split(input_file, output_dir, sp)
    else:
        count = get_column_length(input_file)
        files = math.ceil(count / int(batch_size))
        sp = [int(batch_size)] * files
        split(input_file, output_dir, sp)


def print_help(exit_code=0):
    print('splitcsv.py -i <inputFile> -o <outputDir> (default: output/) -p <splitPattern> (comma separated)\n'
          'OR\n'
          'splitcsv.py -i <inputFile> -o <outputDir> (default: output/) -b <batchSize>')
    sys.exit(exit_code)


def remove(filename):
    if os.path.exists(filename):
        os.remove(filename)


def data_file(i, target_dir):
    return f'{target_dir}/data_{i + 1}.csv'


def get_column_length(filepath):
    with open(filepath, 'r') as mainFile:
        reader = csv.reader(mainFile, delimiter=',')
        return len(next(reader))


def split(filepath, target_dir, column_set):
    os.makedirs(os.path.dirname(target_dir + '/'), exist_ok=True)

    print(f"writing to directory: {target_dir}")

    for fIndex in range(len(column_set)):
        remove(data_file(fIndex, target_dir))

    with open(filepath, 'r') as mainFile:
        reader = csv.reader(mainFile, delimiter=',')
        rows = 0
        for row in reader:
            read_columns = 0
            for i in range(len(column_set)):
                f = open(data_file(i, target_dir), 'a')
                w = csv.writer(f, delimiter=',')
                w.writerow(row[read_columns:read_columns + column_set[i]])
                read_columns += column_set[i]
                f.close()
            rows += 1
            print(f"\rProgress: {rows} rows processed", end="")
    print("\n\rDONE")


if __name__ == '__main__':
    main(sys.argv[1:])
