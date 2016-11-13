#############################
## GAME ELEMENTS
#############################

from cocos.sprite import Sprite

class Wall(Object):

    def __init__(self):
        self.overImg = 'Images/Overworld/o_wall.png'
        self.underImg = 'Images/Upside_Down/u_wall.png'
        self.isMovable = False
        self.isSolid = True

class Switch(Object):

    def __init__(self):
        self.over_on_img = 'Images/Overworld/o_on-switch.png'
        self.over_off_img = 'Images/Overworld/o_off-switch.png'
        self.under_on_img = 'Images/Upside_Down/u_on-switch.png'
        self.under_off_img = 'Images/Upside_Down/u_off-switch.png'
        self.isMovable = False
        self.isSolid = False
        self.isOn = False

class Rock(Object):

    def __init__(self):
        self.overImg = 'Images/Overworld/o_stone.png'
        self.underImg = 'Images/Upside_Down/u_stone.png'
        self.isMovable = True
        self.isSolid = True

class Key(Object):

    def __init__(self):
        self.img = 'Images/key.png'

class Ladder(Object):

    def __init__(self):
        self.overImg = 'Images/Overworld/o_ladder.png'
        self.underImg = 'Images/Upside_Down/u_ladder.png'
        self.isMovable = False
        self.isSolid = False

class Keywall(Object):

    def __init__(self):
        self.overImg = 'Images/Overworld/o_keywall.png'
        self.underImg = 'Images/Upside_Down/u_keywall.png'
        self.isMovable = False
        self.isSolid = True

class Floor(Object):

    def __init__(self):
        self.overImg = 'Images/Overworld/o_floor.png'
        self.underImg = 'Images/Upside_Down/u_floor.png'
        self.isMovable = False
        self.isSolid = False

class Portal(Object):

    def __init__(self):
        self.img = 'Images/Portal.gif'
        self.isMovable = False
        self.isSolid = False


