# -*- coding: utf-8 -*-
"""
Language selector for the scenes. Render English (default) or Italian:

    MORALAI_LANG=en  ~/manim-env/bin/manim -qm scenes/scene_01_framing.py Framing
    MORALAI_LANG=it  ~/manim-env/bin/manim -qm scenes/scene_01_framing.py Framing

Scenes do `from content import D, LANG` and read every on-screen string from D.
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))

LANG = os.environ.get("MORALAI_LANG", "en").lower()
if LANG == "it":
    import intro_data_it as D          # noqa: F401
else:
    import intro_data as D             # noqa: F401
