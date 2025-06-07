from math import ceil

def get_row_index(base, cell_index):
    return ceil(cell_index/base)

def get_column_index(base, cell_index):
    return cell_index - base * int(ceil(cell_index/base)) + base

def get_opposite_index(length, index):
    return length + 1 - index

def get_intersection_index (base, row_index, column_index):
    return column_index + row_index*base - base

def get_intersection_sum(base, cell_index):
    return get_row_index(
        base,
        cell_index
    ) + get_column_index(
        base,
        cell_index
    )

