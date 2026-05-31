#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fetch FREELY-LICENSED, representative images from Wikimedia Commons.

Only images with a free license (CC0 / Public domain / CC-BY / CC-BY-SA) and a
raster mime (jpeg/png) are considered. Each downloaded file gets a sidecar
<case>.json with full attribution so the website can credit it correctly.

Usage:
  list candidates (JSON to stdout):
    python3 tools/commons_fetch.py list  --query "Tesla Model S car" --limit 12
  download a chosen file (by --pageid or --title), write <case>.jpg + <case>.json:
    python3 tools/commons_fetch.py get   --case transportation_bad \
        --out site_media/images --pageid 12345
  search + auto-pick best + download in one shot:
    python3 tools/commons_fetch.py auto  --case transportation_bad \
        --out site_media/images --query "Tesla Model S car" --query "Tesla Model S"
"""
import argparse, json, os, re, sys, urllib.parse, urllib.request, html

API = "https://commons.wikimedia.org/w/api.php"
UA = "moral-ai-viz/1.0 (https://github.com/ivan-gentile/moral-ai-viz; ivopuntogentile@gmail.com)"
FREE_HINTS = ("cc0", "cc-zero", "public domain", "pd-", "cc by", "cc-by",
              "attribution-share", "creativecommons")
RASTER = ("image/jpeg", "image/png")


def _req(url):
    r = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(r, timeout=40) as resp:
        return resp.read()


def _strip(htmltext):
    if not htmltext:
        return ""
    t = re.sub(r"<[^>]+>", "", htmltext)
    return html.unescape(t).strip()


def _is_free(lic):
    l = (lic or "").lower()
    return any(h in l for h in FREE_HINTS)


def search(query, limit=12, thumbw=1280):
    params = {
        "action": "query", "format": "json", "generator": "search",
        "gsrnamespace": "6", "gsrsearch": query, "gsrlimit": str(limit),
        "prop": "imageinfo",
        "iiprop": "url|size|mime|extmetadata", "iiurlwidth": str(thumbw),
    }
    url = API + "?" + urllib.parse.urlencode(params)
    data = json.loads(_req(url).decode("utf-8", "replace"))
    pages = (data.get("query") or {}).get("pages") or {}
    out = []
    for p in pages.values():
        ii = (p.get("imageinfo") or [None])[0]
        if not ii:
            continue
        ext = ii.get("extmetadata") or {}
        def f(k):
            return _strip((ext.get(k) or {}).get("value", ""))
        lic = f("LicenseShortName")
        out.append({
            "pageid": p.get("pageid"),
            "index": p.get("index", 999),
            "title": p.get("title", ""),
            "mime": ii.get("mime", ""),
            "width": ii.get("width", 0),
            "height": ii.get("height", 0),
            "license": lic,
            "license_url": f("LicenseUrl"),
            "artist": f("Artist") or f("Credit"),
            "description": f("ImageDescription")[:240],
            "thumburl": ii.get("thumburl") or ii.get("url"),
            "url": ii.get("url"),
            "descriptionurl": ii.get("descriptionurl", ""),
            "free": _is_free(lic),
        })
    out.sort(key=lambda c: c["index"])
    return out


def rank(cands):
    def score(c):
        s = 0
        if c["free"]:
            s += 1000
        if c["mime"] in RASTER:
            s += 500
        lic = c["license"].lower()
        if "cc0" in lic or "public domain" in lic or "pd" == lic[:2]:
            s += 60
        if c["width"] >= 1000:
            s += 40
        elif c["width"] >= 700:
            s += 20
        bad = ("logo", "icon", "seal", "coat of arms", ".svg")
        if any(b in c["title"].lower() for b in bad):
            s -= 120
        return s
    return sorted(cands, key=score, reverse=True)


def usable(cands):
    return [c for c in rank(cands) if c["free"] and c["mime"] in RASTER and c["thumburl"]]


def download(cand, case, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    ext = ".png" if cand["mime"] == "image/png" else ".jpg"
    fpath = os.path.join(out_dir, case + ext)
    raw = _req(cand["thumburl"])
    with open(fpath, "wb") as fh:
        fh.write(raw)
    meta = {
        "case": case,
        "file": os.path.basename(fpath),
        "title": cand["title"],
        "artist": cand["artist"],
        "license": cand["license"],
        "license_url": cand["license_url"],
        "source_url": cand["descriptionurl"],
        "width": cand["width"], "height": cand["height"],
        "bytes": len(raw),
    }
    with open(os.path.join(out_dir, case + ".json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=2)
    return meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["list", "get", "auto"])
    ap.add_argument("--case", default="")
    ap.add_argument("--out", default="site_media/images")
    ap.add_argument("--query", action="append", default=[])
    ap.add_argument("--pageid", type=int, default=0)
    ap.add_argument("--title", default="")
    ap.add_argument("--limit", type=int, default=12)
    a = ap.parse_args()

    try:
        if a.mode == "list":
            cands = usable(search(a.query[0], a.limit)) if a.query else []
            print(json.dumps(cands, ensure_ascii=False, indent=2))
            return
        if a.mode == "get":
            for q in (a.query or [""]):
                cands = search(q, a.limit) if q else []
                pick = None
                for c in usable(cands):
                    if a.pageid and c["pageid"] == a.pageid:
                        pick = c; break
                    if a.title and a.title.lower() in c["title"].lower():
                        pick = c; break
                if pick:
                    print(json.dumps({"status": "ok", **download(pick, a.case, a.out)},
                                     ensure_ascii=False)); return
            print(json.dumps({"status": "none", "case": a.case})); return
        if a.mode == "auto":
            for q in a.query:
                cands = usable(search(q, a.limit))
                if cands:
                    meta = download(cands[0], a.case, a.out)
                    print(json.dumps({"status": "ok", "query_used": q, **meta},
                                     ensure_ascii=False)); return
            print(json.dumps({"status": "none", "case": a.case})); return
    except Exception as e:
        print(json.dumps({"status": "error", "case": a.case, "error": str(e)}))
        sys.exit(0)


if __name__ == "__main__":
    main()
