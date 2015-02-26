

import math
import random
from operator import itemgetter


def rect(r, d, use_degrees=True):
    if use_degrees:
        d = math.radians(d)
    d -= math.pi
    return round(r*math.sin(d), 2), round(r*math.cos(d), 2)

def polar(destination, origin=(0, 0), return_degrees=True):
    x = destination[0] - origin[0]
    y = destination[1] - origin[1]
    result = math.atan2(x, y)+math.pi
    if return_degrees:
        result = math.degrees(result)
    return result

def distance(origin, destination):
    xs = (origin[0], destination[0])
    ys = (origin[1], destination[1])
    lx = max(xs) - min(xs)
    ly = max(ys) - min(ys)
    return math.sqrt((lx**2) + (ly**2))

def middle(area):
    av_x = 0
    av_y = 0
    for x, y in area:
        av_x += x
        av_y += y
    return (av_x/len(area), av_y/len(area))

def adjacent(center, direct=True, across=True):
    adj = []
    if direct:
        adj += [(0, -1), (1, 0), (0, 1), (-1, 0)]
    if across:
        adj += [(-1, -1), (1, -1), (1, 1), (1, -1)]
    return [(center[0] + i[0], center[1] + i[1]) for i in adj]

def closest(origin, comparisons):
    c = comparisons[0]
    for comp in comparisons[1:]:
        cl = distance(origin, c)
        compl = distance(origin, comp)
        if cl > compl and compl != 0:
            c = comp
    return c

def rand_id(length=16):
    _id = ''
    for i in range(length):
        c = random.choice(list(range(48, 58)) + list(range(65, 91)))
        _id += str(chr(c))
    return _id

def border(area):
    border = set()
    sorted_area = sorted(area)
    last_x, last_y = sorted_area[0]
    for x, y in sorted_area[1:]:
        if y > last_y+1 or x != last_x:
            border.add((x, y))
            border.add((last_x, last_y))
        last_x, last_y = x, y
    sorted_area = sorted(area, key=itemgetter(1, 0))
    last_x, last_y = sorted_area[0]
    for x, y in sorted_area[1:]:
        if x > last_x+1 or y != last_y:
            border.add((x, y))
            border.add((last_x, last_y))
        last_x, last_y = x, y
    return border

def is_inside_triangle(point, a, b):
    c = (a[0], b[1])
    o = (a[1], b[0])
    return distance(point, c) < distance(point, o)

def convex_hull(points):
    # Not done, realized that I don't need this
    hull = points[:4]

    # Finding outermost points
    for p in points:
        if p[0] < hull[0][0]:
            hull[0] = p
        elif p[1] < hull[1][1]:
            hull[1] = p
        elif p[0] > hull[2][0]:
            hull[2] = p
        elif p[1] > hull[3][1]:
            hull[3] = p

    # Dumping all points that are inside
    for p in points:
        if p in hull:
            points.remove(p)
        elif is_inside_triangle(p, hull[1], hull[0]):
            points.remove(p)
        elif is_inside_triangle(p, hull[1], hull[2]):
            points.remove(p)
        elif is_inside_triangle(p, hull[3], hull[2]):
            points.remove(p)
        elif is_inside_triangle(p, hull[3], hull[0]):
            points.remove(p)

    print(len(points))
    return hull



if __name__ == '__main__':
    # print(polar((-1, -1)))
    # print(rect(1, 180), 180)
    # print(distance((1, 1), (1, 7)))
    # print(adjacent((5, 5)))
    # print(rand_id())
    # points = [(random.randint(0, 100), random.randint(0, 100)) for i in range(10)]
    # print(points)
    # print(convex_hull(points))
    print(distance((799, 600), (768, 600)))
    print(distance((799, 600), (799, 601)))
