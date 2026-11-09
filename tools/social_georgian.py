"""Social images for The Georgian Suite (pins 02-10, Instagram posts 01-03).

Usage: python3 social_georgian.py <fonts_dir> <png_dir> <assets_root>

<png_dir> holds Canva PNG exports of the Georgian Suite designs:
  car/1..10.png  carousel (1080 x 1440 or 2x)
  sto/1..4.png   stories (1080 x 1920 or 2x)
  let/1..4.png   A4 letter (1240 x 1754 or 2x)
  photos/terrace.png, photos/door.png, photos/hallway.png
                 the placeholder photographs at their native size (as generated in
                 Canva, before placement), so crops are never taken from an
                 upscaled page export. Any page width works for car/sto/let:
                 pages are only ever scaled down.
Writes <assets_root>/pins/georgian-suite-pin-01..10.jpg (1000 x 1500)
and <assets_root>/instagram/georgian-suite-ig-0N-0M.jpg (1080 x 1350).
Helpers follow tools/mockups.py.
"""
import sys
from PIL import Image, ImageDraw, ImageFont

FONTS, PNG, ROOT = sys.argv[1], sys.argv[2], sys.argv[3]

IVORY = (245, 241, 234)
CHAR = (31, 31, 31)
STONE = (184, 175, 163)
STONE_DK = (125, 118, 108)
GOLD = (168, 139, 90)
GREEN = (47, 59, 51)


def font(name, size):
    return ImageFont.truetype(f"{FONTS}/{name}", size)


PLAY = lambda s: font("PlayfairDisplay-Regular.ttf", s)
PLAYI = lambda s: font("PlayfairDisplay-Italic.ttf", s)
MONL = lambda s: font("Montserrat-Light.ttf", s)
MON = lambda s: font("Montserrat-Regular.ttf", s)
LNUM = ["lnum"]  # Playfair defaults to old-style figures; use lining figures for numbers


def load(kind, n):
    return Image.open(f"{PNG}/{kind}/{n}.png").convert("RGB")


def fit(img, w=None, h=None):
    if w:
        h = round(img.height * w / img.width)
    else:
        w = round(img.width * h / img.height)
    assert w <= img.width and h <= img.height, f"would enlarge {img.size} to {(w, h)}"
    return img.resize((w, h), Image.LANCZOS)


def place(canvas, img, x, y, edge=STONE):
    canvas.paste(img, (x, y))
    if edge is not None:
        d = ImageDraw.Draw(canvas)
        d.rectangle([x - 1, y - 1, x + img.width, y + img.height], outline=edge, width=2)


def rule(d, x, y, w=120, colour=GOLD, h=3):
    d.rectangle([x, y, x + w, y + h], fill=colour)


# --- placeholder photographs at native size (same images as placed in the designs) ---
# terrace: carousel slide 1 (1456 x 1088); door: story 1 (1264 x 1264);
# hallway: letter page 1 (1536 x 1024)
_photo_cache = {}


def photo(name):
    if name not in _photo_cache:
        _photo_cache[name] = Image.open(f"{PNG}/photos/{name}.png").convert("RGB")
    return _photo_cache[name]


def cover(img, w, h, fx=0.5, fy=0.5):
    """Scale-and-crop img to exactly w x h; fx/fy pick the focal point (0-1)."""
    s = max(w / img.width, h / img.height)
    assert s <= 1.0, f"would enlarge {img.size} by {s:.3f} to fill {w} x {h}"
    rw, rh = round(img.width * s), round(img.height * s)
    r = img.resize((rw, rh), Image.LANCZOS)
    x = round((rw - w) * fx)
    y = round((rh - h) * fy)
    return r.crop((x, y, x + w, y + h))


def spaced(text):
    return "   ".join(" ".join(w) for w in text.split(" "))


def wrap(d, text, f, width):
    lines, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if d.textlength(t, font=f) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    return lines


def text_block(d, x, y, text, f, fill, width, lead):
    for i, line in enumerate(wrap(d, text, f, width)):
        d.text((x, y + i * lead), line, font=f, fill=fill)
    return y + len(wrap(d, text, f, width)) * lead


def trio(im, x0, y0, W, edge=STONE):
    """Letter, carousel cover and story cover in a row. Overlaps only cover blank
    areas: the letter title ends at ~70% of its width, the carousel title at ~80%."""
    lw = round(W * 0.46)
    cw = round(W * 0.42)
    lt = fit(load("let", 1), w=lw)
    cr = fit(load("car", 1), w=cw)
    cx = x0 + round(lw * 0.75)
    sx = cx + round(cw * 0.84)
    st = fit(load("sto", 1), w=x0 + W - sx)
    place(im, lt, x0, y0, edge)
    place(im, cr, cx, y0 + 100, edge)
    place(im, st, sx, y0 + 40, edge)
    return max(y0 + lt.height, y0 + 100 + cr.height, y0 + 40 + st.height)


def save(im, path):
    assert im.mode == "RGB"
    im.save(path, "JPEG", quality=90, optimize=True, progressive=False, subsampling=0)
    print("wrote", path, im.size)


# ======================= PINS (1000 x 1500) =======================
PW, PH, M = 1000, 1500, 50
PIN = f"{ROOT}/pins/georgian-suite-pin-%02d.jpg"


def pin_canvas(bg=IVORY):
    im = Image.new("RGB", (PW, PH), bg)
    d = ImageDraw.Draw(im)
    d.text((M, 72), spaced("VELLUM & KEY"), font=MON(22), fill=STONE if bg == GREEN else STONE_DK)
    return im, d


def pin_footer(d, bg=IVORY):
    d.text((M, 1400), "The Georgian Suite", font=PLAYI(34), fill=STONE if bg == GREEN else STONE_DK)


def headline(d, y, text, bg=IVORY, size=76, width=PW - 2 * M, sub=None):
    f = PLAY(size)
    lead = round(size * 1.2)
    y = text_block(d, M, y, text, f, IVORY if bg == GREEN else CHAR, width, lead)
    rule(d, M, y + 28)
    if sub:
        text_block(d, M, y + 66, sub, MONL(30), IVORY if bg == GREEN else CHAR, width, 44)


def photo_pin(n, name, head, sub, fx=0.5, fy=0.5, ph=840):
    im, d = pin_canvas()
    place(im, cover(photo(name), PW - 2 * M, ph, fx, fy), M, 140, edge=None)
    headline(d, 140 + ph + 60, head, sub=sub)
    pin_footer(d)
    save(im, PIN % n)


# pin 01 - letter, carousel cover and story cover above the product line
# (rebuilt here so it shows the current placeholder photographs)
im, d = pin_canvas()
bottom = trio(im, M + 30, 175, PW - 2 * M - 60)
y = text_block(d, M, bottom + 60, "Year-in-review templates for estate agents",
               PLAY(88), CHAR, 640, 98)
rule(d, M, y + 26)
d.text((M, y + 62), "Instagram carousel, stories and an A4 client letter.", font=MONL(32), fill=CHAR)
d.text((M, y + 108), "Editable in Canva.", font=MONL(32), fill=CHAR)
assert y + 108 + 40 < 1390, "pin 01 text runs into the footer"
pin_footer(d)
save(im, PIN % 1)

# pin 02 - deep green front door
photo_pin(2, "door", "Close the year with your clients.",
          "Year-in-review templates for estate agents.", fy=0.35)

# pin 03 - letter page one
im, d = pin_canvas()
lt = fit(load("let", 1), h=1000)
place(im, lt, (PW - lt.width) // 2, 140)
headline(d, 1185, "A year-end letter for your clients.", size=56,
         sub="Four A4 pages to print or send as a PDF.")
pin_footer(d)
save(im, PIN % 3)

# pin 04 - carousel cover and story cover, both reading "The year in review"
im, d = pin_canvas()
c1 = fit(load("car", 1), w=430)
s1 = fit(load("sto", 1), w=430)
place(im, c1, M + 10, 220)
place(im, s1, PW - M - 10 - s1.width, 150)
headline(d, 1000, "Ten slides on your market’s year.",
         sub="Instagram carousel and stories, editable in Canva.")
pin_footer(d)
save(im, PIN % 4)

# pin 05 - hallway with staircase
photo_pin(5, "hallway", "Write your year-end letter in November.",
          "A four-page A4 market letter, editable in Canva.", fx=0.62)

# pin 06 - terrace framed on deep green
im, d = pin_canvas(GREEN)
ph = cover(photo("terrace"), 780, 820, fx=0.45)
x0 = (PW - ph.width) // 2
d.rectangle([x0 - 22, 150 - 22, x0 + ph.width + 21, 150 + ph.height + 21], outline=STONE, width=2)
im.paste(ph, (x0, 150))
headline(d, 1070, "Quiet branding for the year’s end.", bg=GREEN,
         sub="Ivory and charcoal templates with Georgian photography.")
pin_footer(d, GREEN)
save(im, PIN % 6)

# pin 07 - letter, carousel slide and story on deep green
im, d = pin_canvas(GREEN)
bottom = trio(im, M, 170, PW - 2 * M, edge=GREEN)
headline(d, max(bottom + 110, 960), "Your year in review, in Canva.", bg=GREEN,
         sub="Carousel, stories and an A4 client letter.")
pin_footer(d, GREEN)
save(im, PIN % 7)

# pin 08 - contents list above doorway photograph
im, d = pin_canvas()
d.text((M, 150), "Eighteen templates in one set.", font=PLAY(60), fill=CHAR)
rule(d, M, 250)
items = [("10", "Instagram carousel slides", "1080 × 1440 px"),
         ("4", "Instagram stories", "1080 × 1920 px"),
         ("4", "A4 client letter pages", "to print or send as a PDF")]
y = 300
for num, a, b in items:
    d.text((M, y - 4), num, font=PLAY(50), fill=GOLD, features=LNUM)
    d.text((M + 100, y), a, font=MON(30), fill=CHAR)
    d.text((M + 100, y + 44), b, font=MONL(26), fill=STONE_DK)
    y += 118
place(im, cover(photo("door"), PW - 2 * M, 1340 - 680, fy=0.3), M, 680, edge=None)
pin_footer(d)
save(im, PIN % 8)

# pin 09 - three parts of a year-end review above the staircase hallway
im, d = pin_canvas()
d.text((M, 150), "Three parts of a year-end review", font=PLAY(54), fill=CHAR)
rule(d, M, 240)
parts = ["Your area’s year in brief", "What it may mean for your clients",
         "A personal note of thanks"]
y = 290
for i, t in enumerate(parts):
    d.text((M, y - 6), f"0{i + 1}", font=PLAY(46), fill=STONE_DK, features=LNUM)
    d.line([M + 92, y - 4, M + 92, y + 52], fill=STONE, width=2)
    d.text((M + 120, y + 4), t, font=MONL(34), fill=CHAR)
    y += 96
place(im, cover(photo("hallway"), PW - 2 * M, 1340 - 620, fx=0.62), M, 620, edge=None)
pin_footer(d)
save(im, PIN % 9)

# pin 10 - doorway photograph with a story template
im, d = pin_canvas()
place(im, cover(photo("door"), 600, 830, fx=0.5, fy=0.3), M, 140, edge=None)
st = fit(load("sto", 2), h=700)
place(im, st, PW - M - st.width, 250)
headline(d, 1040, "Matching stories for the season.",
         sub="Four Instagram stories, editable in Canva.")
pin_footer(d)
save(im, PIN % 10)


# ======================= INSTAGRAM (1080 x 1350) =======================
IW, IH, IM = 1080, 1350, 80
IG = f"{ROOT}/instagram/georgian-suite-ig-%s.jpg"


def ig_canvas(bg=IVORY):
    im = Image.new("RGB", (IW, IH), bg)
    return im, ImageDraw.Draw(im)


def ig_footer(d, bg=IVORY):
    d.text((IM, IH - 110), "The Georgian Suite", font=PLAYI(32), fill=STONE if bg == GREEN else STONE_DK)


def refit_page(img, bg, label, h=1080):
    """Product page scaled (not stretched) onto a 1080 x 1350 canvas with a small label."""
    im, d = ig_canvas(bg)
    p = fit(img, h=h)
    x = (IW - p.width) // 2
    y = 110
    place(im, p, x, y, edge=STONE if bg == IVORY else bg)
    tf = MONL(28)
    col = IVORY if bg == GREEN else CHAR
    tw = d.textlength(label, font=tf)
    d.text(((IW - tw) / 2, y + h + 50), label, font=tf, fill=col)
    rule(d, (IW - 80) // 2, y + h + 34, w=80)
    return im


def photo_slide(name, fx=0.5, fy=0.5, ph=1020):
    """Photograph across the top with an ivory band. Kept to 1020 px tall because the
    source photos are 1024-1264 px native and must not be enlarged."""
    im, d = ig_canvas()
    im.paste(cover(photo(name), IW, ph, fx, fy), (0, 0))
    d.text((IM, ph + 92), "The Georgian Suite", font=PLAYI(34), fill=STONE_DK)
    t = spaced("VELLUM & KEY")
    f = MON(20)
    d.text((IW - IM - d.textlength(t, font=f), ph + 104), t, font=f, fill=STONE_DK)
    return im


# ---- post 01: the product ----
im, d = ig_canvas()
d.text((IM, 80), spaced("VELLUM & KEY"), font=MON(22), fill=STONE_DK)
trio(im, IM, 170, IW - 2 * IM)
d.text((IM, 960), "The Georgian Suite", font=PLAY(80), fill=CHAR)
rule(d, IM, 1075)
d.text((IM, 1110), "Year-in-review templates for estate agents", font=MONL(34), fill=CHAR)
d.text((IM, 1162), "Carousel, stories and an A4 client letter, editable in Canva",
       font=MONL(26), fill=STONE_DK)
save(im, IG % "01-01")

save(refit_page(load("car", 1), IVORY, "Carousel cover  ·  1080 × 1440 px"), IG % "01-02")
save(refit_page(load("let", 1), GREEN, "A4 client letter  ·  page one"), IG % "01-03")

im, d = ig_canvas()
d.text((IM, 150), "Eighteen templates", font=PLAY(72), fill=CHAR)
rule(d, IM, 260)
car_titles = ["Cover", "Introduction", "Average sold price", "Price by quarter",
              "Homes sold", "Days to sale agreed", "A notable sale",
              "Price by property type", "Looking ahead", "Contact"]
sto_titles = ["Cover", "Average sold price", "Price by quarter", "Full review prompt"]
let_titles = ["Letter to clients", "The year in figures", "Where the market moved",
              "Looking ahead"]


def list_col(x, y, heading, titles, start=1):
    d.text((x, y), heading, font=MON(26), fill=STONE_DK)
    y += 58
    for i, t in enumerate(titles):
        d.text((x, y + 1), f"{start + i:02d}", font=PLAY(26), fill=STONE_DK, features=LNUM)
        d.text((x + 56, y + 2), t, font=MONL(28), fill=CHAR)
        y += 50
    return y


list_col(IM, 320, spaced("CAROUSEL"), car_titles[:5])
list_col(560, 320, " ", car_titles[5:], start=6)
list_col(IM, 700, spaced("STORIES"), sto_titles)
list_col(560, 700, spaced("A4 LETTER"), let_titles)
d.text((IM, 1010), "Ten carousel slides, four stories and a four-page", font=MONL(28), fill=CHAR)
d.text((IM, 1054), "letter, all editable in a free Canva account.", font=MONL(28), fill=CHAR)
ig_footer(d)
save(im, IG % "01-04")

# ---- post 02: the letter ----
save(photo_slide("hallway", fx=0.6), IG % "02-01")
save(refit_page(load("let", 1), IVORY, "A4 client letter  ·  page one of four", h=1080), IG % "02-02")

im, d = ig_canvas()
d.text((IM, 300), "Why a letter", font=PLAY(96), fill=CHAR)
rule(d, IM, 440)
y = 500
for t in ["Some clients still read on paper.",
          "Four A4 pages to print or send as a PDF.",
          "Editable in Canva."]:
    y = text_block(d, IM, y, t, MONL(40), CHAR, IW - 2 * IM, 56) + 34
ig_footer(d)
save(im, IG % "02-03")

# ---- post 03: the look ----
save(photo_slide("door", fy=0.3), IG % "03-01")
save(refit_page(load("car", 1), GREEN, "The year in review  ·  carousel cover"), IG % "03-02")
save(photo_slide("terrace", fx=0.45), IG % "03-03")

im, d = ig_canvas(GREEN)
d.text((IM, 200), "The Georgian Suite", font=PLAY(84), fill=IVORY)
rule(d, IM, 330)
y = 400
for num, t in [("10", "slides in an Instagram carousel"), ("4", "Instagram stories"),
               ("4", "pages in an A4 client letter")]:
    d.text((IM, y - 6), num, font=PLAY(56), fill=IVORY, features=LNUM)
    d.text((IM + 110, y + 14), t, font=MONL(38), fill=IVORY)
    y += 110
d.text((IM, 800), "£28.99", font=PLAY(110), fill=IVORY, features=LNUM)
d.text((IM, 960), "Editable in Canva  ·  instant download", font=MONL(30), fill=STONE)
d.text((IM, IH - 110), spaced("VELLUM & KEY"), font=MON(22), fill=STONE)
save(im, IG % "03-04")
print("done")
