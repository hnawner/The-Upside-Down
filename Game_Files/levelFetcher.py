import csv
import UDLevel
import copy
import Game_elements

def convertBoardToInstances(a, dimension):
    (rows, cols) = (len(a), len(a[0]))
    for row in range(rows):
        for col in range(cols):
            key = a[row][col]

            if key == "_":
                a[row][col] = Game_elements.Floor((row, col), dimension)
            elif key == "P":
                a[row][col] = Game_elements.Player((row, col), dimension)
            elif key == "W":
                a[row][col] = Game_elements.Wall((row, col), dimension)
            elif key == "R":
                a[row][col] = Game_elements.Rock((row, col), dimension)
            elif key == 'K':
                a[row][col] = Game_elements.Key((row, col), dimension)
            elif key == "KW":
                a[row][col] = Game_elements.Keywall((row, col), dimension)
            elif key == "D(L)":
                a[row][col] = Game_elements.Door((row, col), dimension, True)
            elif key == "D(U)":
                a[row][col] = Game_elements.Door((row, col), dimension, False)
            elif key == "S(A)":
                a[row][col] = Game_elements.Switch((row, col), dimension, True)
            elif key == "S(D)":
                a[row][col] = Game_elements.Switch((row, col), dimension, False)
            elif key == "L":
                a[row][col] = Game_elements.Ladder((row, col), dimension)
            elif key == "#":
                a[row][col] = Game_elements.Portal((row, col), dimension)
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


def getLevel(level):
    overworldPath = '../Levels/level%d/%s_level%s.csv' % (level, "o", level)
    upsideDownPath = '../Levels/level%d/%s_level%s.csv' % (level, "u", level)
    persistentPath = '../Levels/level%d/%s_level%s.csv' % (level, "p", level)
    playerLocationPath = '../Levels/level%d/playerStartLoc.txt' % (level)
    playerLocation = [int(i) for i in open(playerLocationPath).readline().split(",")]


    overworld = convertBoardToInstances(getListFromFile(overworldPath), "overworld")
    persistent = convertBoardToInstances(getListFromFile(persistentPath), "persistent")
    upsideDown = convertBoardToInstances(getListFromFile(upsideDownPath), "upsideDown")
    player = Game_elements.Player(playerLocation, "player")

    # overworld = stripByType(getListFromFile(overworldPath), False)
    # persistent = stripByType(getListFromFile(overworldPath), True)
    # upsideDown = stripByType(getListFromFile(upsideDownPath), False)

    return UDLevel.Level(overworld, upsideDown, persistent, player)
