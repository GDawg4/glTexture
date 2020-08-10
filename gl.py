import struct
from collections import namedtuple
from math import sqrt

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


class GL(object):
    def __init__(self, width, height):
        self.curr_color = WHITE
        self.clear_color = BLACK
        self.active_texture = None
        self.active_texture2 = None
        self.active_shader = None
        self.gl_create_window(width, height)

    def gl_create_window(self, width, height):
        self.width = width
        self.height = height
        self.gl_clear()
        self.gl_viewport(0, 0, width, height)

    def gl_viewport(self, x, y, width, height):
        self.view_port_x = x
        self.view_port_y = y
        self.view_port_width = width
        self.view_port_heigth = height

    def gl_clear(self):
        self.pixels = [[self.clear_color for x in range(self.width)] for y in range(self.height)]
        self.z_buffer = [[-float('inf') for x in range(self.width)] for y in range(self.height)]

    def gl_vertex(self, x, y, point_color=None):
        pixel_x = (x+1)*(self.view_port_width/2) + self.view_port_x
        pixel_y = (y+1) * (self.view_port_width / 2) + self.view_port_y

        if pixel_x >= self.width or pixel_x < 0 or pixel_y >= self.height or pixel_y < 0:
            return

        try:
            self.pixels[round(pixel_y)][round(pixel_x)] = color or self.curr_color
        except:
            pass

    def gl_vertex_coord(self, x, y, point_color=None):
        if x >= self.width or x < 0 or y >= self.height or y < 0:
            return

        try:
            self.pixels[y][x] = point_color or self.curr_color
        except:
            pass

    def gl_color(self, r, g, b):
        self.curr_color = color(r, g, b)

    def gl_clear_color(self, r, g, b):
        self.clear_color = color(r, g, b)

    def gl_finish(self, file_name):
        file = open(file_name, 'wb')

        file.write(bytes('B'.encode('ascii')))
        file.write(bytes('M'.encode('ascii')))
        file.write(dword(14 + 40 + self.width * self.height * 3))
        file.write(dword(0))
        file.write(dword(14 + 40))

        # Image Header 40 bytes
        file.write(dword(40))
        file.write(dword(self.width))
        file.write(dword(self.height))
        file.write(word(1))
        file.write(word(24))
        file.write(dword(0))
        file.write(dword(self.width * self.height * 3))
        file.write(dword(0))
        file.write(dword(0))
        file.write(dword(0))
        file.write(dword(0))

        for x in range(self.height):
            for y in range(self.width):
                file.write(self.pixels[x][y])

        file.close()

    def gl_zbuffer(self, filename):
        file = open(filename, 'wb')

        file.write(bytes('B'.encode('ascii')))
        file.write(bytes('M'.encode('ascii')))
        file.write(dword(14 + 40 + self.width * self.height * 3))
        file.write(dword(0))
        file.write(dword(14 + 40))

        file.write(dword(40))
        file.write(dword(self.width))
        file.write(dword(self.height))
        file.write(word(1))
        file.write(word(24))
        file.write(dword(0))
        file.write(dword(self.width * self.height * 3))
        file.write(dword(0))
        file.write(dword(0))
        file.write(dword(0))
        file.write(dword(0))

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
                file.write(color(depth, depth, depth))

        file.close()

    def gl_line(self, v0, v1, color=None):  # NDC
        x_0 = round((v0.x + 1) * (self.view_port_width / 2) + self.view_port_x)
        x_1 = round((v1.x + 1) * (self.view_port_width / 2) + self.view_port_x)
        y_0 = round((v0.y + 1) * (self.view_port_heigth / 2) + self.view_port_y)
        y_1 = round((v1.y + 1) * (self.view_port_heigth / 2) + self.view_port_y)

        self.gl_line_coord(V2(x_0, y_0), V2(x_1, y_1))

    def gl_line_coord(self, v0, v1, color=None):
        x_0 = v0.x
        y_0 = v0.y
        x_1 = v1.x
        y_1 = v1.y

        dx = abs(x_1 - x_0)
        dy = abs(y_1 - y_0)

        steep = dy > dx

        if steep:
            x_0, y_0 = y_0, x_0
            x_1, y_1 = y_1, x_1

        if x_0 > x_1:
            x_0, x_1 = x_1, x_0
            y_0, y_1 = y_1, y_0

        dx = abs(x_1 - x_0)
        dy = abs(y_1 - y_0)

        offset = 0
        limit = 0.5

        if dx == 0:
            if v0.x == v1.x:
                for i in range(v0.y, v1.y):
                    self.gl_vertex_coord(v0.x, i, color)
            elif v0.y == v1.y:
                for i in range(v0.x, v1.x):
                    self.gl_vertex_coord(i, v0.y, color)
        else:
            m = dy / dx
            y = y_0
            for x in range(x_0, x_1 + 1):
                if steep:
                    self.gl_vertex_coord(y, x, color)
                else:
                    self.gl_vertex_coord(x, y, color)

                offset += m
                if offset >= limit:
                    y += 1 if y_0 < y_1 else -1
                    limit += 1


    def draw_poly(self, points, color=None):
        count = len(points)
        for i in range(count):
            v0 = points[i]
            v1 = points[(i + 1) % count]
            self.gl_line_coord(v0, v1, color)

    def load_model(self, file_name, scale=V3(1, 1, 1), translate=V3(0, 0, 0), texture=None, is_wireframe=False):
        model = Obj(file_name)

        light = V3(0, 0, 1)

        for face in model.faces:
            vert_count = len(face)
            if is_wireframe:
                for vert in range(vert_count):
                    v0 = model.vertices[face[vert][0] - 1]
                    v1 = model.vertices[face[(vert + 1) % vert_count][0] - 1]
                    v0 = V2(round(v0[0] * scale.x + translate.x), round(v0[1] * scale.y + translate.y))
                    v1 = V2(round(v1[0] * scale.x + translate.x), round(v1[1] * scale.y + translate.y))
                    self.gl_line_coord(v0, v1)

            else:
                v0 = model.vertices[face[0][0] - 1]
                v1 = model.vertices[face[1][0] - 1]
                v2 = model.vertices[face[2][0] - 1]
                if vert_count > 3:
                    v3 = model.vertices[face[3][0] - 1]

                v0 = transform(v0, scale=scale, translate=translate)
                v1 = transform(v1, scale=scale, translate=translate)
                v2 = transform(v2, scale=scale, translate=translate)
                if vert_count > 3:
                    v3 = transform(v3, scale=scale, translate=translate)

                if texture:
                    vt0 = model.tex_coords[face[0][1] - 1]
                    vt1 = model.tex_coords[face[1][1] - 1]
                    vt2 = model.tex_coords[face[2][1] - 1]
                    vt0 = V2(vt0[0], vt0[1])
                    vt1 = V2(vt1[0], vt1[1])
                    vt2 = V2(vt2[0], vt2[1])
                    if vert_count > 3:
                        vt3 = model.tex_coords[face[3][1] - 1]
                        vt3 = V2(vt3[0], vt3[1])
                else:
                    vt0 = V2(0, 0)
                    vt1 = V2(0, 0)
                    vt2 = V2(0, 0)
                    vt3 = V2(0, 0)

                normal = cross_product(substract_vectors(v0, v1), substract_vectors(v0, v2))
                #print(v0, v1, v2)
                #print(self.substract_vectors(v0, v1), self.substract_vectors(v0, v2))
                #print(normal)
                if vector3_norm(normal) != 0:
                    normal = multiply_vector_with_constant(normal, 1/vector3_norm(normal))
                #print(self.vector3_norm(normal))

                intensity = point_product(normal, light)
                #print(intensity)
                #print(vt0, vt1, vt2)
                if intensity >= 0:
                    self.triangle_bc(v0, v1, v2, texture=texture, tex_coords=(vt0, vt1, vt2), intensity=intensity)
                    #print(v0, v1, v2)
                    #print(vt0, vt1, vt2)
                    #print(intensity, '\n')
                    if vert_count > 3:  # asumamos que 4, un cuadrado
                        self.triangle_bc(v0, v2, v3,
                                         texture=texture,
                                         tex_coords=(vt0, vt2, vt3),
                                         intensity=intensity)

    def triangle(self, A, B, C, color=None):
        def flat_bottom_triangle(v1, v2, v3):
            # self.drawPoly([v1,v2,v3], color)
            for y in range(v1.y, v3.y + 1):
                xi = round(v1.x + (v3.x - v1.x) / (v3.y - v1.y) * (y - v1.y))
                xf = round(v2.x + (v3.x - v2.x) / (v3.y - v2.y) * (y - v2.y))

                if xi > xf:
                    xi, xf = xf, xi

                for x in range(xi, xf + 1):
                    self.gl_vertex_coord(x, y, color or self.curr_color)

        def flat_top_triangle(v1, v2, v3):
            for y in range(v1.y, v3.y + 1):
                xi = round(v2.x + (v2.x - v1.x) / (v2.y - v1.y) * (y - v2.y))
                xf = round(v3.x + (v3.x - v1.x) / (v3.y - v1.y) * (y - v3.y))

                if xi > xf:
                    xi, xf = xf, xi

                for x in range(xi, xf + 1):
                    self.gl_vertex_coord(x, y, color or self.curr_color)

        # A.y <= B.y <= Cy
        if A.y > B.y:
            A, B = B, A
        if A.y > C.y:
            A, C = C, A
        if B.y > C.y:
            B, C = C, B

        if A.y == C.y:
            return

        if A.y == B.y:  # En caso de la parte de abajo sea plana
            flat_bottom_triangle(A, B, C)
        elif B.y == C.y:  # En caso de que la parte de arriba sea plana
            flat_top_triangle(A, B, C)
        else:  # En cualquier otro caso
            # y - y1 = m * (x - x1)
            # B.y - A.y = (C.y - A.y)/(C.x - A.x) * (D.x - A.x)
            # Resolviendo para D.x
            x4 = A.x + (C.x - A.x) / (C.y - A.y) * (B.y - A.y)
            D = V2(round(x4), B.y)
            flat_bottom_triangle(D, B, C)
            flat_top_triangle(A, B, D)

    # Barycentric Coordinates
    def triangle_bc(self, A, B, C, _color=WHITE, texture=None, tex_coords=(), intensity=1):
        # bounding box
        minX = min(A.x, B.x, C.x)
        minY = min(A.y, B.y, C.y)
        maxX = max(A.x, B.x, C.x)
        maxY = max(A.y, B.y, C.y)

        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                if x >= self.width or x < 0 or y >= self.height or y < 0:
                    continue

                u, v, w = bary_coords(A, B, C, V2(x, y))
                #print(A, B, C)
                if u >= 0 and v >= 0 and w >= 0:

                    z = A.z * u + B.z * v + C.z * w
                    if z > self.z_buffer[y][x]:

                        b, g, r = _color
                        b /= 255
                        g /= 255
                        r /= 255

                        b *= intensity
                        g *= intensity
                        r *= intensity

                        if texture:
                            ta, tb, tc = tex_coords
                            tx = ta.x * u + tb.x * v + tc.x * w
                            ty = ta.y * u + tb.y * v + tc.y * w

                            tex_color = texture.get_color(tx, ty)
                            b *= tex_color[0] / 255
                            g *= tex_color[1] / 255
                            r *= tex_color[2] / 255

                        self.gl_vertex_coord(x, y, point_color=color(r, g, b))
                        self.z_buffer[y][x] = z











