from collections import namedtuple
from math import sqrt, pi

V2 = namedtuple('V2', ['x', 'y'])
V3 = namedtuple('V3', ['x', 'y', 'z'])
V4 = namedtuple('V4', ['x', 'y', 'z', 'w'])


def transform(vertex, scale = V3(0, 0, 0), translate = V3(1, 1, 1)):
    return V3(round(vertex[0] * scale.x + translate.x),
              round(vertex[1] * scale.y + translate.y),
              round(vertex[2] * scale.z + translate.z))


def cross_product(first_vector, second_vector):
    return V3(first_vector[1]*second_vector[2]-first_vector[2]*second_vector[1],
              first_vector[2]*second_vector[0]-first_vector[0]*second_vector[2],
              first_vector[0]*second_vector[1]-first_vector[1]*second_vector[0])


def multiply_vector_with_constant(first_vector, constant):
    return V3(first_vector[0]*constant,
              first_vector[1]*constant,
              first_vector[2]*constant)


def point_product(first_vector, second_vector):
    return first_vector.x*second_vector.x+first_vector.y*second_vector.y+first_vector.z*second_vector.z


def substract_vectors(first_vector, second_vector):
    return V3(second_vector[0] - first_vector[0],
              second_vector[1] - first_vector[1],
              second_vector[2] - first_vector[2])


def add_vectors(first_vector, second_vector):
    return V3(second_vector[0] + first_vector[0],
              second_vector[1] + first_vector[1],
              second_vector[2] + first_vector[2])


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


def v_to_matrix(v):
    return [[i] for i in v]


def matrix_multiplication(first_matrix, second_matrix):
    return [[sum(a*b for a, b in zip(X_row, Y_col)) for Y_col in zip(*second_matrix)] for X_row in first_matrix]


def deg_to_rad(number):
    return number * pi/180


def eliminate(r1, r2, col, target=0):
    fac = (r2[col]-target) / r1[col]
    for i in range(len(r2)):
        r2[i] -= fac * r1[i]


def gauss(a):
    for i in range(len(a)):
        if a[i][i] == 0:
            for j in range(i+1, len(a)):
                if a[i][j] != 0:
                    a[i], a[j] = a[j], a[i]
                    break
            else:
                print("MATRIX NOT INVERTIBLE")
                return -1
        for j in range(i+1, len(a)):
            eliminate(a[i], a[j], i)
    for i in range(len(a)-1, -1, -1):
        for j in range(i-1, -1, -1):
            eliminate(a[i], a[j], i)
    for i in range(len(a)):
        eliminate(a[i], a[i], i, target=1)
    return a


def inverse(a):
    tmp = [[] for _ in a]
    for i,row in enumerate(a):
        assert len(row) == len(a)
        tmp[i].extend(row + [0]*i + [1] + [0]*(len(a)-i-1))
    gauss(tmp)
    ret = []
    for i in range(len(tmp)):
        ret.append(tmp[i][len(tmp[i])//2:])
    return ret

def multiply_vectors(first_vector, second_vector):
    return V3(
        first_vector[0]*second_vector[0],
        first_vector[1] * second_vector[1],
        first_vector[2] * second_vector[2]
    )
















