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

    def redrawAll(self):
        for row in range(self.rows):
            for col in range(self.cols):
                currentObject = self.level.overworld[row][col]
                currentSprite = cocos.sprite.Sprite(pyglet.image.load((currentObject.overImg)))
                currentSprite.position = 16+32*col, -16+32*(self.rows-row)
                self.add(currentSprite, z=1)

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

    def on_key_press(self, symbol, modifiers):
        if symbol == key.LEFT:
            print("going left")
        elif symbol == key.RIGHT:
            print("going right")
        elif symbol == key.UP:
            print("going up")
        elif symbol == key.DOWN:
            print("going down")

    def update(self, dt):
        for sprite in self.get_children():
            self.remove(sprite)
        self.redrawAll()

class MainMenu(cocos.menu.Menu):

    def __init__(self):
        super(MainMenu, self).__init__('Catch your husband!')

        self.font_title['font_name'] = 'Edit Undo Line BRK'
        self.font_title['font_size'] = 52
        self.font_title['color'] = (240, 0, 220, 255)

        self.font_item['color'] = (255, 255, 255, 255)
        self.font_item_selected['color'] = (240, 0, 220, 255)

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
        super(OptionsMenu, self).__init__('Catch your husband!')

        self.font_title['font_name'] = 'Edit Undo Line BRK'
        self.font_title['font_size'] = 52
        self.font_title['color'] = (240, 0, 220, 255)

        self.font_item['color'] = (255, 255, 255, 255)
        self.font_item_selected['color'] = (240, 0, 220, 255)

        items = []

        items.append(cocos.menu.ToggleMenuItem(
            'Show FPS:',
            self.on_show_fps,
            cocos.director.director.show_FPS)
        )
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
        r = Game_elements.Rock()
        self.image = cocos.sprite.Sprite(pyglet.image.load(r.overImg))
        self.image.position = 400, 325
        self.add(self.image, z=0)

        self.player = cocos.sprite.Sprite(pyglet.image.load(r.overImg))
        self.player.position = 200, 75
        self.add(self.player, z=1)

        self.enemy = cocos.sprite.Sprite(pyglet.image.load(r.overImg))
        self.enemy.position = 400, 75
        self.add(self.enemy, z=1)

        self.boss = cocos.sprite.Sprite(pyglet.image.load(r.overImg))
        self.boss.scale = 0.4
        rect = self.boss.get_rect()
        rect.midbottom = 600, 50
        self.boss.position = rect.center
        self.add(self.boss, z=1)

        self.player.do(Repeat(JumpBy((0, 0), 100, 1, 1)))
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