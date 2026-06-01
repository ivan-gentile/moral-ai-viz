# AGENTS.md — build a visual companion to a paper (or book chapter)

You are an agent asked to turn a **paper** (or book chapter) into an animated, public
web companion: hand-authored [Manim](https://www.manim.community/) scenes + a
self-contained, generated web page, published to GitHub Pages. This repo is the
**reusable template**; the live example is the Introduction of *Moral AI* (a popular
book — see `scenes/intro_data.py`, `build_site.py`). This file is the playbook. Follow it.

> **Golden rule (scientific venues):** the page is an *honest companion*, never a
> substitute. Every on-screen number, name, date and quotation lives in ONE data module
> and is transcribed verbatim from the source. Scenes/page only *read* it. Nothing is
> invented. Paraphrase the prose; don't reproduce the source word-for-word. Show the
> caveats (the metric where you don't win, inconclusive results) — that is what makes it
> credible. Label any drawn diagram that isn't real data **"schematic"** on screen.

---

## 0. Inputs to get from the user first
- **The source** (PDF / LaTeX / arXiv link) — the source of truth for every number.
- **Audience** (e.g. "general + scientific convention").
- **A NEW repo name** (never modify the source's repo — create a new one) and the GitHub `OWNER`.
- **Language(s)** — English only, or bilingual EN/IT (this repo supports both; see §7).
Read the source and extract its results/claims/figures *and its reference list* before designing anything.

## 1. Environment (no sudo on this box)
A working env may already exist at `~/manim-env`. Check, else build it (one-shot, user-space):
```bash
~/manim-env/bin/manim --version            # expect: Manim Community v0.20.1
bash build_manim_env.sh                     # if missing — installs micromamba + Manim 0.20.1
```
Always invoke Manim by absolute path (`~/manim-env/bin/manim`); it is not on `PATH`.
Render to a per-language media dir so files don't collide:
```bash
MORALAI_LANG=en ~/manim-env/bin/manim -qm --disable_caching --media_dir media_en scenes/<file>.py <ClassName>
# -> media_en/videos/<file>/720p30/<ClassName>.mp4
```

## 2. Honesty discipline (non-negotiable)
- Create **one data module** = the single source of truth (for a paper: `scenes/results_data.py`).
  Header comment citing the paper (authors, venue, year, arXiv/DOI). Transcribe every number verbatim.
- No scene hardcodes or invents a number — they all import from the data module.
- Bar charts must be **true-to-scale** (per-group y-axis with **printed floor/ceil tick labels** when
  metrics have different ranges — NOT a min–max stretch) and carry **error bars (±std)**, omitted only
  where std≈0.
- Any heatmap/diagram that isn't real data is labelled **"schematic"** on screen.
- Keep a **"What we do NOT claim"** box and a clear **attribution** block citing the paper (see §6).

## 3. The data module (copy the shape of `scenes/intro_data.py`)
Reuse these **chrome keys verbatim** so `build_site.py`/`content.py`/the scenes keep working:
`BOOK`/`PAPER` (metadata), `ATTRIBUTION`, `NOT_CLAIM`, `UI`, `SCENE_TITLES`, `STRINGS`, `PAGE`,
and `LANG`/`OTHER_LANG_*`. Replace the *content* keys with paper-shaped ones, e.g.:
```python
PAPER = {"title":..., "authors":[...], "venue":..., "year":..., "url":..., "section":..., "scope":...}

# Results — each metric carries per-method means + stds for the error bars,
# explicit axis bounds (true-to-scale), the paper's table/figure number, and a winner flag.
RESULTS = [
  {"metric":"Accuracy (%)", "unit":"%", "higher_is_better":True,
   "floor":80, "ceil":95,                      # printed y-axis ticks — NOT auto min/max
   "groups":[{"name":"Ours","mean":91.2,"std":0.4,"winner":True},
             {"name":"Baseline A","mean":88.7,"std":0.6},
             {"name":"Baseline B","mean":87.1,"std":0.0}],   # std≈0 -> omit its error bar
   "fn":3},                                     # source table/citation number
  # ... one per metric/figure
]
CLAIMS  = [{"text":"<faithful paraphrase>", "evidence":"Table 2", "fn":...}]
CAVEATS = ["<metric where the method does NOT win>", "<inconclusive / limited-n result>", ...]
FIGURES = [{"caption":"<paraphrase>", "schematic":False, "fn":...}]
```
Keep `source`/`fn` on each item so the page can link the paper and label provenance (`ref N`).

## 4. Scene archetypes (4–6 scenes, ~18–32s each)
House style lives in `scenes/style.py` — import it: `BG=#11141a`, bold white title `to_edge(UP)`,
**GOOD/teal `#5ac8a8`** for the winner, **BAD/coral `#e0736b`** for the loser/caution, `GOLD` for
figures. Helpers: `title_band, footer, body, caption, chip, card, ref_tag, wrap_text, fit`.
Keep everything inside **x∈[-7,7], y∈[-4,4]** with generous buffers.

Typical set for a paper:
1. **Title / thesis** — paper, plain-language one-line claim.
2. **Headline result — true-to-scale bar chart** with ±std error bars (the core scientific scene).
3. **Method / architecture** — a clean diagram (label "schematic" if stylised).
4. **Ablation / breakdown** — bars or a real-data table; "schematic" if illustrative.
5. **Caveats / what we do NOT claim** — including the metric where you don't win.
6. **End card** — paper, authors, venue, "a visual companion".

Hard-won lessons (the frame-review will otherwise re-discover them):
- Import every Manim name you use (`FadeOut`, `Create`, `LaggedStart`, …).
- Per-group axes with printed floor/ceil ticks; never min–max stretch across different metrics.
- Sequence swaps with `LaggedStart(FadeOut(old), FadeIn(new), lag_ratio≈0.65)` — simultaneous
  cross-fades cause ghosting/overlap.
- Put "beat words" in fixed bands so they never collide with the header/subtitle/footer.
- Scale groups to the safe area (`fit(...)`); keep bottom content clear of the footer line.

## 5. Run the workflow (this is the quality engine)
Use the **Workflow** tool. Two lanes in parallel, then a barrier:
- **Render lane** — one agent per scene: render → extract ~5 frames + the last via `ffmpeg`
  (`-sseof -0.5`) → **adversarially review** each frame (clipping at edges, overlapping labels,
  number disagrees with the data module) → fix the scene file → re-render until clean (max ~3).
  *Each agent owns one scene file* (no write races). If bilingual, the same agent renders both
  languages (`media_en`/`media_it`) and fixes the shared file for both.
- **Image/source lane** — one agent per item: fetch a **freely-licensed** representative image
  via `tools/commons_fetch.py` (and/or find the cited source URL), *visually verify* it, retry with
  better queries if wrong. For a bilingual edition, a second pass finds an Italian-language article.
- **Fact-check barrier** — one agent confirms **every on-screen literal matches the data module**,
  all metrics/claims are present, no long verbatim quotes remain, and every image has a credit.

See `workflows/scripts/*.js` (committed examples) for the exact structure to copy.

## 6. Build the page
`build_site.py` generates a self-contained `index.html` (dark, mobile-friendly, inline CSS,
Fraunces + Newsreader + Space Mono) from the data module + image credits. It already renders:
prominent **attribution/citation block**, per-section videos, a "by the numbers" grid, an honest
**"What we do NOT claim"** box, a **references** list (links the source's own citations), **image
credits**, and a language toggle. For a paper, swap the book-shaped section builders
(`domain_block`/`numbers_block`/`values_block`) for results/claims/figures builders that read
`RESULTS`/`CLAIMS`/`FIGURES`; keep the hero, honesty box, references, credits and footer.
```bash
python3 build_site.py        # writes index.html (and it/index.html if bilingual)
```

## 7. Bilingual (optional)
`scenes/content.py` selects the data module by `MORALAI_LANG`. To add a language, create a mirror
module with the **same keys** (e.g. `results_data_it.py`), render with `MORALAI_LANG=it --media_dir media_it`,
and `build_site.py` emits `it/index.html` with a toggle. Cite a same-language source per item where one exists.

## 8. Images (free licences only)
```bash
python3 tools/commons_fetch.py auto --case <id> --out site_media/images --query "<subject>"
# only CC0 / Public domain / CC-BY / CC-BY-SA accepted; writes <id>.json with artist + licence + source.
```
Label representative images as such; never copy a copyrighted news photo onto the public site.

## 9. Publish to GitHub Pages + verify
```bash
OWNER=<owner> REPO=<new-repo> bash publish.sh     # stages media_<lang> -> site_media/<lang>, builds,
                                                  # commits main, pushes, (re)creates gh-pages, enables Pages
URL=https://<owner>.github.io/<new-repo>/
curl -s -o /dev/null -w "%{http_code} %{content_type}\n" "$URL"                       # page 200
curl -s -o /dev/null -w "%{http_code} %{content_type}\n" "${URL}site_media/en/<Class>.mp4"   # video 200
```
Poll ~30–60s for the build; confirm a video and an image serve. To update one scene later:
re-render it → `publish.sh` (or copy its mp4 into `site_media/<lang>/`, rebuild, recommit gh-pages).

## 10. Definition of done
- [ ] Env verified (`manim --version` = 0.20.1).
- [ ] `<source>_data.py` holds every literal verbatim, with a citation header.
- [ ] 4–6 scenes render clean (frame-reviewed): no clipping/overlap; bars true-to-scale **with ±std**; schematics labelled.
- [ ] Fact-check passed: every on-screen literal matches the data module; caveats shown; no long verbatim quotes.
- [ ] Images freely-licensed + credited; references link the source's own citations.
- [ ] Page live on GitHub Pages (page + a video + an image all 200), citation/attribution block prominent.

## File map (reuse vs adapt)
| Reuse as-is | Adapt per source |
|---|---|
| `build_manim_env.sh`, `tools/commons_fetch.py`, `scenes/style.py`, `scenes/content.py`, `publish.sh`, the workflow pattern | the data module (`*_data.py`), the scene files, `build_site.py` section builders, README |
