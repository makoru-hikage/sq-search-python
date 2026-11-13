"""
square_search.py

Square Search (Yamata) algorithm — Python implementation.

The algorithm maps a 1-D haystack onto a virtual √n × √n grid and exploits
the D₄ symmetry group to check up to 8 cells per inner iteration, reducing
the worst-case comparison count from n to roughly √n / 2.

Reference: ~/projects/sasquare-docs/sasquare.pdf
Section references (§) point to chapters in the SASQUARE paper:
  §8    The Opposites         — Chapter 8; each section is one D₄ transform
  §8.1  The Opposite Index    — base formula used by all transforms below
  §8.2  Rotation 0°           — identity; the canonical (q, r) cell itself
  §8.3  Rotation 90°          — quarter-turn clockwise
  §8.4  Rotation 180°         — half-turn; point reflection through centre
  §8.5  Rotation 270°         — quarter-turn counter-clockwise
  §8.6  Horizontal Opposite   — reflect across the vertical axis
  §8.7  Vertical Opposite     — reflect across the horizontal axis
  §8.8  Antidiagonal Opposite — reflect across the anti-diagonal
  §8.9  Diagonal Opposite     — reflect across the main diagonal
"""

import math

def find_nearest_square_root(n):
    b = math.isqrt(n)
    return b if b * b >= n else b + 1

def get_row_index(base, cell_index):
    return cell_index // base + 1

def get_column_index(base, cell_index):
    return (cell_index % base) + 1

def get_intersection_index(base, row_index, column_index):
    return base * (row_index - 1) + (column_index - 1)

def square_search(haystack, needle):
    n           = len(haystack)
    base        = find_nearest_square_root(n)
    base_middle = (base + 1) // 2
    b2          = base * base
    odd_base    = base % 2 == 1   # centre-column dedup applies to odd bases only

    # Skip list allocation when input is already a perfect square
    if b2 == n:
        padded = haystack
    else:
        sentinel = object()
        padded   = haystack + [sentinel] * (b2 - n)

    for k in range(base_middle):

        # ── Diagonal cell (offset == 0, q == r == k) ────────────────────────
        # Axis of symmetry: main diagonal.
        # D₄ reflections (§8.6–§8.9) alias rotations (§8.2–§8.5) exactly.
        #   §8.6 == §8.3  §8.7 == §8.5  §8.8 == §8.4  §8.9 == §8.2
        cell = k * base + k
        if padded[cell]                    == needle: return cell                # §8.2
        if padded[base*k + base - k - 1]   == needle: return base*k + base-k-1  # §8.3
        if padded[b2 - cell - 1]           == needle: return b2 - cell - 1      # §8.4
        if padded[base*(base - k - 1) + k] == needle: return base*(base-k-1)+k  # §8.5
        # §8.6–§8.9 skipped — proven duplicates on the main diagonal

        last = base_middle - k - 1   # last valid inner offset for this k

        # ── Full-orbit off-diagonal steps (offset 1 .. last−1) ──────────────
        # All 8 heads are distinct; check all of them.
        for offset in range(1, last):
            q    = k
            r    = k + offset
            cell = q * base + r

            if padded[cell]                    == needle: return cell
            if padded[base*r + base - q - 1]   == needle: return base*r + base - q - 1
            if padded[b2   - cell - 1]          == needle: return b2 - cell - 1
            if padded[base*(base - r - 1) + q]  == needle: return base*(base - r - 1) + q
            if padded[base*q - r + base - 1]    == needle: return base*q - r + base - 1
            if padded[base*(base - q - 1) + r]  == needle: return base*(base - q - 1) + r
            if padded[b2   - base*r - q - 1]    == needle: return b2 - base*r - q - 1
            if padded[base*r + q]               == needle: return base*r + q

        # ── Last inner step (offset == last) ────────────────────────────────
        # For odd base: r = k + last = base_middle − 1 — the centre column.
        # Axis of symmetry: vertical axis.
        # D₄ reflections alias rotations (different pairing from diagonal):
        #   §8.6 == §8.2  §8.7 == §8.4  §8.8 == §8.3  §8.9 == §8.5
        # For even base: no centre column exists — all 8 heads remain distinct.
        if last > 0:
            q    = k
            r    = k + last
            cell = q * base + r

            if padded[cell]                    == needle: return cell                # §8.2
            if padded[base*r + base - q - 1]   == needle: return base*r + base - q - 1  # §8.3
            if padded[b2   - cell - 1]          == needle: return b2 - cell - 1      # §8.4
            if padded[base*(base - r - 1) + q]  == needle: return base*(base - r - 1) + q  # §8.5
            if not odd_base:                    # even base: 4 more distinct heads
                if padded[base*q - r + base - 1]    == needle: return base*q - r + base - 1
                if padded[base*(base - q - 1) + r]  == needle: return base*(base - q - 1) + r
                if padded[b2   - base*r - q - 1]    == needle: return b2 - base*r - q - 1
                if padded[base*r + q]               == needle: return base*r + q
            # §8.6–§8.9 skipped for odd base — proven duplicates on the centre column

    return -1
