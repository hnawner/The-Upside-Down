#############################
## GAME ELEMENTS
#############################

pathToImgs = '../Images/'

class Player(Object):
    def __init__(self):
        self.img = pathToImgs + 'player-sprites/knt2_fr1.gif'
        self.hasKey = False

class Wall(Object):
    def __init__(self):
        global pathToImgs
        self.overImg = pathToImgs + 'Overworld/o_wall.png'
        self.underImg = pathToImgs + 'Upside_Down/u_wall.png'
        self.isMovable = False
        self.isSolid = True

class Switch(object):

    def __init__(self, isOn = False):
        self.isMovable = False
        self.isSolid = False

        if self.isOn:
            turnOn()
        else:
            turnOff()

    def turnOn():
        global pathToImgs
        self.isOn = True
        self.over_img ='key.png'
        self.over_img = pathToImgs + 'Overworld/o_off_switch.png'

    def turnOff():
        global pathToImgs
        self.isOn = False
        self.under_on_img = pathToImgs + 'Upside_Down/u_on_switch.png'
        self.under_off_img = pathToImgs + 'Upside_Down/u_off_switch.png'



class Rock(object):

    def __init__(self):
        global pathToImgs
        self.overImg = pathToImgs + 'Overworld/o_stone.png'
        self.underImg = pathToImgs + 'Upside_Down/u_stone.png'
        self.isMovable = True
        self.isSolid = True

class Key(object):

    def __init__(self):
        global pathToImgs
        self.img = pathToImgs + 'key.png'

class Ladder(object):

    def __init__(self):
        global pathToImgs
        self.overImg = pathToImgs + 'Overworld/o_ladder.png'
        self.underImg = pathToImgs + 'Upside_Down/u_ladder.png'
        self.isMovable = False
        self.isSolid = False

class Keywall(object):

    def __init__(self):
        self.overImg = pathToImgs + 'Overworld/o_keywall.png'
        self.underImg = pathToImgs + 'Upside_Down/u_keywall.png'
        self.isMovable = False
        self.isSolid = True

class Door(object, locked = True):

    def __init__(self):
        if locked:
            self.lock()
        else:
            self.unlock()

    def unlock():
        global pathToImgs
        self.locked = False
        self.isMovable = False
        self.isSolid = False
        self.overImg = pathToImgs + 'Overworld/o_floor.png'
        self.underImg = pathToImgs + 'Upside_Down/u_floor.png'

    def lock():
        global pathToImgs
        self.locked = True
        self.isMovable = False
        self.isSolid = True
        self.overImg = pathToImgs + 'Overworld/o_door.png'
        self.underImg = pathToImgs + 'Upside_Down/u_door.png'


class Floor(object):

    def __init__(self):
        self.overImg = pathToImgs + 'Overworld/o_floor.png'
        self.underImg = pathToImgs + 'Upside_Down/u_floor.png'
        self.isMovable = False
        self.isSolid = False

class Portal(object):

    def __init__(self):
        self.img = pathToImgs + 'Portal.gif'
        self.isMovable = False
        self.isSolid = False


