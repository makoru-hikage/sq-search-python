import math
import parts
import symmetry

def find_nearest_square_root(n):
    b = 1
    while b ** 2 < n:
        b += 1
    return b

def square_search(haystack, needle):
    haystack_size = len(haystack)
    base = find_nearest_square_root(haystack_size)
    base_middle = math.floor((base + 1) / 2)
    
    cell = 1
    last_iterated_cell = base_middle + base_middle * base - base

    while cell <= last_iterated_cell:
        ho = symmetry.horizontal_opposite(base, cell)
        vo = symmetry.vertical_opposite(base, cell)
        dso = symmetry.vertical_opposite(base, cell)

        if haystack[cell - 1] == needle:
            return cell

        if ho <= haystack_size and haystack[ho-1] == needle:
            return ho

        if vo <= haystack_size and haystack[vo-1] == needle:
            return vo
        
        if dso <= haystack_size and haystack[dso-1] == needle:
            return dso

        if parts.get_column_index(cell, base) != base_middle:
            cell += 1
        else:
            cell = cell + base - base_middle + 1

    return 0

