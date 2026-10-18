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

def get_heads(base, cell_index):
    return [
        cell_index,
        horizontal_opposite(base, cell_index),
        vertical_opposite(base, cell_index),
        antidiagonal_opposite(base, cell_index),
        diagonal_opposite(base, cell_index),
        rotation_90(base, cell_index),
        rotation_180(base, cell_index),
        rotation_270(base, cell_index),
    ]

def get_top_left_quadrant_last_cell(base):
    base_middle = (base + 1) // 2
    return (base + 1) * (base_middle - 1)

def square_search(haystack, needle):
    base         = find_nearest_square_root(len(haystack))
    base_middle  = (base + 1) // 2
    sentinel     = object()
    padded       = haystack + [sentinel] * (base * base - len(haystack))

    cell             = 0
    last_iterated_cell = get_top_left_quadrant_last_cell(base)

    while cell <= last_iterated_cell:
        found = next((c for c in get_heads(base, cell) if padded[c] == needle), -1)

        if found != -1:
            return found

        if get_column_index(base, cell) != base_middle:
            cell += 1
        else:
            cell = cell + base - base_middle + 1

    return -1
