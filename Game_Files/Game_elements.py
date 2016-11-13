#############################
## GAME ELEMENTS
#############################

from cocos.sprite import Sprite

pathToImgs = '../Images/'

class Wall(object):

    def __init__(self):
        global pathToImgs
        self.overImg = pathToImgs + 'Overworld/o_wall.png'
        self.underImg = pathToImgs + 'Upside_Down/u_wall.png'
        self.isMovable = False
        self.isSolid = True

class Switch(object):

    def __init__(self):
        global pathToImgs
        self.over_on_img ='key.png'
        self.over_off_img = pathToImgs + 'Overworld/o_off_switch.png'
        self.under_on_img = pathToImgs + 'Upside_Down/u_on_switch.png'
        self.under_off_img = pathToImgs + 'Upside_Down/u_off_switch.png'
        self.isMovable = False
        self.isSolid = False
        self.isOn = False

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


