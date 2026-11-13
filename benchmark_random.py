import math
import time
import random
from square_search import square_search

def linear_search(haystack, needle):
    for i, val in enumerate(haystack):
        if val == needle:
            return i
    return -1

def timed_batch(fn, arr, needles):
    start = time.perf_counter()
    for n in needles:
        fn(arr, n)
    return (time.perf_counter() - start) / len(needles) * 1e6

N_QUERIES   = 2000
FOUND_RATIO = 0.9

# Python list access is ~50ns/element — cap sizes to keep runtime sane.
# At n=65536, linear avg query = 32768 steps × ~0.5µs = 16ms × 2000 = 32s total.
SIZES = [900, 10000, 65536]

print(f"RANDOM NEEDLE BENCHMARK  ({N_QUERIES} queries: "
      f"{int(FOUND_RATIO*100)}% hit  {int((1-FOUND_RATIO)*100)}% miss)\n")
print(f"{'n':>8} | {'b':>5} | {'Linear µs':>10} | {'Yamata µs':>10} | {'ratio':>6}")
print("-" * 52)

random.seed(42)

for size in SIZES:
    b    = math.isqrt(size); b = b if b*b >= size else b+1
    pool = size * 4
    arr  = random.sample(range(pool), size)

    n_found = int(N_QUERIES * FOUND_RATIO)
    n_miss  = N_QUERIES - n_found

    found_needles   = [arr[random.randint(0, size - 1)] for _ in range(n_found)]
    missing_needles = [pool + i for i in range(n_miss)]
    needles = found_needles + missing_needles
    random.shuffle(needles)

    t_li = timed_batch(linear_search, arr, needles)
    t_or = timed_batch(square_search, arr, needles)

    print(f"{size:>8} | {b:>5} | {t_li:>10.3f} | {t_or:>10.3f} | {t_li/t_or:>6.2f}x")
