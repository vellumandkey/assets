"""Etsy mockups for The Travertine Suite (adapted from mockups.py).

Usage:
  python3 mockups_travertine.py [FONTS_DIR] [PNG_DIR] [OUT_DIR]

PNG_DIR must contain full-resolution Canva exports:
  lp/1.png .. lp/20.png  Listing Presentation (DAHaP9ShJ_M), PNG, width 2246 (2246x1588)
  lb/1.png, lb/2.png     Pre-Valuation Leave-Behind (DAHaQLYSCLM), PNG, width 1588 (1588x2246)
Writes five 2000x2000 JPEGs (quality 90) named travertine-suite-0N-*.jpg into OUT_DIR.
"""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONTS = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/fonts"
PNG = sys.argv[2] if len(sys.argv) > 2 else "."
OUT = sys.argv[3] if len(sys.argv) > 3 else "/home/claude/assets/etsy"

IVORY = (245, 241, 234)
CHAR = (31, 31, 31)
STONE = (184, 175, 163)
STONE_DK = (125, 118, 108)
GOLD = (168, 139, 90)
GREEN = (47, 59, 51)
S = 2000
M = 160  # outer margin
QUALITY = 90


def font(name, size):
    return ImageFont.truetype(f"{FONTS}/{name}", size)


PLAY = lambda s: font("PlayfairDisplay-Regular.ttf", s)
PLAYI = lambda s: font("PlayfairDisplay-Italic.ttf", s)
MONL = lambda s: font("Montserrat-Light.ttf", s)
MON = lambda s: font("Montserrat-Regular.ttf", s)

_cache = {}


def load(kind, n):
    key = (kind, n)
    if key not in _cache:
        _cache[key] = Image.open(f"{PNG}/{kind}/{n}.png").convert("RGB")
    return _cache[key]


def fit(img, w=None, h=None):
    if w:
        h = round(img.height * w / img.width)
    else:
        w = round(img.width * h / img.height)
    out = img.resize((w, h), Image.LANCZOS, reducing_gap=3.0)
    # light sharpening restores crispness of small text after strong downscaling
    if w < img.width * 0.75:
        out = out.filter(ImageFilter.UnsharpMask(radius=0.8, percent=60, threshold=2))
    return out


def place(canvas, img, x, y, edge=STONE):
    canvas.paste(img, (x, y))
    d = ImageDraw.Draw(canvas)
    if edge is not None:
        d.rectangle([x - 1, y - 1, x + img.width, y + img.height], outline=edge, width=2)


def new(bg=IVORY):
    im = Image.new("RGB", (S, S), bg)
    return im, ImageDraw.Draw(im)


def rule(d, x, y, w=120, colour=GOLD, h=3):
    d.rectangle([x, y, x + w, y + h], fill=colour)


def centre_text(d, y, text, f, fill):
    w = d.textlength(text, font=f)
    d.text(((S - w) / 2, y), text, font=f, fill=fill)


def wrap(d, text, f, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return "\n".join(lines)


def header(d, title, fill=CHAR, size=76):
    d.text((M, 110), title, font=PLAY(size), fill=fill)
    rule(d, M, 232)


BRAND = "V E L L U M   &   K E Y"


def save(im, name):
    im.save(f"{OUT}/{name}", quality=QUALITY, optimize=True, subsampling=0)


# ---------- 01 Hero ----------
def m1():
    im, d = new()
    d.text((M, 130), BRAND, font=MON(28), fill=STONE_DK)
    pres = fit(load("lp", 1), w=1280)
    leave = fit(load("lb", 1), w=680)
    place(im, pres, M, 280)
    place(im, leave, S - M - leave.width, 440)
    y = 1530
    d.text((M, y), "The Travertine Suite", font=PLAY(88), fill=CHAR)
    rule(d, M, y + 135)
    d.text((M, y + 170), "Listing presentation and pre-valuation leave-behind for estate agents",
           font=MONL(38), fill=CHAR)
    d.text((M, y + 230), "22 editable Canva templates  ·  A4 landscape and A4 portrait",
           font=MONL(32), fill=STONE_DK)
    save(im, "travertine-suite-01-hero.jpg")


# ---------- 02 Inside pages ----------
def m2():
    im, d = new()
    header(d, "Inside the listing presentation")
    big = [(7, "Our valuation"), (16, "Our fees and terms")]
    bw, gap = 820, 40
    for i, (n, cap) in enumerate(big):
        t = fit(load("lp", n), w=bw)
        x = M + i * (bw + gap)
        place(im, t, x, 320)
        d.text((x, 320 + t.height + 28), cap, font=MON(30), fill=STONE_DK)
    small = [(8, "Pricing strategy"), (5, "The market"), (15, "Offer to completion"),
             (19, "Next steps")]
    sg = 32
    sw = (S - 2 * M - 3 * sg) // 4
    y0 = 1060
    for i, (n, cap) in enumerate(small):
        t = fit(load("lp", n), w=sw)
        x = M + i * (sw + sg)
        place(im, t, x, y0)
        d.text((x, y0 + t.height + 24), cap, font=MON(28), fill=STONE_DK)
    centre_text(d, 1520, "Twenty A4 landscape pages to guide the valuation appointment",
                MONL(40), CHAR)
    centre_text(d, 1590, "Every price, fee and figure is a placeholder for your own",
                MONL(32), STONE_DK)
    centre_text(d, 1830, BRAND, MON(26), STONE_DK)
    save(im, "travertine-suite-02-inside.jpg")


# ---------- 03 What's included ----------
def m3():
    im, d = new()
    header(d, "What’s included")
    d.text((M, 280), "Listing presentation  ·  20 pages  ·  A4 landscape", font=MON(30),
           fill=STONE_DK)
    gap = 24
    tw = (S - 2 * M - 4 * gap) // 5
    y_top = 340
    th = 0
    for i in range(20):
        t = fit(load("lp", i + 1), w=tw)
        th = t.height
        x = M + (i % 5) * (tw + gap)
        y = y_top + (i // 5) * (th + gap)
        place(im, t, x, y)
    y1 = y_top + 4 * th + 3 * gap + 60
    d.text((M, y1), "Pre-valuation leave-behind  ·  2 pages  ·  A4 portrait", font=MON(30),
           fill=STONE_DK)
    lh = S - 150 - (y1 + 60)
    lx = M
    for n in (1, 2):
        t = fit(load("lb", n), h=lh)
        place(im, t, lx, y1 + 60)
        lx += t.width + gap
    # summary block to the right of the leave-behind
    tx = lx + 90
    ty = y1 + 90
    d.text((tx, ty), "22 editable Canva templates", font=PLAY(60), fill=CHAR)
    rule(d, tx, ty + 100)
    d.multiline_text((tx, ty + 140),
                     "Ivory, stone and deep green, with\nfree Canva fonts and elements.\n"
                     "Template links arrive in a PDF.",
                     font=MONL(34), fill=CHAR, spacing=16)
    sy = ty + 330
    for j, (col, name) in enumerate([(IVORY, "Ivory"), (STONE, "Stone"), (GREEN, "Deep green")]):
        sx = tx + j * 210
        d.rectangle([sx, sy, sx + 70, sy + 70], fill=col, outline=STONE, width=2)
        d.text((sx, sy + 86), name, font=MON(24), fill=STONE_DK)
    save(im, "travertine-suite-03-included.jpg")


LEADER_GAP = 20   # px between end of a callout label and the start of its leader line
LEADER_W = 2      # uniform leader stroke (px at final size)
DOT_R = 10
SS = 4            # supersampling factor for anti-aliased lines and dots


def aa_leaders(im, lines, dots, colour=STONE_DK, dot_colour=GOLD):
    """Draw leader lines and end dots anti-aliased: render at SS x on a transparent
    layer covering only their bounding box, downsample with LANCZOS, composite."""
    pad = DOT_R + 4
    xs = [v for l in lines for v in (l[0], l[2])] + [p[0] for p in dots]
    ys = [v for l in lines for v in (l[1], l[3])] + [p[1] for p in dots]
    x0, y0 = int(min(xs)) - pad, int(min(ys)) - pad
    x1, y1 = int(max(xs)) + pad, int(max(ys)) + pad
    w, h = x1 - x0, y1 - y0
    layer = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    for ax, ay, bx, by in lines:
        ld.line([((ax - x0) * SS, (ay - y0) * SS), ((bx - x0) * SS, (by - y0) * SS)],
                fill=colour + (255,), width=LEADER_W * SS)
    for px, py in dots:
        cx, cy = (px - x0) * SS, (py - y0) * SS
        ld.ellipse([cx - DOT_R * SS, cy - DOT_R * SS, cx + DOT_R * SS, cy + DOT_R * SS],
                   fill=dot_colour + (255,))
    layer = layer.resize((w, h), Image.LANCZOS)
    region = im.crop((x0, y0, x1, y1)).convert("RGBA")
    region.alpha_composite(layer)
    im.paste(region.convert("RGB"), (x0, y0))


# ---------- 04 Editable in Canva ----------
def m4():
    im, d = new()
    header(d, "Editable in a free Canva account")
    page = fit(load("lp", 16), w=1200)
    px0, py0 = S - M - page.width, 330
    place(im, page, px0, py0)
    col_x, col_w = M, px0 - M - 70
    # (fx, fy) are points on page 16; text block sits in the left column
    callouts = [
        (0.032, 0.115, 350, "Headings and labels are editable text"),
        (0.032, 0.255, 600, "Fee as a percentage plus VAT, ready for your own figures"),
        (0.60, 0.72, None, "Replace the photographs with your own"),  # None = horizontal
    ]
    f = MONL(38)
    lines, dots = [], []
    for fx, fy, ty, text in callouts:
        px, py = px0 + int(page.width * fx), py0 + int(page.height * fy)
        body = wrap(d, text, f, col_w)
        first = body.split("\n")[0]
        fb = d.textbbox((col_x, 0), first, font=f)
        mid = (fb[1] + fb[3]) / 2  # vertical centre of the first line, relative to ty
        horizontal = ty is None
        if horizontal:  # align the first line of the label with the dot
            ty = round(py - mid)
        ly = py if horizontal else ty + mid
        bb = d.multiline_textbbox((col_x, ty), body, font=f, spacing=12)
        lines.append((bb[2] + LEADER_GAP, ly, px, py))
        dots.append((px, py))
        d.multiline_text((col_x, ty), body, font=f, fill=CHAR, spacing=12)
    aa_leaders(im, lines, dots)
    steps = [
        ("1", "Open the template links in the PDF"),
        ("2", "Choose “Use template” to save your own copy"),
        ("3", "Replace photographs, text and figures, then download"),
    ]
    y = 1400
    d.line([M, y - 50, S - M, y - 50], fill=STONE, width=2)
    cw = (S - 2 * M) // 3
    for i, (n, t) in enumerate(steps):
        x = M + i * cw
        d.text((x, y), n, font=PLAY(80), fill=GOLD)
        d.multiline_text((x + 80, y + 18), wrap(d, t, MONL(34), cw - 120), font=MONL(34),
                         fill=CHAR, spacing=12)
    centre_text(d, 1690, "Free Canva fonts and elements  ·  a copy of your own to reuse",
                MONL(32), STONE_DK)
    centre_text(d, 1830, BRAND, MON(26), STONE_DK)
    save(im, "travertine-suite-04-edit.jpg")


# ---------- 05 Leave-behind (deep green) ----------
def m5():
    im, d = new(GREEN)
    header(d, "The pre-valuation leave-behind", fill=IVORY)
    h = 1150
    a = fit(load("lb", 1), h=h)
    b = fit(load("lb", 2), h=h)
    gap = S - 2 * M - a.width - b.width
    place(im, a, M, 320, edge=None)
    place(im, b, M + a.width + gap, 320, edge=None)
    cy = 320 + h + 30
    d.text((M, cy), "Page one  ·  Before we meet", font=MON(30), fill=STONE)
    d.text((M + a.width + gap, cy), "Page two  ·  Preparing for your valuation", font=MON(30),
           fill=STONE)
    d.text((M, 1620), "A two-page A4 note to send ahead of the valuation appointment,",
           font=MONL(40), fill=IVORY)
    d.text((M, 1680), "with documents to have to hand and questions to ask.",
           font=MONL(40), fill=IVORY)
    d.text((M, 1830), BRAND, font=MON(26), fill=STONE)
    save(im, "travertine-suite-05-leave-behind.jpg")


if __name__ == "__main__":
    for fn in (m1, m2, m3, m4, m5):
        fn()
    print("done")
