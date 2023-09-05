def calculate_line_intersect(l1: tuple[tuple, tuple], l2: tuple[tuple, tuple]) -> tuple | None:
    try:
        interx = (((l1[0][0]*l1[1][1]-l1[0][1]*l1[1][0])*(l2[0][0]-l2[1][0])-(l1[0][0]-l1[1][0])*(l2[0][0]*l2[1][1]-l2[0][1]*l2[1][0])) /
                  ((l1[0][0]-l1[1][0])*(l2[0][1]-l2[1][1])-(l1[0][1]-l1[1][1])*(l2[0][0]-l2[1][0])))
        intery = (((l1[0][0]*l1[1][1]-l1[0][1]*l1[1][0])*(l2[0][1]-l2[1][1])-(l1[0][1]-l1[1][1])*(l2[0][0]*l2[1][1]-l2[0][1]*l2[1][0])) /
                  ((l1[0][0]-l1[1][0])*(l2[0][1]-l2[1][1])-(l1[0][1]-l1[1][1])*(l2[0][0]-l2[1][0])))
        intersect = interx, intery
    except ZeroDivisionError():
        intersect = None
    finally:
        return intersect


def get_segment_point_intersect(line: tuple[tuple, tuple], point: tuple[int]) -> bool:
    if line[0][0] < line[1][0]:
        if point[0] < line[0][0]:
            return False
        if point[0] > line[1][0]:
            return False
    elif line[0][0] == line[1][0]:
        if point[0] != line[0][0]:
            return False
    else:
        if point[0] > line[0][0]:
            return False
        if point[0] < line[1][0]:
            return False

    if line[0][1] < line[1][1]:
        if point[1] < line[0][1]:
            return False
        if point[1] > line[1][1]:
            return False
    elif line[0][1] == line[1][1]:
        if point[1] != line[0][1]:
            return False
    else:
        if point[1] > line[0][1]:
            return False
        if point[1] < line[1][1]:
            return False
    return True


def calculate_segment_intersect(l1: tuple[tuple, tuple], l2: tuple[tuple, tuple]) -> tuple | None:
    point = calculate_line_intersect(l1, l2)
    if point == None:
        return None
    elif not get_segment_point_intersect(l1, point):
        return None
    elif not get_segment_point_intersect(l2, point):
        return None
    else:
        return point
