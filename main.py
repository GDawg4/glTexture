from gl import color, V2, V3
from ray import RayTracer
from obj import Obj, Texture, EnvMap
from sphere import *

brick = Material(diffuse=color(0.8, 0.25, 0.25), spec=16)
brickMat = Material(texture=Texture('brick2.bmp'))
stone = Material(diffuse=color(0.7, 0.7, 0.7), spec=16)
stoneMap = Material(texture=Texture('stone.bmp'))
mirror = Material(spec=64, mat_type=REFLECTIVE)
wood = Material(diffuse=color(0.71, 0.40, 0.11), spec=16)
water = Material(diffuse=color(0.61, 0.83, 0.86), spec=16, mat_type=REFLECTIVE)

green = Material(diffuse=color(0.19, 0.82, 0.59), spec=32)
orange = Material(diffuse=color(0.96, 0.58, 0.13), spec=16)

boxMat = Material(texture = Texture('box.bmp'))

earthMat = Material(texture = Texture('earthDay.bmp'))

glass = Material(spec=64, ior=1.5, mat_type=TRANSPARENT)

width = 512
height = 512
r = RayTracer(width, height)
r.gl_clear_color(0.2, 0.6, 0.8)
r.gl_clear()

r.env_map = EnvMap('envMap2.bmp')

r.dir_light = DirectionalLight(direction = V3(1, -1, -2), intensity = 0.5)
r.ambient_light = AmbientLight(strength = 0.1)
r.point_lights.append(PointLight(position=V3(-2, 5, -15), intensity=0.2))
r.point_lights.append(PointLight(position=V3(2, 5, -15), intensity=0.2))

#House
r.scene.append(Sphere((0, 5, -15), 2, earthMat))
for y in range(-2, 3):
    for x in range(-3, 4):
        if x == 0 and y != 2:
            r.scene.append(AABB((x, y, -15), (1, 1, 1), boxMat))
        elif (x == -2 or x == 2) and y == 0:
            r.scene.append(AABB((x, y, -15), (1, 1, 1), glass))
        else:
            r.scene.append(AABB((x, y, -15), (1, 1, 1), brickMat))
        r.scene.append(AABB((x, y, -20), (1, 1, 1), brickMat))
#
    for x in range(-20, -15):
        r.scene.append(AABB((-3, y, x), (1, 1, 1), brickMat))
        r.scene.append(AABB((3, y, x), (1, 1, 1), brickMat))

for z in range(-15, 0):
    for x in range(-1, 2):
        r.scene.append(AABB((x, -2, z), (1, 0.1, 1), stoneMap))

for y in range(-11, 3):
    for x in range(-8, -3):
        r.scene.append(AABB((x, y, -15), (1, 1, 0.1), water))
    for x in range(4, 9):
        r.scene.append(AABB((x, y, -15), (1, 1, 0.1), water))

r.rt_render()

r.gl_finish('output.bmp')

