#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate the self-contained index.html for the Moral AI Introduction companion
from the single source of truth (scenes/intro_data.py) + gathered image credits
(site_media/images/<case>.json). Run:  python3 build_site.py

The page never invents text: all prose comes from intro_data. Images that are
missing degrade gracefully to a typographic tile.
"""
import html, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "scenes"))
import intro_data as D

IMG_DIR = os.path.join(HERE, "site_media", "images")
MEDIA = os.path.join(HERE, "site_media")


def esc(s):
    return html.escape(str(s), quote=True)


def credit(case_id):
    """Return (img_rel_path, artist, license, license_url, source_url) or None."""
    j = os.path.join(IMG_DIR, case_id + ".json")
    if not os.path.exists(j):
        return None
    try:
        m = json.load(open(j, encoding="utf-8"))
    except Exception:
        return None
    f = m.get("file")
    if not f or not os.path.exists(os.path.join(IMG_DIR, f)):
        return None
    return {
        "src": "site_media/images/" + f,
        "artist": m.get("artist", "").strip() or "Wikimedia Commons",
        "license": m.get("license", "").strip() or "see source",
        "license_url": m.get("license_url", "").strip(),
        "source_url": m.get("source_url", "").strip(),
    }


def has_video(cls):
    return os.path.exists(os.path.join(MEDIA, cls + ".mp4"))


# scene class -> (anchor, kicker, blurb)
SCENES = [
    ("Framing", "framing", "01 · The framing",
     "Pessimists cry “the robots are coming”; optimists can’t wait. The book’s answer to “half empty or half full?” is: both."),
    ("DoubleEdgedLedger", "ledger", "02 · The ledger",
     "Eleven everyday domains, each carrying good news and bad news — sometimes from the very same technique."),
    ("ByTheNumbers", "numbers", "03 · By the numbers",
     "The Introduction’s hard figures, each in its own context. Different units — shown for scale, never as a ranking."),
    ("SixValues", "values", "04 · The values",
     "Six moral values the rest of the book is built around — and the authors’ reminder that the list isn’t exhaustive."),
    ("BabyAndBathwater", "thesis", "05 · The thesis",
     "Don’t underestimate the dangers; don’t overestimate them either. Keep the AI baby — lose the bathwater."),
]
SCENE_BY_KEY = {s[1]: s for s in SCENES}


def video_block(cls, poster_kicker, blurb, autoplay=True):
    if not has_video(cls):
        return (f'<div class="vid vid--missing"><span>{esc(poster_kicker)}</span>'
                f'<p>{esc(blurb)}</p></div>')
    extra = ' autoplay loop muted' if autoplay else ' muted'
    return (
        f'<figure class="vid reveal">'
        f'<video playsinline preload="metadata" controls{extra} '
        f'src="site_media/{esc(cls)}.mp4"></video>'
        f'<figcaption>{esc(blurb)}</figcaption></figure>'
    )


def img_or_tile(case_id, tone, headline):
    c = credit(case_id)
    if not c:
        cls = "tile tile--good" if tone == "good" else "tile tile--bad"
        return f'<div class="{cls}"><span>{esc(headline)}</span></div>', None
    cap = []
    if c["license_url"]:
        cap.append(f'<a href="{esc(c["license_url"])}" target="_blank" rel="noopener">'
                   f'{esc(c["artist"])} · {esc(c["license"])}</a>')
    elif c["source_url"]:
        cap.append(f'<a href="{esc(c["source_url"])}" target="_blank" rel="noopener">'
                   f'{esc(c["artist"])} · {esc(c["license"])}</a>')
    else:
        cap.append(f'{esc(c["artist"])} · {esc(c["license"])}')
    figc = f'<figcaption class="credit">{cap[0]}</figcaption>'
    img = (f'<figure class="ph"><img loading="lazy" alt="Representative image: {esc(headline)}" '
           f'src="{esc(c["src"])}">{figc}</figure>')
    return img, c


def side_panel(dom, tone):
    side = dom[tone]
    case_id = f'{dom["key"]}_{tone}'
    kicker = "Good news" if tone == "good" else "Bad news"
    imghtml, _ = img_or_tile(case_id, tone, side["head"])
    src = side["source"]
    srcbits = esc(src["pub"])
    if src.get("date"):
        srcbits += " · " + esc(src["date"])
    num = side.get("number")
    numhtml = f'<span class="bignum">{esc(num)}</span>' if num else ""
    return f'''
      <article class="panel panel--{tone}">
        {imghtml}
        <div class="panel__body">
          <p class="kicker kicker--{tone}">{esc(kicker)}<span class="ref">ref&nbsp;{esc(side["fn"])}</span></p>
          <h4>{esc(side["head"])}</h4>
          {numhtml}
          <p class="detail">{esc(side["detail"])}</p>
          <a class="src" href="{esc(src["url"])}" target="_blank" rel="noopener">{srcbits} <span aria-hidden="true">↗</span></a>
        </div>
      </article>'''


def domain_block(dom, idx):
    return f'''
    <section class="domain reveal" id="d-{esc(dom["key"])}">
      <header class="domain__head">
        <span class="domain__idx">{idx:02d}</span>
        <h3>{esc(dom["title"])}</h3>
        <span class="domain__rule"></span>
      </header>
      <div class="split">
        {side_panel(dom, "good")}
        {side_panel(dom, "bad")}
      </div>
    </section>'''


def numbers_block():
    cards = []
    for n in D.NUMBERS:
        tone = n.get("tone", "bad")
        cards.append(f'''
        <div class="numcard numcard--{tone} reveal">
          <div class="numcard__val">{esc(n["value"])}</div>
          <div class="numcard__lab">{esc(n["label"])}</div>
          <p class="numcard__ctx">{esc(n["context"])}</p>
          <span class="ref ref--corner">ref&nbsp;{esc(n["fn"])}</span>
        </div>''')
    return "\n".join(cards)


def values_block():
    accents = ["#5ac8a8", "#7aa2f7", "#e7b86b", "#9ece6a", "#bb9af7", "#e0736b"]
    out = []
    for i, v in enumerate(D.VALUES):
        out.append(f'''
        <div class="valcard reveal" style="--accent:{accents[i % len(accents)]}">
          <span class="valcard__bar"></span>
          <h4>{esc(v["name"])}</h4>
          <p>{esc(v["illustration"])}</p>
        </div>''')
    return "\n".join(out)


def references_block():
    seen, rows = set(), []
    for dom in D.DOMAINS:
        for tone in ("good", "bad"):
            s = dom[tone]["source"]
            fn = dom[tone]["fn"]
            key = (fn, s["url"])
            if key in seen:
                continue
            seen.add(key)
            datebit = f' ({esc(s["date"])})' if s.get("date") else ""
            rows.append((fn, f'''
        <li class="ref-item">
          <span class="ref-num">{esc(fn)}</span>
          <span class="ref-txt"><strong>{esc(dom["title"])} — {esc("good" if tone=="good" else "bad")}.</strong>
          {esc(s["title"])}. <em>{esc(s["pub"])}</em>{datebit}.
          <a href="{esc(s["url"])}" target="_blank" rel="noopener">link ↗</a></span>
        </li>'''))
    rows.sort(key=lambda r: r[0])
    return "\n".join(r[1] for r in rows)


def credits_block():
    items = []
    for dom in D.DOMAINS:
        for tone in ("good", "bad"):
            cid = f'{dom["key"]}_{tone}'
            c = credit(cid)
            if not c:
                continue
            link = c["source_url"] or c["license_url"]
            label = f'{c["artist"]} — {c["license"]}'
            inner = (f'<a href="{esc(link)}" target="_blank" rel="noopener">{esc(label)}</a>'
                     if link else esc(label))
            items.append(f'<li><b>{esc(dom["title"])} / {esc(tone)}:</b> {inner}</li>')
    if not items:
        return '<li>Images pending.</li>'
    return "\n".join(items)


def not_claim_block():
    return "\n".join(f'<li>{esc(x)}</li>' for x in D.NOT_CLAIM)


CSS = r"""
:root{
  --bg:#0e1116; --bg2:#11141a; --panel:#161b24; --panel2:#1b2130; --line:#28303f;
  --ink:#f4f6fa; --mute:#97a0b3; --good:#5ac8a8; --bad:#e0736b; --gold:#e7b86b;
  --maxw:1180px;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0;background:var(--bg);color:var(--ink);
  font-family:"Newsreader",Georgia,serif;font-size:19px;line-height:1.65;
  -webkit-font-smoothing:antialiased;overflow-x:hidden;
}
body::before{
  content:"";position:fixed;inset:0;z-index:-2;pointer-events:none;
  background:
    radial-gradient(60vw 60vw at 8% -6%, rgba(90,200,168,.12), transparent 60%),
    radial-gradient(55vw 55vw at 100% 105%, rgba(224,115,107,.12), transparent 60%);
}
body::after{
  content:"";position:fixed;inset:0;z-index:-1;pointer-events:none;opacity:.035;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
}
a{color:var(--good);text-decoration:none}
a:hover{text-decoration:underline}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 24px}
.mono{font-family:"Space Mono",ui-monospace,monospace}
h1,h2,h3,h4{font-family:"Fraunces",Georgia,serif;font-weight:600;line-height:1.05;margin:0}
.eyebrow{font-family:"Space Mono",monospace;font-size:13px;letter-spacing:.22em;
  text-transform:uppercase;color:var(--mute)}

/* hero */
.hero{position:relative;padding:18vh 0 9vh;border-bottom:1px solid var(--line);overflow:hidden}
.hero .seam{position:absolute;top:0;bottom:0;left:50%;width:1px;
  background:linear-gradient(var(--good),var(--bad));opacity:.25}
.hero h1{font-size:clamp(56px,12vw,150px);letter-spacing:-.02em;font-weight:600;
  font-optical-sizing:auto}
.hero .sub{font-size:clamp(20px,2.6vw,30px);color:var(--mute);margin-top:.4em;
  font-family:"Fraunces",serif;font-style:italic}
.hero .q{margin-top:2.2rem;font-size:clamp(22px,3vw,34px);max-width:22ch}
.both{background:linear-gradient(92deg,var(--good),var(--gold) 45%,var(--bad));
  -webkit-background-clip:text;background-clip:text;color:transparent;font-weight:600}
.hero .meta{margin-top:2.4rem;font-size:15px;color:var(--mute);
  display:flex;gap:18px;flex-wrap:wrap;align-items:center}
.badge{border:1px solid var(--line);border-radius:999px;padding:5px 13px;
  font-family:"Space Mono",monospace;font-size:12px;letter-spacing:.08em;color:var(--mute)}

/* section scaffolding */
.section{padding:8.5vh 0;border-bottom:1px solid var(--line)}
.section__head{display:flex;align-items:baseline;gap:20px;margin-bottom:2.4rem;flex-wrap:wrap}
.section__head .eyebrow{white-space:nowrap}
.section h2{font-size:clamp(34px,5.5vw,62px);letter-spacing:-.01em}
.lead{color:var(--mute);max-width:62ch;font-size:21px}

/* video */
.vid{margin:2.6rem 0 0;border-radius:14px;overflow:hidden;border:1px solid var(--line);
  background:var(--bg2);box-shadow:0 24px 60px -28px rgba(0,0,0,.8)}
.vid video{display:block;width:100%;height:auto;background:var(--bg2)}
.vid figcaption{padding:14px 18px;color:var(--mute);font-size:15px;border-top:1px solid var(--line)}
.vid--missing{padding:48px;text-align:center;color:var(--mute)}
.vid--missing span{font-family:"Space Mono",monospace;font-size:12px;letter-spacing:.2em;text-transform:uppercase}

/* domain split cards */
.domain{padding:5.5vh 0;border-bottom:1px dashed var(--line)}
.domain:last-child{border-bottom:none}
.domain__head{display:flex;align-items:center;gap:18px;margin-bottom:1.8rem}
.domain__idx{font-family:"Space Mono",monospace;color:var(--gold);font-size:15px}
.domain__head h3{font-size:clamp(28px,4vw,44px)}
.domain__rule{flex:1;height:1px;background:var(--line)}
.split{display:grid;grid-template-columns:1fr 1fr;gap:22px}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:14px;overflow:hidden;
  display:flex;flex-direction:column;transition:transform .35s ease,border-color .35s ease}
.panel:hover{transform:translateY(-4px)}
.panel--good{border-top:3px solid var(--good)}
.panel--good:hover{border-color:var(--good)}
.panel--bad{border-top:3px solid var(--bad)}
.panel--bad:hover{border-color:var(--bad)}
.ph{margin:0;position:relative;aspect-ratio:16/10;overflow:hidden;background:var(--panel2)}
.ph img{width:100%;height:100%;object-fit:cover;display:block;
  transition:transform .6s ease,filter .6s ease;filter:saturate(.92)}
.panel:hover .ph img{transform:scale(1.05);filter:saturate(1.05)}
.ph .credit{position:absolute;right:8px;bottom:8px;margin:0;font-family:"Space Mono",monospace;
  font-size:10.5px;color:#cfd6e2;background:rgba(8,10,14,.66);backdrop-filter:blur(3px);
  padding:3px 8px;border-radius:6px;max-width:75%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.ph .credit a{color:#cfd6e2}
.tile{aspect-ratio:16/10;display:flex;align-items:center;justify-content:center;padding:22px;text-align:center}
.tile span{font-family:"Fraunces",serif;font-size:26px}
.tile--good{background:linear-gradient(135deg,rgba(90,200,168,.16),rgba(90,200,168,.04));color:var(--good)}
.tile--bad{background:linear-gradient(135deg,rgba(224,115,107,.16),rgba(224,115,107,.04));color:var(--bad)}
.panel__body{padding:18px 20px 20px}
.kicker{font-family:"Space Mono",monospace;font-size:12px;letter-spacing:.16em;text-transform:uppercase;
  display:flex;align-items:center;gap:10px;margin:0 0 8px}
.kicker--good{color:var(--good)}
.kicker--bad{color:var(--bad)}
.ref{font-size:10px;color:var(--mute);border:1px solid var(--line);border-radius:5px;padding:1px 6px;letter-spacing:.06em}
.panel__body h4{font-size:24px;margin:0 0 6px}
.bignum{font-family:"Space Mono",monospace;font-weight:700;font-size:30px;display:block;margin:.1em 0 .2em}
.panel--good .bignum{color:var(--good)} .panel--bad .bignum{color:var(--bad)}
.detail{color:#c6cdda;font-size:17px;margin:.3em 0 1em}
.src{font-family:"Space Mono",monospace;font-size:12.5px;letter-spacing:.04em;color:var(--mute)}
.src:hover{color:var(--ink)}

/* numbers grid */
.numgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
.numcard{position:relative;background:var(--panel);border:1px solid var(--line);border-radius:13px;
  padding:22px 20px 26px;min-height:170px}
.numcard--good{border-left:3px solid var(--good)} .numcard--bad{border-left:3px solid var(--bad)}
.numcard__val{font-family:"Space Mono",monospace;font-weight:700;font-size:34px}
.numcard--good .numcard__val{color:var(--good)} .numcard--bad .numcard__val{color:var(--bad)}
.numcard__lab{font-family:"Fraunces",serif;font-size:19px;margin:.3em 0 .4em}
.numcard__ctx{color:var(--mute);font-size:15px;line-height:1.5;margin:0}
.ref--corner{position:absolute;top:14px;right:14px}
.numnote{margin-top:1.4rem;color:var(--mute);font-family:"Space Mono",monospace;font-size:12.5px;letter-spacing:.06em}

/* values */
.valgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.valcard{background:var(--panel);border:1px solid var(--line);border-radius:13px;padding:24px 22px;position:relative;overflow:hidden}
.valcard__bar{position:absolute;top:0;left:0;right:0;height:3px;background:var(--accent)}
.valcard h4{font-size:25px;margin:.2em 0 .5em;color:var(--ink)}
.valcard p{color:var(--mute);font-size:16px;margin:0}
.caveat{margin-top:1.8rem;color:var(--gold);font-style:italic;font-size:19px}

/* honesty box */
.honesty{background:linear-gradient(180deg,rgba(231,184,107,.07),transparent);
  border:1px solid var(--line);border-left:3px solid var(--gold);border-radius:13px;padding:30px 32px}
.honesty h2{font-size:30px;margin-bottom:1rem}
.honesty ul{margin:0;padding-left:1.1em;color:#c6cdda}
.honesty li{margin:.5em 0}

/* references + credits */
.cols2{columns:2;column-gap:42px}
@media(max-width:760px){.cols2{columns:1}}
.ref-list,.credits-list{list-style:none;padding:0;margin:0;font-size:15px}
.ref-item{break-inside:avoid;display:flex;gap:12px;margin:0 0 1em;color:#c6cdda}
.ref-num{font-family:"Space Mono",monospace;color:var(--gold);min-width:1.6em}
.ref-txt em{color:var(--mute)}
.credits-list li{break-inside:avoid;margin:.45em 0;color:#c6cdda}
.credits-list b{color:var(--ink);font-family:"Space Mono",monospace;font-size:13px;font-weight:700}

/* footer */
.foot{padding:7vh 0 9vh;color:var(--mute);font-size:15px}
.foot .big{font-family:"Fraunces",serif;font-size:30px;color:var(--ink);margin-bottom:.3em}
.foot a{color:var(--good)}

/* reveal */
.reveal{opacity:0;transform:translateY(24px);transition:opacity .7s ease,transform .7s ease}
.reveal.in{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){.reveal{opacity:1;transform:none;transition:none}}

@media(max-width:860px){
  body{font-size:18px}
  .split{grid-template-columns:1fr}
  .numgrid{grid-template-columns:repeat(2,1fr)}
  .valgrid{grid-template-columns:1fr}
  .hero{padding:12vh 0 7vh}
}
"""

JS = r"""
const io=new IntersectionObserver((es)=>{es.forEach(e=>{if(e.isIntersecting)e.target.classList.add('in')})},{threshold:.12});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
// play videos only while on screen (autoplay+muted+loop set inline)
const vo=new IntersectionObserver((es)=>{es.forEach(e=>{const v=e.target;
  if(e.isIntersecting){v.play&&v.play().catch(()=>{});}else{v.pause&&v.pause();}})},{threshold:.35});
document.querySelectorAll('video').forEach(v=>vo.observe(v));
"""


def build():
    F, T, B = D.FRAMING, D.THESIS, D.BOOK
    authors = " · ".join(B["authors"])
    s1 = SCENE_BY_KEY["framing"]; s2 = SCENE_BY_KEY["ledger"]
    s3 = SCENE_BY_KEY["numbers"]; s4 = SCENE_BY_KEY["values"]; s5 = SCENE_BY_KEY["thesis"]
    domains_html = "\n".join(domain_block(d, i + 1) for i, d in enumerate(D.DOMAINS))

    head = f'''<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Moral AI — a visual companion to the Introduction</title>
<meta name="description" content="An animated, source-checked visual companion to the Introduction of &quot;Moral AI and How We Get There&quot; by Schaich Borg, Sinnott-Armstrong & Conitzer.">
<meta property="og:title" content="Moral AI — a visual companion">
<meta property="og:description" content="The same technology, two faces: eleven domains of AI good news and bad news, with the book's own sources.">
<meta property="og:type" content="website">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;1,9..144,400&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>'''

    hero = f'''
<header class="hero"><div class="seam"></div><div class="wrap">
  <p class="eyebrow">Visual companion · Introduction</p>
  <h1>Moral AI</h1>
  <p class="sub">{esc(B["subtitle"])}</p>
  <p class="q">“{esc(F["verdict_question"])}”<br>Our answer is: <span class="both">both.</span></p>
  <div class="meta">
    <span class="badge">{esc(authors)}</span>
    <span class="badge">{esc(B["publisher"])}, {esc(B["year"])}</span>
    <span class="badge">Introduction · pp. {esc(B["pages"])}</span>
  </div>
</div></header>'''

    framing = f'''
<section class="section" id="framing"><div class="wrap">
  <div class="section__head"><span class="eyebrow">{esc(s1[2])}</span><h2>What’s the problem?</h2></div>
  <p class="lead">{esc(F["verdict_gloss"])}</p>
  {video_block(s1[0], s1[2], s1[3])}
</div></section>'''

    ledger_intro = f'''
<section class="section" id="ledger"><div class="wrap">
  <div class="section__head"><span class="eyebrow">{esc(s2[2])}</span><h2>The same technology, two faces</h2></div>
  <p class="lead">{esc(s2[3])}</p>
  {video_block(s2[0], s2[2], s2[3])}
  {domains_html}
</div></section>'''

    numbers = f'''
<section class="section" id="numbers"><div class="wrap">
  <div class="section__head"><span class="eyebrow">{esc(s3[2])}</span><h2>By the numbers</h2></div>
  <p class="lead">{esc(s3[3])}</p>
  <div class="numgrid">{numbers_block()}</div>
  <p class="numnote">// different units — shown for scale of the stakes, never as a single ranking</p>
  {video_block(s3[0], s3[2], s3[3])}
</div></section>'''

    values = f'''
<section class="section" id="values"><div class="wrap">
  <div class="section__head"><span class="eyebrow">{esc(s4[2])}</span><h2>Six moral values at stake</h2></div>
  <div class="valgrid">{values_block()}</div>
  <p class="caveat">“{esc(D.VALUES_CAVEAT)}”</p>
  {video_block(s4[0], s4[2], s4[3])}
</div></section>'''

    thesis = f'''
<section class="section" id="thesis"><div class="wrap">
  <div class="section__head"><span class="eyebrow">{esc(s5[2])}</span><h2>Keep the baby, lose the bathwater</h2></div>
  <p class="lead">{esc(T["not_underestimate"])} {esc(T["not_overestimate"])} {esc(T["balance"])}</p>
  {video_block(s5[0], s5[2], s5[3])}
  <p class="q" style="font-size:clamp(24px,3.6vw,40px);margin-top:2.4rem;max-width:26ch">
    “{esc(T["baby_bathwater"])}”</p>
</div></section>'''

    honesty = f'''
<section class="section"><div class="wrap"><div class="honesty reveal">
  <h2>What we do <em>not</em> claim</h2>
  <ul>{not_claim_block()}</ul>
</div></div></section>'''

    refs = f'''
<section class="section" id="references"><div class="wrap">
  <div class="section__head"><span class="eyebrow">Provenance</span><h2>References</h2></div>
  <p class="lead">The sources the authors cite in the Introduction (notes 1–23). The book reports these cases; we link what it cites.</p>
  <ol class="ref-list cols2" style="margin-top:1.6rem">{references_block()}</ol>
</div></section>'''

    credits = f'''
<section class="section" id="credits"><div class="wrap">
  <div class="section__head"><span class="eyebrow">Image credits</span><h2>Representative images</h2></div>
  <p class="lead">Freely-licensed photographs (Wikimedia Commons). Unless noted, they illustrate the domain rather than the exact event.</p>
  <ul class="credits-list cols2" style="margin-top:1.4rem">{credits_block()}</ul>
</div></section>'''

    foot = f'''
<footer class="foot"><div class="wrap">
  <p class="big">Moral AI <span style="color:var(--mute);font-size:.7em">— {esc(B["subtitle"])}</span></p>
  <p>A visual companion to the Introduction (“What’s the Problem?”) of the book by {esc(authors)} ·
     {esc(B["publisher"])}, {esc(B["year"])} · ISBN {esc(B["isbn"])}.</p>
  <p>Every figure, name and quotation is transcribed from the book. Animations hand-authored in Manim CE.
     Renderer based on <a href="https://github.com/HarleyCoops/Math-To-Manim" target="_blank" rel="noopener">Math-To-Manim</a>.</p>
  <p style="margin-top:1.2em;color:#6b7488">Staging build · not affiliated with or endorsed by the authors or publisher.</p>
</div></footer>'''

    return (head + hero + framing + ledger_intro + numbers + values + thesis
            + honesty + refs + credits + foot
            + f"<script>{JS}</script></body></html>")


if __name__ == "__main__":
    html_out = build()
    out = os.path.join(HERE, "index.html")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(html_out)
    imgs = len([1 for d in D.DOMAINS for t in ("good", "bad") if credit(f'{d["key"]}_{t}')])
    vids = len([1 for s in SCENES if has_video(s[0])])
    print(f"wrote {out}  ({len(html_out)//1024} KB)")
    print(f"images embedded: {imgs}/22   scene videos present: {vids}/5")
