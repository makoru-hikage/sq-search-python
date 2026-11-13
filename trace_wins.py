import random
import math

random.seed(42)
SIZE  = 900
BASE  = 30          # math.isqrt(900) = 30
BM    = (BASE + 1) // 2  # base_middle = 15
B2    = BASE * BASE

arr    = random.sample(range(SIZE * 10), SIZE)
first  = arr[0]
middle = arr[SIZE // 2]   # value at cell 450
last   = arr[-1]          # value at cell 899

print(f"base={BASE}  base_middle={BM}  b²={B2}")
print(f"needle 'first'  = {first}  (value at cell 0)")
print(f"needle 'middle' = {middle}  (value at cell {SIZE//2})")
print(f"needle 'last'   = {last}  (value at cell {SIZE-1})")
print()

# ── Trace Yamata for each needle ─────────────────────────────────────────────

def trace_search(haystack, needle, label):
    n           = len(haystack)
    base        = math.isqrt(n); base = base if base*base >= n else base+1
    base_middle = (base + 1) // 2
    b2          = base * base
    odd_base    = base % 2 == 1
    padded      = haystack  # perfect square

    checks = 0

    def chk(idx, k, offset, section):
        nonlocal checks
        checks += 1
        if padded[idx] == needle:
            print(f"  [{label}] found at k={k} offset={offset} "
                  f"head={section} cell={idx}  after {checks} checks")
            return True
        return False

    for k in range(base_middle):

        # ── Diagonal cell (q == r == k) ──────────────────────────────────────
        # 4 unique heads — main diagonal is an axis of D₄ symmetry.
        cell = k * base + k
        if chk(cell,                     k, 0, "§8.2"): return checks
        if chk(base*k + base - k - 1,    k, 0, "§8.3"): return checks
        if chk(b2 - cell - 1,            k, 0, "§8.4"): return checks
        if chk(base*(base - k - 1) + k,  k, 0, "§8.5"): return checks

        last = base_middle - k - 1

        # ── Full-orbit off-diagonal steps (offset 1 .. last-1) ───────────────
        # 8 unique heads — no axis of symmetry, all distinct.
        for offset in range(1, last):
            q = k; r = k + offset; cell = q * base + r
            if chk(cell,                        k, offset, "§8.2"): return checks
            if chk(base*r + base - q - 1,       k, offset, "§8.3"): return checks
            if chk(b2 - cell - 1,               k, offset, "§8.4"): return checks
            if chk(base*(base - r - 1) + q,     k, offset, "§8.5"): return checks
            if chk(base*q - r + base - 1,       k, offset, "§8.6"): return checks
            if chk(base*(base - q - 1) + r,     k, offset, "§8.7"): return checks
            if chk(b2 - base*r - q - 1,         k, offset, "§8.8"): return checks
            if chk(base*r + q,                  k, offset, "§8.9"): return checks

        # ── Last inner step (offset == last) ─────────────────────────────────
        # Odd base: r lands on the centre column — 4 unique heads.
        # Even base: no centre column — 8 unique heads.
        if last > 0:
            q = k; r = k + last; cell = q * base + r
            if chk(cell,                        k, last, "§8.2"): return checks
            if chk(base*r + base - q - 1,       k, last, "§8.3"): return checks
            if chk(b2 - cell - 1,               k, last, "§8.4"): return checks
            if chk(base*(base - r - 1) + q,     k, last, "§8.5"): return checks
            if not odd_base:                    # even base: 4 more distinct heads
                if chk(base*q - r + base - 1,   k, last, "§8.6"): return checks
                if chk(base*(base - q - 1) + r, k, last, "§8.7"): return checks
                if chk(b2 - base*r - q - 1,     k, last, "§8.8"): return checks
                if chk(base*r + q,               k, last, "§8.9"): return checks

    print(f"  [{label}] NOT FOUND after {checks} checks")
    return checks

c_first  = trace_search(arr, first,  "first")
c_middle = trace_search(arr, middle, "middle")
c_last   = trace_search(arr, last,   "last")

print()
print("── How many checks Yamata does vs linear scan position ──────────────────")
print(f"  first:  Yamata={c_first} checks  |  linear scans to position 0  (1 comparison)")
print(f"  middle: Yamata={c_middle} checks  |  linear scans to position {SIZE//2}  (~{SIZE//2+1} comparisons)")
print(f"  last:   Yamata={c_last} checks  |  linear scans to position {SIZE-1}  (~{SIZE} comparisons)")
