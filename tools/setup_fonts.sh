#!/usr/bin/env bash
# Usage: bash tools/setup_fonts.sh <out_dir>
# Fetches Playfair Display and Montserrat (SIL OFL) from npm and converts WOFF to TTF.
set -euo pipefail
OUT="${1:-fonts}"; mkdir -p "$OUT"; TMP="$(mktemp -d)"
cd "$TMP"
npm pack @fontsource/playfair-display@5.1.0 @fontsource/montserrat@5.1.0 >/dev/null 2>&1
for f in *.tgz; do tar xzf "$f"; mv package "${f%.tgz}"; done
pip install --quiet --break-system-packages fonttools brotli >/dev/null 2>&1 || true
python3 - "$OUT" <<'PY'
import sys, glob
from fontTools.ttLib import TTFont
out = sys.argv[1]
want = {
 "PlayfairDisplay-Regular.ttf": "fontsource-playfair-display-*/files/playfair-display-latin-400-normal.woff",
 "PlayfairDisplay-Italic.ttf":  "fontsource-playfair-display-*/files/playfair-display-latin-400-italic.woff",
 "Montserrat-Light.ttf":        "fontsource-montserrat-*/files/montserrat-latin-300-normal.woff",
 "Montserrat-Regular.ttf":      "fontsource-montserrat-*/files/montserrat-latin-400-normal.woff",
}
for name, pat in want.items():
    src = glob.glob(pat)[0]
    f = TTFont(src); f.flavor = None; f.save(f"{out}/{name}")
    print("ok", name)
PY
