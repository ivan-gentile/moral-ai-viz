#!/usr/bin/env bash
# Bootstrap a self-contained Manim CE 0.20.1 environment with NO sudo.
# Built on the native Linux filesystem (~/manim-env) for speed; the slow
# Windows mount (/mnt/d) only holds the repo + final media.
set -euo pipefail

MM_BIN="$HOME/.local/bin/micromamba"
ENV_PREFIX="$HOME/manim-env"
export MAMBA_ROOT_PREFIX="$HOME/micromamba"

echo "### 1/5 Installing micromamba (static binary, user-space)..."
mkdir -p "$HOME/.local/bin"
if [ ! -x "$MM_BIN" ]; then
  curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest \
    | tar -xj -C "$HOME/.local" bin/micromamba
fi
"$MM_BIN" --version

echo "### 2/5 Creating env (python 3.11 + ffmpeg + cairo + pango + pkg-config)..."
"$MM_BIN" create -y -p "$ENV_PREFIX" \
  python=3.11 ffmpeg cairo pango pkg-config -c conda-forge

echo "### 3/5 Installing prebuilt manimpango + pycairo (cannot build from source here)..."
"$MM_BIN" install -y -p "$ENV_PREFIX" -c conda-forge manimpango pycairo

echo "### 4/5 pip install manim 0.20.1 (no build isolation, reuse conda binaries)..."
"$MM_BIN" run -p "$ENV_PREFIX" pip install --no-build-isolation "manim==0.20.1"

echo "### 5/5 Verifying..."
"$MM_BIN" run -p "$ENV_PREFIX" manim --version
echo "BUILD_OK"
