from gl import GL
from linear_algebra import V2, V3, V4, vector3_norm, multiply_vector_with_constant
from obj import Texture
from shaders import *

lower_left = V2(-1, -1)
lower_right = V2(1, -1)
top_left = V2(-1, 1)
top_right = V2(1, 1)
center = V2(0, 0)

r = GL(1000, 1000)
r.active_shader = toon_shader
light = V3(1, 0, 1)
r.light = multiply_vector_with_constant(light, 1/vector3_norm(light))
t = Texture('./textures/model.bmp')
r.active_texture = t
r.load_model('./models/model.obj',
             scale=V3(300, 300, 300),
             translate=V3(500, 500, 0))

#r.gl_zbuffer('zbuffer.bmp')
r.gl_finish('test.bmp')