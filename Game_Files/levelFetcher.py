import csv
import UDLevel
import copy

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

def getListFromFile(path):
    levelList = []
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            levelList.append(row)

    return clean2dList(levelList)

def stripByType(a, keepOnlyPersistant = False):
    persistantObjects = ["S(D)", "S(A)", "D(L)", "D(U)" "R", "#", "KW"]

    newList = copy.deepcopy(a)
    (rows, cols) = (len(a), len(a[0]))

    for row in range(rows):
        for col in range(cols):
            if newList[row][col] in persistantObjects:
                if keepOnlyPersistant == False:
                    newList[row][col] = "_"
            else:
                if keepOnlyPersistant == True:
                    newList[row][col] = "_"

    return newList


def getLevel(level):
    overworldPath = '../Levels/level%d/%s_level%s.csv' % (level, "o", level)
    upsideDownPath = '../Levels/level%d/%s_level%s.csv' % (level, "u", level)

    overworld = stripByType(getListFromFile(overworldPath), False)
    persistant = stripByType(getListFromFile(overworldPath), True)
    upsideDown = stripByType(getListFromFile(upsideDownPath), False)

    print(overworld)
    print(persistant)
    print(upsideDown)

    return UDLevel.Level(overworld, persistant, upsideDown)
