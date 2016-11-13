import csv

def rowIsEmpty(a):
    for val in a:
        if not val == "": return False
    return True

def cleanRows(a):
    cleanList = []
    for row in a:
        if not rowIsEmpty(row):
            cleanList.append(row)
    return cleanList

def cleanCols(a):
    (rows, cols) = (len(a), len(a[0]))
    cleanList = [[] for x in range(rows)]

    for col in range(cols):
        colIsEmpty = True
        for row in range(rows):
            if not a[row][col] == "":
                colIsEmpty = False
        if not colIsEmpty:
            for row in range(rows):
                cleanList[row].append(a[row][col])

    return cleanList

def clean2dList(a):
    return cleanCols(cleanRows(a))

def getLevel(level, dimension):
    level = str(level)
    levelList = []
    path = 'level%s/%s_level%s.csv' % (level, dimension, level)
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            levelList.append(row)

    return clean2dList(levelList)