# Moral AI — visual companion

An animated, public web companion to books and papers, built with hand-authored
[Manim](https://www.manim.community/) scenes and a generated, self-contained web page.
This repo is the **reusable template**: the first companion visualizes the
**Introduction** of *Moral AI and How We Get There* (Schaich Borg, Sinnott-Armstrong
& Conitzer, Pelican, 2024). More chapters / other sources can be added the same way.

> Pipeline: **author scenes → render & adversarially review → gather licensed sources →
> generate the page → stage on GitHub Pages → (later) port to thinkgentile.com.**

## Layout

```
scenes/
  intro_data.py      # SINGLE SOURCE OF TRUTH (EN) — numbers, paraphrases, sources, UI strings
  intro_data_it.py   # Italian mirror (same keys) — full IT translation
  content.py         # language selector: MORALAI_LANG=en|it picks the data module
  style.py           # shared house style (palette, safe-area, text helpers)
  scene_0*.py        # one Manim Scene subclass each (language-agnostic; read content.D)
tools/
  commons_fetch.py   # pull freely-licensed images (Wikimedia Commons) with attribution
build_manim_env.sh   # one-shot, sudo-free Manim CE 0.20.1 environment (micromamba)
build_site.py        # generate index.html (EN) + it/index.html (IT) from the data modules
site_media/
  en/ it/            # final mp4s per language          images/  shared, credited photos
  it_sources/        # per-case Italian-language source overlays (built by a workflow)
index.html  it/index.html   # generated pages (committed; served from gh-pages)
```

**Bilingual.** Scenes render in either language via an env var and a separate media dir:
```bash
MORALAI_LANG=en  ~/manim-env/bin/manim -qm --media_dir media_en scenes/scene_01_framing.py Framing
MORALAI_LANG=it  ~/manim-env/bin/manim -qm --media_dir media_it scenes/scene_01_framing.py Framing
```
`build_site.py` emits both pages; a language toggle links `/` (EN) ⇄ `/it/` (IT). The Italian
page cites an Italian-language article per case where one was found, falling back to the source
the authors cite. **Citation discipline:** the site is an *unofficial companion*; prose is our
paraphrase (no long verbatim quotes), and the stories are explicitly the ones the authors chose
for the book's Introduction.

## 1. Environment (no sudo required)

```bash
bash build_manim_env.sh          # installs micromamba + Manim CE 0.20.1 into ~/manim-env
~/manim-env/bin/manim --version  # -> Manim Community v0.20.1
```

The env lives on the native Linux filesystem (fast) and is git-ignored.

## 2. Render a scene

```bash
~/manim-env/bin/manim -qm --disable_caching scenes/scene_01_framing.py Framing
# -> media/videos/scene_01_framing/720p30/Framing.mp4
# frame-check:
ffmpeg -y -sseof -1.5 -i <mp4> -frames:v 1 /tmp/check.png   # then look at it
```

## 3. Gather licensed images

```bash
python3 tools/commons_fetch.py auto --case transportation_bad \
  --out site_media/images --query "Tesla Model S car"
```

Only free licenses (CC0 / Public domain / CC-BY / CC-BY-SA) are accepted; each file
gets a `<case>.json` sidecar with artist + license + source URL.

## 4. Build the page & publish

```bash
python3 build_site.py            # regenerate index.html from the source of truth
# copy final mp4s into site_media/, then publish to gh-pages (see build_site.py header)
```

## Honesty discipline (non-negotiable)

- Every on-screen number, name, date and quotation is transcribed from the book and
  lives only in `scenes/intro_data.py`. Scenes and the page read from it; nothing is invented.
- Quotations are shown in quotation marks with author credit; everything else is a
  faithful paraphrase. The book *reports* the cases; we link the source the authors cite.
- Figures use different units and are **not** comparable on one axis — shown for scale, not ranking.
- Photographs are freely-licensed, **representative** images (credited on the page); unless
  noted they do not depict the exact event. Glass/balance diagrams are schematic, not data.

## Credits

Visual companion generated with Manim CE. Source material © the book's authors / Pelican
Books. Image credits are listed on the page and in `site_media/images/*.json`.
Renderer based on the Manim toolchain from
[HarleyCoops/Math-To-Manim](https://github.com/HarleyCoops/Math-To-Manim) (LLM pipeline bypassed; scenes hand-authored).
