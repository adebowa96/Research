"""Builds the 48 x 36 in APHA 2026 poster (poster/MRKH_APHA2026_Poster.pptx).
Run make_figures.py and make_map.js first. Usage: python3 scripts/make_poster.py

Inline markup in poster text: **bold**, ^{sup} for superscript citations."""
import json
import re
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

HERE = Path(__file__).parent
ROOT = HERE.parent
FIG = ROOT / "figures"
data = json.loads((HERE / "data.json").read_text())
N = data["total_included"]

NAVY = RGBColor(0x0D, 0x36, 0x6B)
BLUE = RGBColor(0x2A, 0x78, 0xD6)
ORANGE = RGBColor(0xC4, 0x4E, 0x1B)
PANEL = RGBColor(0xEE, 0xF4, 0xFC)
PANEL_WARM = RGBColor(0xFD, 0xEE, 0xE7)
INK = RGBColor(0x0B, 0x0B, 0x0B)
INK_2 = RGBColor(0x52, 0x51, 0x4E)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
FONT = "Arial"

W, H = 48.0, 36.0
MARGIN = 0.75
GUTTER = 0.6
COL_W = (W - 2 * MARGIN - 2 * GUTTER) / 3
COL_X = [MARGIN + i * (COL_W + GUTTER) for i in range(3)]
TOP = 6.1
BOTTOM = H - 0.6

prs = Presentation()
prs.slide_width = Inches(W)
prs.slide_height = Inches(H)
slide = prs.slides.add_slide(prs.slide_layouts[6])

TOKEN = re.compile(r"(\*\*.+?\*\*|\^\{.+?\})")


def add_runs(par, text, size, color=INK, bold=False, italic=False):
    for piece in TOKEN.split(text):
        if not piece:
            continue
        run = par.add_run()
        is_bold = bold
        sup = False
        if piece.startswith("**"):
            piece, is_bold = piece[2:-2], True
        elif piece.startswith("^{"):
            piece, sup = piece[2:-1], True
        run.text = piece
        f = run.font
        f.name, f.size, f.bold, f.italic = FONT, Pt(size), is_bold, italic
        f.color.rgb = color
        if sup:
            f._element.set("baseline", "30000")


def rect(x, y, w, h, fill, line=None, shape=MSO_SHAPE.RECTANGLE):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.solid()
    s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
        s.line.width = Pt(2)
    s.shadow.inherit = False
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = 0.08
    return s


def textbox(x, y, w, h, paras, size=24, color=INK, align=PP_ALIGN.LEFT,
            anchor=MSO_ANCHOR.TOP, bullet=False, space_after=8, line_spacing=1.1):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Inches(0.1)
    tf.margin_top = tf.margin_bottom = Inches(0.05)
    for i, p in enumerate(paras):
        par = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        par.alignment = align
        par.space_after = Pt(space_after)
        par.line_spacing = line_spacing
        add_runs(par, ("•  " + p) if bullet else p, size, color)
    return tb


def header(col, y, title):
    x = COL_X[col]
    rect(x, y, COL_W, 0.85, NAVY)
    textbox(x + 0.15, y, COL_W - 0.3, 0.85, [title], size=34, color=WHITE,
            anchor=MSO_ANCHOR.MIDDLE, space_after=0)
    return y + 1.05


def image(path, x, y, w):
    with Image.open(path) as im:
        aspect = im.height / im.width
    slide.shapes.add_picture(str(path), Inches(x), Inches(y), Inches(w), Inches(w * aspect))
    return y + w * aspect


def caption(x, y, w, text, h=0.9):
    textbox(x, y, w, h, [text], size=18, color=INK_2, space_after=0)
    return y + h


# ------------------------------------------------------------------ title banner
rect(0, 0, W, 5.6, NAVY)
rect(0, 5.6, W, 0.12, BLUE)
textbox(MARGIN, 0.35, W - 2 * MARGIN, 2.6,
        ["Mental Health and Psychosocial Outcomes Among Individuals With "
         "Mayer-Rokitansky-Küster-Hauser (MRKH) Syndrome: A Scoping Review"],
        size=64, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, space_after=0,
        line_spacing=1.0)
textbox(MARGIN, 3.05, W - 2 * MARGIN, 0.9,
        ["Ifeoluwanimi P. Shobayo, BSc, MSPHc  |  Paul Okojie, PhD  |  Robyn Anderson, PhD"],
        size=36, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, space_after=0)
textbox(MARGIN, 3.95, W - 2 * MARGIN, 1.4,
        ["Department of Public and Community Health, Liberty University",
         "APHA 2026 Annual Meeting & Expo  ·  Sexual and Reproductive Health Section"],
        size=28, color=RGBColor(0xCD, 0xE2, 0xFB), align=PP_ALIGN.CENTER,
        anchor=MSO_ANCHOR.MIDDLE, space_after=2)

# ------------------------------------------------------------------ column 1
c, x = 0, COL_X[0]
y = header(c, TOP, "Background")
textbox(x, y, COL_W, 4.3, [
    "MRKH syndrome is a rare Müllerian aplasia: congenital absence of the uterus and upper "
    "two-thirds of the vagina in individuals with a 46,XX karyotype and functional ovaries. "
    "It affects approximately 1 in 4,500–5,000 female births^{1,2} and is typically diagnosed "
    "in adolescence, a critical period for identity formation and social development.",
    "The diagnosis carries profound implications for fertility, psychosexual development, and "
    "self-image, yet psychosocial outcomes remain underexplored and insufficiently integrated "
    "into clinical and public health frameworks.",
], size=26)
y += 3.55

# At-a-glance tiles
tiles = [("~1:5,000", "female births"), ("46,XX", "karyotype;\nfunctional ovaries"),
         ("Teens", "typical age at\ndiagnosis"), ("No uterus", "uterovaginal\nagenesis")]
tw = (COL_W - 3 * 0.25) / 4
textbox(x, y, COL_W, 0.6, ["**MRKH Syndrome at a Glance**"], size=24, color=NAVY, space_after=0)
y += 0.65
for i, (big, small) in enumerate(tiles):
    tx = x + i * (tw + 0.25)
    rect(tx, y, tw, 2.5, PANEL, line=BLUE, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    textbox(tx, y + 0.2, tw, 0.9, [f"**{big}**"], size=30, color=NAVY, align=PP_ALIGN.CENTER,
            anchor=MSO_ANCHOR.MIDDLE, space_after=0)
    textbox(tx, y + 1.1, tw, 1.3, small.split("\n"), size=19, color=INK_2,
            align=PP_ALIGN.CENTER, space_after=0, line_spacing=1.0)
y += 2.8

# Research question
rect(x, y, COL_W, 2.2, PANEL_WARM, line=ORANGE, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
textbox(x + 0.2, y + 0.1, COL_W - 0.4, 2.0, [
    "**Research Question:** What mental health outcomes and coping mechanisms are reported "
    "among individuals with MRKH syndrome, and what healthcare system gaps exist?"],
    size=24, anchor=MSO_ANCHOR.MIDDLE, space_after=0)
y += 2.45

y = header(c, y, "Learning Objectives")
textbox(x, y, COL_W, 3.3, [
    "**1.** Identify key mental health outcomes, including depression, anxiety, reduced quality "
    "of life, and psychosexual challenges, reported among individuals with MRKH syndrome.",
    "**2.** Describe coping mechanisms and psychosocial responses, including adaptive and "
    "maladaptive strategies, documented in MRKH populations.",
], size=25)
y += 2.6

y = header(c, y, "Methods")
textbox(x, y, COL_W, 4.2, [
    "**Design:** Scoping review following Arksey & O'Malley's five-stage framework^{3}; "
    "reported per PRISMA-ScR^{4}.",
    "**Databases:** PubMed/MEDLINE, Scopus, PsycINFO, CINAHL (January 2019 – March 2026).",
    "**Included:** Primary quantitative, qualitative, and mixed-methods studies reporting "
    "psychological outcomes and/or coping mechanisms in MRKH populations.",
    "**Excluded:** Studies focused solely on anatomical, surgical, or fertility outcomes.",
], size=24, space_after=6)
y += 3.7
img_w = 10.8
y = image(FIG / "prisma_flow.png", x + (COL_W - img_w) / 2, y, img_w)
caption(x, y + 0.05, COL_W, "PRISMA-ScR flow diagram of study selection.", h=0.5)
col1_end = y + 0.55

# ------------------------------------------------------------------ column 2
c, x = 1, COL_X[1]
y = header(c, TOP, "Results")
textbox(x, y, COL_W, 1.5, [
    f"**{N} studies** met inclusion criteria across quantitative, qualitative, and "
    "mixed-methods designs. Studies could report more than one outcome domain."], size=25)
y += 1.55
y = image(FIG / "fig1_outcomes_bar.png", x, y, COL_W)
y = caption(x, y + 0.05, COL_W,
            f"**Fig 1.** Frequency of outcome domains across included studies (N = {N}). "
            "Counts do not sum to 34 because studies could report multiple domains.", h=0.95)
textbox(x, y, COL_W, 1.5, [
    "Findings are consistent with pre-2019 evidence of elevated distress, anxiety, and "
    "depression and poorer mental health–related quality of life in MRKH^{5–7}, and with a "
    "prior systematic review^{8}."], size=24)
y += 1.6

dw = COL_W * 0.78
y = image(FIG / "fig2_design_donut.png", x + (COL_W - dw) / 2, y, dw)
y = caption(x, y + 0.05, COL_W,
            f"**Fig 2.** Study design distribution (N = {N}). Cross-sectional studies are a "
            "subset of quantitative designs.", h=0.95)

y = header(c, y + 0.1, f"Coping Mechanisms (n = 21 studies, 62%)")
chips = [("Peer & community support", False), ("Psychological counseling", False),
         ("Identity reconstruction", False), ("Spiritual coping", False),
         ("Adaptive acceptance", False), ("Avoidance (maladaptive)", True)]
cw = (COL_W - 0.3) / 2
for i, (label, maladaptive) in enumerate(chips):
    cx = x + (i % 2) * (cw + 0.3)
    cy = y + (i // 2) * 1.05
    rect(cx, cy, cw, 0.85, PANEL_WARM if maladaptive else PANEL,
         line=ORANGE if maladaptive else BLUE, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    textbox(cx, cy, cw, 0.85, [label], size=22, color=ORANGE if maladaptive else NAVY,
            align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, space_after=0)
y += 3 * 1.05 + 0.1
textbox(x, y, COL_W, 0.6, ["Blue = adaptive strategies; orange = maladaptive strategy."],
        size=18, color=INK_2, space_after=0)
col2_end = y + 0.6

# ------------------------------------------------------------------ column 3
c, x = 2, COL_X[2]
y = header(c, TOP, "Geographic Distribution of Studies")
y = image(FIG / "fig3_geographic_map.png", x, y, COL_W)
y = caption(x, y + 0.05, COL_W,
            f"**Fig 3.** Included studies by region (N = {N}). 26 of 34 (76%) originated in "
            "Europe or North America; only 3 (9%) came from Africa or South America.", h=0.95)

y = header(c, y + 0.1, "Healthcare System Gaps (n = 18 studies, 53%)")
textbox(x, y, COL_W, 3.6, [
    "Delayed diagnosis in adolescence without concurrent psychosocial support",
    "Limited access to multidisciplinary care teams (psychology, social work, gynecology)",
    "Mental health insufficiently integrated into MRKH care models",
    "Lack of standardized mental health screening protocols at diagnosis",
], size=27, bullet=True, space_after=6)
y += 3.2

y = header(c, y, "Public Health Implications")
textbox(x, y, COL_W, 4.3, [
    "Integrate mental health screening into standard MRKH diagnostic pathways",
    "Develop multidisciplinary care protocols including psychology and social work",
    "Expand research investment in low- and middle-income and underrepresented settings",
    "Advocate for peer support infrastructure within reproductive health services",
    "Train providers in psychosocially informed MRKH care",
], size=27, bullet=True, space_after=6)
y += 4.0

y = header(c, y, "Limitations")
textbox(x, y, COL_W, 3.4, [
    "Review limited to 2019–2026; earlier foundational research not synthesized",
    "Heterogeneous designs and outcome measures limit direct comparison",
    "Most studies from high-income countries, limiting global generalizability",
    "Several studies relied on self-reported mental health outcomes",
], size=26, bullet=True, space_after=5)
y += 2.9

# Key takeaways callout (all figures derived from data.json)
kt_h = 3.6
rect(x, y, COL_W, kt_h, PANEL_WARM, line=ORANGE, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
top = dict(data["outcomes"])["Depression & anxiety"]
low_region = sum(n for _, n, code in data["regions"] if code in ("AF", "SA"))
textbox(x + 0.2, y + 0.1, COL_W - 0.4, kt_h - 0.2, [
    "**Key Takeaways**",
    f"•  About 3 in 4 studies ({top}/{N}) reported depression or anxiety",
    f"•  Coping strategies were documented in 21/{N} studies, yet remain unsupported by systematic clinical pathways",
    f"•  Only {low_region} of {N} studies came from Africa or South America",
], size=25, anchor=MSO_ANCHOR.MIDDLE, space_after=6)
col3_end = y + kt_h

# ------------------------------------------------------------------ conclusions (col 2 bottom)
x = COL_X[1]
y = col2_end + 0.15
y = header(1, y, "Conclusions")
concl_h = BOTTOM - y
rect(x, y, COL_W, concl_h, PANEL, line=NAVY, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
textbox(x + 0.2, y + 0.1, COL_W - 0.4, concl_h - 0.2, [
    "MRKH-related psychosocial burden is substantial yet under-integrated into care models. "
    "Depression, anxiety, reduced quality of life, and psychosexual challenges are frequently "
    "reported and co-occurring, while documented coping mechanisms remain unsupported by "
    "systematic clinical pathways.",
    "**Multidisciplinary, mental health–inclusive care and greater research investment are "
    "urgently needed**, particularly in underrepresented and low-resource settings.",
], size=25, anchor=MSO_ANCHOR.MIDDLE, space_after=10)

# ------------------------------------------------------------------ references + acknowledgements (col 3 bottom)
x = COL_X[2]
y = col3_end + 0.1
textbox(x, y, COL_W, BOTTOM - y, [
    "**References:** ^{1}Herlin M, et al. Hum Reprod. 2016;31(10):2384–2390. "
    "^{2}ACOG Committee Opinion No. 728. Obstet Gynecol. 2018;131(1):e35–e42. "
    "^{3}Arksey H, O'Malley L. Int J Soc Res Methodol. 2005;8(1):19–32. "
    "^{4}Tricco AC, et al. Ann Intern Med. 2018;169(7):467–473. "
    "^{5}Heller-Boersma JG, et al. Psychosomatics. 2009;50(3):277–281. "
    "^{6}Laggari V, et al. J Psychosom Obstet Gynaecol. 2009;30(2):83–88. "
    "^{7}Liao LM, et al. Am J Obstet Gynecol. 2011;205(2):117.e1–6. "
    "^{8}Facchin F, et al. J Health Psychol. 2021;26(1):26–39.",
    "**Acknowledgements:** Conducted under the mentorship of Dr. Paul Okojie and "
    "Dr. Robyn Anderson, Department of Public and Community Health, Liberty University. "
    "No external funding was received.",
], size=17, color=INK_2, space_after=4, line_spacing=1.0, anchor=MSO_ANCHOR.BOTTOM)

for name, end in (("col1", col1_end), ("col2", col2_end), ("col3", col3_end)):
    if end > BOTTOM:
        print(f"WARNING: {name} content ends at {end:.2f} in, past bottom {BOTTOM:.2f} in")
    else:
        print(f"{name}: ends at {end:.2f} in (bottom {BOTTOM:.2f})")

out = ROOT / "poster" / "MRKH_APHA2026_Poster.pptx"
out.parent.mkdir(exist_ok=True)
prs.save(out)
print("wrote", out)
