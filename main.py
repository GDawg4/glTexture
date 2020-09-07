from gl import color, V2, V3
from ray import RayTracer
from obj import Obj, Texture
from sphere import Sphere, Material

snow = Material(diffuse=color(1, 1, 1))
charcoal = Material(diffuse=color(0, 0, 0))
orange = Material(diffuse=color(1, 0.27, 0))
light_grey = Material(diffuse=color(0.8, 0.8, 0.8))
grey = Material(diffuse=color(0.5, 0.5, 0.5))

width = 500
height = 800
r = RayTracer(width, height)

r.clear_color = color(0, 0, 0.5)
r.gl_clear()

r.scene.append(Sphere(V3(0, -2, -7), 1, snow))
r.scene.append(Sphere(V3(0, -1.75, -6), 0.25, charcoal))
r.scene.append(Sphere(V3(0, -0.5, -7), 0.8, snow))
r.scene.append(Sphere(V3(0, -1, -6), 0.15, charcoal))
r.scene.append(Sphere(V3(0, 0.7, -7), 0.6, snow))
r.scene.append(Sphere(V3(0, -0.37, -6), 0.15, charcoal))
r.scene.append(Sphere(V3(0, 0.6, -6), 0.05, orange))

r.scene.append(Sphere(V3(0.145, 0.45, -6), 0.05, grey))
r.scene.append(Sphere(V3(-0.145, 0.45, -6), 0.05, grey))
r.scene.append(Sphere(V3(0.055, 0.4, -6), 0.05, grey))
r.scene.append(Sphere(V3(-0.055, 0.4, -6), 0.05, grey))

r.scene.append(Sphere(V3(0.145, 0.7, -6), 0.05, light_grey))
r.scene.append(Sphere(V3(-0.145, 0.7, -6), 0.05, light_grey))

r.scene.append(Sphere(V3(0.125, 0.58, -5), 0.02, charcoal))
r.scene.append(Sphere(V3(-0.125, 0.58, -5), 0.02, charcoal))

r.rt_render()

r.gl_finish('output.bmp')

