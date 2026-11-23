#!/usr/bin/env python3
"""news-image-20261123: front-page summary of world news, Monday 23 Nov 2026.

Draws a 1024x1024 PNG with PIL only. No network, no randomness, no clock:
running it twice produces byte-identical output.
Lead story: the Papua forest fires. Also today: COP31, US House,
Kyiv, the Merkury, and the Banten factory fire.
"""
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
BOLD = FONT_DIR / "DejaVuSans-Bold.ttf"
REG = FONT_DIR / "DejaVuSans.ttf"

NAVY = (15, 42, 74)
RED = (180, 35, 24)
INK = (26, 26, 26)
GREY = (85, 85, 85)
LIGHT_GREY = (120, 120, 120)
PAPER = (255, 255, 255)
PANEL_BG = (245, 241, 234)
GOLD = (201, 162, 39)
ORANGE = (232, 93, 4)
AMBER = (244, 140, 6)
YELLOW = (255, 183, 3)


def font(path, size):
    return ImageFont.truetype(str(path), size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, fill, max_width, spacing=6):
    lines = wrap(draw, text, fnt, max_width)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def vgrad(draw, box, top, bottom):
    """Vertical gradient inside box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    height = max(1, y1 - y0)
    for i in range(height):
        t = i / height
        col = tuple(int(top[c] + (bottom[c] - top[c]) * t) for c in range(3))
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=col)


def draw_hero(draw):
    """Burning sky: near-black smoke, ember glow, tall flame tongues,
    a scorched Papua island silhouette with dead trees."""
    # Sky: almost black at top, blood-red ember glow near the flames.
    vgrad(draw, (0, 160, W, 430), (14, 10, 12), (150, 34, 12))
    # Thick, dark smoke banks rolling across the sky.
    puffs = [
        (40, 168, 300, 252, (52, 44, 40)),
        (280, 178, 560, 252, (66, 52, 44)),
        (540, 164, 830, 246, (48, 40, 38)),
        (800, 184, 1000, 258, (60, 48, 42)),
        (150, 218, 440, 300, (74, 58, 48)),
        (600, 222, 920, 302, (56, 46, 40)),
    ]
    for x0, y0, x1, y1, col in puffs:
        draw.ellipse([x0, y0, x1, y1], fill=col)
    # Embers rising through the smoke.
    embers = [
        (120, 200, 3, ORANGE), (240, 185, 2, YELLOW), (360, 210, 3, ORANGE),
        (480, 190, 2, YELLOW), (620, 205, 3, ORANGE), (740, 185, 2, YELLOW),
        (860, 210, 3, ORANGE), (950, 195, 2, YELLOW), (180, 250, 2, ORANGE),
        (540, 255, 3, YELLOW), (820, 255, 2, ORANGE),
    ]
    for ex, ey, r, col in embers:
        draw.ellipse([ex - r, ey - r, ex + r, ey + r], fill=col)

    # Papua island silhouette (simplified), scorched dark green-black.
    island = [
        (70, 330), (120, 300), (180, 295), (260, 288), (350, 285),
        (470, 290), (580, 300), (700, 312), (820, 300), (940, 325),
        (960, 345), (880, 360), (720, 375), (540, 372), (380, 378),
        (240, 372), (130, 362), (75, 350),
    ]
    draw.polygon(island, fill=(22, 30, 20), outline=(8, 12, 8))
    # Dead, charred trees standing on the island (thin black spikes).
    for tx in (150, 230, 330, 470, 600, 730, 850):
        draw.polygon([(tx, 300), (tx + 4, 330), (tx + 8, 300)], fill=(8, 8, 8))
        draw.line([(tx + 4, 300), (tx + 4, 288)], fill=(8, 8, 8), width=3)
    # Fire points on the island (red core, orange halo, bigger).
    fires = [(300, 330), (430, 325), (560, 335), (700, 340),
             (830, 330), (180, 320), (900, 340)]
    for fx, fy in fires:
        draw.ellipse([fx - 12, fy - 12, fx + 12, fy + 12], fill=ORANGE)
        draw.ellipse([fx - 7, fy - 7, fx + 7, fy + 7], fill=(220, 30, 10))
    # Tall flame tongues along the bottom edge: dark red, orange, yellow.
    flames = [
        (40, 430, 90, 340, 140, 430), (120, 430, 180, 322, 240, 430),
        (220, 430, 290, 336, 360, 430), (340, 430, 410, 318, 480, 430),
        (460, 430, 540, 338, 620, 430), (600, 430, 670, 320, 740, 430),
        (720, 430, 800, 336, 880, 430), (860, 430, 930, 324, 1000, 430),
    ]
    for x0, yb, xm, ym, x1, _ in flames:
        draw.polygon([(x0, yb), (xm, ym), (x1, yb)], fill=(160, 20, 8))
    mid = [
        (55, 430, 100, 362, 145, 430), (140, 430, 190, 348, 240, 430),
        (240, 430, 300, 358, 360, 430), (360, 430, 420, 342, 480, 430),
        (480, 430, 550, 360, 620, 430), (620, 430, 680, 344, 740, 430),
        (740, 430, 810, 358, 880, 430), (880, 430, 940, 348, 990, 430),
    ]
    for x0, yb, xm, ym, x1, _ in mid:
        draw.polygon([(x0, yb), (xm, ym), (x1, yb)], fill=ORANGE)
    inner = [
        (70, 430, 105, 392, 140, 430), (170, 430, 205, 385, 240, 430),
        (280, 430, 320, 390, 360, 430), (410, 430, 450, 382, 490, 430),
        (540, 430, 580, 392, 620, 430), (670, 430, 705, 385, 740, 430),
        (800, 430, 840, 390, 880, 430), (910, 430, 945, 388, 980, 430),
    ]
    for x0, yb, xm, ym, x1, _ in inner:
        draw.polygon([(x0, yb), (xm, ym), (x1, yb)], fill=YELLOW)
    # Caption chip.
    draw.rectangle([24, 176, 24 + 430, 176 + 30], fill=(0, 0, 0))
    draw.text((36, 182), "SOUTH PAPUA \u2014 HARDEST HIT",
              font=font(BOLD, 18), fill=(255, 255, 255))


def draw_icon_a(draw, x, y):
    """Tree + flame: the forest fires."""
    draw.polygon([(x + 30, y), (x + 8, y + 34), (x + 52, y + 34)],
                 fill=(47, 110, 60))
    draw.polygon([(x + 30, y + 18), (x + 4, y + 52), (x + 56, y + 52)],
                 fill=(34, 90, 48))
    draw.rectangle([x + 26, y + 52, x + 34, y + 66], fill=(90, 60, 30))
    draw.polygon([(x + 68, y + 66), (x + 78, y + 38), (x + 88, y + 66)],
                 fill=ORANGE)
    draw.polygon([(x + 73, y + 66), (x + 78, y + 50), (x + 83, y + 66)],
                 fill=YELLOW)


def draw_icon_b(draw, x, y):
    """Market stall awning + flame: the Tolikara market fire."""
    for i, col in enumerate([RED, PAPER, RED, PAPER, RED]):
        draw.rectangle([x + i * 18, y + 6, x + (i + 1) * 18, y + 24],
                       fill=col, outline=INK)
    draw.polygon([(x, y + 24), (x + 90, y + 24), (x + 80, y + 66),
                  (x + 10, y + 66)], fill=(150, 100, 50))
    draw.rectangle([x + 10, y + 40, x + 80, y + 66], fill=(120, 78, 38))
    draw.polygon([(x + 36, y + 40), (x + 45, y + 16), (x + 54, y + 40)],
                 fill=ORANGE)


def draw_icon_c(draw, x, y):
    """Cloud + rain seeding: smoke and the response."""
    draw.ellipse([x + 6, y + 22, x + 40, y + 46], fill=(170, 180, 195))
    draw.ellipse([x + 28, y + 10, x + 66, y + 44], fill=(190, 198, 210))
    draw.ellipse([x + 58, y + 24, x + 88, y + 46], fill=(170, 180, 195))
    draw.rectangle([x + 6, y + 38, x + 88, y + 48], fill=(170, 180, 195))
    for dx in (14, 38, 62):
        draw.polygon([(x + dx, y + 54), (x + dx + 5, y + 66),
                      (x + dx + 10, y + 54)], fill=(60, 120, 200))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # --- Masthead (0-88): navy bar -------------------------------------
    draw.rectangle([0, 0, W, 88], fill=NAVY)
    draw.text((32, 12), "THE WORLD IN ONE DAY",
              font=font(BOLD, 20), fill=(255, 255, 255))
    draw.text((32, 38), "MONDAY 23 NOVEMBER 2026",
              font=font(BOLD, 34), fill=(255, 255, 255))
    draw.rectangle([0, 88, W, 92], fill=GOLD)

    # --- Lead headline (88-160) ----------------------------------------
    draw.text((32, 92), "PAPUA STILL BURNING",
              font=font(BOLD, 48), fill=RED)
    draw.text((32, 140),
              "436 hectares hit in South Papua; smoke reaches five provinces",
              font=font(REG, 18), fill=GREY)

    # --- Hero panel (160-430) ------------------------------------------
    draw_hero(draw)

    # --- Stat strip (430-540): four boxes ------------------------------
    stats = [
        ("436 ha", "hectares hit in South Papua"),
        ("39", "active fire points"),
        ("104", "hotspots burning"),
        ("81,355", "respiratory cases in Mimika"),
    ]
    box_w = W // 4
    for i, (num, label) in enumerate(stats):
        x0 = i * box_w
        if i:
            draw.line([(x0, 448), (x0, 522)], fill=(210, 210, 210), width=2)
        draw.text((x0 + 24, 448), num, font=font(BOLD, 44), fill=INK)
        draw_wrapped(draw, x0 + 24, 500, label, font(REG, 17), GREY,
                     box_w - 48, spacing=2)
    draw.line([(0, 540), (W, 540)], fill=(210, 210, 210), width=2)

    # --- Three story panels (540-880) ----------------------------------
    panels = [
        ("THE FOREST FIRES",
         "Fires burning since 18 July in Nabire. South Papua lost "
         "25,838 ha in Jan\u2013Jul; Wasur National Park lost 8,707 ha.",
         draw_icon_a),
        ("TOLIKARA MARKET FIRE",
         "On 19 Nov, fire swept Karubaga market in Tolikara: 100 kiosks "
         "and 3 shophouses destroyed. No lives lost.",
         draw_icon_b),
        ("SMOKE & RESPONSE",
         "Crews flew 13 cloud-seeding flights by 31 Oct. Satellites and "
         "drones track the fires as smoke spreads to 5 provinces.",
         draw_icon_c),
    ]
    px, pw, gap = 24, 312, 16
    for i, (title, body, icon) in enumerate(panels):
        x0 = px + i * (pw + gap)
        draw.rectangle([x0, 556, x0 + pw, 868], fill=PANEL_BG,
                       outline=(210, 205, 195), width=2)
        icon(draw, x0 + 24, 576)
        ty = draw_wrapped(draw, x0 + 24, 656, title, font(BOLD, 23), INK,
                          pw - 48, spacing=4)
        draw_wrapped(draw, x0 + 24, ty + 10, body, font(REG, 18), INK,
                     pw - 48, spacing=5)

    # --- Bottom strip (880-1024): ALSO TODAY ---------------------------
    draw.rectangle([0, 880, W, H], fill=NAVY)
    draw.text((32, 892), "ALSO TODAY", font=font(BOLD, 22),
              fill=(255, 255, 255))
    items = [
        "COP31 ends with no climate deal in Turkiye",
        "US Democrats win 258 House seats",
        "Russian strikes on Kyiv kill at least 11",
        "Russian warship Merkury sunk off Benghazi",
        "Banten candy factory fire: 24 dead",
    ]
    y = 922
    for item in items:
        draw.ellipse([32, y + 7, 40, y + 15], fill=RED)
        draw.text((50, y), item, font=font(REG, 17), fill=(255, 255, 255))
        y += 19

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    img.save(out_dir / "entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
