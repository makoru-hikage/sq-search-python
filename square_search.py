import math

def find_nearest_square_root(n):
    b = 1
    while b ** 2 < n:
        b += 1
    return b

def get_row_index(base, cell_index):
    return math.ceil(cell_index/base)

def get_column_index(base, cell_index):
    return cell_index - base * int(math.ceil(cell_index/base)) + base

def get_intersection_index(base, row_index, column_index):
    return column_index + row_index*base - base

def get_opposite_index(length, index):
    return length + 1 - index

def horizontal_opposite(base, cell_index):
    return get_intersection_index(
        base,
        get_row_index(base, cell_index),
        get_opposite_index(base, get_column_index(base, cell_index))
    )

def vertical_opposite(base, cell_index):
    return get_intersection_index(
        base,
        get_opposite_index(base, get_row_index(base, cell_index)),
        get_column_index(base, cell_index)
    )

def antidiagonal_opposite(base, cell_index):
    return get_intersection_index(
        base,
        get_opposite_index(base, get_column_index(base, cell_index)),
        get_opposite_index(base, get_row_index(base, cell_index))
    )

def diagonal_opposite(base, cell_index):
    return get_intersection_index(
        base,
        get_column_index(base, cell_index),
        get_row_index(base, cell_index)
    )

def get_top_left_quadrant_last_cell(base):
    base_middle = math.floor((base + 1) / 2)
    return base_middle + base_middle * base - base

def square_search(haystack, needle):
    haystack_size = len(haystack)
    base = find_nearest_square_root(haystack_size)
    base_middle = math.floor((base + 1) / 2)

    cell = 1
    last_iterated_cell = get_top_left_quadrant_last_cell(base)

    while cell <= last_iterated_cell:
        ho  = horizontal_opposite(base, cell)
        vo  = vertical_opposite(base, cell)
        dso = antidiagonal_opposite(base, cell)

        if haystack[cell - 1] == needle:
            return cell

        if ho <= haystack_size and haystack[ho - 1] == needle:
            return ho

        if vo <= haystack_size and haystack[vo - 1] == needle:
            return vo

        if dso <= haystack_size and haystack[dso - 1] == needle:
            return dso

        if get_column_index(cell, base) != base_middle:
            cell += 1
        else:
            cell = cell + base - base_middle + 1

    return 0
