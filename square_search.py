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

# ── Helper utilities ──────────────────────────────────────────────────────────

def find_nearest_square_root(n):
    """Return the ceiling of √n: the smallest integer b such that b² >= n.

    This is the base b defined in §1.1 of the SASQUARE paper.  All section
    references throughout this module use b as the grid side length.
    """
    b = math.isqrt(n)
    return b if b * b >= n else b + 1

# ── Core search ───────────────────────────────────────────────────────────────

def square_search(haystack, needle):
    """Search for needle in haystack using the Square Search (Yamata) algorithm.

    Args:
        haystack: list to search (any element type).
        needle:   value to find.

    Returns:
        Index of needle in haystack, or -1 if not found.
    """
    n           = len(haystack)
    base        = find_nearest_square_root(n)   # §1.1 — side length of the virtual √n × √n grid
    base_middle = (base + 1) // 2               # §7.1 — M(b) = ⌈b/2⌉; extent of the top-left quadrant
    b2          = base * base                   # §1.2 — total cells in the padded grid
    odd_base    = base % 2 == 1                 # True when the grid has a physical centre column / row

    # Pad to a perfect square so every (row, col) address is valid.
    # object() is the fill value — no user value can ever be identical to a
    # freshly created object(), so padded cells can never produce a false positive.
    if b2 == n:
        padded = haystack
    else:
        padded = haystack + [object()] * (b2 - n)

    # Walk the upper triangle of the top-left quadrant (Q1, §7.5): all (q, r) pairs where
    # 0 <= q <= r < base_middle.  For each representative cell D₄ symmetry maps
    # (q, r) onto up to 8 cells spread across all four quadrants, so one step
    # covers the entire orbit.
    for k in range(base_middle):
        # k is both the row index (q) and the starting column (r = k) for this
        # triangle row.  offset steps r rightward toward the last column.

        # ── Diagonal cell (offset == 0, q == r == k) ────────────────────────
        # The cell lies on the main diagonal — an axis of D₄ symmetry.
        # Reflections §8.6–§8.9 coincide with rotations §8.2–§8.5 here,
        # so only 4 distinct orbit members exist (not 8).
        cell = k * base + k
        if padded[cell]                    == needle: return cell                      # §8.2  Rotation 0°           top-left
        if padded[base*k + base - k - 1]   == needle: return base*k + base - k - 1    # §8.3  Rotation 90°          top-right
        if padded[b2 - cell - 1]           == needle: return b2 - cell - 1            # §8.4  Rotation 180°         bottom-right
        if padded[base*(base - k - 1) + k] == needle: return base*(base - k - 1) + k  # §8.5  Rotation 270°         bottom-left
        # §8.6–§8.9 skipped — proven duplicates on the main diagonal
        #   §8.6 == §8.3  §8.7 == §8.5  §8.8 == §8.4  §8.9 == §8.2

        # last = number of offsets remaining after the diagonal for this triangle row
        # (also the value of r at the final step: r = k + last)
        last = base_middle - k - 1

        # ── Full-orbit off-diagonal steps (offset 1 .. last-1) ──────────────
        # The cell is off both axes of symmetry, so all 8 D₄ orbit members are
        # distinct — every one must be checked.
        for offset in range(1, last):
            q    = k           # 0-based row index    — r(b,n)−1 in §1.3
            r    = k + offset  # 0-based column index — c(b,n)−1 in §1.4
            cell = q * base + r  # intersection i(b, q+1, r+1) from §2; §8.2 canonical head

            if padded[cell]                    == needle: return cell                      # §8.2  Rotation 0°           top-left,  above diagonal
            if padded[base*r + base - q - 1]   == needle: return base*r + base - q - 1    # §8.3  Rotation 90°          top-right
            if padded[b2 - cell - 1]           == needle: return b2 - cell - 1            # §8.4  Rotation 180°         bottom-right
            if padded[base*(base - r - 1) + q] == needle: return base*(base - r - 1) + q  # §8.5  Rotation 270°         bottom-left
            if padded[base*q - r + base - 1]   == needle: return base*q - r + base - 1    # §8.6  Horizontal Opposite   top-left,  below diagonal
            if padded[base*(base - q - 1) + r] == needle: return base*(base - q - 1) + r  # §8.7  Vertical Opposite     bottom-left
            if padded[b2 - base*r - q - 1]     == needle: return b2 - base*r - q - 1      # §8.8  Antidiagonal Opposite bottom-right
            if padded[base*r + q]              == needle: return base*r + q               # §8.9  Diagonal Opposite     top-right

        # ── Last inner step (offset == last) ────────────────────────────────
        # For odd base: r = k + last = base_middle − 1 — the centre column.
        # Axis of symmetry: vertical axis.
        # Reflections §8.6–§8.9 alias rotations (different pairing from diagonal):
        #   §8.6 == §8.2  §8.7 == §8.4  §8.8 == §8.3  §8.9 == §8.5
        # For even base: no centre column exists — all 8 heads remain distinct.
        if last > 0:
            q    = k           # 0-based row index    — r(b,n)−1 in §1.3
            r    = k + last    # 0-based column index — c(b,n)−1 in §1.4
            cell = q * base + r  # intersection i(b, q+1, r+1) from §2

            if padded[cell]                    == needle: return cell                      # §8.2  Rotation 0°           top-left
            if padded[base*r + base - q - 1]   == needle: return base*r + base - q - 1    # §8.3  Rotation 90°          top-right
            if padded[b2 - cell - 1]           == needle: return b2 - cell - 1            # §8.4  Rotation 180°         bottom-right
            if padded[base*(base - r - 1) + q] == needle: return base*(base - r - 1) + q  # §8.5  Rotation 270°         bottom-left
            if not odd_base:                   # even base: no centre column, 4 more distinct heads
                if padded[base*q - r + base - 1]   == needle: return base*q - r + base - 1    # §8.6  Horizontal Opposite
                if padded[base*(base - q - 1) + r] == needle: return base*(base - q - 1) + r  # §8.7  Vertical Opposite
                if padded[b2 - base*r - q - 1]     == needle: return b2 - base*r - q - 1      # §8.8  Antidiagonal Opposite
                if padded[base*r + q]               == needle: return base*r + q               # §8.9  Diagonal Opposite
            # §8.6–§8.9 skipped for odd base — proven duplicates on the centre column

    return -1  # needle not found
