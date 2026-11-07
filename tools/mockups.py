import sys
from PIL import Image, ImageDraw, ImageFont

FONTS, PNG, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

IVORY = (245, 241, 234)
CHAR = (31, 31, 31)
STONE = (184, 175, 163)
STONE_DK = (125, 118, 108)
GOLD = (168, 139, 90)
GREEN = (47, 59, 51)
S = 2000


def font(name, size):
    return ImageFont.truetype(f"{FONTS}/{name}", size)


PLAY = lambda s: font("PlayfairDisplay-Regular.ttf", s)
PLAYI = lambda s: font("PlayfairDisplay-Italic.ttf", s)
MONL = lambda s: font("Montserrat-Light.ttf", s)
MON = lambda s: font("Montserrat-Regular.ttf", s)


def load(kind, n):
    return Image.open(f"{PNG}/{kind}/{n}.png").convert("RGB")


def fit(img, w=None, h=None):
    if w:
        h = round(img.height * w / img.width)
    else:
        w = round(img.width * h / img.height)
    return img.resize((w, h), Image.LANCZOS)


def place(canvas, img, x, y, edge=STONE):
    canvas.paste(img, (x, y))
    d = ImageDraw.Draw(canvas)
    d.rectangle([x - 1, y - 1, x + img.width, y + img.height], outline=edge, width=2)


def new(bg=IVORY):
    im = Image.new("RGB", (S, S), bg)
    return im, ImageDraw.Draw(im)


def rule(d, x, y, w=160, colour=GOLD, h=3):
    d.rectangle([x, y, x + w, y + h], fill=colour)


def centre_text(d, y, text, f, fill):
    w = d.textlength(text, font=f)
    d.text(((S - w) / 2, y), text, font=f, fill=fill)


# ---------- M1 Hero ----------
im, d = new()
letter = fit(load("let", 1), h=1130)
car = fit(load("car", 1), h=870)
story = fit(load("sto", 1), h=1000)
place(im, letter, 160, 250)
place(im, car, 740, 430)
place(im, story, S - 160 - story.width, 330)
d.text((160, 1470), "The Georgian Suite", font=PLAY(124), fill=CHAR)
rule(d, 160, 1650)
d.text((160, 1690), "Year-in-review templates for estate agents", font=MONL(46), fill=CHAR)
d.text((160, 1760), "18 editable Canva designs  ·  carousel, stories and A4 client letter",
       font=MONL(34), fill=STONE_DK)
d.text((160, 120), "V E L L U M   &   K E Y", font=MON(28), fill=STONE_DK)
im.save(f"{OUT}/01-hero.jpg", quality=92)

# ---------- M2 Client letter spread ----------
im, d = new()
d.text((200, 150), "The client letter", font=PLAY(84), fill=CHAR)
rule(d, 200, 275)
p2 = fit(load("let", 2), w=760)
p3 = fit(load("let", 3), w=760)
place(im, p2, 200, 360)
place(im, p3, 1040, 360)
centre_text(d, 1490, "A four-page A4 market review to print or email to your clients",
            MONL(40), CHAR)
centre_text(d, 1560, "Editable figures, charts and commentary  ·  your branding, your data",
            MONL(32), STONE_DK)
p1 = fit(load("let", 1), h=270)
p4 = fit(load("let", 4), h=270)
place(im, p1, 200, 1660)
place(im, p4, 200 + p1.width + 30, 1660)
d.text((200 + 2 * p1.width + 90, 1760), "Cover letter and outlook pages included",
       font=PLAYI(36), fill=STONE_DK)
im.save(f"{OUT}/02-client-letter.jpg", quality=92)

# ---------- M3 What's included ----------
im, d = new()
d.text((160, 120), "What’s included", font=PLAY(84), fill=CHAR)
rule(d, 160, 245)
d.text((160, 290), "10 Instagram carousel slides  ·  1080 × 1440 px", font=MON(30), fill=STONE_DK)
tw, gap = 312, 30
for i in range(10):
    t = fit(load("car", i + 1), w=tw)
    x = 160 + (i % 5) * (tw + gap)
    y = 350 + (i // 5) * (t.height + gap)
    place(im, t, x, y)
y0 = 350 + 2 * (round(1440 * tw / 1080) + gap) + 40
d.text((160, y0), "4 Instagram stories  ·  1080 × 1920 px", font=MON(30), fill=STONE_DK)
d.text((1030, y0), "4-page A4 client letter", font=MON(30), fill=STONE_DK)
sw = 180
for i in range(4):
    t = fit(load("sto", i + 1), w=sw)
    place(im, t, 160 + i * (sw + 25), y0 + 60)
lw = 215
for i in range(4):
    t = fit(load("let", i + 1), w=lw)
    place(im, t, 1030 + i * (lw + 22), y0 + 60)
im.save(f"{OUT}/03-whats-included.jpg", quality=92)

# ---------- M4 Edit in Canva ----------
im, d = new()
d.text((160, 120), "Editable in a free Canva account", font=PLAY(76), fill=CHAR)
rule(d, 160, 235)
slide = fit(load("car", 4), w=860)
sx, sy = 160, 320
place(im, slide, sx, sy)
callouts = [
    (0.80, 0.14, "Every headline and\nlabel is editable text"),
    (0.78, 0.68, "Chart bars resize to\nyour own figures"),
    (0.20, 0.955, "Add your agency name\nand details"),
]
cx = 1180
cy_list = [380, 900, 1380]
for (fx, fy, text), cy in zip(callouts, cy_list):
    px, py = sx + int(slide.width * fx), sy + int(slide.height * fy)
    d.line([px, py, cx - 30, cy + 40], fill=STONE_DK, width=3)
    d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=GOLD)
    d.multiline_text((cx, cy), text, font=MONL(44), fill=CHAR, spacing=14)
steps = [("01", "Open the links\nin your PDF"), ("02", "Replace photos,\ntext and figures"),
         ("03", "Download and\nshare or print")]
for i, (n, t) in enumerate(steps):
    x = 160 + i * 590
    d.text((x, 1530), n, font=PLAY(72), fill=GOLD)
    d.multiline_text((x + 120, 1545), t, font=MONL(36), fill=CHAR, spacing=10)
centre_text(d, 1840, "Free Canva fonts and elements only  ·  instant download",
            MONL(32), STONE_DK)
im.save(f"{OUT}/04-edit-in-canva.jpg", quality=92)

# ---------- M5 Carousel and stories (deep green) ----------
im, d = new(GREEN)
d.text((160, 120), "The carousel and stories", font=PLAY(76), fill=IVORY)
rule(d, 160, 235)
picks = [1, 3, 4, 6, 7, 10]
tw = 339
for i, n in enumerate(picks):
    t = fit(load("car", n), w=tw)
    x = 160 + (i % 3) * (tw + 36)
    y = 320 + (i // 3) * (t.height + 36)
    place(im, t, x, y, edge=GREEN)
st = fit(load("sto", 4), h=940)
place(im, st, S - 160 - st.width, 320, edge=GREEN)
d.text((160, 1590), "Ten slides that walk clients through your market’s year,",
       font=MONL(40), fill=IVORY)
d.text((160, 1650), "with matching stories to send them to the full review.",
       font=MONL(40), fill=IVORY)
d.text((160, 1800), "V E L L U M   &   K E Y", font=MON(28), fill=STONE)
im.save(f"{OUT}/05-carousel-and-stories.jpg", quality=92)
print("done")
