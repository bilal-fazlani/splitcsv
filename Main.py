import csv
import os

if __name__ == '__main__':

    columnSet = [2, 2, 2]
    filePath = '/Users/bilal/projects/splitcsv/large-file.csv'
    targetDir = '/Users/bilal/projects/splitcsv/output/'
    os.makedirs(os.path.dirname(targetDir + '/'), exist_ok=True)

    with open(filePath, 'r') as mainFile:
        reader = csv.reader(mainFile, delimiter=',')
        for row in reader:
            readColumns = 0
            for i in range(len(columnSet)):
                f = open(f'{targetDir}/data_{i+1}.csv', 'a')
                w = csv.writer(f, delimiter=',')
                w.writerow(row[readColumns:readColumns+columnSet[i]])
                readColumns += columnSet[i]
                f.close()

