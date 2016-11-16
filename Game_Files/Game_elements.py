#############################
## GAME ELEMENTS
#############################
import pyglet
pathToImgs = '../Images/'

class Player(object):
    def __init__(self, location = None, dimension = None):
        self.dimension = dimension
        self.location = location
        self.overImg = pyglet.image.load(pathToImgs + 'player-sprites/knt2_fr1.gif')
        self.underImg = pyglet.image.load(pathToImgs + 'player-sprites/knt2_fr1.gif')
        self.keyCount = 0

    def addKey(self):
        self.keyCount += 1
        self.overImg = pyglet.image.load(pathToImgs + 'player-sprites/keyman.png')
        self.underImg = pyglet.image.load(pathToImgs + 'player-sprites/keyman.png')

    def removeKey(self):
        self.keyCount -= 1
        self.overImg = pyglet.image.load(pathToImgs + 'player-sprites/knt2_fr1.gif')
        self.underImg = pyglet.image.load(pathToImgs + 'player-sprites/knt2_fr1.gif')

class Wall(object):
    def __init__(self, location = None, dimension = None):
        self.dimension = dimension
        self.location = location
        self.overImg = pyglet.image.load(pathToImgs + 'Overworld/o_wall.png')
        self.underImg = pyglet.image.load(pathToImgs + 'Upside_Down/u_wall.png')
        self.isMovable = False
        self.isSolid = True

class Switch(object):
    def __init__(self, location = None, dimension = None, isOn = False):
        self.dimension = dimension
        self.location = location
        self.isMovable = False
        self.isSolid = False

        if isOn:
            self.activate()
        else:
            self.deactivate()

    def activate(self):
        self.isOn = True
        self.overImg = pyglet.image.load(pathToImgs + 'Overworld/o_on_switch.png')
        self.underImg = pyglet.image.load(pathToImgs + 'Upside_Down/u_on_switch.png')

    def deactivate(self):
        #global pyglet.image.load(pathToImgs
        self.isOn = False
        self.overImg = pyglet.image.load(pathToImgs + 'Overworld/o_off_switch.png')
        self.underImg = pyglet.image.load(pathToImgs + 'Upside_Down/u_off_switch.png')

class Rock(object):
    def __init__(self, location = None, dimension = None):
        self.dimension = dimension
        self.location = location
        self.overImg = pyglet.image.load(pathToImgs + 'Overworld/o_stone.png')
        self.underImg = pyglet.image.load(pathToImgs + 'Upside_Down/u_stone.png')
        self.isMovable = True
        self.isSolid = True

class Key(object):
    def __init__(self, location = None, dimension = None):
        self.dimension = dimension
        self.location = location
        self.overImg = pyglet.image.load(pathToImgs + 'key.png')
        self.underImg = pyglet.image.load(pathToImgs + 'key.png')
        self.isMovable = False
        self.isSolid = False

class Ladder(object):
    def __init__(self, location = None, dimension = None):
        self.dimension = dimension
        self.location = location
        self.overImg = pyglet.image.load(pathToImgs + 'Overworld/o_ladder.png')
        self.underImg = pyglet.image.load(pathToImgs + 'Upside_Down/u_ladder.png')
        self.isMovable = False
        self.isSolid = False

class Keywall(object):
    def __init__(self, location = None, dimension = None):
        self.dimension = dimension
        self.location = location
        self.overImg = pyglet.image.load(pathToImgs + 'Overworld/o_keywall.png')
        self.underImg = pyglet.image.load(pathToImgs + 'Upside_Down/u_keywall.png')
        self.isMovable = False
        self.isSolid = True

class Door(object):
    def __init__(self, location = None, dimension = None, locked = True):
        self.dimension = dimension
        self.location = location

        if locked:
            self.lock()
        else:
            self.unlock()

    def unlock(self):
        self.locked = False
        self.isMovable = False
        self.isSolid = False
        self.overImg = pyglet.image.load(pathToImgs + 'Overworld/o_floor.png')
        self.underImg = pyglet.image.load(pathToImgs + 'Upside_Down/u_floor.png')

    def lock(self):
        self.locked = True
        self.isMovable = False
        self.isSolid = True
        self.overImg = pyglet.image.load(pathToImgs + 'Overworld/o_door.png')
        self.underImg = pyglet.image.load(pathToImgs + 'Upside_Down/u_door.png')


class Floor(object):
    def __init__(self, location = None, dimension = None):
        self.dimension = dimension
        self.location = location
        self.overImg = pyglet.image.load(pathToImgs + 'Overworld/o_floor.png')
        self.underImg = pyglet.image.load(pathToImgs + 'Upside_Down/u_floor.png')
        self.isMovable = False
        self.isSolid = False

class Portal(object):
    def __init__(self, location = None, dimension = None):
        self.dimension = dimension
        self.location = location
        self.overImg = pyglet.image.load(pathToImgs + 'Portal.gif')
        self.underImg = pyglet.image.load(pathToImgs + 'Portal.gif')
        self.isMovable = False
        self.isSolid = False


