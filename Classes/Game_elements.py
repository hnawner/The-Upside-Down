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

class Switch(Object):

    def __init__(self):
        global pathToImgs
        self.over_on_img = pathToImgs + 'Overworld/o_on-switch.png'
        self.over_off_img = pathToImgs + 'Overworld/o_off-switch.png'
        self.under_on_img = pathToImgs + 'Upside_Down/u_on-switch.png'
        self.under_off_img = pathToImgs + 'Upside_Down/u_off-switch.png'
        self.isMovable = False
        self.isSolid = False
        self.isOn = False

class Rock(Object):

    def __init__(self):
        global pathToImgs
        self.overImg = pathToImgs + 'Overworld/o_stone.png'
        self.underImg = pathToImgs + 'Upside_Down/u_stone.png'
        self.isMovable = True
        self.isSolid = True

class Key(Object):

    def __init__(self):
        global pathToImgs
        self.img = pathToImgs + 'key.png'

class Ladder(Object):

    def __init__(self):
        global pathToImgs
        self.overImg = pathToImgs + 'Overworld/o_ladder.png'
        self.underImg = pathToImgs + 'Upside_Down/u_ladder.png'
        self.isMovable = False
        self.isSolid = False

class Keywall(Object):

    def __init__(self):
        self.overImg = pathToImgs + 'Overworld/o_keywall.png'
        self.underImg = pathToImgs + 'Upside_Down/u_keywall.png'
        self.isMovable = False
        self.isSolid = True

class Floor(Object):

    def __init__(self):
        self.overImg = pathToImgs + 'Overworld/o_floor.png'
        self.underImg = pathToImgs + 'Upside_Down/u_floor.png'
        self.isMovable = False
        self.isSolid = False

class Portal(Object):

    def __init__(self):
        self.img = pathToImgs + 'Portal.gif'
        self.isMovable = False
        self.isSolid = False


