from gl import GL
from linear_algebra import V2, V3, V4, vector3_norm, multiply_vector_with_constant
from obj import Texture
from shaders import *

lower_left = V2(-1, -1)
lower_right = V2(1, -1)
top_left = V2(-1, 1)
top_right = V2(1, 1)
center = V2(0, 0)


# light = V3(1, 0, 1)
#
# r.light = multiply_vector_with_constant(light, 1/vector3_norm(light))

r = GL(500, 500)

r.active_texture = Texture('./textures/model.bmp')
r.active_shader = gourad

pos_model = V3(0, 0, -5)

r.look_at(pos_model, V3(0, 3, 0))
r.load_model('./models/model.obj',
             pos_model,
             V3(2, 2, 2),
             V3(0, 0, 0))

r.gl_finish('high.bmp')

r.look_at(pos_model, V3(0, 0, 0))
r.load_model('./models/model.obj',
             pos_model,
             V3(2, 2, 2),
             V3(0, 0, 0))
r.gl_finish('med.bmp')


r.look_at(pos_model, V3(0, -1, 0))
r.load_model('./models/model.obj',
             pos_model,
             V3(2, 2, 2),
             V3(0, 0, 0))
r.gl_finish('low.bmp')

r.look_at(pos_model, V3(0, 0, 1))
r.load_model('./models/model.obj',
             pos_model,
             V3(2, 2, 2),
             V3(0, 0, 25))
r.gl_finish('dutch.bmp')