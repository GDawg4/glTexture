import struct
from collections import namedtuple
from math import sqrt, tan, sin, cos, pi
from linear_algebra import V2, V3, V4, vector3_norm, multiply_vector_with_constant

from obj import Obj
from linear_algebra import *

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2
MAX_RECURSION_DEPTH = 3

def char(c):
    return struct.pack('=c', c.encode('ascii'))


def word(w):
    return struct.pack('=h', w)


def dword(d):
    # 4 bytes
    return struct.pack('=l', d)


def color(r, g, b):
    return bytes([int(b * 255), int(g * 255), int(r * 255)])


def reflect_vector(normal, dirVector):
    # R = 2 * (N dot L) * N - L
    reflect = 2 * point_product(normal, dirVector)
    reflect = multiply_vector_with_constant(normal, reflect)
    reflect = substract_vectors(dirVector, reflect)
    reflect = multiply_vector_with_constant(reflect, 1/vector3_norm(reflect))
    return reflect


def refract_vector(N, I, ior):
    # N = normal
    # I = incident vector
    # ior = index of refraction
    # Snell's Law
    cosi = max(-1, min(1, point_product(I, N)))
    etai = 1
    etat = ior

    if cosi < 0:
        cosi = -cosi
    else:
        etai, etat = etat, etai
        N = multiply_vector_with_constant(N, -1)

    eta = etai / etat
    k = 1 - eta * eta * (1 - (cosi * cosi))

    if k < 0:  # Total Internal Reflection
        return None

    R = add_vectors(multiply_vector_with_constant(I, eta), multiply_vector_with_constant(N, eta * cosi - k ** 0.5))
    return multiply_vector_with_constant(R, 1/vector3_norm(R))


def fresnel(N, I, ior):
    # N = normal
    # I = incident vector
    # ior = index of refraction
    cosi = max(-1, min(1, point_product(I, N)))
    etai = 1
    etat = ior

    if cosi > 0:
        etai, etat = etat, etai

    sint = etai / etat * (max(0, 1 - cosi * cosi) ** 0.5)

    if sint >= 1:  # Total Internal Reflection
        return 1

    cost = max(0, 1 - sint * sint) ** 0.5
    cosi = abs(cosi)
    Rs = ((etat * cosi) - (etai * cost)) / ((etat * cosi) + (etai * cost))
    Rp = ((etai * cosi) - (etat * cost)) / ((etai * cosi) + (etat * cost))
    return (Rs * Rs + Rp * Rp) / 2


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

        self.cam_position = V3(0, 0, 0)
        self.fov = 60

        self.scene = []

        self.point_light = None
        self.ambient_light = None

        self.env_map = None

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
        for y in range(0, self.height, 2):
            for x in range(0, self.width, 2):

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

                self.gl_vertex_coord(x, y, self.cast_ray(self.cam_position, direction))

    def scene_intercept(self, orig, direction, orig_obj=None):
        temp_z = float('inf')
        material = None
        intersect = None

        # Revisamos cada rayo contra cada objeto
        for obj in self.scene:
            if obj is not orig_obj:
                hit = obj.ray_intersect(orig, direction)
                if hit is not None:
                    if hit.distance < temp_z:
                        temp_z = hit.distance
                        material = obj.material
                        intersect = hit

        return material, intersect

    def cast_ray(self, orig, direction, orig_obj=None, recursion=0):
        material, intersect = self.scene_intercept(orig, direction, orig_obj)

        if material is None or recursion >= MAX_RECURSION_DEPTH:
            if self.env_map:
                return self.env_map.getColor(direction)
            return self.clear_color

        object_color = [material.diffuse[2] / 255,
                        material.diffuse[1] / 255,
                        material.diffuse[0] / 255]

        ambient_color = [0, 0, 0]
        diffuse_color = [0, 0, 0]
        spec_color = [0, 0, 0]

        reflect_color = [0, 0, 0]
        refract_color = [0, 0, 0]

        final_color = [0, 0, 0]

        shadow_intensity = 0

        # Direccion de vista
        view_dir = substract_vectors(intersect.point, self.cam_position)
        view_dir = multiply_vector_with_constant(view_dir, 1/vector3_norm(view_dir))

        if self.ambient_light:
            ambient_color = [self.ambient_light.strength * self.ambient_light.color[2] / 255,
                             self.ambient_light.strength * self.ambient_light.color[1] / 255,
                             self.ambient_light.strength * self.ambient_light.color[0] / 255]

        if self.point_light:
            # Sacamos la direccion de la luz para este punto
            light_dir = substract_vectors(intersect.point, self.point_light.position)
            light_dir = multiply_vector_with_constant(light_dir, 1/vector3_norm(light_dir))

            # Calculamos el valor del diffuse color
            intensity = self.point_light.intensity * max(0, point_product(light_dir, intersect.normal))
            diffuse_color = [intensity * self.point_light.color[2] / 255,
                             intensity * self.point_light.color[1] / 255,
                             intensity * self.point_light.color[2] / 255]

            # Iluminacion especular
            reflect = reflect_vector(intersect.normal, light_dir)  # Reflejar el vector de luz

            # spec_intensity: lightIntensity * ( view_dir dot reflect) ** especularidad
            spec_intensity = self.point_light.intensity * (max(0, point_product(view_dir, reflect)) ** material.spec)
            spec_color = [spec_intensity * self.point_light.color[2] / 255,
                          spec_intensity * self.point_light.color[1] / 255,
                          spec_intensity * self.point_light.color[0] / 255]

            shad_mat, shad_inter = self.scene_intercept(intersect.point, light_dir, intersect.sceneObject)
            if shad_inter is not None and shad_inter.distance < vector3_norm(
                    substract_vectors(intersect.point, self.point_light.position)):
                shadow_intensity = 1

        if material.mat_type == OPAQUE:
            # Formula de iluminacion, PHONG
            final_color = add_vectors(ambient_color, multiply_vector_with_constant(add_vectors(diffuse_color, spec_color), 1 - shadow_intensity))

        elif material.mat_type == REFLECTIVE:
            reflect = reflect_vector(intersect.normal, multiply_vector_with_constant(direction, -1))
            reflect_color = self.cast_ray(intersect.point, reflect, intersect.sceneObject, recursion + 1)
            reflect_color = [reflect_color[2] / 255,
                             reflect_color[1] / 255,
                             reflect_color[0] / 255]

            final_color = add_vectors(reflect_color, multiply_vector_with_constant(spec_color, 1-shadow_intensity))
            #final_color = reflect_color + (1 - shadow_intensity) * spec_color

        elif material.mat_type == TRANSPARENT:

            outside = point_product(direction, intersect.normal) < 0
            bias = multiply_vector_with_constant(intersect.normal, 0.001)
            kr = fresnel(intersect.normal, direction, material.ior)

            reflect = reflect_vector(intersect.normal, multiply_vector_with_constant(direction, -1))
            reflect_orig = add_vectors(intersect.point, bias) if outside else substract_vectors(bias, intersect.point)
            reflect_color = self.cast_ray(reflect_orig, reflect, None, recursion + 1)
            reflect_color = [reflect_color[2] / 255,
                             reflect_color[1] / 255,
                             reflect_color[0] / 255]

            if kr < 1:
                refract = refract_vector(intersect.normal, direction, material.ior)
                refract_orig = substract_vectors(bias, intersect.point) if outside else add_vectors(intersect.point, bias)
                refract_color = self.cast_ray(refract_orig, refract, None, recursion + 1)
                refract_color = [refract_color[2] / 255,
                                 refract_color[1] / 255,
                                 refract_color[0] / 255]

            final_color = add_vectors(add_vectors(multiply_vector_with_constant(reflect_color, kr),
                                                  multiply_vector_with_constant(refract_color, 1-kr)),
                                      multiply_vector_with_constant(spec_color, 1-shadow_intensity))

        # Le aplicamos el color del objeto
        final_color = multiply_vectors(final_color, object_color)

        # Nos aseguramos que no suba el valor de color de 1
        r = min(1, final_color[0])
        g = min(1, final_color[1])
        b = min(1, final_color[2])

        return color(r, g, b)