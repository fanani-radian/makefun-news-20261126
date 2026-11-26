#!/usr/bin/env python3
"""Draw the make.fun news-image-20261126 entry: a dense one-day front page
summing up world news of Thursday 26 November 2026. All stories verified
against named sources (see README.md). Output: 1024x1024 PNG, <= 1 MiB.

Layout (own design for this day's stories): navy masthead, lead story with a
drawn missile illustration, numbers panel, WITA timeline strip, three
columns (Middle East & Gulf / Ukraine & Europe + Americas & Africa /
Asia & Oceania), four "Also today" briefs, a pin map and a date-check box.
"""
import math
import os
import textwrap  # noqa: F401  (kept for parity with the shared helper style)
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (247, 243, 234)      # newsprint
INK = (18, 24, 38)
NAVY = (16, 35, 63)
RED = (178, 34, 34)
BLUE = (30, 90, 160)
TEAL = (14, 110, 110)
GOLD = (176, 124, 20)
GREY = (90, 90, 90)
CARD = (255, 255, 255)
LINE = (200, 192, 175)

F_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
F_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, max_w):
    """Greedy word wrap by pixel width."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(d, x, y, lines, f, fill, leading):
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += leading
    return y


def section_head(d, x, y, w, color, title):
    d.rectangle([x, y, x + 12, y + 12], fill=color)
    d.text((x + 18, y - 1), title, font=font(F_SANS_B, 13), fill=INK)
    d.line([x, y + 17, x + w, y + 17], fill=color, width=2)
    return y + 24


def story(d, x, y, w, headline, summary, source):
    """One compact story: headline (<=2 lines), 1-line summary, source tag."""
    f_h, f_s, f_t = font(F_SANS_B, 12), font(F_SANS, 10), font(F_SANS_I, 9)
    hl = wrap(d, headline, f_h, w)
    y = draw_text_block(d, x, y, hl[:2], f_h, INK, 13)
    sl = wrap(d, summary, f_s, w)
    y = draw_text_block(d, x, y, sl[:2], f_s, (50, 50, 50), 11)
    d.text((x, y), source, font=f_t, fill=GREY)
    return y + 9


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# ---------------- MASTHEAD ----------------
d.rectangle([0, 0, W, 108], fill=NAVY)
d.text((16, 10), "THE WORLD IN ONE DAY  \u2022  A FRONT PAGE OF THURSDAY'S NEWS",
       font=font(F_SANS_B, 12), fill=(180, 200, 230))
d.text((16, 28), "WORLD NEWS", font=font(F_SERIF, 52), fill=(255, 255, 255))
d.text((700, 30), "THURSDAY", font=font(F_SERIF, 30), fill=(255, 255, 255))
d.text((700, 62), "26 NOVEMBER 2026", font=font(F_SANS_B, 22), fill=(255, 210, 90))
d.text((16, 92), "25 stories  \u2022  4 regions  \u2022  Every story first reported today",
       font=font(F_SANS, 11), fill=(180, 200, 230))
d.rectangle([0, 108, W, 112], fill=RED)
d.text((16, 118), "SUMMING UP THURSDAY 26 NOVEMBER 2026 \u2014 KIM CALLS FOR BROADER NUCLEAR USE, GULF WAR WIDENS, ASIAN MARKETS ROUTED",
       font=font(F_SANS_B, 11), fill=RED)
d.text((16, 132), "Sources: Reuters  \u2022  AP  \u2022  CNN  \u2022  WSJ  \u2022  Yonhap  \u2022  Globes",
       font=font(F_SANS, 10), fill=GREY)

# ---------------- HERO (lead story) ----------------
hx, hy, hw, hh = 16, 152, 624, 148
d.rectangle([hx, hy, hx + hw, hy + hh], fill=CARD, outline=LINE, width=1)
# drawn scene: night sky, missile silhouette, launch flame, banner
ax, ay, aw, ah = hx + 10, hy + 10, 210, 128
d.rectangle([ax, ay, ax + aw, ay + ah], fill=(12, 24, 48))
d.ellipse([ax + 168, ay + 8, ax + 196, ay + 36], fill=(235, 225, 190))  # moon
for sx, sy in [(ax + 24, ay + 14), (ax + 60, ay + 30), (ax + 120, ay + 10),
               (ax + 150, ay + 52), (ax + 44, ay + 58), (ax + 96, ay + 22),
               (ax + 186, ay + 70), (ax + 18, ay + 84)]:
    d.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))
# distant mountains / ground
d.polygon([(ax, ay + ah), (ax, ay + 104), (ax + 60, ay + 88),
           (ax + 120, ay + 104), (ax + 150, ay + 92), (ax + aw, ay + 106),
           (ax + aw, ay + ah)], fill=(24, 34, 52))
# missile silhouette (vertical, centre-left)
mx0, my0 = ax + 78, ay + 18
d.polygon([(mx0, my0), (mx0 + 8, my0 + 14), (mx0 + 16, my0),
           (mx0 + 16, my0 + 52), (mx0, my0 + 52)], fill=(210, 214, 220))  # body + nose
d.rectangle([mx0 + 2, my0 + 30, mx0 + 14, my0 + 34], fill=(178, 34, 34))   # red band
d.polygon([(mx0 - 8, my0 + 66), (mx0, my0 + 52), (mx0, my0 + 66)], fill=(180, 184, 190))
d.polygon([(mx0 + 24, my0 + 66), (mx0 + 16, my0 + 52), (mx0 + 16, my0 + 66)],
          fill=(180, 184, 190))
# flame + smoke
d.polygon([(mx0 + 3, my0 + 66), (mx0 + 8, my0 + 92), (mx0 + 13, my0 + 66)],
          fill=(255, 170, 40))
d.polygon([(mx0 + 6, my0 + 66), (mx0 + 8, my0 + 82), (mx0 + 10, my0 + 66)],
          fill=(255, 230, 120))
for scx, scy, sr in [(ax + 40, ay + 100, 9), (ax + 62, ay + 106, 12),
                     (ax + 128, ay + 102, 10), (ax + 152, ay + 108, 12)]:
    d.ellipse([scx - sr, scy - sr, scx + sr, scy + sr], fill=(150, 155, 165))
# banner strip across the bottom of the art panel
d.rectangle([ax, ay + ah - 20, ax + aw, ay + ah], fill=RED)
d.text((ax + 8, ay + ah - 17), "CALLS FOR BROADER NUCLEAR USE",
       font=font(F_SANS_B, 9), fill=(255, 255, 255))
# hero text
tx = hx + 232
d.text((tx, hy + 8), "LEAD STORY \u2014 NORTH KOREA", font=font(F_SANS_B, 11), fill=RED)
y = hy + 26
y = draw_text_block(d, tx, y, wrap(d, "Kim calls for broader tactical nuclear use",
                                   font(F_SERIF, 20), hw - 244), font(F_SERIF, 20), INK, 23)
y = draw_text_block(d, tx, y + 2, wrap(d, "Kim Jong Un inspects nuclear production and weapons "
       "research sites, saying North Korea should deploy tactical nuclear weapons "
       "\u201cacross multiple domains\u201d as production is \u201csystematically expanded\u201d. "
       "Its nuclear status, he says, is \u201cabsolutely inviolable\u201d.",
       font(F_SANS, 10), hw - 244), font(F_SANS, 10), (50, 50, 50), 12)
d.text((tx, hy + hh - 18), "KCNA  \u2022  Reuters  \u2022  CNN", font=font(F_SANS_I, 10), fill=GREY)

# ---------------- RIGHT: numbers panel ----------------
rx, ry, rw = 656, 152, 352
d.rectangle([rx, ry, rx + rw, ry + 148], fill=NAVY)
d.text((rx + 12, ry + 8), "THE DAY IN NUMBERS", font=font(F_SANS_B, 12), fill=(255, 210, 90))
nums = [("NIKKEI 225", "\u22122.8%"), ("KOSPI", "\u22126.2%"), ("S&P 500", "\u22120.25%"),
        ("BRENT CRUDE", "$94.61"), ("GOLD / OZ", "$3,535.80"), ("BITCOIN", "$58,734")]
for i, (k, v) in enumerate(nums):
    nx = rx + 12 + (i % 3) * 116
    ny = ry + 30 + (i // 3) * 34
    d.text((nx, ny), k, font=font(F_SANS_B, 9), fill=(180, 200, 230))
    d.text((nx, ny + 12), v, font=font(F_SANS_B, 15), fill=(255, 255, 255))
d.text((rx + 12, ry + 104), "Nikkei 57,012 \u2022 Dow +0.33%, Nasdaq -0.62% \u2022 Brent $94.61.",
       font=font(F_SANS, 10), fill=(200, 210, 225))
d.text((rx + 12, ry + 122), "Market data: 25 Nov closes", font=font(F_SANS_I, 9), fill=(150, 170, 200))

# ---------------- TIMELINE STRIP (WITA) ----------------
ty = 310
d.rectangle([16, ty, 1008, ty + 46], fill=(232, 226, 210))
d.text((26, ty + 4), "HOW THE DAY UNFOLDED \u2014 WITA (UTC+8)",
       font=font(F_SANS_B, 11), fill=INK)
tl = [
    ("02:40", "Nigeria attack reported"),
    ("04:15", "Giza tanker fire kills 31"),
    ("06:04", "Kim's KCNA nuclear order"),
    ("07:31", "Taiwan tariff confidence"),
    ("08:00", "Nikkei opens +0.3%"),
    ("ALL DAY", "US markets shut today"),
]
for bi, (label, txt) in enumerate(tl):
    x = 26 + bi * 162
    d.text((x, ty + 20), label, font=font(F_SANS_B, 10), fill=RED)
    draw_text_block(d, x, ty + 33, wrap(d, txt, font(F_SANS, 9), 152),
                    font(F_SANS, 9), INK, 11)
    if bi < 5:
        d.line([x + 154, ty + 20, x + 154, ty + 42], fill=LINE, width=1)

# ---------------- GRID: 3 columns ----------------
gy = 368
col_w = 320
cols = [
    ("MIDDLE EAST & GULF", RED, [
        ("Gulf war widens, oil tops $94",
         "Houthi drone hits Riyadh's tallest tower again; 11 hurt.",
         "Reuters; WSJ"),
        ("Giza tanker blast kills 31",
         "Fuel tanker overturns on Ring Road; fire engulfs 27 vehicles.",
         "AP; Reuters; CNN"),
        ("Judges urge dropping Netanyahu case",
         "Court urges dropping Case 4000 bribery charge over weak evidence.",
         "Reuters; CNN; Globes"),
        ("Two tankers hit mines in Hormuz",
         "Iran says vessels struck mines, caught fire; warns ships to coordinate passage.",
         "Reuters; Jerusalem Post"),
        ("Dubai Islamic Bank buys Emirates Islamic",
         "$159B-asset Islamic lender created in rare UAE banking merger.",
         "Reuters"),
    ]),
    ("UKRAINE & EUROPE", TEAL, [
        ("Poland plans border no-fly zone",
         "12\u201350 km strip after 3 Russian missiles landed in Poland.",
         "Reuters; Notes from Poland"),
        ("Ukraine hits Savasleyka air base",
         "3 MiG-31s + 2 Su-34s damaged; 88 of 112 drones downed.",
         "Reuters; General Staff"),
        ("Ukraine claims two Samara refinery hits",
         "Ukraine claims hits on Kuibyshev, Syzran refineries; fires, 1 killed.",
         "Reuters; General Staff"),
        ("EU leaders meet 26-27 Nov",
         "26\u201327 Nov Summit weighs EUR 45B Ukraine loan; US holds ~60 Patriot interceptors.",
         "Reuters; FT"),
    ]),
    ("ASIA & OCEANIA", BLUE, [
        ("North Korea expels Swiss envoy",
         "Astier persona non grata; Pyongyang office shut over sanctions row.",
         "Reuters; Yonhap"),
        ("Taiwan confident of keeping 15% tariff",
         "Government says agreed US rate stands after Section 301 plan.",
         "Reuters"),
        ("Trump team unveils Section 301 duties",
         "China capped 20% (40% if truce fails), Taiwan 15%; 14 economies hit.",
         "Reuters; USTR"),
        ("Hasina asks again to fly home 16 Dec",
         "Dhaka refuses; says India must extradite her; border tightened.",
         "Reuters; TBS"),
        ("PIA shifts UK flights to own fleet",
         "Norse Atlantic suspends ops; 2 flights cancelled from today.",
         "Reuters"),
        ("SoftBank \u221215% in Tokyo rout",
         "Tokyo Electron \u221214%, Kioxia \u221214% as AI sell-off deepens.",
         "WSJ; Dow Jones"),
    ]),
]
# second section inside column 2 (Americas & Africa) after Ukraine & Europe
col2_extra = ("AMERICAS & AFRICA", BLUE, [
    ("Nigeria: \u226530 killed in Niger State",
     "Militants burn Borgu villages; UN rights chief warns of escalation.",
     "Reuters; Insight International"),
    ("Saudi national kidnapped in Niger",
     "Suspected IS affiliate holds hostage seized near Tillaberi.",
     "Reuters"),
    ("ECOWAS approves regional force plan",
     "Regional force deployment roadmap set for end-2027.",
     "ECOWAS; APA"),
    ("Thanksgiving: US markets shut",
     "S&P \u22120.25%, Dow +0.33% at 25 Nov close; Americans mark the day.",
     "LPL; Barron's"),
    ("US economy grew 4.3% in Q3",
     "Card\u00f3n Fastest in 3 years, revised up from 3.4%; PCE inflation 3.8% in Oct.",
     "Reuters; CNN"),
])
final_ys = []
for ci, (title, color, items) in enumerate(cols):
    x = 16 + ci * (col_w + 16)
    y = section_head(d, x, gy, col_w, color, title)
    for hl, sm, src in items:
        y = story(d, x, y, col_w, hl, sm, src)
        y += 1
        d.line([x, y, x + col_w, y], fill=(225, 220, 208), width=1)
        y += 4
    if ci == 1:
        title2, color2, items2 = col2_extra
        y = section_head(d, x, y + 2, col_w, color2, title2)
        for hl, sm, src in items2:
            y = story(d, x, y, col_w, hl, sm, src)
            y += 1
            d.line([x, y, x + col_w, y], fill=(225, 220, 208), width=1)
            y += 4
    final_ys.append(y)

# ---------------- ALSO TODAY ----------------
ay = max(final_ys) + 2
d.text((16, ay), "ALSO TODAY", font=font(F_SANS_B, 11), fill=INK)
d.line([16, ay + 16, 1008, ay + 16], fill=RED, width=2)
also = [
    ("Fed Beige Book: modest growth",
     "Modest growth, wage gains, persistent price pressure. \u2014 Reuters"),
    ("UCL: Barca, Liverpool win",
     "Barcelona 4-1, Liverpool 3-0; PSG held 2-2, Bayern lose 2-1. — UEFA"),
    ("Macy's parade postponed",
     "Macy's 100th parade moved to Saturday — first weather postponement ever. — Reuters"),
    ("Gukesh-Sindarov chess drawn",
     "World title match in Geneva level 1-1 after two draws; Game 3 today. — Chess.com"),
]
for ai, (h, t) in enumerate(also):
    ax = 16 + ai * 248
    d.text((ax, ay + 22), h, font=font(F_SANS_B, 11), fill=INK)
    draw_text_block(d, ax, ay + 38, wrap(d, t, font(F_SANS, 10), 232),
                    font(F_SANS, 10), (50, 50, 50), 12)

# ---------------- BOTTOM: pin map + date-check ----------------
by = ay + 84
d.line([16, by, 1008, by], fill=LINE, width=1)
by += 8
mx, my, mw, mh = 16, by, 600, 96
d.rectangle([mx, my, mx + mw, my + mh], fill=(222, 234, 240), outline=LINE)
d.text((mx + 8, my + 4), "WHERE IT HAPPENED", font=font(F_SANS_B, 10), fill=INK)
land = (170, 190, 170)
polys = [
    [(28, 22), (120, 14), (150, 26), (128, 52), (96, 58), (60, 46), (30, 38)],
    [(118, 60), (152, 58), (158, 76), (138, 92), (124, 78)],
    [(300, 18), (336, 12), (344, 30), (322, 38), (300, 32)],
    [(300, 42), (344, 40), (348, 66), (330, 86), (308, 70), (296, 54)],
    [(348, 12), (560, 8), (576, 30), (540, 52), (470, 56), (410, 44), (352, 34)],
    [(500, 74), (556, 72), (560, 86), (516, 90), (498, 82)],
]
for p in polys:
    d.polygon([(mx + px, my + 8 + py) for px, py in p], fill=land)
pins = [  # (x, y, label, dx, dy) label offset from pin
    (545, 28, "PYONGYANG", -64, -4),
    (432, 52, "RIYADH", -46, -4),
    (322, 46, "GIZA", -34, 8),
    (338, 42, "JERUSALEM", 6, -8),
    (318, 18, "WARSAW", -50, -4),
    (400, 14, "SAVASLEYKA", 6, -4),
    (310, 64, "BORGU, NIGERIA", 6, 2),
    (548, 40, "TAIPEI", 6, 2),
    (472, 44, "DHAKA", 6, -4),
    (566, 28, "TOKYO", -42, -12),
]
for px, py, lab, lx, ly in pins:
    X, Y = mx + px, my + 8 + py
    d.ellipse([X - 4, Y - 4, X + 4, Y + 4], fill=RED, outline=(255, 255, 255), width=1)
    d.text((X + lx, Y + ly), lab, font=font(F_SANS_B, 8), fill=INK)
# date-check box
dx, dw = 632, 376
d.rectangle([dx, my, dx + dw, my + mh], fill=(255, 250, 230), outline=GOLD, width=1)
d.text((dx + 10, my + 6), "DATE-CHECKED  \u2022  26 NOV 2026",
       font=font(F_SANS_B, 10), fill=(120, 80, 0))
chk = ("Every story above happened, or was first reported, on Thu 26 Nov 2026 "
       "in some time zone. Names, numbers and dates are as reported by the "
       "sources named. Nothing here is invented.")
y = draw_text_block(d, dx + 10, my + 24, wrap(d, chk, font(F_SANS, 10), dw - 20),
                    font(F_SANS, 10), INK, 13)
d.text((dx + 10, my + mh - 18), "WORLD NEWS \u2014 26 NOVEMBER 2026  \u2022  news-image-20261126",
       font=font(F_SANS_B, 9), fill=INK)

bottom = my + mh
print("saved; columns end at", final_ys, "also-row at", ay, "bottom at", bottom)
assert bottom <= H, f"layout overflow: bottom {bottom} > {H}"

# Write the picture where the harness can read it: the folder named by
# MAKEFUN_OUTPUT_DIR when set (the grader's writable /output; the repo
# itself is read-only there), otherwise beside this script.
out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", Path(__file__).resolve().parent))
out_dir.mkdir(parents=True, exist_ok=True)
img.save(out_dir / "entry.png", optimize=True)
print("wrote", out_dir / "entry.png")
