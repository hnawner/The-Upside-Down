import csv
import UDLevel
import copy
import Game_elements

def convertBoardToInstances(a):
    (rows, cols) = (len(a), len(a[0]))
    for row in range(rows):
        for col in range(cols):
            key = a[row][col]

            if key == "_":
                a[row][col] = Game_elements.Floor((row, col))
            elif key == "P":
                a[row][col] = Game_elements.Player((row, col))
            elif key == "W":
                a[row][col] = Game_elements.Wall((row, col))
            elif key == "R":
                a[row][col] = Game_elements.Rock((row, col))
            elif key == 'K':
                a[row][col] = Game_elements.Key((row, col))
            elif key == "KW":
                a[row][col] = Game_elements.Keywall((row, col))
            elif key == "D(L)":
                a[row][col] = Game_elements.Door((row, col), True)
            elif key == "D(U)":
                a[row][col] = Game_elements.Door((row, col), False)
            elif key == "S(A)":
                a[row][col] = Game_elements.Switch((row, col), True)
            elif key == "S(D)":
                a[row][col] = Game_elements.Switch((row, col), False)
            elif key == "L":
                a[row][col] = Game_elements.Ladder((row, col))
            elif key == "#":
                a[row][col] = Game_elements.Portal((row, col))
    return a

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
    persistantObjects = ["S(D)", "S(A)", "D(L)", "D(U)", "R", "#", "KW"]

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

    overworld = convertBoardToInstances(
                stripByType(getListFromFile(overworldPath), False))
    persistant = convertBoardToInstances(
                 stripByType(getListFromFile(overworldPath), True))
    upsideDown = convertBoardToInstances(
                stripByType(getListFromFile(upsideDownPath), False))

    # overworld = stripByType(getListFromFile(overworldPath), False)
    # persistant = stripByType(getListFromFile(overworldPath), True)
    # upsideDown = stripByType(getListFromFile(upsideDownPath), False)

    return UDLevel.Level(overworld, upsideDown, persistant)
