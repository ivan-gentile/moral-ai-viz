#!/usr/bin/env bash
# Publish the bilingual visual companion to GitHub Pages (staging).
# Run AFTER scenes are rendered (EN+IT) and Italian sources gathered.
set -euo pipefail

OWNER="${OWNER:-ivan-gentile}"
REPO="${REPO:-moral-ai-viz}"
DESC="Animated visual companion (EN/IT) to the Introduction of 'Moral AI and How We Get There'"

cd "$(dirname "$0")"
shopt -s nullglob

echo "### 1/6 Stage per-language mp4s + regenerate both pages"
mkdir -p site_media/en site_media/it
for mp4 in media_en/videos/*/720p30/*.mp4; do cp -f "$mp4" "site_media/en/$(basename "$mp4")"; done
for mp4 in media_it/videos/*/720p30/*.mp4; do cp -f "$mp4" "site_media/it/$(basename "$mp4")"; done
python3 build_site.py

echo "### 2/6 git commit on main"
if [ ! -d .git ]; then git init -q && git checkout -q -b main; fi
git add -A
git commit -q -m "Bilingual EN/IT companion: clearer book citation, reduced verbatim, Italian sources" || echo "(nothing to commit)"

echo "### 3/6 create/push repo (main)"
if ! gh repo view "$OWNER/$REPO" >/dev/null 2>&1; then
  gh repo create "$REPO" --public --source=. --remote=origin --push --description "$DESC"
else
  git remote get-url origin >/dev/null 2>&1 || git remote add origin "https://github.com/$OWNER/$REPO.git"
  git push -q -u origin main
fi

echo "### 4/6 publish orphan gh-pages (site at root, incl. it/)"
git branch -D gh-pages 2>/dev/null || true
git checkout -q --orphan gh-pages
git rm -rq --cached . >/dev/null 2>&1 || true
touch .nojekyll
git add -f index.html it site_media .nojekyll
git commit -q -m "Publish bilingual site (gh-pages)"
git push -q -u origin gh-pages --force
git checkout -qf main

echo "### 5/6 ensure Pages enabled (gh-pages /)"
gh api -X POST "repos/$OWNER/$REPO/pages" -f 'source[branch]=gh-pages' -f 'source[path]=/' \
  >/dev/null 2>&1 || echo "(Pages already enabled)"

echo "### 6/6 verify"
URL="https://$OWNER.github.io/$REPO/"
echo "EN: $URL"
echo "IT: ${URL}it/"
