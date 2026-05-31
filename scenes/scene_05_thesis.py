# -*- coding: utf-8 -*-
"""
Scene 5 - The thesis: don't under- or over-estimate; keep the baby, lose the bathwater.
Source: Moral AI, Introduction p. xx. Verbatim fragments in quotation marks.
Render: manim -qm --disable_caching scenes/scene_05_thesis.py BabyAndBathwater
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))

from manim import *
from style import (BG, INK, MUTE, GOOD, BAD, GOLD, PANEL, LINE,
                   title_band, footer, body, caption, chip)
import intro_data as D


class BabyAndBathwater(Scene):
    def construct(self):
        T = D.THESIS
        head = title_band("Don't throw out the baby", "the book's thesis")
        foot = footer("the thesis")
        self.play(FadeIn(head, shift=DOWN * 0.2), FadeIn(foot), run_time=0.9)

        # --- a balance that settles level -------------------------------
        pivot = np.array([0, 0.55, 0])
        post = Line([0, -1.5, 0], pivot + UP * 0.1, color=INK, stroke_width=4)
        fulcrum = Triangle(color=INK, fill_opacity=1).scale(0.22)
        fulcrum.move_to(pivot + UP * 0.16)

        beam = Line(pivot + LEFT * 2.7, pivot + RIGHT * 2.7, color=INK, stroke_width=5)

        def pan(end_sign):
            x = 2.4 * end_sign
            top = pivot + RIGHT * x
            hang = Line(top, top + DOWN * 0.6, color=MUTE, stroke_width=2)
            tray = Line(top + DOWN * 0.6 + LEFT * 0.45, top + DOWN * 0.6 + RIGHT * 0.45,
                        color=INK, stroke_width=4)
            w = RoundedRectangle(corner_radius=0.06, width=0.5, height=0.32,
                                 fill_color=GOLD, fill_opacity=1, stroke_width=0)
            w.move_to(tray.get_center() + UP * 0.18)
            return VGroup(hang, tray, w)

        scale = VGroup(beam, pan(-1), pan(1))
        lab_l = caption("underestimate\nthe dangers", color=BAD, size=18)
        lab_l.move_to(pivot + LEFT * 2.4 + DOWN * 1.35)
        lab_r = caption("overestimate\nthe dangers", color=BAD, size=18)
        lab_r.move_to(pivot + RIGHT * 2.4 + DOWN * 1.35)

        self.play(Create(post), FadeIn(fulcrum), run_time=0.7)
        self.play(Create(beam), FadeIn(scale[1]), FadeIn(scale[2]), run_time=0.8)
        self.play(FadeIn(lab_l), FadeIn(lab_r), run_time=0.6)

        # wobble, then settle level (neither under nor over)
        self.play(Rotate(scale, angle=-0.14, about_point=pivot), run_time=0.7)
        self.play(Rotate(scale, angle=0.26, about_point=pivot), run_time=0.8)
        self.play(Rotate(scale, angle=-0.12, about_point=pivot), run_time=0.7)
        balanced = chip("addressed thoughtfully", color=BG, fill=GOOD, size=22)
        balanced.move_to(pivot + UP * 1.05)
        self.play(FadeIn(balanced, shift=DOWN * 0.1), run_time=0.7)
        self.wait(1.0)

        scale_grp = VGroup(post, fulcrum, scale, lab_l, lab_r, balanced)

        # --- the verbatim thesis ----------------------------------------
        l1 = body(f"“{T['not_underestimate']} {T['not_overestimate']}”",
                  color=INK, size=26, w=52)
        l1.move_to([0, 0.7, 0])
        l2 = body(f"“{T['baby_bathwater']}”", color=INK, size=24, w=54)
        l2.next_to(l1, DOWN, buff=0.4)
        thesis_grp = VGroup(l1, l2)

        self.play(FadeOut(scale_grp), run_time=0.6)
        self.play(Write(l1), run_time=1.6)
        self.play(FadeIn(l2, shift=UP * 0.1), run_time=1.2)
        self.wait(1.8)

        # --- end card ----------------------------------------------------
        self.play(FadeOut(thesis_grp), FadeOut(foot), FadeOut(head), run_time=0.6)
        bt = Text("Moral AI", font_size=46, color=INK, weight=BOLD)
        bs = Text("and How We Get There", font_size=26, color=MUTE)
        names = caption(" · ".join(D.BOOK["authors"]), color=MUTE, size=20)
        sec = caption("Introduction · What's the Problem?", color=GOLD, size=20)
        tagline = caption("a visual companion · every figure & source from the book",
                          color=MUTE, size=16)
        endcard = VGroup(bt, bs, sec, names, tagline).arrange(DOWN, buff=0.28)
        endcard.move_to(ORIGIN)
        rule = Line(LEFT * 2.4, RIGHT * 2.4, color=LINE, stroke_width=1.5)
        rule.next_to(sec, DOWN, buff=0.22)
        self.play(FadeIn(bt, shift=UP * 0.1), FadeIn(bs), run_time=1.0)
        self.play(FadeIn(sec), Create(rule), run_time=0.7)
        self.play(FadeIn(names), FadeIn(tagline), run_time=0.8)
        self.wait(3.0)
