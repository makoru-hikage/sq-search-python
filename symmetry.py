from parts import *

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

def opposite_intersection_sum(base, cell_index):
    return sum((
        get_opposite_index(base, get_row_index(base, cell_index)),
        get_opposite_index(base, get_column_index(base, cell_index))
    ))

def descending_opposite(base, cell_index):
    o_is = opposite_intersection_sum(base, cell_index)
    opposite_row_index = get_opposite_index(
        base,
        get_row_index(base, cell_index)
    )
    opposite_column_index = get_opposite_index(
        base,
        get_column_index(base, cell_index)
    )

    return get_intersection_index(
        base,
        o_is - opposite_row_index,
        o_is - opposite_column_index
    )

