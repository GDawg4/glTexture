from gl import color
from linear_algebra import V2, V3, V4, \
    vector3_norm, multiply_vector_with_constant, point_product, substract_vectors, add_vectors

WHITE = color(1,1,1)


class AmbientLight(object):
    def __init__(self, strength = 0, _color = WHITE):
        self.strength = strength
        self.color = _color


class PointLight(object):
    def __init__(self, position = V3(0,0,0), _color = WHITE, intensity = 1):
        self.position = position
        self.intensity = intensity
        self.color = _color


class Material(object):
    def __init__(self, diffuse = WHITE, spec = 0):
        self.diffuse = diffuse
        self.spec = spec


class Intersect(object):
    def __init__(self, distance, point, normal, scene_object):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.sceneObject = scene_object


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

        temp = multiply_vector_with_constant(direction, t0)
        hit = add_vectors(orig, temp)
        norm = substract_vectors(self.center, hit)
        norm = multiply_vector_with_constant(norm, 1/vector3_norm(norm))

        return Intersect(distance=t0,
                         point=hit,
                         normal=norm,
                         scene_object=self)
