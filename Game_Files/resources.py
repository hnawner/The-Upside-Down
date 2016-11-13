import pyglet
import levelFetcher

pyglet.resource.path = ["resources/Upside_Down"]
pyglet.resource.reindex()

player = pyglet.resource.image("u_keywall.png")
enemy = pyglet.resource.image("u_wall.png")
boss = pyglet.resource.image("u_off-switch.png")
background = pyglet.resource.image("u_on-switch.png")

level = levelFetcher.getLevel(1)
o_board = level.overworld
u_board = level.upsideDown
p_board = level.persistant

game_music = pyglet.resource.media('tetris.mp3', streaming=False)