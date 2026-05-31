#!/usr/bin/env bash
# Publish the visual companion to GitHub Pages (staging).
# Run AFTER scenes are rendered + reviewed and build_site.py has produced index.html.
# Owner/repo are parameterized; defaults match this project.
set -euo pipefail

OWNER="${OWNER:-ivan-gentile}"
REPO="${REPO:-moral-ai-viz}"
DESC="Animated visual companion to the Introduction of 'Moral AI and How We Get There'"

cd "$(dirname "$0")"

echo "### 1/6 Stage final mp4s into site_media/ + regenerate index.html"
shopt -s nullglob
for mp4 in media/videos/*/720p30/*.mp4; do cp -f "$mp4" "site_media/$(basename "$mp4")"; done
python3 build_site.py

echo "### 2/6 git init + first commit on main"
if [ ! -d .git ]; then
  git init -q && git checkout -q -b main
fi
git add -A
git commit -q -m "Visual companion: Moral AI Introduction (scenes + page + sourced images)" || echo "(nothing to commit)"

echo "### 3/6 create the public repo + push main"
if ! gh repo view "$OWNER/$REPO" >/dev/null 2>&1; then
  gh repo create "$REPO" --public --source=. --remote=origin --push --description "$DESC"
else
  git remote get-url origin >/dev/null 2>&1 || git remote add origin "https://github.com/$OWNER/$REPO.git"
  git push -q -u origin main
fi

echo "### 4/6 publish site on an orphan gh-pages branch (site at root)"
git checkout -q --orphan gh-pages
git rm -rq --cached . >/dev/null 2>&1 || true
touch .nojekyll
git add -f index.html site_media .nojekyll
git commit -q -m "Publish site (gh-pages)"
git push -q -u origin gh-pages --force
git checkout -qf main   # -f: the orphan branch leaves main's files untracked

echo "### 5/6 enable Pages from gh-pages /"
gh api -X POST "repos/$OWNER/$REPO/pages" -f 'source[branch]=gh-pages' -f 'source[path]=/' \
  >/dev/null 2>&1 || echo "(Pages may already be enabled)"

echo "### 6/6 verify"
URL="https://$OWNER.github.io/$REPO/"
echo "Live URL: $URL  (Pages build takes ~30-60s)"
