# -*- coding: utf-8 -*-
"""
Scene 4 - Six moral values at stake (and the book says the list isn't exhaustive).
Source: Moral AI, Introduction pp. xix-xx.
Render: manim -qm --disable_caching scenes/scene_04_values.py SixValues
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))

from manim import *
from style import (BG, INK, MUTE, GOOD, BAD, GOLD, PANEL, LINE,
                   title_band, footer, body, caption, card)
import intro_data as D

ACCENTS = ["#5ac8a8", "#7aa2f7", "#e7b86b", "#9ece6a", "#bb9af7", "#e0736b"]


class SixValues(Scene):
    def construct(self):
        head = title_band("Six moral values at stake",
                          "what the rest of the book is about")
        foot = footer("the values")
        self.play(FadeIn(head, shift=DOWN * 0.2), FadeIn(foot), run_time=1.1)
        self.wait(0.6)

        def value_card(v, accent):
            box = card(4.05, 2.05, fill=PANEL)
            bar = Line(box.get_corner(UL) + DOWN * 0.18 + RIGHT * 0.22,
                       box.get_corner(UR) + DOWN * 0.18 + LEFT * 0.22,
                       color=accent, stroke_width=3)
            name = Text(v["name"], font_size=27, color=INK, weight=BOLD)
            name.next_to(bar, DOWN, buff=0.16)
            ill = caption(v["illustration"], color=MUTE, size=14.5, w=34)
            ill.next_to(name, DOWN, buff=0.18)
            inner = VGroup(name, ill)
            inner.move_to(box.get_center() + DOWN * 0.12)
            return VGroup(box, bar, inner)

        cards = VGroup(*[value_card(v, ACCENTS[i % len(ACCENTS)])
                         for i, v in enumerate(D.VALUES)])
        grid = cards.arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.4))
        grid.move_to([0, -0.35, 0])
        if grid.width > 13.2:
            grid.scale(13.2 / grid.width)

        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in cards],
                              lag_ratio=0.5, run_time=8.5))
        self.wait(3.2)

        caveat = caption(f"“{D.VALUES_CAVEAT}”", color=GOLD, size=19, w=70)
        caveat.to_edge(DOWN, buff=0.55)
        self.play(FadeOut(foot), FadeIn(caveat, shift=UP * 0.1), run_time=1.2)
        self.wait(3.5)
