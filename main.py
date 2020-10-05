from gl import color, V2, V3
from ray import RayTracer
from obj import Obj, Texture, EnvMap
from sphere import *

brick = Material(diffuse=color(0.8, 0.25, 0.25), spec=16)
stone = Material(diffuse=color(0.7, 0.7, 0.7), spec=4)
mirror = Material(spec=64, mat_type=REFLECTIVE)

green = Material(diffuse=color(0.19, 0.82, 0.59), spec=32)
orange = Material(diffuse=color(0.96, 0.58, 0.13), spec=16)

glass = Material(spec=64, ior=1.5, mat_type=TRANSPARENT)

width = 256
height = 256
r = RayTracer(width, height)
r.gl_clear_color(0.2, 0.6, 0.8)
r.gl_clear()

r.env_map = EnvMap('envmap.bmp')

r.point_light = PointLight(position=V3(0, 0, 0), intensity=1)
r.ambient_light = AmbientLight(strength=0.1)

r.scene.append(Plane(V3(0, -3, 0), V3(0, 1, 0), stone))
r.scene.append(Plane(V3(0, 3, 0), V3(0, 1, 0), stone))
r.scene.append(Plane(V3(0, 0, -10), V3(0, 0, 1), stone))
r.scene.append(Plane(V3(-3, 0, 0), V3(1, 0, 0), stone))
r.scene.append(Plane(V3(3, 0, 0), V3(1, 0, 0), stone))

r.scene.append(AABB((-1.5, -1, -5), 1.5, green))
r.scene.append(AABB((1.5, -1, -5), 1.5, orange))



r.rt_render()

r.gl_finish('output.bmp')

