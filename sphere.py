from gl import color
from linear_algebra import V2, V3, V4, vector3_norm, multiply_vector_with_constant, point_product, substract_vectors

WHITE = color(1,1,1)

class Material(object):
    def __init__(self, diffuse=WHITE):
        self.diffuse = diffuse


class Intersect(object):
    def __init__(self, distance):
        self.distance = distance


class Sphere(object):
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def ray_intersect(self, orig, direction):
        L = substract_vectors(orig, self.center)
        tca = point_product(L, direction)
        l = vector3_norm(L)
        d = (l**2 - tca**2) ** 0.5
        if d > self.radius:
            return None

        thc = (self.radius ** 2 - d**2) ** 0.5
        t0 = tca - thc
        t1 = tca + thc
        if t0 < 0:
            t0 = t1

        if t0 < 0:
            return None

        return Intersect(distance=t0)
