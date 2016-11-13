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
        #r,g,b,a
        self.level = levelFetcher.getLevel(levelNum)


        self.collision_manager = cm.CollisionManagerBruteForce()

        s = Game_elements.Switch()
        self.player = cocos.sprite.Sprite(pyglet.resource.image(s.over_on_img))
        self.player.position = 48, 16+7*32
        self.player.velocity = 0, 0
        self.player.speed = 150
        self.add(self.player, z=2)

        self.player.cshape = cm.AARectShape(
            self.player.position,
            self.player.width//2,
            self.player.height//2
        )
        self.collision_manager.add(self.player)
        


        #self.boss = cocos.sprite.Sprite(resources.boss)
        #self.boss.position = 400, 600
        #self.boss.scale = 0.4
        #self.add(self.boss, z=1)

        #self.boss.cshape = cm.AARectShape(
        #    self.boss.position,
        #    self.boss.width//2,
        #    self.boss.height//2
        #)
        #self.collision_manager.add(self.boss)


        #self.o_board = resources.o_board
        #self.u_board = resources.u_board
        #self.p_board = resources.p_board

        self.rows = len(self.level.overworld)
        self.cols = len(self.level.overworld[0])
        #upsideDown
        #persistant

        self.objects = list(range(self.rows**2))

        #[cocos.sprite.Sprite(resources.enemy)
         #               for i in range(100)]

        for row in range(self.rows):
            for col in range(self.cols):
                if self.level.overworld[row][col] == 'W':
                    self.objects[10*row+col] = cocos.sprite.Sprite(pyglet.resource.image((Game_elements.Wall.overImg)))
                    self.objects[10*row+col].position = 16+32*col, -16+32*(self.rows-row)
                    #self.enemies[10*row+col].position = 16+32*col, -16+32*(self.rows-row)
        #enem.position = positions[num]
                    self.objects[10*row+col].cshape = cm.AARectShape(
                        self.objects[10*row+col].position,
                        self.objects[10*row+col].width//2,
                        self.objects[10*row+col].height//2
                    )
                    self.collision_manager.add(self.objects[10*row+col])
                    self.add(self.objects[10*row+col], z=1)
                if self.level.overworld[row][col] == 'P':
                    pass

                    #self.batch.add(self.enemies[10*row+col])
        #for enem in self.enemies:
         #   self.batch.add(enem)

        #self.add(self.batch, z=1)





        #self.player.do(Move())

        # move_basic = MoveBy((120, 0), 1)
        # self.enemies[0].do(Repeat(move_basic + Reverse(move_basic)))
        # self.enemies[1].do(Repeat(Reverse(move_basic) + move_basic))

        # move_complex = (MoveBy((-75, 75), 1) +
        #                 Delay(0.5) +
        #                 MoveBy((-75, -75), 1) +
        #                 Delay(0.5) +
        #                 MoveBy((75, -75), 1) +
        #                 Delay(0.5) +
        #                 MoveBy((75, 75), 1) +
        #                 Delay(0.5))
        # self.enemies[2].do(Repeat(move_complex))
        # self.enemies[3].do(Repeat(Reverse(move_complex)))

        # move_jump = AccelDeccel(JumpBy((200, 0), 75, 3, 3))
        # move_jump_rot = AccelDeccel(RotateBy(360, 3))
        # self.enemies[4].do(Repeat(move_jump + Reverse(move_jump)))
        # self.enemies[4].do(Repeat(move_jump_rot + Reverse(move_jump_rot)))
        # self.enemies[5].do(Repeat(Reverse(move_jump) + move_jump))
        # self.enemies[5].do(Repeat(Reverse(move_jump_rot) + move_jump_rot))

        self.schedule(self.update)

    #def on_enter(self):
    #    super(Game, self).on_enter()

        # try:
        #     music_player.queue(resources.game_music)
        # except:
        #     pass

        # music_player.play()

        # music_player.eos_action = 'loop'

    def on_exit(self):
        super(Game, self).on_exit()

        music_player.seek(1)
        music_player.pause()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.LEFT:
            self.player.position = self.player.position[0] -32, self.player.position[1]
            self.player.cshape.center = self.player.position
            collisions = self.collision_manager.objs_colliding(self.player)
            if collisions:
                self.player.position = self.player.position[0] +32, self.player.position[1]

        elif symbol == key.RIGHT:
            self.player.position = self.player.position[0] +32, self.player.position[1]
            self.player.cshape.center = self.player.position
            collisions = self.collision_manager.objs_colliding(self.player)
            if collisions:
                self.player.position = self.player.position[0] -32, self.player.position[1]

        elif symbol == key.UP:
            self.player.position = self.player.position[0], self.player.position[1] +32
            self.player.cshape.center = self.player.position
            collisions = self.collision_manager.objs_colliding(self.player)
            if collisions:
                self.player.position = self.player.position[0], self.player.position[1] -32

        elif symbol == key.DOWN:
            self.player.position = self.player.position[0], self.player.position[1] -32
            self.player.cshape.center = self.player.position
            collisions = self.collision_manager.objs_colliding(self.player)
            if collisions:
                self.player.position = self.player.position[0], self.player.position[1] +32


    def update(self, dt):
        collisions = self.collision_manager.objs_colliding(self.player)
        if collisions:
            if self.boss in collisions:
                print("You won!")
            #self.player.velocity = 0, 0
            #self.player.position = self.player.position[0] - 1,self.player.position[1] - 1
            self.player.cshape.center = self.player.position
        else:
            self.player.cshape.center = self.player.position
            #for enem in self.enemies:
             #   enem.cshape.center = enem.position
            



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
        s = Game_elements.Switch()
        self.image = cocos.sprite.Sprite(pyglet.resource.image((s.over_on_img)))
        self.image.position = 400, 325
        self.add(self.image, z=0)

        self.player = cocos.sprite.Sprite(pyglet.resource.image((s.over_on_img)))
        self.player.position = 200, 75
        self.add(self.player, z=1)

        self.enemy = cocos.sprite.Sprite(pyglet.resource.image((s.over_on_img)))
        self.enemy.position = 400, 75
        self.add(self.enemy, z=1)

        self.boss = cocos.sprite.Sprite(pyglet.resource.image((s.over_on_img)))
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