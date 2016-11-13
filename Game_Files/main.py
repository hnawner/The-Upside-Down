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
        self.schedule(self.update)
        self.isOverworld = True
        self.inPortal = False
        self.justInPortal = False
        # init overworld
        for row in range(self.rows):
            for col in range(self.cols):
                self.level.overworld[row][col].location = (row, col)
        # init upsidedown
        for row in range(self.rows):
            for col in range(self.cols):
                self.level.upsideDown[row][col].location = (row, col)
        # init persistant
        for row in range(self.rows):
            for col in range(self.cols):
                self.level.persistant[row][col].location = (row, col)
                if (isinstance(self.level.persistant[row][col], Game_elements.Player)):
                    self.player = self.level.persistant[row][col]
                    self.player.location = (row, col)
    
    def redrawAll(self):
        if self.isOverworld:
            self.drawOverworld()
            self.drawPersistant()
        else:
            self.drawUpsideDown()
            self.drawPersistantDark()

    def drawOverworld(self, z=1):
        for row in range(self.rows):
            for col in range(self.cols):
                currentObject = self.level.overworld[row][col]
                
                if isinstance(currentObject, Game_elements.Floor):
                    continue

                currentSprite = cocos.sprite.Sprite(pyglet.image.load((currentObject.overImg)))
                currentSprite.position = 16+32*col, -16+32*(self.rows-row)
                self.add(currentSprite, z=1)

    def drawPersistant(self, z=0):
        for row in range(self.rows):
            for col in range(self.cols):
                currentObject = self.level.persistant[row][col]

                if isinstance(currentObject, Game_elements.Rock) or isinstance(currentObject, Game_elements.Key) or isinstance(currentObject, Game_elements.Player):
                    extraSprite = cocos.sprite.Sprite(pyglet.image.load((Game_elements.Floor().overImg)))
                    extraSprite.position = 16+32*col, -16+32*(self.rows-row)
                    self.add(extraSprite, z=0)

                currentSprite = cocos.sprite.Sprite(pyglet.image.load((currentObject.overImg)))
                currentSprite.position = 16+32*col, -16+32*(self.rows-row)
                self.add(currentSprite, z=0)

    def drawPersistantDark(self):
        for row in range(self.rows):
            for col in range(self.cols):
                currentObject = self.level.persistant[row][col]

                if isinstance(currentObject, Game_elements.Rock) or isinstance(currentObject, Game_elements.Key) or isinstance(currentObject, Game_elements.Player):
                    extraSprite = cocos.sprite.Sprite(pyglet.image.load((Game_elements.Floor().underImg)))
                    extraSprite.position = 16+32*col, -16+32*(self.rows-row)
                    self.add(extraSprite, z=0)

                currentSprite = cocos.sprite.Sprite(pyglet.image.load((currentObject.underImg)))
                currentSprite.position = 16+32*col, -16+32*(self.rows-row)
                self.add(currentSprite, z=0)

    def drawUpsideDown(self, z=2):
        for row in range(self.rows):
            for col in range(self.cols):
                currentObject = self.level.upsideDown[row][col]
                
                if isinstance(currentObject, Game_elements.Floor):
                    continue

                currentSprite = cocos.sprite.Sprite(pyglet.image.load((currentObject.overImg)))
                currentSprite.position = 16+32*col, -16+32*(self.rows-row)
                self.add(currentSprite, z=2)


    def on_enter(self):
        super(Game, self).on_enter()

        # try:
        #     music_player.queue(resources.game_music)
        # except:
        #     pass

        # music_player.play()

        # music_player.eos_action = 'loop'

    def on_exit(self):
        super(Game, self).on_exit()

        #music_player.seek(1)
        #music_player.pause()

    def testCollisions(self, row, col, drow, dcol, dimension):
        # test persistant
        if (dimension == 'persistant'):
            nextSpacePer = self.level.persistant[row+drow][col+dcol]
            # test portals
            if (isinstance(nextSpacePer, Game_elements.Portal)):
                self.isOverworld = not self.isOverworld
                self.inPortal = True
                self.justInPortal = True
                return True

            if (isinstance(nextSpacePer, Game_elements.Keywall)):
                if (self.player.hasKey):
                    return True
                else: return False
            # test moveability
            if (nextSpacePer.isMovable):
                if (self.doMove(nextSpacePer.location[0], nextSpacePer.location[1], drow, dcol)):
                    nextSpacePer = self.level.persistant[row+drow][col+dcol]
                    #self.updateLocation(row, col, drow, dcol, 'persistant')
                    return True
                else: return False
            # test for walls etc
            elif (not nextSpacePer.isSolid):
                #self.updateLocation(row, col, drow, dcol, 'persistant')
                return True
            else: return False
        # test overworld
        elif (dimension == 'overworld'):
            nextSpaceOver = self.level.overworld[row+drow][col+dcol]
            # test for key
            if (isinstance(nextSpaceOver, Game_elements.Key)):
                self.player.hasKey = True
                #self.updateLocation(row, col, drow, dcol, 'overworld')
                return True
            # test moveability
            elif (nextSpaceOver.isMovable):
                if (self.testCollisions(nextSpaceOver[0], nextSpaceOver[1], drow, dcol, 'overworld')):
                    nextSpaceOver = self.level.overworld[row+drow][col+dcol]
                    #self.updateLocation(row, col, drow, dcol, 'overworld')
                    return True
                else: return False
            # test for walls etc
            elif (not nextSpaceOver.isSolid):
                #self.updateLocation(row, col, drow, dcol, 'overworld')
                return True
            else: return False
        # test upsidedown
        elif (dimension == 'upsideDown'):
            nextSpaceUnder = self.level.upsideDown[row+drow][col+dcol]
            # test for key
            if (isinstance(nextSpaceUnder, Game_elements.Key)):
                self.player.hasKey = True
                #self.updateLocation(row, col, drow, dcol, 'upsideDown')
                return True
            # test moveability
            elif (nextSpaceUnder.isMovable):
                if (self.testCollisions(nextSpaceUnder.location[0], nextSpaceUnder.location[1], drow, dcol, 'upsideDown')):
                    nextSpaceUnder = self.level.upsideDown[row+drow][col+dcol]
                    #self.updateLocation(row, col, drow, dcol, 'upsideDown')
                    return True
                else: return False
            # test for walls etc
            elif (not nextSpaceUnder.isSolid):
                #self.updateLocation(row, col, drow, dcol, 'upsideDown')
                return True
            else: return False

    def updateLocation(self, row, col, drow, dcol, dimension):
        if (dimension == 'overworld'):
            self.level.overworld[row][col].location = (row+drow, col+dcol) # updated player location
            self.level.overworld[row+drow][col+dcol] = self.level.overworld[row][col]
            if not self.inPortal or self.justInPortal:
                self.level.overworld[row][col] = Game_elements.Floor()
            else:
                self.level.overworld[row][col] = Game_elements.Portal()
        elif (dimension == 'upsideDown'):
            self.level.upsideDown[row][col].location = (row+drow, col+dcol) # updated player location
            self.level.upsideDown[row+drow][col+dcol] = self.level.upsideDown[row][col]
            if not self.inPortal or self.justInPortal:
                self.level.upsideDown[row][col] = Game_elements.Floor()
            else:
                self.level.upsideDown[row][col] = Game_elements.Portal()
        else:
            self.level.persistant[row][col].location = (row+drow, col+dcol) # updated player location
            self.level.persistant[row+drow][col+dcol] = self.level.persistant[row][col]
            if not self.inPortal or self.justInPortal:
                self.level.persistant[row][col] = Game_elements.Floor()
            else:
                self.level.persistant[row][col] = Game_elements.Portal()

    def doMove(self, row, col, drow, dcol):
        if (row + drow >= self.rows or row + drow < 0 or col + dcol < 0 or col + dcol >= self.cols):
            return False
        if (self.testCollisions(row, col, drow, dcol, 'persistant') == False):
            return False
        if (self.isOverworld):
            if (self.testCollisions(row, col, drow, dcol, 'overworld') == False):
                return False
        else:
            if (self.testCollisions(row, col, drow, dcol, 'upsideDown') == False):
                return False

        self.updateLocation(row, col, drow, dcol, 'overworld')
        self.updateLocation(row, col, drow, dcol, 'upsideDown')
        self.updateLocation(row, col, drow, dcol, 'persistant')

        if self.justInPortal: 
            self.justInPortal = False
        else:
            if self.inPortal: self.inPortal = False
        return True


    def on_key_press(self, symbol, modifiers):
        if symbol == key.LEFT:
            self.doMove(self.player.location[0], self.player.location[1], 0, -1)
        elif symbol == key.RIGHT:
            self.doMove(self.player.location[0], self.player.location[1], 0, +1)
        elif symbol == key.UP:
            self.doMove(self.player.location[0], self.player.location[1], -1, 0)
        elif symbol == key.DOWN:
            self.doMove(self.player.location[0], self.player.location[1], +1, 0)

    def update(self, dt):
        for sprite in self.get_children():
            self.remove(sprite)
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

#elf.player = cocos.sprite.Sprite(pyglet.resource.image((Game_elements.Switch.over_on_img)))
class BackgroundLayer(cocos.layer.Layer):
    def __init__(self):
        super(BackgroundLayer, self).__init__()
        r = Game_elements.Player()
        self.image = cocos.sprite.Sprite(pyglet.image.load(r.overImg))
        self.image.position = 400, 75
        self.add(self.image, z=0)

        self.player = cocos.sprite.Sprite(pyglet.image.load(r.overImg))
        self.player.position = 0, 295
        self.add(self.player, z=1)

        self.enemy = cocos.sprite.Sprite(pyglet.image.load(r.overImg))
        self.enemy.position = 385, 75
        self.add(self.enemy, z=1)

        self.boss = cocos.sprite.Sprite(pyglet.image.load(r.overImg))
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