from gl import color
from linear_algebra import V2, V3, V4, \
    vector3_norm, multiply_vector_with_constant, point_product, substract_vectors, add_vectors

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2
WHITE = color(1, 1, 1)


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
    def __init__(self, diffuse=WHITE, spec=0, ior=1, mat_type=OPAQUE):
        self.diffuse = diffuse
        self.spec = spec
        self.mat_type = mat_type
        self.ior = ior


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

class Plane(object):
    def __init__(self, position, normal, material):
        self.position = position
        self.normal = multiply_vector_with_constant(normal, 1/vector3_norm(normal))
        self.material = material

    def ray_intersect(self, orig, dir):
        # t = (( position - origRayo) dot normal) / (dirRayo dot normal)

        denom = point_product(dir, self.normal)

        if abs(denom) > 0.0001:
            t = point_product(self.normal, substract_vectors(orig, self.position)) / denom
            if t > 0:
                # P = O + tD
                hit = add_vectors(orig, multiply_vector_with_constant(dir, t))

                return Intersect(distance=t,
                                 point=hit,
                                 normal=self.normal,
                                 scene_object=self)

        return None


class AABB(object):
    def __init__(self, position, size, material):
        self.position = position
        self.size = size
        self.material = material
        self.planes = []

        half_size = size / 2

        self.planes.append(Plane(add_vectors(position, V3(half_size, 0, 0)), V3(1, 0, 0), material))
        self.planes.append(Plane(add_vectors(position, V3(-half_size, 0, 0)), V3(-1, 0, 0), material))

        self.planes.append(Plane(add_vectors(position, V3(0, half_size, 0)), V3(0, 1, 0), material))
        self.planes.append(Plane(add_vectors(position, V3(0, -half_size, 0)), V3(0, -1, 0), material))

        self.planes.append(Plane(add_vectors(position, V3(0, 0, half_size)), V3(0, 0, 1), material))
        self.planes.append(Plane(add_vectors(position, V3(0, 0, -half_size)), V3(0, 0, -1), material))

    def ray_intersect(self, orig, dir):
        epsilon = 0.001

        bounds_min = [0,0,0]
        bounds_max = [0,0,0]

        for i in range(3):
            bounds_min[i] = self.position[i] - (epsilon + self.size / 2)
            bounds_max[i] = self.position[i] + (epsilon + self.size / 2)

        t = float('inf')
        intersect = None

        for plane in self.planes:
            plane_inter = plane.ray_intersect(orig, dir)

            if plane_inter is not None:

                # Si estoy dentro del bounding box
                if bounds_min[0] <= plane_inter.point[0] <= bounds_max[0]:
                    if bounds_min[1] <= plane_inter.point[1] <= bounds_max[1]:
                        if bounds_min[2] <= plane_inter.point[2] <= bounds_max[2]:
                            if plane_inter.distance < t:
                                t = plane_inter.distance
                                intersect = plane_inter

        if intersect is None:
            return None

        return Intersect(distance=intersect.distance,
                         point=intersect.point,
                         normal=intersect.normal,
                         scene_object=self)
