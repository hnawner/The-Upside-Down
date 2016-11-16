from __future__ import division

from cocos.actions import AccelDeccel
from cocos.actions import Delay
from cocos.actions import FadeTo
from cocos.actions import JumpBy
from cocos.actions import Move
from cocos.actions import MoveBy
from cocos.actions import Repeat
from cocos.actions import Reverse
from cocos.actions import RotateBy
from cocos.scenes.transitions import FlipAngular3DTransition
from pyglet.window import key

import cocos
import cocos.collision_model as cm
import pyglet
import levelFetcher
import Game_elements

class Game(cocos.layer.ColorLayer):
    is_event_handler = True

    def __init__(self, levelNum):
        super(Game, self).__init__(22, 102, 225, 255)
        self.level = levelFetcher.getLevel(levelNum)
        self.rows = len(self.level.overworld)
        self.cols = len(self.level.overworld[0])
        self.isOverworld = True
        self.onSwitch = False
        self.spritesList = self.make3dList(self.rows, self.cols)
        self.cellsToDraw = [(row, col) for row in range(self.rows) for col in range(self.cols)]

        self.schedule(self.update)

    def make3dList(self, rows, cols):
        a=[]
        for row in range(rows): a += [[None]*cols]
        for row in range(rows):
            for col in range(cols):
                a[row][col] = []
        return a

    def redrawAll(self):
        for cell in self.cellsToDraw:
            (row, col) = cell

            self.removeSprites(row, col)

            self.drawFloorCell(row, col)
            self.drawCell(row, col, self.level.persistent)

            if self.isOverworld:
                self.drawCell(row, col, self.level.overworld)
            else:
                self.drawCell(row, col, self.level.upsideDown)

            self.drawPlayer()

        self.cellsToDraw = []

    def removeSprites(self, row, col):
        for sprite in self.spritesList[row][col]:
            self.remove(sprite)
        self.spritesList[row][col] = []

    def addSprite(self, row, col, sprite):
        self.spritesList[row][col].append(sprite)
        self.add(sprite)

    def drawPlayer(self):
        (row, col) = self.level.player.location
        sprite = cocos.sprite.Sprite(self.level.player.overImg)
        sprite.position = 16+32*col, -16+32*(self.rows-row)
        self.addSprite(row, col, sprite)

    def drawFloorCell(self, row, col):
        if self.isOverworld:
            sprite = cocos.sprite.Sprite(Game_elements.Floor().overImg)
        else:
            sprite = cocos.sprite.Sprite(Game_elements.Floor().underImg)

        sprite.position = 16+32*col, -16+32*(self.rows-row)
        self.addSprite(row, col, sprite)

    def drawCell(self, row, col, dimension):
        if isinstance(dimension[row][col], Game_elements.Floor): 
            return

        if self.isOverworld:
            sprite = cocos.sprite.Sprite(dimension[row][col].overImg)
        else:
            sprite = cocos.sprite.Sprite(dimension[row][col].underImg)

        sprite.position = 16+32*col, -16+32*(self.rows-row)
        self.addSprite(row, col, sprite)

    def on_enter(self):
        super(Game, self).on_enter()

        #game_music = pyglet.resource.media('tetris.mp3', streaming=False)

        # try:
        #     music_player.queue(game_music)
        # except:
        #     pass

        # music_player.play()

        # music_player.eos_action = 'loop'

    def on_exit(self):
        super(Game, self).on_exit()

        #music_player.seek(1)
        #music_player.pause()


    def isLegalMove(self, gameElement, drow, dcol, dimension):
        (row, col) = gameElement.location

        testRow = row + drow
        testCol = col + dcol

        testObject = dimension[testRow][testCol]

        if testObject.isSolid:
            if testObject.isMovable:
                return self.doMove(testObject, drow, dcol)
            return False
        else:
            return True

    def updateLocation(self, gameElement, row, col, newRow, newCol):
        if gameElement.dimension == "persistent":
            self.level.persistent[row][col] = Game_elements.Floor((row, col), "persistent")
            self.level.persistent[newRow][newCol] = gameElement
        elif gameElement.dimension == "overworld":
            self.level.overworld[row][col] = Game_elements.Floor((row, col), "overworld")
            self.level.overworld[newRow][newCol] = gameElement
        elif gameElement.dimension == "upsideDown":
            self.level.upsideDown[row][col] = Game_elements.Floor((row, col), "upsideDown")
            self.level.upsideDown[newRow][newCol] = gameElement

        gameElement.location = (newRow, newCol)

    def updateStates(self):
        dimensionList = [(self.level.persistent, "persistent")]
        if self.isOverworld:
            dimensionList.append((self.level.overworld, "overworld"))
        else:
            dimensionList.append((self.level.upsideDown, "upsideDown"))             

        for row in range(self.rows):
            for col in range(self.cols):
                for dimension, dimensionName in dimensionList:
                    if isinstance(dimension[row][col], Game_elements.Portal):
                        if self.level.player.location == (row, col):
                            self.isOverworld = not self.isOverworld
                            self.cellsToDraw = [(row, col) for row in range(self.rows) for col in range(self.cols)]
                    if isinstance(dimension[row][col], Game_elements.Key):
                        if self.level.player.location == (row, col):
                            dimension[row][col] = Game_elements.Floor((row, col), dimensionName)
                            self.level.player.addKey()
                    if isinstance(dimension[row][col], Game_elements.Keywall):
                        if self.level.player.keyCount > 0:
                            dimension[row][col].isSolid = False
                        if self.level.player.location == (row, col):
                            self.level.player.removeKey()
                            dimension[row][col] = Game_elements.Floor((row, col), dimensionName)
                    if isinstance(dimension[row][col], Game_elements.Switch):
                        if isinstance(self.level.persistent[row][col], Game_elements.Rock):
                            dimension[row][col].activate()
                        else:
                            dimension[row][col].deactivate()
                    if isinstance(dimension[row][col], Game_elements.Door):
                        up = (1, 0)
                        down = (-1, 0)
                        left = (0, -1)
                        right = (0, 1)

                        for (drow, dcol) in (up, down, left, right):
                            if isinstance(dimension[row+drow][col+dcol], Game_elements.Switch):
                                if dimension[row+drow][col+dcol].isOn:
                                    dimension[row][col].unlock()
                                    self.cellsToDraw.append((row, col))
                    if isinstance(dimension[row][col], Game_elements.Ladder):
                        if self.level.player.location == (row, col):
                            print("YOU WON!")


    def doMove(self, gameElement, drow, dcol):
        (row, col) = gameElement.location
        (newRow, newCol) = (row + drow, col + dcol)

        if gameElement.dimension == "player" or gameElement.dimension == "persistent":
            if not self.isLegalMove(gameElement, drow, dcol, self.level.persistent): return False
            if self.isOverworld:
                if not self.isLegalMove(gameElement, drow, dcol, self.level.overworld): return False
            else:
                if not self.isLegalMove(gameElement, drow, dcol, self.level.upsideDown): return False

        if gameElement.dimension == "overworld":
            if not self.isLegalMove(gameElement, drow, dcol, self.level.overworld): return False

        if gameElement.dimension == "overworld":
            if not self.isLegalMove(gameElement, drow, dcol, self.level.overworld): return False


        self.updateLocation(gameElement, row, col, newRow, newCol)
        self.updateStates()
        self.cellsToDraw.append((row, col))
        self.cellsToDraw.append((newRow, newCol))

        return True

    def on_key_press(self, symbol, modifiers):
        if symbol == key.LEFT:
            self.doMove(self.level.player, 0, -1)
        elif symbol == key.RIGHT:
            self.doMove(self.level.player, 0, +1)
        elif symbol == key.UP:
            self.doMove(self.level.player, -1, 0)
        elif symbol == key.DOWN:
            self.doMove(self.level.player, +1, 0)

    def update(self, dt):
        self.redrawAll()

class MainMenu(cocos.menu.Menu):

    def __init__(self):
        super(MainMenu, self).__init__('Upside-Down')

        self.font_title['font_name'] = 'Edit Undo Line BRK'
        self.font_title['font_size'] = 43
        self.font_title['color'] = (255, 180, 0, 255)

        self.font_item['color'] = (55, 55, 55, 255)
        self.font_item_selected['color'] = (255,255, 255, 255)

        items = []

        items.append(cocos.menu.MenuItem('New game', self.on_new_game))
        items.append(cocos.menu.MenuItem('Options', self.on_options))
        items.append(cocos.menu.MenuItem('Quit', self.on_quit))

        self.create_menu(items, cocos.menu.shake(), cocos.menu.shake_back())

    def on_new_game(self):
        game_layer = Game(1)
        game_scene = cocos.scene.Scene(game_layer)
        cocos.director.director.push(
            FlipAngular3DTransition(game_scene, 1))

    def on_options(self):
        self.parent.switch_to(1)

    def on_quit(self):
        pyglet.app.exit()


class OptionsMenu(cocos.menu.Menu):
    def __init__(self):
        super(OptionsMenu, self).__init__('Upside-Down')

        self.font_title['font_name'] = 'Edit Undo Line BRK'
        self.font_title['font_size'] = 43
        self.font_title['color'] = (255, 180, 0, 255)

        self.font_item['color'] = (55, 55, 55, 255)
        self.font_item_selected['color'] = (255,255, 255, 255)

        items = []

        #items.append(cocos.menu.ToggleMenuItem(
        #    'Show FPS:',
        #    self.on_show_fps,
        #    cocos.director.director.show_FPS)
        #)
        items.append(cocos.menu.MenuItem('Fullscreen', self.on_fullscreen))
        items.append(cocos.menu.MenuItem('Back', self.on_quit))
        self.create_menu(items, cocos.menu.shake(), cocos.menu.shake_back())

    def on_fullscreen(self):
        cocos.director.director.window.set_fullscreen(
            not cocos.director.director.window.fullscreen)

    def on_quit(self):
        self.parent.switch_to(0)

    def on_show_fps(self, value):
        cocos.director.director.show_FPS = value

class BackgroundLayer(cocos.layer.Layer):
    def __init__(self):
        super(BackgroundLayer, self).__init__()
        r = Game_elements.Player()

        self.image = cocos.sprite.Sprite(r.overImg)
        self.image.position = 400, 75
        self.add(self.image, z=0)

        self.player = cocos.sprite.Sprite(r.overImg)
        self.player.position = 0, 295
        self.add(self.player, z=1)

        self.enemy = cocos.sprite.Sprite(r.overImg)
        self.enemy.position = 385, 75
        self.add(self.enemy, z=1)

        self.boss = cocos.sprite.Sprite(r.overImg)
        self.boss.scale = 0.4
        rect = self.boss.get_rect()
        rect.midbottom = 600, 50
        self.boss.position = rect.center
        self.add(self.boss, z=1)

        self.player.do(Repeat(
            MoveBy((-25, 0), 0.25) +
            MoveBy((50, 0), 0.5) +
            MoveBy((-25, 0), 0.25)))
        self.enemy.do(Repeat(
            MoveBy((-25, 0), 0.25) +
            MoveBy((50, 0), 0.5) +
            MoveBy((-25, 0), 0.25)))
        self.boss.do(Repeat(FadeTo(155, 0.5) + FadeTo(255, 0.5)))

if __name__ == '__main__':
    cocos.director.director.init(
        width=12*32,
        height=12*32,
        caption="The Upside-Down"
    )

    music_player = pyglet.media.Player()
    music_player.volume = 1

    scene = cocos.scene.Scene()
    scene.add(cocos.layer.MultiplexLayer(MainMenu(), OptionsMenu()), z=1)
    scene.add(BackgroundLayer(), z=0)
    cocos.director.director.run(scene)