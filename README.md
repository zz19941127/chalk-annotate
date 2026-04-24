# chalk-annotate

Hand-drawn chalk-textured annotations for LaTeX Beamer presentations.

Pre-rendered PNG overlays with natural grain and opacity variation — far more realistic than pure TikZ decorations.

## Quick Start

### TeX Live (recommended)

```bash
tlmgr install chalk-annotate
```

Then in your `.tex` file:

```latex
\usepackage{chalk-annotate}
\hlellipse{important}
```

### Overleaf

1. Upload `chalk-annotate.sty` to your project root
2. Upload the `assets/` folder (keep the folder structure)
3. Add to your preamble:

```latex
\usepackage{chalk-annotate}
```

4. Use annotations in your slides:

```latex
\hlellipse{important}            % red (default)
\hlellipse[blue]{important}      % blue
\hlbox[green]{key finding}       % green box
\hlunderline[orange]{underline}  % orange underline
```

5. Set compiler to **XeLaTeX** (Menu → Compiler → XeLaTeX)

### Local

Same as Overleaf — place `chalk-annotate.sty` and `assets/` next to your `.tex` file, then compile with `xelatex`.

## Commands

All commands take an optional `[color]` argument (default: `red`).

| Command | Effect |
|---------|--------|
| `\hlellipse[color]{text}` | Chalk ellipse around text |
| `\hlunderline[color]{text}` | Chalk underline below text |
| `\hlbox[color]{text}` | Chalk box with light fill + border |
| `\hlcircle[color]{text}` | Chalk rounded rectangle |
| `\hlarrowright[color]{text}` | Chalk arrow pointing right |
| `\hlstrike[color]{text}` | Chalk diagonal strike-through |

## Available Colors

`red` · `blue` · `green` · `orange` · `purple`

Mix freely in the same document:

```latex
\hlellipse{default red}
\hlellipse[blue]{blue}
\hlbox[green]{$\beta_1 < 0$}
\hlunderline[orange]{underlined text}
\hlellipse[purple]{purple}
```

## Box Details

`\hlbox` uses two layers:
- **Light fill** — behind text (does not obscure content)
- **Chalk border** — on top of text

## Customization

### Add a new color

1. Edit `generate-colors.py` — add your color to `COLORS` dict:

```python
COLORS = {
    ...
    "teal": (0, 128, 128),  # #008080
}
```

2. Run: `python3 generate-colors.py`
3. Upload the new `assets/teal/` folder to your project
4. Use: `\hlellipse[teal]{text}`

### Use your own hand-drawn images

Replace any PNG in `assets/<color>/` with your own. Requirements:

- Transparent background (RGBA PNG)
- File must cover the full canvas (will be stretched to fit text)
- Keep the same filename: `ann-ellipse.png`, `ann-underline.png`, etc.

Works great with Procreate, Photoshop, or any drawing app — just export as transparent PNG.

### Change asset path

If your images live elsewhere:

```latex
\usepackage{chalk-annotate}
\annsetpath{images/annotations}  % now looks in images/annotations/<color>/
```

## File Structure

```
your-project/
  chalk-annotate.sty
  assets/
    red/
      ann-ellipse.png
      ann-underline.png
      ann-box-fill.png
      ann-box-border.png
      ann-arrow-right.png
      ann-strike.png
    blue/
      ...
    green/
      ...
    orange/
      ...
    purple/
      ...
```

## Requirements

- XeLaTeX or LuaLaTeX
- Packages automatically loaded: `tikz`, `graphicx`, `calc`
- TikZ libraries: `calc`, `backgrounds`

## License

MIT
