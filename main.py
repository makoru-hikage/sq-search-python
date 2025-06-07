from square_search import square_search

haystack = [69, 49, 4, 50, 47, 95, 60, 31, 32, 77, 67, 41, 33, 98, 16, 13, 68, 90, 42, 99, 27, 7, 52]
needle = 42

found = square_search(haystack, needle)

if found >= 1 and found <= len(haystack):
    print (f'The needle, {needle}, is found at cell {found}')
