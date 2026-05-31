#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate the self-contained companion pages from the source-of-truth modules:
  English -> ./index.html        (videos in site_media/en/)
  Italian -> ./it/index.html     (videos in site_media/it/, Italian sources overlaid)

  python3 build_site.py            # builds both languages

The page never invents text: prose comes from intro_data[_it].py. Images are
shared (site_media/images/, language-neutral). Missing images degrade to a tile.
"""
import html, importlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "scenes"))
IMG_DIR = os.path.join(HERE, "site_media", "images")
MEDIA = os.path.join(HERE, "site_media")
IT_SRC = os.path.join(MEDIA, "it_sources")

# globals set per-language by build()
D = None
LANG = "en"
BASE = ""        # relative prefix to repo root assets ("" for en, "../" for it)


def esc(s):
    return html.escape(str(s), quote=True)


def credit(case_id):
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
        "src": BASE + "site_media/images/" + f,
        "artist": m.get("artist", "").strip() or "Wikimedia Commons",
        "license": m.get("license", "").strip() or "see source",
        "license_url": m.get("license_url", "").strip(),
        "source_url": m.get("source_url", "").strip(),
    }


def it_source(case_id):
    """Italian-language source overlay produced by the workflow (it only)."""
    j = os.path.join(IT_SRC, case_id + ".json")
    if not os.path.exists(j):
        return None
    try:
        m = json.load(open(j, encoding="utf-8"))
    except Exception:
        return None
    if m.get("found") and m.get("url"):
        return {"pub": m.get("pub", ""), "title": m.get("title", ""),
                "url": m["url"], "date": m.get("date", "")}
    return None


def has_video(cls):
    return os.path.exists(os.path.join(MEDIA, LANG, cls + ".mp4"))


def video_block(cls, blurb):
    if not has_video(cls):
        return (f'<div class="vid vid--missing"><span>video</span>'
                f'<p>{esc(blurb)}</p></div>')
    return (
        f'<figure class="vid reveal">'
        f'<video playsinline preload="metadata" controls autoplay loop muted '
        f'src="{BASE}site_media/{LANG}/{esc(cls)}.mp4"></video>'
        f'<figcaption>{esc(blurb)}</figcaption></figure>'
    )


def img_or_tile(case_id, tone, headline):
    c = credit(case_id)
    if not c:
        cls = "tile tile--good" if tone == "good" else "tile tile--bad"
        return f'<div class="{cls}"><span>{esc(headline)}</span></div>'
    if c["license_url"] or c["source_url"]:
        link = c["license_url"] or c["source_url"]
        cap = (f'<a href="{esc(link)}" target="_blank" rel="noopener">'
               f'{esc(c["artist"])} · {esc(c["license"])}</a>')
    else:
        cap = f'{esc(c["artist"])} · {esc(c["license"])}'
    return (f'<figure class="ph"><img loading="lazy" '
            f'alt="{esc(headline)}" src="{esc(c["src"])}">'
            f'<figcaption class="credit">{cap}</figcaption></figure>')


def side_panel(dom, tone):
    side = dom[tone]
    case_id = f'{dom["key"]}_{tone}'
    kicker = D.UI["good_news"] if tone == "good" else D.UI["bad_news"]
    imghtml = img_or_tile(case_id, tone, side["head"])
    src = side["source"]
    if LANG == "it":
        ov = it_source(case_id)
        if ov:
            src = ov
    srcbits = esc(src["pub"]) + (" · " + esc(src["date"]) if src.get("date") else "")
    num = side.get("number")
    numhtml = f'<span class="bignum">{esc(num)}</span>' if num else ""
    return f'''
      <article class="panel panel--{tone}">
        {imghtml}
        <div class="panel__body">
          <p class="kicker kicker--{tone}">{esc(kicker)}<span class="ref">{esc(D.UI["ref"])}&nbsp;{esc(side["fn"])}</span></p>
          <h4>{esc(side["head"])}</h4>
          {numhtml}
          <p class="detail">{esc(side["detail"])}</p>
          <a class="src" href="{esc(src["url"])}" target="_blank" rel="noopener">{esc(D.UI["source"])}: {srcbits} <span aria-hidden="true">↗</span></a>
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
    out = []
    for n in D.NUMBERS:
        tone = n.get("tone", "bad")
        out.append(f'''
        <div class="numcard numcard--{tone} reveal">
          <div class="numcard__val">{esc(n["value"])}</div>
          <div class="numcard__lab">{esc(n["label"])}</div>
          <p class="numcard__ctx">{esc(n["context"])}</p>
          <span class="ref ref--corner">{esc(D.UI["ref"])}&nbsp;{esc(n["fn"])}</span>
        </div>''')
    return "\n".join(out)


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
    short = {"good": D.PAGE["good_label_short"], "bad": D.PAGE["bad_label_short"]}
    for dom in D.DOMAINS:
        for tone in ("good", "bad"):
            s = dom[tone]["source"]
            fn = dom[tone]["fn"]
            extra = ""
            if LANG == "it":
                ov = it_source(f'{dom["key"]}_{tone}')
                if ov:
                    extra = (f' · <a href="{esc(ov["url"])}" target="_blank" '
                             f'rel="noopener">IT: {esc(ov["pub"])} ↗</a>')
            if (fn, s["url"]) in seen:
                continue
            seen.add((fn, s["url"]))
            datebit = f' ({esc(s["date"])})' if s.get("date") else ""
            rows.append((fn, f'''
        <li class="ref-item">
          <span class="ref-num">{esc(fn)}</span>
          <span class="ref-txt"><strong>{esc(dom["title"])} — {esc(short[tone])}.</strong>
          {esc(s["title"])}. <em>{esc(s["pub"])}</em>{datebit}.
          <a href="{esc(s["url"])}" target="_blank" rel="noopener">link ↗</a>{extra}</span>
        </li>'''))
    rows.sort(key=lambda r: r[0])
    return "\n".join(r[1] for r in rows)


def credits_block():
    items = []
    for dom in D.DOMAINS:
        for tone in ("good", "bad"):
            c = credit(f'{dom["key"]}_{tone}')
            if not c:
                continue
            link = c["source_url"] or c["license_url"]
            label = f'{c["artist"]} — {c["license"]}'
            inner = (f'<a href="{esc(link)}" target="_blank" rel="noopener">{esc(label)}</a>'
                     if link else esc(label))
            items.append(f'<li><b>{esc(dom["title"])} / {esc(tone)}:</b> {inner}</li>')
    return "\n".join(items) if items else "<li>—</li>"


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
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:"Newsreader",Georgia,serif;font-size:19px;line-height:1.65;
  -webkit-font-smoothing:antialiased;overflow-x:hidden}
body::before{content:"";position:fixed;inset:0;z-index:-2;pointer-events:none;
  background:radial-gradient(60vw 60vw at 8% -6%, rgba(90,200,168,.12), transparent 60%),
             radial-gradient(55vw 55vw at 100% 105%, rgba(224,115,107,.12), transparent 60%)}
body::after{content:"";position:fixed;inset:0;z-index:-1;pointer-events:none;opacity:.035;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}
a{color:var(--good);text-decoration:none}
a:hover{text-decoration:underline}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 24px}
h1,h2,h3,h4{font-family:"Fraunces",Georgia,serif;font-weight:600;line-height:1.05;margin:0}
.eyebrow{font-family:"Space Mono",monospace;font-size:13px;letter-spacing:.22em;
  text-transform:uppercase;color:var(--mute)}

/* language bar */
.langbar{position:absolute;top:22px;right:24px;z-index:3}
.langbar a{font-family:"Space Mono",monospace;font-size:12px;letter-spacing:.1em;
  text-transform:uppercase;color:var(--mute);border:1px solid var(--line);
  border-radius:999px;padding:7px 14px}
.langbar a:hover{color:var(--ink);border-color:var(--mute);text-decoration:none}

/* hero */
.hero{position:relative;padding:16vh 0 8vh;border-bottom:1px solid var(--line);overflow:hidden}
.hero .seam{position:absolute;top:0;bottom:0;left:50%;width:1px;
  background:linear-gradient(var(--good),var(--bad));opacity:.22}
.hero h1{font-size:clamp(56px,12vw,150px);letter-spacing:-.02em;font-optical-sizing:auto}
.hero .sub{font-size:clamp(20px,2.6vw,30px);color:var(--mute);margin-top:.3em;
  font-family:"Fraunces",serif;font-style:italic}
.hero .byline{font-family:"Space Mono",monospace;font-size:13.5px;letter-spacing:.04em;
  color:var(--mute);margin:.9em 0 0}
.attrib{max-width:60ch;margin:1.8rem 0 0;border-left:2px solid var(--gold);
  padding:.2rem 0 .2rem 18px}
.attrib p{margin:.35em 0;font-size:18px;color:#c6cdda}
.attrib .muted{color:var(--mute);font-size:15px}
.readbook{display:inline-block;margin-top:.6rem;font-family:"Space Mono",monospace;
  font-size:13px;letter-spacing:.05em;border:1px solid var(--good);border-radius:8px;
  padding:8px 14px;color:var(--good)}
.readbook:hover{background:rgba(90,200,168,.1);text-decoration:none}
.hero .q{margin-top:2.4rem;font-size:clamp(22px,3vw,34px);max-width:24ch}
.both{background:linear-gradient(92deg,var(--good),var(--gold) 45%,var(--bad));
  -webkit-background-clip:text;background-clip:text;color:transparent;font-weight:600}

/* sections */
.section{padding:8vh 0;border-bottom:1px solid var(--line)}
.section__head{display:flex;align-items:baseline;gap:20px;margin-bottom:2.2rem;flex-wrap:wrap}
.section h2{font-size:clamp(34px,5.5vw,60px);letter-spacing:-.01em}
.lead{color:var(--mute);max-width:62ch;font-size:21px}

.vid{margin:2.4rem 0 0;border-radius:14px;overflow:hidden;border:1px solid var(--line);
  background:var(--bg2);box-shadow:0 24px 60px -28px rgba(0,0,0,.8)}
.vid video{display:block;width:100%;height:auto;background:var(--bg2)}
.vid figcaption{padding:13px 18px;color:var(--mute);font-size:15px;border-top:1px solid var(--line)}
.vid--missing{padding:46px;text-align:center;color:var(--mute)}
.vid--missing span{font-family:"Space Mono",monospace;font-size:12px;letter-spacing:.2em;text-transform:uppercase}

.domain{padding:5vh 0;border-bottom:1px dashed var(--line)}
.domain:last-child{border-bottom:none}
.domain__head{display:flex;align-items:center;gap:18px;margin-bottom:1.6rem}
.domain__idx{font-family:"Space Mono",monospace;color:var(--gold);font-size:15px}
.domain__head h3{font-size:clamp(28px,4vw,44px)}
.domain__rule{flex:1;height:1px;background:var(--line)}
.split{display:grid;grid-template-columns:1fr 1fr;gap:22px}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:14px;overflow:hidden;
  display:flex;flex-direction:column;transition:transform .35s ease,border-color .35s ease}
.panel:hover{transform:translateY(-4px)}
.panel--good{border-top:3px solid var(--good)} .panel--good:hover{border-color:var(--good)}
.panel--bad{border-top:3px solid var(--bad)} .panel--bad:hover{border-color:var(--bad)}
.ph{margin:0;position:relative;aspect-ratio:16/10;overflow:hidden;background:var(--panel2)}
.ph img{width:100%;height:100%;object-fit:cover;display:block;
  transition:transform .6s ease,filter .6s ease;filter:saturate(.92)}
.panel:hover .ph img{transform:scale(1.05);filter:saturate(1.05)}
.ph .credit{position:absolute;right:8px;bottom:8px;margin:0;font-family:"Space Mono",monospace;
  font-size:10.5px;color:#cfd6e2;background:rgba(8,10,14,.66);backdrop-filter:blur(3px);
  padding:3px 8px;border-radius:6px;max-width:78%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.ph .credit a{color:#cfd6e2}
.tile{aspect-ratio:16/10;display:flex;align-items:center;justify-content:center;padding:22px;text-align:center}
.tile span{font-family:"Fraunces",serif;font-size:26px}
.tile--good{background:linear-gradient(135deg,rgba(90,200,168,.16),rgba(90,200,168,.04));color:var(--good)}
.tile--bad{background:linear-gradient(135deg,rgba(224,115,107,.16),rgba(224,115,107,.04));color:var(--bad)}
.panel__body{padding:18px 20px 20px}
.kicker{font-family:"Space Mono",monospace;font-size:12px;letter-spacing:.16em;text-transform:uppercase;
  display:flex;align-items:center;gap:10px;margin:0 0 8px}
.kicker--good{color:var(--good)} .kicker--bad{color:var(--bad)}
.ref{font-size:10px;color:var(--mute);border:1px solid var(--line);border-radius:5px;padding:1px 6px;letter-spacing:.06em}
.panel__body h4{font-size:24px;margin:0 0 6px}
.bignum{font-family:"Space Mono",monospace;font-weight:700;font-size:30px;display:block;margin:.1em 0 .2em}
.panel--good .bignum{color:var(--good)} .panel--bad .bignum{color:var(--bad)}
.detail{color:#c6cdda;font-size:17px;margin:.3em 0 1em}
.src{font-family:"Space Mono",monospace;font-size:12.5px;letter-spacing:.02em;color:var(--mute)}
.src:hover{color:var(--ink)}

.numgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
.numcard{position:relative;background:var(--panel);border:1px solid var(--line);border-radius:13px;
  padding:22px 20px 26px;min-height:172px}
.numcard--good{border-left:3px solid var(--good)} .numcard--bad{border-left:3px solid var(--bad)}
.numcard__val{font-family:"Space Mono",monospace;font-weight:700;font-size:33px}
.numcard--good .numcard__val{color:var(--good)} .numcard--bad .numcard__val{color:var(--bad)}
.numcard__lab{font-family:"Fraunces",serif;font-size:19px;margin:.3em 0 .4em}
.numcard__ctx{color:var(--mute);font-size:15px;line-height:1.5;margin:0}
.ref--corner{position:absolute;top:14px;right:14px}
.numnote{margin-top:1.4rem;color:var(--mute);font-family:"Space Mono",monospace;font-size:12.5px;letter-spacing:.06em}

.valgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.valcard{background:var(--panel);border:1px solid var(--line);border-radius:13px;padding:24px 22px;position:relative;overflow:hidden}
.valcard__bar{position:absolute;top:0;left:0;right:0;height:3px;background:var(--accent)}
.valcard h4{font-size:25px;margin:.2em 0 .5em;color:var(--ink)}
.valcard p{color:var(--mute);font-size:16px;margin:0}
.caveat{margin-top:1.8rem;color:var(--gold);font-style:italic;font-size:19px}

.honesty{background:linear-gradient(180deg,rgba(231,184,107,.07),transparent);
  border:1px solid var(--line);border-left:3px solid var(--gold);border-radius:13px;padding:30px 32px}
.honesty h2{font-size:30px;margin-bottom:1rem}
.honesty ul{margin:0;padding-left:1.1em;color:#c6cdda}
.honesty li{margin:.5em 0}

.cols2{columns:2;column-gap:42px}
@media(max-width:760px){.cols2{columns:1}}
.ref-list,.credits-list{list-style:none;padding:0;margin:0;font-size:15px}
.ref-item{break-inside:avoid;display:flex;gap:12px;margin:0 0 1em;color:#c6cdda}
.ref-num{font-family:"Space Mono",monospace;color:var(--gold);min-width:1.6em}
.ref-txt em{color:var(--mute)}
.credits-list li{break-inside:avoid;margin:.45em 0;color:#c6cdda}
.credits-list b{color:var(--ink);font-family:"Space Mono",monospace;font-size:13px;font-weight:700}

.foot{padding:7vh 0 9vh;color:var(--mute);font-size:15px}
.foot .big{font-family:"Fraunces",serif;font-size:30px;color:var(--ink);margin-bottom:.3em}
.foot a{color:var(--good)}

.reveal{transition:opacity .7s ease,transform .7s ease}
body.anim .reveal{opacity:0;transform:translateY(24px)}
body.anim .reveal.in{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){body.anim .reveal{opacity:1;transform:none;transition:none}}

@media(max-width:860px){
  body{font-size:18px}
  .split{grid-template-columns:1fr}
  .numgrid{grid-template-columns:repeat(2,1fr)}
  .valgrid{grid-template-columns:1fr}
  .hero{padding:13vh 0 7vh}
}
"""

JS = r"""
(function(){
  var rm = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  try{
    if(!rm && 'IntersectionObserver' in window){
      document.body.classList.add('anim');
      var io=new IntersectionObserver(function(es){es.forEach(function(e){
        if(e.isIntersecting) e.target.classList.add('in');});},
        {threshold:.12, rootMargin:'0px 0px -8% 0px'});
      document.querySelectorAll('.reveal').forEach(function(el){io.observe(el);});
    }
  }catch(e){ document.body.classList.remove('anim'); }
  try{
    if('IntersectionObserver' in window){
      var vo=new IntersectionObserver(function(es){es.forEach(function(e){var v=e.target;
        if(e.isIntersecting){ v.play && v.play().catch(function(){}); } else { v.pause && v.pause(); }});},
        {threshold:.35});
      document.querySelectorAll('video').forEach(function(v){vo.observe(v);});
    }
  }catch(e){}
})();
"""


def build():
    B, A, P = D.BOOK, D.ATTRIBUTION, D.PAGE
    F, T = D.FRAMING, D.THESIS
    authors = " · ".join(B["authors"])
    isbn = B["isbn"].replace("-", "")
    book_url = f"https://books.google.com/books?vid=ISBN{isbn}"
    ST = D.SCENE_TITLES
    blurbs = P["blurbs"]
    domains_html = "\n".join(domain_block(d, i + 1) for i, d in enumerate(D.DOMAINS))
    htmllang = "it" if LANG == "it" else "en"

    head = f'''<!doctype html><html lang="{htmllang}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Moral AI — {esc(A["kicker"])}</title>
<meta name="description" content="{esc(A["kicker"])} Moral AI and How We Get There ({esc(authors)}).">
<meta property="og:title" content="Moral AI — {esc(B["section"])}">
<meta property="og:description" content="{esc(A["selection"])}">
<meta property="og:type" content="website">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;1,9..144,400&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>'''

    hero = f'''
<header class="hero"><div class="seam"></div>
  <nav class="langbar"><a href="{esc(D.OTHER_LANG_HREF)}">{esc(D.OTHER_LANG_LABEL)} ↔</a></nav>
  <div class="wrap">
    <p class="eyebrow">{esc(A["kicker"])}</p>
    <h1>Moral AI</h1>
    <p class="sub">{esc(B["subtitle"])}</p>
    <p class="byline">{esc(authors)} · {esc(B["publisher"])}, {esc(B["year"])} · {esc(B["section"])}</p>
    <div class="attrib">
      <p>{esc(A["selection"])}</p>
      <p>{esc(A["method"])}</p>
      <p class="muted">{esc(A["not_affiliated"])}</p>
      <a class="readbook" href="{esc(book_url)}" target="_blank" rel="noopener">{esc(A["read_the_book"])} ↗</a>
    </div>
    <p class="q">{esc(F["verdict_question"])}<br>{esc(F["verdict_pre"])} <span class="both">{esc(F["verdict"])}</span></p>
  </div>
</header>'''

    def sec(key, body_html):
        return f'''
<section class="section" id="{key}"><div class="wrap">
  <div class="section__head"><span class="eyebrow">{esc(ST[key]["eyebrow"])}</span><h2>{esc(ST[key]["title"])}</h2></div>
  <p class="lead">{esc(blurbs[key])}</p>
  {body_html}
</div></section>'''

    framing = sec("framing", video_block("Framing", blurbs["framing"]))
    ledger = sec("ledger", video_block("DoubleEdgedLedger", blurbs["ledger"]) + domains_html)
    numbers = sec("numbers",
                  f'<div class="numgrid">{numbers_block()}</div>'
                  f'<p class="numnote">// {esc(D.STRINGS["numbers_note"])}</p>'
                  + video_block("ByTheNumbers", blurbs["numbers"]))
    values = sec("values",
                 f'<div class="valgrid">{values_block()}</div>'
                 f'<p class="caveat">{esc(D.VALUES_CAVEAT)}</p>'
                 + video_block("SixValues", blurbs["values"]))
    thesis = sec("thesis",
                 video_block("BabyAndBathwater", blurbs["thesis"])
                 + f'<p class="q" style="font-size:clamp(24px,3.6vw,40px);margin-top:2.2rem;max-width:30ch">{esc(T["baby_bathwater"])}</p>')

    honesty = f'''
<section class="section"><div class="wrap"><div class="honesty reveal">
  <h2>{esc(P["notclaim_pre"])}<em>{esc(P["notclaim_em"])}</em>{esc(P["notclaim_post"])}</h2>
  <ul>{not_claim_block()}</ul>
</div></div></section>'''

    refs = f'''
<section class="section" id="references"><div class="wrap">
  <div class="section__head"><span class="eyebrow">{esc(P["references_eyebrow"])}</span><h2>{esc(P["references_h"])}</h2></div>
  <p class="lead">{esc(P["references_lead"])}</p>
  <ol class="ref-list cols2" style="margin-top:1.6rem">{references_block()}</ol>
</div></section>'''

    credits = f'''
<section class="section" id="credits"><div class="wrap">
  <div class="section__head"><span class="eyebrow">{esc(P["credits_eyebrow"])}</span><h2>{esc(P["credits_h"])}</h2></div>
  <p class="lead">{esc(P["credits_lead"])}</p>
  <ul class="credits-list cols2" style="margin-top:1.4rem">{credits_block()}</ul>
</div></section>'''

    foot = f'''
<footer class="foot"><div class="wrap">
  <p class="big">Moral AI <span style="color:var(--mute);font-size:.7em">— {esc(B["subtitle"])}</span></p>
  <p>{esc(P["footer_companion"])} {esc(authors)} · {esc(B["publisher"])}, {esc(B["year"])} · ISBN {esc(B["isbn"])}.
     <a href="{esc(book_url)}" target="_blank" rel="noopener">{esc(A["read_the_book"])} ↗</a></p>
  <p>{esc(P["footer_method"])} <a href="https://github.com/HarleyCoops/Math-To-Manim" target="_blank" rel="noopener">Math-To-Manim</a>.</p>
  <p style="margin-top:1.2em;color:#6b7488">{esc(P["footer_staging"])}</p>
</div></footer>'''

    return (head + hero + framing + ledger + numbers + values + thesis
            + honesty + refs + credits + foot
            + f"<script>{JS}</script></body></html>")


def build_lang(lang):
    global D, LANG, BASE
    LANG = lang
    BASE = "" if lang == "en" else "../"
    D = importlib.import_module("intro_data" if lang == "en" else "intro_data_it")
    out = os.path.join(HERE, "index.html") if lang == "en" else os.path.join(HERE, "it", "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    html_out = build()
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(html_out)
    imgs = sum(1 for d in D.DOMAINS for t in ("good", "bad") if credit(f'{d["key"]}_{t}'))
    vids = sum(1 for c in ("Framing", "DoubleEdgedLedger", "ByTheNumbers", "SixValues", "BabyAndBathwater") if has_video(c))
    its = 0
    if lang == "it":
        its = sum(1 for d in D.DOMAINS for t in ("good", "bad") if it_source(f'{d["key"]}_{t}'))
    print(f"[{lang}] wrote {out}  ({len(html_out)//1024} KB) · images {imgs}/22 · videos {vids}/5"
          + (f" · IT sources {its}/22" if lang == "it" else ""))


if __name__ == "__main__":
    build_lang("en")
    build_lang("it")
