# -*- coding: utf-8 -*-
"""
Scene 3 - By the numbers: the Introduction's hard literals, in context.
The units are deliberately incommensurable -> shown as cards, never one axis.
Source: Moral AI, Introduction (figures with the authors' footnotes).
Render: manim -qm --disable_caching scenes/scene_03_numbers.py ByTheNumbers
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))

from manim import *
from style import (BG, INK, MUTE, GOOD, BAD, GOLD, PANEL, LINE,
                   title_band, footer, body, caption, card, ref_tag)
import intro_data as D


class ByTheNumbers(Scene):
    def construct(self):
        head = title_band("By the numbers", "Every figure is the book's own")
        self.play(FadeIn(head, shift=DOWN * 0.2), run_time=0.9)

        note = caption("different units — shown for scale, not as a ranking",
                       color=MUTE, size=20)
        note.next_to(head, DOWN, buff=0.18)
        self.play(FadeIn(note), run_time=0.6)

        CARD_W = 2.95
        CARD_H = 2.18

        def fact_card(n):
            tone = GOOD if n.get("tone") == "good" else BAD
            box = card(CARD_W, CARD_H, fill=PANEL)
            val = Text(n["value"], font_size=32, color=tone, weight=BOLD)
            lab = caption(n["label"], color=INK, size=17, w=24)
            ctx = caption(n["context"], color=MUTE, size=13, w=34)
            rt = ref_tag(n["fn"], color=MUTE).scale(0.8)
            # value + label + context stacked, leaving room for the ref chip
            stack = VGroup(val, lab, ctx).arrange(DOWN, buff=0.12)
            # never let content spill past the box; scale the stack if needed
            inner_w = CARD_W - 0.34
            inner_h = CARD_H - 0.62          # reserve a band for the ref chip
            if stack.width > inner_w:
                stack.scale(inner_w / stack.width)
            if stack.height > inner_h:
                stack.scale(inner_h / stack.height)
            stack.move_to(box.get_top() + DOWN * (stack.height / 2 + 0.18))
            rt.move_to(box.get_corner(DR) + LEFT * 0.42 + UP * 0.26)
            return VGroup(box, stack, rt)

        cards = VGroup(*[fact_card(n) for n in D.NUMBERS])
        # 7 cards -> 4 on top row, 3 centered on the bottom row
        top = VGroup(*cards[:4]).arrange(RIGHT, buff=0.3)
        bot = VGroup(*cards[4:]).arrange(RIGHT, buff=0.3)
        grid = VGroup(top, bot).arrange(DOWN, buff=0.35).move_to([0, -0.55, 0])
        if grid.width > 13.2:
            grid.scale(13.2 / grid.width)

        self.play(LaggedStart(*[FadeIn(c, scale=0.85) for c in cards],
                              lag_ratio=0.22, run_time=4.0))
        self.wait(3.4)

        # gentle emphasis sweep across the figures (value mobject = c[1][0])
        good_idx = {i for i, n in enumerate(D.NUMBERS) if n.get("tone") == "good"}
        for i, c in enumerate(cards):
            base = GOOD if i in good_idx else BAD
            self.play(c[1][0].animate.set_color(GOLD), run_time=0.32)
            self.play(c[1][0].animate.set_color(base), run_time=0.32)
            self.wait(0.2)
        self.wait(3.2)
