#!/usr/bin/env python3
"""
steampunk-ui palette validator.

Checks every ink and signal token against ALL FOUR surfaces, not merely the
page ground. A token that clears AA on --void but fails on --iron-3 will be
unreadable on a button or a panel header, which is exactly where labels live.

    python3 tools/contrast.py                  # validate the shipped variants
    python3 tools/contrast.py --derive '#1a1410' '#c87533'
                                               # check a palette you are deriving

Exit code is non-zero if any token fails, so it drops straight into CI.
"""

import argparse
import sys

AA, AAA = 4.5, 7.0


# --------------------------------------------------------------------------- maths

def _linear(channel: int) -> float:
    c = channel / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hexstr: str) -> float:
    h = hexstr.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _linear(r) + 0.7152 * _linear(g) + 0.0722 * _linear(b)


def contrast(fg: str, bg: str) -> float:
    a, b = luminance(fg), luminance(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


# --------------------------------------------------------------------------- palettes

FOUNDRY = {
    "surfaces": {"void": "#14110d", "iron": "#1c1813",
                 "iron-2": "#241f18", "iron-3": "#2e2820"},
    "rules":    {"seam": "#3a3227", "seam-lit": "#4d4231"},
    "tokens": {
        "ink":       "#e8dfcd",
        "ink-dim":   "#a2937a",
        "ink-faint": "#9d8f75",
        "copper":    "#cd7c48",
        "brass":     "#c9a227",
        "brass-hi":  "#f0d891",
        "verdigris": "#5f9e7d",
        "ember":     "#e8922a",
        "rust":      "#e86951",
    },
    # Gradient stops and engraved edges. Never used as a text colour, so they
    # are deliberately exempt from the AA sweep.
    "non_text": {"brass-lo": "#7d6318"},
}

VARIANTS = {
    "foundry": FOUNDRY,
    "soot": {
        "surfaces": {"void": "#0d0b08", "iron": "#14110d",
                     "iron-2": "#1c1813", "iron-3": "#241f18"},
        "rules":    FOUNDRY["rules"],
        "tokens":   {**FOUNDRY["tokens"], "copper": "#c9a227"},
    },
    "blueprint": {
        "surfaces": FOUNDRY["surfaces"],
        "rules":    FOUNDRY["rules"],
        "tokens":   {**FOUNDRY["tokens"], "brass": "#7cbcd6", "oxide": "#7cbcd6"},
    },
    "verdigris": {
        "surfaces": FOUNDRY["surfaces"],
        "rules":    FOUNDRY["rules"],
        "tokens": {
            **FOUNDRY["tokens"],
            "copper":    "#5f9e7d",
            "brass":     "#7fbb9b",
            "brass-hi":  "#c3e3d2",
            "verdigris": "#c9a227",
        },
    },
}


# --------------------------------------------------------------------------- report

def check(name: str, palette: dict) -> int:
    surfaces = palette["surfaces"]
    planes = list(surfaces.items())
    failures = 0

    print(f"\n\033[1m{name}\033[0m")
    header = "  " + f"{'token':20}{'hex':10}" + "".join(f"{p:>10}" for p, _ in planes) + f"{'min':>8}  grade"
    print(header)
    print("  " + "-" * (len(header) - 2))

    for token, value in palette["tokens"].items():
        ratios = [contrast(value, bg) for _, bg in planes]
        worst = min(ratios)
        grade = "AAA" if worst >= AAA else "AA" if worst >= AA else "FAIL"
        if grade == "FAIL":
            failures += 1
        colour = "\033[31m" if grade == "FAIL" else ""
        reset = "\033[0m" if colour else ""
        cells = "".join(f"{r:10.2f}" for r in ratios)
        print(f"  {token:20}{value:10}{cells}{worst:8.2f}  {colour}{grade}{reset}")

    # Surfaces must be VISIBLE as separate planes, not accessible as text pairs.
    print("\n  surface separation (target 1.05 to 1.25, higher stops reading as one object)")
    for i in range(len(planes) - 1):
        (an, av), (bn, bv) = planes[i], planes[i + 1]
        r = contrast(av, bv)
        flag = "" if 1.03 <= r <= 1.30 else "   <- outside the band"
        print(f"    {an:8} / {bn:8} {r:6.2f}{flag}")

    # Hairlines are checked against the panel plane (the second surface), which
    # is where they actually get drawn.
    panel = list(surfaces.values())[1]
    print(f"\n  rules against the panel plane {panel} (want a visible hairline, 1.2 to 2.5)")
    for rn, rv in palette["rules"].items():
        print(f"    {rn:12} {rv} {contrast(rv, panel):6.2f}")

    non_text = palette.get("non_text")
    if non_text:
        print("\n  non-text tokens (gradient stops, engraved edges) exempt from the AA sweep")
        for tn, tv in non_text.items():
            print(f"    {tn:12} {tv}")

    return failures


def derive(ground: str, accent: str) -> int:
    """Sanity-check a palette being derived for a new project."""
    print(f"\n\033[1mderived: ground {ground}, accent {accent}\033[0m")
    r = contrast(accent, ground)
    print(f"  accent on ground: {r:.2f}  {'ok' if r >= AA else 'FAIL, lift the accent value'}")
    if luminance(ground) > 0.06:
        print("  WARNING: ground is too light. Steampunk grounds sit under ~0.05 luminance.")
    h = ground.lstrip("#")
    rr, gg, bb = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    if not (rr >= gg >= bb):
        print("  WARNING: ground is not warm. Red must lead, then green, then blue.")
        print("           A cool grey beside brass reads as dirt, not as metal.")
    return 0 if r >= AA else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate a steampunk-ui palette.")
    ap.add_argument("--variant", choices=sorted(VARIANTS), help="check one variant only")
    ap.add_argument("--derive", nargs=2, metavar=("GROUND", "ACCENT"),
                    help="sanity-check a palette you are deriving")
    args = ap.parse_args()

    if args.derive:
        return derive(*args.derive)

    names = [args.variant] if args.variant else list(VARIANTS)
    failures = sum(check(n, VARIANTS[n]) for n in names)

    print()
    if failures:
        print(f"\033[31m{failures} token(s) below AA. Lift the value channel, hold the hue.\033[0m")
    else:
        print("\033[32mAll tokens clear AA on every surface.\033[0m")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
