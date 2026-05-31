# -*- coding: utf-8 -*-
"""
Shared house style for the Moral AI Introduction scenes.

Palette / layout language (consistent across all scenes):
  * background  #11141a   (near-black blue)
  * ink/white   #f4f6fa   bold titles, to_edge(UP)
  * muted       #8b93a7   captions, footnote tags, eyebrows
  * GOOD (hope) #5ac8a8   teal  -> "good news"
  * BAD  (fear) #e0736b   warm coral -> "bad news"
  * gold        #e7b86b   neutral emphasis for figures
  * panel/line  card fills and hairlines

Everything is kept inside x in [-6.7, 6.7], y in [-3.8, 3.8] with buffers.
Import * from manim so scenes & helpers share the same names.
"""
from manim import *

# --- colours ---------------------------------------------------------------
BG    = "#11141a"
INK   = "#f4f6fa"
MUTE  = "#8b93a7"
GOOD  = "#5ac8a8"
BAD   = "#e0736b"
GOLD  = "#e7b86b"
PANEL = "#1b2030"
PANEL2= "#222a3d"
LINE  = "#2c3346"

COLORS = dict(bg=BG, ink=INK, mute=MUTE, good=GOOD, bad=BAD, gold=GOLD,
              panel=PANEL, line=LINE)

# apply background globally for every scene that imports this module
config.background_color = BG

# --- safe area -------------------------------------------------------------
SAFE_W = 13.4      # full usable width  (x in +/- 6.7)
SAFE_H = 7.6       # full usable height (y in +/- 3.8)
BODY_TOP = 2.7     # content sits below the title band


def wrap_text(text, max_chars):
    """Greedy word-wrap into a multi-line string (Manim Text honours \\n)."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + (1 if cur else 0) <= max_chars:
            cur = f"{cur} {w}".strip()
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return "\n".join(lines)


def fit(mob, max_w=SAFE_W, max_h=SAFE_H):
    """Scale a mobject down so it never spills outside the safe area."""
    if mob.width > max_w:
        mob.scale(max_w / mob.width)
    if mob.height > max_h:
        mob.scale(max_h / mob.height)
    return mob


# --- text constructors -----------------------------------------------------
def eyebrow(text, color=MUTE):
    return Text(text.upper(), font_size=20, color=color, weight=MEDIUM)


def title(text, color=INK, size=40):
    return Text(text, font_size=size, color=color, weight=BOLD)


def title_band(text, eyebrow_text=None):
    """Bold white title pinned to the top edge, optional muted eyebrow above."""
    t = title(text)
    g = VGroup(t)
    if eyebrow_text:
        e = eyebrow(eyebrow_text)
        g = VGroup(e, t).arrange(DOWN, buff=0.16, aligned_edge=ORIGIN)
    g.to_edge(UP, buff=0.45)
    return g


def body(text, color=INK, size=28, w=None, weight=NORMAL):
    if w:
        text = wrap_text(text, w)
    return Text(text, font_size=size, color=color, weight=weight, line_spacing=0.9)


def caption(text, color=MUTE, size=20, w=None):
    if w:
        text = wrap_text(text, w)
    return Text(text, font_size=size, color=color, line_spacing=0.85)


def ref_tag(n, color=MUTE, prefix="ref"):
    """Small provenance chip, e.g. 'ref 6' -> the book's footnote number."""
    label = Text(f"{prefix} {n}", font_size=16, color=color, weight=MEDIUM)
    box = SurroundingRectangle(label, color=color, buff=0.1,
                               corner_radius=0.08, stroke_width=1.2)
    return VGroup(box, label)


def chip(text, color=INK, fill=PANEL, size=26, pad=0.22):
    label = Text(text, font_size=size, color=color, weight=BOLD)
    box = RoundedRectangle(corner_radius=0.16, width=label.width + 2 * pad,
                           height=label.height + 2 * pad * 0.9,
                           fill_color=fill, fill_opacity=1.0,
                           stroke_color=LINE, stroke_width=1.4)
    return VGroup(box, label)


def card(width, height, fill=PANEL, stroke=LINE, sw=1.4, radius=0.18):
    return RoundedRectangle(corner_radius=radius, width=width, height=height,
                            fill_color=fill, fill_opacity=1.0,
                            stroke_color=stroke, stroke_width=sw)


def footer(scene_label):
    """Persistent bottom-left brand + bottom-right book credit."""
    left = Text("MORAL AI  ·  " + scene_label.upper(), font_size=15, color=MUTE)
    right = Text("Schaich Borg · Sinnott-Armstrong · Conitzer  (2024)",
                 font_size=15, color=MUTE)
    left.to_corner(DL, buff=0.3)
    right.to_corner(DR, buff=0.3)
    return VGroup(left, right)
