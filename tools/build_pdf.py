import sys
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm

FONTS = sys.argv[1]
OUT = sys.argv[2]

pdfmetrics.registerFont(TTFont("Play", f"{FONTS}/PlayfairDisplay-Regular.ttf"))
pdfmetrics.registerFont(TTFont("PlayI", f"{FONTS}/PlayfairDisplay-Italic.ttf"))
pdfmetrics.registerFont(TTFont("MonL", f"{FONTS}/Montserrat-Light.ttf"))
pdfmetrics.registerFont(TTFont("Mon", f"{FONTS}/Montserrat-Regular.ttf"))

IVORY = HexColor("#F5F1EA")
CHAR = HexColor("#1F1F1F")
STONE = HexColor("#B8AFA3")
STONE_DK = HexColor("#7D766C")
GOLD = HexColor("#A88B5A")
GREEN = HexColor("#2F3B33")

W, H = A4
M = 22 * mm

LINKS = [
    ("Instagram carousel", "10 slides · 1080 × 1440 px", "[TEMPLATE LINK: keep private, never commit]"),
    ("Instagram stories", "4 pages · 1080 × 1920 px", "[TEMPLATE LINK: keep private, never commit]"),
    ("A4 client market letter", "4 pages · A4 portrait", "[TEMPLATE LINK: keep private, never commit]"),
]

DISCLOSURE = ("Layouts are designed by Vellum & Key; some imagery and copy were created "
              "with AI assistance and are provided as editable placeholders.")

c = canvas.Canvas(OUT, pagesize=A4)
c.setTitle("The Georgian Suite — Your Templates")
c.setAuthor("Vellum & Key")
c.setSubject("Canva template links and editing guide")


def background(fill=IVORY):
    c.setFillColor(fill)
    c.rect(0, 0, W, H, stroke=0, fill=1)


def rule(x, y, w=20 * mm, colour=GOLD, weight=0.75):
    c.setStrokeColor(colour)
    c.setLineWidth(weight)
    c.line(x, y, x + w, y)


def footer(n, colour=STONE_DK):
    c.setFont("MonL", 7.5)
    c.setFillColor(colour)
    c.drawString(M, 14 * mm, "Vellum & Key  ·  The Georgian Suite")
    c.drawRightString(W - M, 14 * mm, str(n))


def wrap(text, font, size, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if pdfmetrics.stringWidth(t, font, size) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(text, x, y, width, font="MonL", size=10, leading=15, colour=CHAR):
    c.setFont(font, size)
    c.setFillColor(colour)
    for line in wrap(text, font, size, width):
        c.drawString(x, y, line)
        y -= leading
    return y


# ---------- Page 1: cover ----------
background(GREEN)
c.setFillColor(STONE)
c.setFont("Mon", 8)
c.drawString(M, H - 30 * mm, "V E L L U M   &   K E Y")
rule(M, H / 2 + 52 * mm, 22 * mm)
c.setFillColor(IVORY)
c.setFont("Play", 44)
c.drawString(M, H / 2 + 30 * mm, "The Georgian")
c.drawString(M, H / 2 + 13 * mm, "Suite")
c.setFont("MonL", 12)
c.drawString(M, H / 2 - 4 * mm, "Year-in-review templates for estate agents")
c.setFillColor(STONE)
c.setFont("MonL", 9.5)
c.drawString(M, H / 2 - 12 * mm, "18 editable designs  ·  Instagram carousel, stories and A4 client letter")
c.setFont("PlayI", 11)
c.setFillColor(STONE)
c.drawString(M, 30 * mm, "Editorial marketing templates for agents who sell exceptional homes.")
c.showPage()

# ---------- Page 2: welcome + links ----------
background()
y = H - 32 * mm
c.setFillColor(CHAR)
c.setFont("Play", 26)
c.drawString(M, y, "Welcome")
rule(M, y - 8 * mm)
y -= 18 * mm
y = para("Thank you for choosing The Georgian Suite. Everything you need to share your market's "
         "year with clients is here, ready to make your own in Canva. A free Canva account is all "
         "you need.", M, y, W - 2 * M, size=10.5, leading=16)

y -= 12 * mm
c.setFont("Play", 18)
c.setFillColor(CHAR)
c.drawString(M, y, "Your template links")
y -= 6 * mm
c.setFont("MonL", 9)
c.setFillColor(STONE_DK)
c.drawString(M, y, "Select a title below to open it in Canva, then choose “Use template” to make your own copy.")
y -= 10 * mm

box_h = 26 * mm
for i, (name, spec, url) in enumerate(LINKS, 1):
    top = y
    c.setStrokeColor(STONE)
    c.setLineWidth(0.6)
    c.line(M, top, W - M, top)
    c.setFont("Play", 22)
    c.setFillColor(STONE)
    c.drawString(M, top - 13 * mm, f"0{i}")
    c.setFont("Play", 15)
    c.setFillColor(CHAR)
    c.drawString(M + 18 * mm, top - 9 * mm, name)
    c.setFont("MonL", 9)
    c.setFillColor(STONE_DK)
    c.drawString(M + 18 * mm, top - 15 * mm, spec)
    c.setFont("Mon", 9)
    c.setFillColor(GOLD)
    c.drawString(M + 18 * mm, top - 21 * mm, url)
    c.setFont("Mon", 8.5)
    c.setFillColor(GREEN)
    c.drawRightString(W - M, top - 9 * mm, "OPEN IN CANVA  →")
    c.linkURL(url, (M, top - box_h, W - M, top), relative=0, thickness=0)
    y -= box_h
c.setStrokeColor(STONE)
c.line(M, y, W - M, y)

y -= 12 * mm
c.setFont("MonL", 8.5)
c.setFillColor(STONE_DK)
para("If a link does not open, copy the address beneath its title into your browser. Please keep "
     "these links for your own use; they are licensed to you as the purchaser.",
     M, y, W - 2 * M, size=8.5, leading=13, colour=STONE_DK)
footer(2)
c.showPage()

# ---------- Page 3: how to edit + tips ----------
background()
y = H - 32 * mm
c.setFillColor(CHAR)
c.setFont("Play", 26)
c.drawString(M, y, "Making it yours")
rule(M, y - 8 * mm)
y -= 20 * mm

steps = [
    ("Open your link", "Select a template link and sign in to Canva, or create a free account."),
    ("Use template", "Choose “Use template”. Canva saves a private copy to your account."),
    ("Replace the photographs", "Drag your own images onto each photo frame. They crop to fit."),
    ("Edit text and figures", "Click any text to replace the placeholders. Charts are shapes: resize "
                              "each bar or move each point to match your data."),
    ("Download and share", "Download carousels and stories as PNG for Instagram, and the letter as "
                           "PDF Print for printing or PDF Standard for email."),
]
for i, (t, d) in enumerate(steps, 1):
    c.setFont("Play", 18)
    c.setFillColor(GOLD)
    c.drawString(M, y - 1 * mm, f"{i}")
    c.setFont("Mon", 11)
    c.setFillColor(CHAR)
    c.drawString(M + 12 * mm, y, t)
    y2 = para(d, M + 12 * mm, y - 6 * mm, W - 2 * M - 12 * mm, size=9.5, leading=14, colour=STONE_DK)
    y = y2 - 6 * mm

y -= 4 * mm
c.setStrokeColor(STONE)
c.setLineWidth(0.6)
c.line(M, y, W - M, y)
y -= 12 * mm
c.setFont("Play", 18)
c.setFillColor(CHAR)
c.drawString(M, y, "For a premium result")
y -= 10 * mm
tips = [
    "Choose one strong, well-lit photograph per slide or page rather than several smaller ones.",
    "Keep the white space. It is what makes the layouts feel considered.",
    "Use real, sourced figures and update the source line on each page.",
    "Stay with the two typefaces provided so every piece feels part of one set.",
    "Read each slide on your phone before posting; small text should still be legible.",
]
for t in tips:
    c.setFillColor(GOLD)
    c.circle(M + 1.2 * mm, y + 1.2 * mm, 0.8 * mm, stroke=0, fill=1)
    y = para(t, M + 6 * mm, y, W - 2 * M - 6 * mm, size=9.5, leading=14) - 3 * mm
footer(3)
c.showPage()

# ---------- Page 4: licence, disclosure, support ----------
background()
y = H - 32 * mm
c.setFillColor(CHAR)
c.setFont("Play", 26)
c.drawString(M, y, "Good to know")
rule(M, y - 8 * mm)
y -= 22 * mm

sections = [
    ("Licence", "These templates are licensed to the purchasing agent or agency for use in their own "
                "marketing. You may edit, print and publish your finished designs. You may not resell, "
                "share or distribute the templates or links, in whole or in part."),
    ("Sample content", "All figures, names, addresses and market commentary are placeholders. Replace "
                       "them with your own accurate information before publishing."),
    ("About this design", DISCLOSURE),
    ("Support", "Message us on Etsy and we will reply within one working day."),
]
for t, d in sections:
    c.setFont("Mon", 8)
    c.setFillColor(STONE_DK)
    c.drawString(M, y, " ".join(t.upper()))
    y = para(d, M, y - 7 * mm, W - 2 * M, size=10, leading=15.5) - 10 * mm

c.setFont("PlayI", 16)
c.setFillColor(CHAR)
c.drawString(M, 46 * mm, "With thanks,")
c.setFont("Play", 16)
c.drawString(M, 38 * mm, "Vellum & Key")
rule(M, 33 * mm, 22 * mm)
footer(4)
c.showPage()
c.save()
print("ok", OUT)
