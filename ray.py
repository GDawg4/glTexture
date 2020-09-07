import struct
from collections import namedtuple
from math import sqrt, tan, sin, cos, pi
from linear_algebra import V2, V3, V4, vector3_norm, multiply_vector_with_constant

from obj import Obj
from linear_algebra import *


def char(c):
    return struct.pack('=c', c.encode('ascii'))


def word(w):
    return struct.pack('=h', w)


def dword(d):
    # 4 bytes
    return struct.pack('=l', d)


def color(r, g, b):
    return bytes([int(b * 255), int(g * 255), int(r * 255)])


BLACK = color(0, 0, 0)
WHITE = color(1, 1, 1)

RED = color(1, 0, 0)
GREEN = color(0, 1, 0)
BLUE = color(0, 0, 1)

YELLOW = color(1, 1, 0)
PURPLE = color(1, 0, 1)
AQUA = color(0, 1, 1)

class RayTracer(object):
    def __init__(self, width, height):
        self.curr_color = WHITE
        self.clear_color = BLACK
        self.gl_create_window(width, height)

        self.camPosition = V3(0, 0, 0)
        self.fov = 60

        self.scene = []

    def gl_create_window(self, width, height):
        self.width = width
        self.height = height
        self.gl_clear()
        self.gl_viewport(0, 0, width, height)

    def gl_viewport(self, x, y, width, height):
        self.vp_x = x
        self.vp_y = y
        self.vp_width = width
        self.vp_height = height

    def gl_clear(self):
        self.pixels = [[self.clear_color for x in range(self.width)] for y in range(self.height)]

        # Z - buffer, depthbuffer, buffer de profudidad
        self.z_buffer = [[float('inf') for x in range(self.width)] for y in range(self.height)]

    def gl_background(self, texture):

        self.pixels = [[texture.getColor(x / self.width, y / self.height) for x in range(self.width)] for y in
                       range(self.height)]

    def gl_vertex(self, x, y, color_to_paint=None):
        pixel_x = (x + 1) * (self.vp_width / 2) + self.vp_x
        pixel_y = (y + 1) * (self.vp_height / 2) + self.vp_y

        if pixel_x >= self.width or pixel_x < 0 or pixel_y >= self.height or pixel_y < 0:
            return

        try:
            self.pixels[round(pixel_y)][round(pixel_x)] = color_to_paint or self.curr_color
        except:
            pass

    def gl_vertex_coord(self, x, y, color=None):
        if x < self.vp_x or x >= self.vp_x + self.vp_width or y < self.vp_y or y >= self.vp_y + self.vp_height:
            return

        if x >= self.width or x < 0 or y >= self.height or y < 0:
            return

        try:
            self.pixels[y][x] = color or self.curr_color
        except:
            pass

    def gl_color(self, r, g, b):
        self.curr_color = color(r, g, b)

    def gl_clear_color(self, r, g, b):
        self.clear_color = color(r, g, b)

    def gl_finish(self, filename):
        archivo = open(filename, 'wb')

        # File header 14 bytes
        archivo.write(bytes('B'.encode('ascii')))
        archivo.write(bytes('M'.encode('ascii')))
        archivo.write(dword(14 + 40 + self.width * self.height * 3))
        archivo.write(dword(0))
        archivo.write(dword(14 + 40))

        # Image Header 40 bytes
        archivo.write(dword(40))
        archivo.write(dword(self.width))
        archivo.write(dword(self.height))
        archivo.write(word(1))
        archivo.write(word(24))
        archivo.write(dword(0))
        archivo.write(dword(self.width * self.height * 3))
        archivo.write(dword(0))
        archivo.write(dword(0))
        archivo.write(dword(0))
        archivo.write(dword(0))

        # Pixeles, 3 bytes cada uno
        for x in range(self.height):
            for y in range(self.width):
                archivo.write(self.pixels[x][y])

        archivo.close()

    def gl_z_buffer(self, filename):
        archivo = open(filename, 'wb')

        # File header 14 bytes
        archivo.write(bytes('B'.encode('ascii')))
        archivo.write(bytes('M'.encode('ascii')))
        archivo.write(dword(14 + 40 + self.width * self.height * 3))
        archivo.write(dword(0))
        archivo.write(dword(14 + 40))

        # Image Header 40 bytes
        archivo.write(dword(40))
        archivo.write(dword(self.width))
        archivo.write(dword(self.height))
        archivo.write(word(1))
        archivo.write(word(24))
        archivo.write(dword(0))
        archivo.write(dword(self.width * self.height * 3))
        archivo.write(dword(0))
        archivo.write(dword(0))
        archivo.write(dword(0))
        archivo.write(dword(0))

        # Minimo y el maximo
        min_z = float('inf')
        max_z = -float('inf')
        for x in range(self.height):
            for y in range(self.width):
                if self.z_buffer[x][y] != -float('inf'):
                    if self.z_buffer[x][y] < min_z:
                        min_z = self.z_buffer[x][y]

                    if self.z_buffer[x][y] > max_z:
                        max_z = self.z_buffer[x][y]

        for x in range(self.height):
            for y in range(self.width):
                depth = self.z_buffer[x][y]
                if depth == -float('inf'):
                    depth = min_z
                depth = (depth - min_z) / (max_z - min_z)
                archivo.write(color(depth, depth, depth))

        archivo.close()

    def rt_render(self):
        # pixel por pixel
        for y in range(self.height):
            for x in range(self.width):

                # pasar valor de pixel a coordenadas NDC (-1 a 1)
                p_x = 2 * ((x + 0.5) / self.width) - 1
                p_y = 2 * ((y + 0.5) / self.height) - 1

                # FOV(angulo de vision), asumiendo que el near plane esta a 1 unidad de la camara
                t = tan((self.fov * pi / 180) / 2)
                r = t * self.width / self.height
                p_x *= r
                p_y *= t

                # Nuestra camara siempre esta viendo hacia -Z
                direction = V3(p_x, p_y, -1)
                direction = multiply_vector_with_constant(direction, 1/vector3_norm(direction))

                material = None

                for obj in self.scene:
                    intersect = obj.ray_intersect(self.camPosition, direction)
                    if intersect is not None:
                        if intersect.distance < self.z_buffer[y][x]:
                            self.z_buffer[y][x] = intersect.distance
                            material = obj.material

                if material is not None:
                    self.gl_vertex_coord(x, y, material.diffuse)

