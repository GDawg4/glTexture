from gl import GL
from linear_algebra import V2, V3, V4, vector3_norm, multiply_vector_with_constant
from obj import Texture
from shaders import *
import random

lower_left = V2(-1, -1)
lower_right = V2(1, -1)
top_left = V2(-1, 1)
top_right = V2(1, 1)
center = V2(0, 0)

r = GL(1920, 1080)
light = V3(-1, 1, 1)

for x in range(2, 1920 - 2):
    for y in range(2, 1080 - 2):

        size = random.randint(1, 2400)
        if size == 1:
            r.gl_vertex_coord(x, y)
        elif size == 2:
            r.gl_vertex_coord(x, y)
            r.gl_vertex_coord(x + 1, y)
            r.gl_vertex_coord(x, y + 1)
            r.gl_vertex_coord(x - 1, y)
            r.gl_vertex_coord(x, y - 1)

#
r.light = multiply_vector_with_constant(light, 1/vector3_norm(light))
r.active_shader = gourad

posModel = V3(0, 0, -5)
r.look_at(posModel, V3(2, 2, 0))
r.active_shader = black_and_white
r.active_texture = Texture('./textures/cty1.bmp')
r.load_model('./models/city.obj', V3(1.5, 0.7, -7), V3(0.006, 0.002, 0.002), V3(0, 30, 0))
r.active_shader = toon_shader
r.active_texture = Texture('./textures/rock1.bmp')
r.load_model('./models/rock1.obj', V3(-5, 2, -5), V3(0.002, 0.002, 0.002), V3(0, 0, 0))
r.load_model('./models/rock1.obj', V3(4, -2, -5), V3(0.002, 0.002, 0.002), V3(0, 0, 25))
r.active_texture = Texture('./textures/street.bmp')
r.load_model('./models/street.obj', V3(-0.5, -0.5, -5), V3(0.002, 0.002, 0.006), V3(0, 25, 0))
r.active_shader = gourad
r.active_texture = Texture('./textures/jeep.bmp')
r.load_model('./models/jeep.obj', V3(0.5, 0, -3), V3(0.4, 0.4, 0.4), V3(0, -150, 0))
r.active_texture = Texture('./textures/ufo.bmp')
r.load_model('./models/ufo.obj', V3(-7, -3, -8), V3(0.055, 0.055, 0.055), V3(20, 0, 0))
# r.gl_finish('scene.bmp')
r.gl_finish('scene2.bmp')


# r.look_at(pos_model, V3(0, 0, 1))
# r.load_model('./models/model.obj',
#              pos_model,
#              V3(2, 2, 2),
#              V3(0, 0, 25))
# r.gl_finish('dutch.bmp')