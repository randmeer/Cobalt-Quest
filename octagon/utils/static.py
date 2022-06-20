import math
from pygame import Vector2


def hypo(a, b):
    """
    hypotenuse of a right-angled triangle
    """
    c = math.sqrt(a ** 2 + b ** 2)
    return c


def angle_deg(p1, p2):
    """
    angle between two points in degrees
    """
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    if dx == 0:
        if dy == 0:
            deg = 0
        else:
            deg = 0 if p1[1] > p2[1] else 180
    elif dy == 0:
        deg = 90 if p1[0] < p2[0] else 270
    else:
        deg = math.atan(dy / dx) / math.pi * 180
        lowering = p1[1] < p2[1]
        if (lowering and deg < 0) or (not lowering and deg > 0):
            deg += 270
        else:
            deg += 90
    return deg


def conv_deg_rad(deg):
    """
    convert degrees to radians
    """
    rad = deg * math.pi / 180
    return rad


def conv_rad_deg(rad):
    """
    convert radians to degrees
    """
    deg = rad * 180 / math.pi
    return deg


def get_deltas(radians):
    """
    gets delta x and y for any angle in radians
    """
    dx = math.sin(radians)
    dy = -math.cos(radians)
    return dx, dy


def sign(num):
    """
    get the sign of a number

    positive value --> 1
    negative value --> -1
    zero --> 0
    """
    try:
        return num / abs(num)
    except ZeroDivisionError:
        return 0


def flip(num):
    """
    flip the sign of a value
    """
    return 1 ^ num


def equal_sign(num1, num2):
    """
    returns True if the signs of two numbers are equal
    """
    if num1 * num2 > 0:
        return True
    else:
        return False


def sin(num):
    """
    sine
    """
    return math.sin(num)


def cos(num):
    """
    cosine
    """
    return math.cos(num)


def tuple_add(tuple1, tuple2):
    """
    returns the two tuples added together
    """
    return tuple1[0] + tuple2[0], tuple1[1] + tuple2[1]


def tuple_subtract(tuple1, tuple2):
    """
    returns the second tuple subtracted from the first one
    """
    return tuple1[0] - tuple2[0], tuple1[1] - tuple2[1]


def tuple_factor(tuple1, factor):
    """
    returns the tuple multiplied with the factor
    """
    return tuple1[0] * factor, tuple1[1] * factor


def list_add(list1, list2):
    """
    adds the second list to the first list
    """
    for i in range(len(list1)):
        list1[i] += list2[i]


def list_round(list1):
    rounded_list = []
    for i in list1:
        rounded_list.append(round(i))
    return rounded_list


def xor(x, y):
    return bool((x and not y) or (not x and y))


def vector_from_points(point1, point2):
    return Vector2(tuple_subtract(point1, point2))
