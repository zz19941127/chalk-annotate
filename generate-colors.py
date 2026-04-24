#!/usr/bin/env python3
"""Generate chalk-textured annotation PNGs in multiple colors for comparison."""

from PIL import Image, ImageDraw
import math
import random
import os

SCALE = 4

COLORS = {
    "red":        (192, 57, 43),     # #c0392b 经典红
    "blue":       (41, 98, 168),     # #2962a8 学院蓝
    "green":      (30, 120, 80),     # #1e7850 绿
    "orange":     (211, 84, 0),      # #d35400 暖橙
    "purple":     (106, 36, 138),    # #6a248a 加深紫
}

OUT_DIR = "assets"
os.makedirs(OUT_DIR, exist_ok=True)


def chalk_dot(draw, x, y, radius, color, alpha_range=(100, 255)):
    r, g, b = color
    alpha = random.randint(*alpha_range)
    if radius < 0.3:
        radius = 0.3
    draw.ellipse([x - radius, y - radius, x + radius, y + radius],
                 fill=(r, g, b, alpha))


def chalk_stroke(draw, points, color, width=4, density=2, alpha_range=(100, 255)):
    for x, y in points:
        w = width * (0.6 + 0.8 * random.random())
        for _ in range(density):
            ox = random.gauss(0, w * 0.12)
            oy = random.gauss(0, w * 0.12)
            chalk_dot(draw, x + ox, y + oy, w / 2, color, alpha_range)


def ellipse_points(cx, cy, rx, ry, n=150, jitter=1.8):
    pts = []
    for i in range(n):
        a = (i / n) * 2 * math.pi
        squiggle = 0.8 * math.sin(a * 5 + random.gauss(0, 0.3))
        px = cx + (rx + squiggle) * math.cos(a) + random.gauss(0, jitter)
        py = cy + (ry + squiggle) * math.sin(a) + random.gauss(0, jitter)
        pts.append((px, py))
    return pts


def line_points(x1, y1, x2, y2, jitter=0.8):
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    n = max(int(dist * 0.8), 20)
    pts = []
    for i in range(n):
        t = i / n
        x = x1 + (x2 - x1) * t + random.gauss(0, jitter)
        y = y1 + (y2 - y1) * t + random.gauss(0, jitter)
        pts.append((x, y))
    return pts


def curved_line_points(x1, y1, x2, y2, bow=2.0, jitter=0.6):
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    n = max(int(dist * 0.8), 20)
    pts = []
    for i in range(n):
        t = i / n
        x = x1 + (x2 - x1) * t + random.gauss(0, jitter)
        y_bow = bow * 4 * t * (1 - t)
        y = y1 + (y2 - y1) * t + y_bow + random.gauss(0, jitter * 0.5)
        pts.append((x, y))
    return pts


def gen_ellipse(color, w=300, h=180):
    W, H = w * SCALE, h * SCALE
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = W / 2, H / 2
    rx, ry = (w / 2 - 14) * SCALE, (h / 2 - 12) * SCALE
    pts = ellipse_points(cx, cy, rx, ry, 150, 1.8 * SCALE)
    chalk_stroke(draw, pts, color, width=3.5 * SCALE, density=3)
    pts2 = ellipse_points(cx + random.gauss(0, 0.4 * SCALE),
                          cy + random.gauss(0, 0.4 * SCALE),
                          rx + random.gauss(0, 0.3 * SCALE),
                          ry + random.gauss(0, 0.3 * SCALE), 100, 1.2 * SCALE)
    chalk_stroke(draw, pts2, color, width=2.5 * SCALE, density=2, alpha_range=(60, 160))
    return img.resize((w, h), Image.LANCZOS)


def gen_underline(color, w=300, h=50):
    W, H = w * SCALE, h * SCALE
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    pts = curved_line_points(8 * SCALE, H / 2, (w - 8) * SCALE, H / 2,
                             bow=1.5 * SCALE, jitter=0.5 * SCALE)
    chalk_stroke(draw, pts, color, width=3.5 * SCALE, density=3)
    return img.resize((w, h), Image.LANCZOS)


def gen_box_fill(color, w=260, h=170):
    """浅色底色层 — 放在文字后面，不遮挡文字"""
    W, H = w * SCALE, h * SCALE
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    m = 14 * SCALE
    r, g, b = color
    # 混色：原色 + 白色，取 20% 不透明度 → 柔和底色
    fill_alpha = 40
    draw.rounded_rectangle([m, m, W - m, H - m], radius=4 * SCALE,
                           fill=(r, g, b, fill_alpha))
    return img.resize((w, h), Image.LANCZOS)


def gen_box_border(color, w=260, h=170):
    """边框层 — 放在文字上面，只有边框线条"""
    W, H = w * SCALE, h * SCALE
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    m = 14 * SCALE
    for side in [
        line_points(m, m, W - m, m, 0.7 * SCALE),
        line_points(W - m, m, W - m, H - m, 0.7 * SCALE),
        line_points(W - m, H - m, m, H - m, 0.7 * SCALE),
        line_points(m, H - m, m, m, 0.7 * SCALE),
    ]:
        chalk_stroke(draw, side, color, width=2.8 * SCALE, density=3)
    return img.resize((w, h), Image.LANCZOS)


def gen_strike(color, w=260, h=100):
    W, H = w * SCALE, h * SCALE
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    pts = line_points(10 * SCALE, (h - 18) * SCALE,
                      (w - 10) * SCALE, 18 * SCALE, 1.0 * SCALE)
    chalk_stroke(draw, pts, color, width=3 * SCALE, density=3)
    return img.resize((w, h), Image.LANCZOS)


def gen_arrow_right(color, w=120, h=60):
    W, H = w * SCALE, h * SCALE
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    y_mid = H / 2
    pts = line_points(6 * SCALE, y_mid, (w - 35) * SCALE, y_mid, 0.6 * SCALE)
    chalk_stroke(draw, pts, color, width=3 * SCALE, density=3)
    tip_x = (w - 8) * SCALE
    for pts in [
        line_points((w - 38) * SCALE, y_mid - 12 * SCALE, tip_x, y_mid, 0.5 * SCALE),
        line_points((w - 38) * SCALE, y_mid + 12 * SCALE, tip_x, y_mid, 0.5 * SCALE),
    ]:
        chalk_stroke(draw, pts, color, width=3 * SCALE, density=3)
    return img.resize((w, h), Image.LANCZOS)


if __name__ == "__main__":
    generators = {
        "ellipse":     gen_ellipse,
        "underline":   gen_underline,
        "box-fill":    gen_box_fill,
        "box-border":  gen_box_border,
        "arrow-right": gen_arrow_right,
        "strike":      gen_strike,
    }

    for color_name, color_rgb in COLORS.items():
        d = os.path.join(OUT_DIR, color_name)
        os.makedirs(d, exist_ok=True)
        for ann_type, gen_fn in generators.items():
            random.seed(42)
            img = gen_fn(color_rgb)
            path = os.path.join(d, f"ann-{ann_type}.png")
            img.save(path, "PNG")
        print(f"  {color_name}: {list(generators.keys())}")

    # Default (red) at assets/ root
    for ann_type, gen_fn in generators.items():
        random.seed(42)
        img = gen_fn(COLORS["red"])
        img.save(os.path.join(OUT_DIR, f"ann-{ann_type}.png"), "PNG")

    print(f"\nDone! Colors: {', '.join(COLORS.keys())}")
    print("Each color in assets/<color>/ann-*.png")
