import math
import time
import bisect
import random
from square_search import square_search

def linear_search(haystack, needle):
    for i, val in enumerate(haystack):
        if val == needle:
            return i
    return -1

def binary_search_sorted(haystack, needle):
    idx = bisect.bisect_left(haystack, needle)
    if idx < len(haystack) and haystack[idx] == needle:
        return idx
    return -1

def binary_search_unsorted(haystack, needle):
    s = sorted(haystack)
    idx = bisect.bisect_left(s, needle)
    if idx < len(s) and s[idx] == needle:
        return idx
    return -1

def benchmark(fn, haystack, needle, iterations=10000):
    start = time.perf_counter()
    for _ in range(iterations):
        fn(haystack, needle)
    return (time.perf_counter() - start) / iterations * 1e6

# Scale iterations down for large n to keep runtime sane
def iters_for(size):
    if size <= 900:   return 10000
    if size <= 3600:  return 2000
    return 500

SIZES = [4, 9, 16, 25, 49, 64, 100, 225, 400, 625, 900,
         1024, 1600, 2500, 3600, 4900, 6400, 8100, 10000, 12100]

# ── Unsorted arrays ───────────────────────────────────────────────────────────

print("UNSORTED ARRAYS")
print("(Binary search includes sorting cost)\n")

header = f"{'Size':>6} | {'b':>4} | {'Needle':>8} | {'Linear µs':>10} | {'Yamata µs':>10} | {'Binary µs':>10} | {'Winner':>8}"
print(header)
print("-" * len(header))

random.seed(42)

for size in SIZES:
    b = math.isqrt(size); b = b if b*b >= size else b+1
    arr = random.sample(range(size * 10), size)
    it  = iters_for(size)
    cases = [
        ("first",   arr[0]),
        ("middle",  arr[size // 2]),
        ("last",    arr[-1]),
        ("missing", size * 10 + 1),
    ]
    for label, needle in cases:
        t_linear = benchmark(linear_search,           arr, needle, it)
        t_yamata = benchmark(square_search,            arr, needle, it)
        t_binary = benchmark(binary_search_unsorted,   arr, needle, it)
        times    = {"Linear": t_linear, "Yamata": t_yamata, "Binary": t_binary}
        winner   = min(times, key=times.get)
        print(f"{size:>6} | {b:>4} | {label:>8} | {t_linear:>10.3f} | {t_yamata:>10.3f} | {t_binary:>10.3f} | {winner:>8}")
    print()
