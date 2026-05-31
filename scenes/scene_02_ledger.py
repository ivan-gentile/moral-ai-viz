# -*- coding: utf-8 -*-
"""
Scene 2 - The double-edged ledger: 11 domains, each with good vs bad news.
Source: Moral AI, Introduction pp. xiv-xviii (the 11 paired examples).
Render: manim -qm --disable_caching scenes/scene_02_ledger.py DoubleEdgedLedger
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))

from manim import *
from style import (BG, INK, MUTE, GOOD, BAD, GOLD, PANEL, LINE,
                   title_band, footer, body, caption, chip, ref_tag)
from content import D


class DoubleEdgedLedger(Scene):
    def construct(self):
        ST = D.SCENE_TITLES["ledger"]
        head = title_band(ST["title"], ST["eyebrow"])
        foot = footer(ST["foot"])
        self.play(FadeIn(head, shift=DOWN * 0.2), FadeIn(foot), run_time=0.9)

        # persistent scaffold: column headers + central spine
        gh = chip(D.UI["good_news"], color=BG, fill=GOOD, size=24).move_to([-3.9, 2.05, 0])
        bh = chip(D.UI["bad_news"], color=BG, fill=BAD, size=24).move_to([3.9, 2.05, 0])
        spine = Line([0, 1.55, 0], [0, -1.95, 0], color=LINE, stroke_width=1.6)
        self.play(FadeIn(gh, shift=DOWN * 0.15), FadeIn(bh, shift=DOWN * 0.15),
                  Create(spine), run_time=0.8)

        # progress dots (eleven)
        dots = VGroup(*[Dot(radius=0.07, color=LINE) for _ in D.DOMAINS])
        dots.arrange(RIGHT, buff=0.28).move_to([0, -2.5, 0])
        self.play(FadeIn(dots), run_time=0.5)

        def side(text, color, x):
            t = body(text, color=color, size=22, w=16)
            t.move_to([x, 0.15, 0])
            return t

        cur = None
        for i, dom in enumerate(D.DOMAINS):
            name = chip(dom["title"], color=INK, fill=PANEL, size=24).move_to([0, 0.45, 0])
            g = side(dom["good"]["head"], GOOD, -3.9)
            grt = ref_tag(dom["good"]["fn"], color=MUTE, prefix=D.UI["ref"]).next_to(g, DOWN, buff=0.3)
            b = side(dom["bad"]["head"], BAD, 3.9)
            brt = ref_tag(dom["bad"]["fn"], color=MUTE, prefix=D.UI["ref"]).next_to(b, DOWN, buff=0.3)
            grp = VGroup(name, g, grt, b, brt)

            new_dots = dots.copy()
            for j, d in enumerate(new_dots):
                d.set_color(GOLD if j == i else (GOOD if j < i else LINE))

            if cur is None:
                self.play(FadeIn(grp, shift=UP * 0.1), Transform(dots, new_dots),
                          run_time=0.7)
            else:
                # Sequence the swap so the outgoing and incoming headlines never
                # share the screen (avoids ghosting / colliding text mid-fade).
                self.play(
                    LaggedStart(
                        FadeOut(cur, shift=UP * 0.12),
                        FadeIn(grp, shift=UP * 0.12),
                        lag_ratio=0.65,
                    ),
                    Transform(dots, new_dots),
                    run_time=0.85,
                )
            cur = grp
            self.wait(1.1)

        self.play(FadeOut(cur), FadeOut(spine), FadeOut(gh), FadeOut(bh),
                  FadeOut(dots), run_time=0.7)

        # closing: tip of the iceberg + the eleven names
        tip = body(D.THESIS["tip_of_iceberg"], color=INK, size=30, w=40)
        tip.move_to([0, 1.4, 0])
        names = VGroup(*[caption(d["title"], color=MUTE, size=22) for d in D.DOMAINS])
        names.arrange_in_grid(rows=2, buff=(0.7, 0.45)).move_to([0, -0.7, 0])
        self.play(Write(tip), run_time=1.2)
        self.play(LaggedStart(*[FadeIn(n) for n in names], lag_ratio=0.12, run_time=1.8))
        self.wait(2.0)
