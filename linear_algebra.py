from collections import namedtuple
from math import sqrt

V2 = namedtuple('V2', ['x', 'y'])
V3 = namedtuple('V3', ['x', 'y', 'z'])
V4 = namedtuple('V4', ['x', 'y', 'z', 'w'])

def transform(vertex, scale = V3(0, 0, 0), translate = V3(1, 1, 1)):
    return V3(round(vertex[0] * scale.x + translate.x),
              round(vertex[1] * scale.y + translate.y),
              round(vertex[2] * scale.z + translate.z))


def cross_product(first_vector, second_vector):
    return V3(first_vector.y*second_vector.z-first_vector.z*second_vector.y,
              first_vector.z*second_vector.x-first_vector.x*second_vector.z,
              first_vector.x*second_vector.y-first_vector.y*second_vector.x)


def multiply_vector_with_constant(first_vector, constant):
    return V3(first_vector.x*constant,
              first_vector.y*constant,
              first_vector.z*constant)


def point_product(first_vector, second_vector):
    return first_vector.x*second_vector.x+first_vector.y*second_vector.y+first_vector.z*second_vector.z


def substract_vectors(first_vector, second_vector):
    return V3(second_vector.x - first_vector.x,
              second_vector.y - first_vector.y,
              second_vector.z - first_vector.z)


def vector3_norm(vector):
    return sqrt(vector.x ** 2 + vector.y ** 2 + vector.z ** 2)


def bary_coords(A, B, C, P):
    # u es para la A, v es para B, w para C
    try:
        u = (((B.y - C.y) * (P.x - C.x) + (C.x - B.x) * (P.y - C.y)) /
             ((B.y - C.y) * (A.x - C.x) + (C.x - B.x) * (A.y - C.y)))

        v = (((C.y - A.y) * (P.x - C.x) + (A.x - C.x) * (P.y - C.y)) /
             ((B.y - C.y) * (A.x - C.x) + (C.x - B.x) * (A.y - C.y)))

        w = 1 - u - v
    except:
        return -1, -1, -1

    return u, v, w