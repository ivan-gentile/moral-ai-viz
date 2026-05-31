# -*- coding: utf-8 -*-
"""
Scene 1 - Framing: pessimist vs optimist, and "the glass is both".
Source: Moral AI, Introduction pp. xiii-xiv. Verbatim lines in quotation marks.
Render: manim -qm --disable_caching scenes/scene_01_framing.py Framing
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))

from manim import *
from style import (BG, INK, MUTE, GOOD, BAD, GOLD, PANEL, LINE,
                   title_band, footer, body, caption, chip)
import intro_data as D


class Framing(Scene):
    def construct(self):
        F = D.FRAMING
        head = title_band("What's the problem?", "Moral AI  ·  Introduction")
        foot = footer("framing")
        self.play(FadeIn(head, shift=DOWN * 0.2), run_time=1.0)
        self.play(FadeIn(foot), run_time=0.6)

        # --- Act 1: the alarm (verbatim) ----------------------------------
        alarm = body(f"“{F['alarm']}”", color=INK, size=38, w=26)
        alarm.move_to([0, 0.4, 0])
        sub = caption("This alarm is spreading fast.", color=MUTE, size=24)
        sub.next_to(alarm, DOWN, buff=0.4)
        self.play(Write(alarm), run_time=1.4)
        self.play(FadeIn(sub), run_time=0.6)
        self.wait(1.4)
        self.play(FadeOut(alarm), FadeOut(sub), run_time=0.7)

        # --- Act 2: the two camps -----------------------------------------
        divider = Line([0, 1.45, 0], [0, -2.95, 0], color=LINE, stroke_width=1.5)

        TOP_Y = 1.45   # both column tops align here so neither hits the footer

        def camp(label, items, color, x):
            hdr = chip(label, color=BG, fill=color, size=26)
            bullets = VGroup(*[
                body("•  " + t, color=INK, size=23, w=26) for t in items
            ]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            col = VGroup(hdr, bullets).arrange(DOWN, buff=0.4)
            # pin each column's top edge to a common y, then centre horizontally
            col.move_to([x, 0, 0])
            col.align_to([x, TOP_Y, 0], UP)
            return hdr, bullets, col

        ph, pb, pcol = camp(F["pessimist_label"], F["pessimist_short"], BAD, -3.45)
        oh, ob, ocol = camp(F["optimist_label"], F["optimist_short"], GOOD, 3.45)

        self.play(Create(divider), run_time=0.6)
        self.play(FadeIn(ph, shift=DOWN * 0.2), FadeIn(oh, shift=DOWN * 0.2),
                  run_time=0.8)
        self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.15) for b in pb],
                              lag_ratio=0.25, run_time=1.8))
        self.play(LaggedStart(*[FadeIn(b, shift=LEFT * 0.15) for b in ob],
                              lag_ratio=0.25, run_time=1.8))
        self.wait(1.6)

        camps = VGroup(divider, ph, pb, oh, ob)
        self.play(FadeOut(camps), run_time=0.7)

        # --- Act 3: the glass is both -------------------------------------
        q = caption(f"“{F['verdict_question']}”", color=MUTE, size=26)
        q.move_to([0, 2.0, 0])

        # schematic glass (clearly a metaphor, not data)
        outline = Polygon([-0.62, 1.0, 0], [0.62, 1.0, 0],
                          [0.44, -1.0, 0], [-0.44, -1.0, 0],
                          color=INK, stroke_width=3)
        liquid = Polygon([-0.53, 0.0, 0], [0.53, 0.0, 0],
                         [0.44, -1.0, 0], [-0.44, -1.0, 0],
                         fill_color=GOOD, fill_opacity=0.55, stroke_width=0)
        surface = Line([-0.53, 0.0, 0], [0.53, 0.0, 0], color=GOOD, stroke_width=3)
        glass = VGroup(outline, liquid, surface).scale(1.25).move_to([0, -0.35, 0])

        empty_lbl = caption("half empty", color=BAD, size=22).next_to(glass, RIGHT, buff=0.9).shift(UP * 0.85)
        full_lbl = caption("half full", color=GOOD, size=22).next_to(glass, LEFT, buff=0.9).shift(DOWN * 0.6)
        ea = Arrow(empty_lbl.get_left(), glass.get_top() + RIGHT * 0.2 + DOWN * 0.25,
                   color=BAD, stroke_width=2.5, max_tip_length_to_length_ratio=0.12, buff=0.15)
        fa = Arrow(full_lbl.get_right(), glass.get_center() + DOWN * 0.2,
                   color=GOOD, stroke_width=2.5, max_tip_length_to_length_ratio=0.12, buff=0.15)

        self.play(FadeIn(q), run_time=0.7)
        self.play(Create(outline), run_time=0.8)
        self.play(FadeIn(liquid), Create(surface), run_time=0.7)
        self.play(FadeIn(empty_lbl), GrowArrow(ea),
                  FadeIn(full_lbl), GrowArrow(fa), run_time=1.0)
        self.wait(1.0)

        # verdict  (fade the footer so the closing lines have room to breathe)
        pre = body("Our answer is:  ", color=INK, size=40)
        both = Text("both.", font_size=44, weight=BOLD)
        both.set_color_by_gradient(GOOD, BAD)
        verdict = VGroup(pre, both).arrange(RIGHT, buff=0.12)
        verdict.move_to([0, -2.2, 0])
        gloss = caption(D.FRAMING["verdict_gloss"], color=MUTE, size=18, w=82)
        gloss.next_to(verdict, DOWN, buff=0.28)

        self.play(Write(verdict), FadeOut(foot), run_time=1.2)
        self.play(FadeIn(gloss), run_time=0.7)
        self.wait(2.0)
