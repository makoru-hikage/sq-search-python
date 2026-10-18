import time
import bisect
from square_search import square_search


def linear_search(haystack, needle):
    for i, val in enumerate(haystack):
        if val == needle:
            return i
    return -1


def binary_search(haystack, needle):
    idx = bisect.bisect_left(haystack, needle)
    if idx < len(haystack) and haystack[idx] == needle:
        return idx
    return -1


def benchmark(fn, haystack, needle, iterations=10000):
    start = time.perf_counter()
    for _ in range(iterations):
        fn(haystack, needle)
    return (time.perf_counter() - start) / iterations * 1e6


SIZES      = [4, 9, 16, 25, 49, 64, 100, 225, 400, 625, 900]
ITERATIONS = 10000

header = f"{'Size':>5} | {'Needle':>8} | {'Linear µs':>10} | {'Orochi µs':>10} | {'Binary µs':>10} | {'Winner':>8}"
print(header)
print("-" * len(header))

for size in SIZES:
    arr = list(range(size))

    cases = [
        ("first",   arr[0]),
        ("middle",  arr[size // 2]),
        ("last",    arr[-1]),
        ("missing", size + 1),
    ]

    for label, needle in cases:
        t_linear = benchmark(linear_search, arr, needle, ITERATIONS)
        t_orochi = benchmark(square_search, arr, needle, ITERATIONS)
        t_binary = benchmark(binary_search, arr, needle, ITERATIONS)

        times  = {"Linear": t_linear, "Orochi": t_orochi, "Binary": t_binary}
        winner = min(times, key=times.get)

        print(f"{size:>5} | {label:>8} | {t_linear:>10.3f} | {t_orochi:>10.3f} | {t_binary:>10.3f} | {winner:>8}")

    print()
