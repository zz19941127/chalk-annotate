#!/usr/bin/env bash
# ============================================================
#  package-ctan.sh — Build CTAN-ready .zip for chalk-annotate
#  Usage: bash package-ctan.sh
# ============================================================
set -euo pipefail

PKG="chalk-annotate"
DIR=$(cd "$(dirname "$0")" && pwd)
BUILD="$DIR/.ctan-build"
ZIP="$DIR/${PKG}.zip"

echo "==> Cleaning previous build..."
rm -rf "$BUILD" "$ZIP"
mkdir -p "$BUILD/$PKG"

echo "==> Copying package files..."
cp "$DIR/chalk-annotate.sty"  "$BUILD/$PKG/"
cp "$DIR/README.md"           "$BUILD/$PKG/"
cp "$DIR/LICENSE"             "$BUILD/$PKG/"

# Documentation PDF
if [ -f "$DIR/chalk-annotate-doc.pdf" ]; then
  cp "$DIR/chalk-annotate-doc.pdf" "$BUILD/$PKG/"
  echo "    Documentation PDF found."
else
  echo "    WARNING: chalk-annotate-doc.pdf not found. Compile it first:"
  echo "      cd $DIR && xelatex chalk-annotate-doc.tex && xelatex chalk-annotate-doc.tex"
fi

echo "==> Flattening PNG assets..."
# assets/<color>/ann-<type>.png → ann-<type>-<color>.png
for color_dir in "$DIR"/assets/*/; do
  color=$(basename "$color_dir")
  for png in "$color_dir"ann-*.png; do
    [ -f "$png" ] || continue
    type=$(basename "$png" .png)          # e.g. ann-ellipse
    type=${type#ann-}                      # strip ann- prefix → ellipse
    flat_name="ann-${type}-${color}.png"  # ann-ellipse-red.png
    cp "$png" "$BUILD/$PKG/$flat_name"
    echo "    $flat_name"
  done
done

echo "==> Creating zip..."
cd "$BUILD"
zip -r -q "$ZIP" "$PKG"
cd "$DIR"

echo ""
echo "==> Done! CTAN package: $ZIP"
echo "    Files in package:"
zipinfo -1 "$ZIP" | sort

echo ""
echo "==> Next steps:"
echo "    1. Review the zip contents above"
echo "    2. Upload to https://ctan.org/upload"
echo "    3. Package name: $PKG"
echo "    4. License: MIT"
