def find_nearest_square_root(n):
    b = 1
    while b ** 2 < n:
        b += 1
    return b

def get_row_index(base, cell_index):
    return cell_index // base + 1

def get_column_index(base, cell_index):
    return (cell_index % base) + 1

def get_intersection_index(base, row_index, column_index):
    return base * (row_index - 1) + (column_index - 1)

def get_opposite_index(length, index):
    return length + 1 - index

def rotation_90(base, cell_index):
    return get_intersection_index(
        base,
        get_column_index(base, cell_index),
        get_opposite_index(base, get_row_index(base, cell_index))
    )

def rotation_180(base, cell_index):
    return get_intersection_index(
        base,
        get_opposite_index(base, get_row_index(base, cell_index)),
        get_opposite_index(base, get_column_index(base, cell_index))
    )

def rotation_270(base, cell_index):
    return get_intersection_index(
        base,
        get_opposite_index(base, get_column_index(base, cell_index)),
        get_row_index(base, cell_index)
    )

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
    base_middle = (base + 1) // 2
    return (base + 1) * (base_middle - 1)

def square_search(haystack, needle):
    haystack_size = len(haystack)
    base = find_nearest_square_root(haystack_size)
    base_middle = (base + 1) // 2

    cell = 0
    last_iterated_cell = get_top_left_quadrant_last_cell(base)

    while cell <= last_iterated_cell:
        ho  = horizontal_opposite(base, cell)
        vo  = vertical_opposite(base, cell)
        aso = antidiagonal_opposite(base, cell)
        dso = diagonal_opposite(base, cell)

        if haystack[cell] == needle:
            return cell

        if ho < haystack_size and haystack[ho] == needle:
            return ho

        if vo < haystack_size and haystack[vo] == needle:
            return vo

        if aso < haystack_size and haystack[aso] == needle:
            return aso

        if dso < haystack_size and haystack[dso] == needle:
            return dso

        if get_column_index(base, cell) != base_middle:
            cell += 1
        else:
            cell = cell + base - base_middle + 1

    return -1
