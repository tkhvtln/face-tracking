import cv2
import numpy
import math


def compute_transform_params(frame, tx, ty, cx, cy, wx, hy, width, height):
    ab = (1, 0)
    cd = (cx, cy)
    scale = 1

    angle = 0 #int(-math.degrees(ab[0] * cd[0] + ab[1] * cd[1]) / (math.sqrt(ab[0] ** 2 + cd[0] ** 2) + math.sqrt(ab[1] ** 2 + cd[1] ** 2)))

    w, h = rotated_rect_with_max_area(width, height, math.radians(angle))
    r = (100 - ((w * h * 100) / (width * height))) / 100

    s1 = width * height
    s2 = wx * hy

    if s1 != 0 and s2 != 0:
        scale = (100 - (s2 * 100 / s1)) / 100 + 1 
    

    rotate_matrix = cv2.getRotationMatrix2D((frame.shape[1] / 2, frame.shape[0] / 2), angle, 1)
    translation_matrix = numpy.float32([[1, 0, -tx], [0, 1, -ty]])

    return angle, scale, translation_matrix, rotate_matrix
    

def rotated_rect_with_max_area(w, h, angle):
    if w <= 0 or h <= 0:
        return 0,0

    width_is_longer = w >= h
    side_long, side_short = (w, h) if width_is_longer else (h, w)

    sin_a, cos_a = abs(math.sin(angle)), abs(math.cos(angle))
    if side_short <= 2. * sin_a * cos_a * side_long or abs(sin_a - cos_a) < 1e-10:     
        x = 0.5 * side_short
        wr, hr = (x / sin_a,x / cos_a) if width_is_longer else (x / cos_a, x / sin_a)
    else:
        cos_2a = cos_a * cos_a - sin_a * sin_a
        wr, hr = (w * cos_a - h * sin_a) / cos_2a, (h * cos_a - w * sin_a) / cos_2a

    return wr, hr
