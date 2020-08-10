from gl import *


def gourad(render, **kwargs):
    u, v, w = kwargs['bary_cords']
    t_a, t_b, t_c = kwargs['tex_coords']
    n_a, n_b, n_c = kwargs['normals']
    b, g, r = kwargs['color']

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        t_x = t_a.x * u + t_b.x * v + t_c.x * w
        t_y = t_a.y * u + t_b.y * v + t_c.y * w
        tex_color = render.active_texture.getColor(t_x, t_y)
        b *= tex_color[0] / 255
        g *= tex_color[1] / 255
        r *= tex_color[2] / 255

    n_x = n_a[0] * u + n_b[0] * v + n_c[0] * w
    n_y = n_a[1] * u + n_b[1] * v + n_c[1] * w
    n_z = n_a[2] * u + n_b[2] * v + n_c[2] * w

    normal = V3(n_x, n_y, n_z)

    intensity = point_product(normal, render.light)

    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r, g, b
    else:
        return 0,0,0
