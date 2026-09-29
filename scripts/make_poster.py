"""Builds the 48 x 36 in APHA 2026 poster on the Liberty University template
(poster/template/liberty_template.pptx: navy background + Liberty logo).
Output: poster/MRKH_APHA2026_Poster.pptx. Run make_figures.py and make_map.js first.

Inline markup in poster text: **bold**, *italic*, ^{sup} superscript."""
import json
import re
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.util import Inches, Pt

HERE = Path(__file__).parent
ROOT = HERE.parent
FIG = ROOT / "figures"
data = json.loads((HERE / "data.json").read_text())
N = data["total_included"]
P = data["prisma"]
OUT = dict(data["outcomes"])
DES = {name: n for name, n, _ in data["designs"]}
REG = {name: n for name, n, _ in data["regions"]}

NAVY = RGBColor(0x0A, 0x25, 0x4E)  # Liberty template header navy
BLUE = RGBColor(0x2A, 0x78, 0xD6)
ORANGE = RGBColor(0xC4, 0x4E, 0x1B)
PANEL = RGBColor(0xEE, 0xF4, 0xFC)
PANEL_WARM = RGBColor(0xFD, 0xEE, 0xE7)
BLACK = RGBColor(0, 0, 0)
GREY = RGBColor(0x40, 0x40, 0x40)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
FONT = "Times New Roman"

# Column geometry taken from the Liberty sample poster
LEFT_X, LEFT_W = 0.55, 11.25
MID_X, MID_W = 12.23, 24.54
RIGHT_X, RIGHT_W = 37.12, 10.5
TOP = 6.95
BOTTOM = 35.75

prs = Presentation(str(ROOT / "poster" / "template" / "liberty_template.pptx"))
slide = prs.slides[0]
logo = slide.shapes[0]

TOKEN = re.compile(r"(\*\*.+?\*\*|\*.+?\*|\^\{.+?\})")


def add_runs(par, text, size, color=BLACK, bold=False):
    for piece in TOKEN.split(text):
        if not piece:
            continue
        b, i, sup = bold, False, False
        if piece.startswith("**"):
            piece, b = piece[2:-2], True
        elif piece.startswith("^{"):
            piece, sup = piece[2:-1], True
        elif piece.startswith("*"):
            piece, i = piece[1:-1], True
        run = par.add_run()
        run.text = piece
        f = run.font
        f.name, f.size, f.bold, f.italic = FONT, Pt(size), b, i
        f.color.rgb = color
        if sup:
            f._element.set("baseline", "30000")


def box(x, y, w, h, fill=WHITE, line=WHITE, shape=MSO_SHAPE.RECTANGLE, line_w=1.5):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.solid()
    s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
        s.line.width = Pt(line_w)
    s.shadow.inherit = False
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = 0.12
    return s


def text(x, y, w, h, paras, size=22, color=BLACK, align=PP_ALIGN.JUSTIFY,
         anchor=MSO_ANCHOR.TOP, space_after=6, fill=None, bullet=False, margin=0.14):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is not None:
        tb.fill.solid()
        tb.fill.fore_color.rgb = fill
        tb.line.color.rgb = WHITE
    tf = tb.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Inches(margin)
    tf.margin_top = tf.margin_bottom = Inches(0.08)
    for k, ptxt in enumerate(paras):
        par = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
        par.alignment = align
        par.space_after = Pt(space_after)
        par.line_spacing = 1.0
        if bullet and not ptxt.startswith("**"):
            ptxt = "•  " + ptxt
        add_runs(par, ptxt, size, color)
    return tb


def header(x, y, w, title, size=48):
    text(x, y, w, 0.95, [title], size=size, color=WHITE, align=PP_ALIGN.CENTER,
         anchor=MSO_ANCHOR.MIDDLE, space_after=0, fill=NAVY)
    return y + 0.95


def image(path, x, y, w=None, h=None):
    with Image.open(path) as im:
        aspect = im.height / im.width
    if w is None:
        w = h / aspect
    h = w * aspect
    slide.shapes.add_picture(str(path), Inches(x), Inches(y), Inches(w), Inches(h))
    return w, h


def caption(x, y, w, title, sub, size=22):
    tb = text(x, y, w, 1.0, [f"**{title}**", sub], size=size, align=PP_ALIGN.LEFT,
              space_after=0, margin=0.05)
    return tb


# ---------------------------------------------------------------- title band
box(0, 0, 48, 6.9, fill=WHITE, line=None)
text(6.6, 0.25, 40.8, 6.4, [
    "**Mental Health and Psychosocial Outcomes Among Individuals With**",
    "**Mayer-Rokitansky-Küster-Hauser (MRKH) Syndrome: A Scoping Review**",
], size=64, align=PP_ALIGN.CENTER, space_after=0)
text(6.6, 2.75, 40.8, 1.0,
     ["Ifeoluwanimi P. Shobayo, BSc, MSPHc, Paul Okojie, PhD, Robyn Anderson, PhD"],
     size=45, align=PP_ALIGN.CENTER, space_after=0)
text(6.6, 3.75, 40.8, 1.8, [
    "Department of Public and Community Health, Liberty University",
    "APHA 2026 Annual Meeting & Expo · Sexual and Reproductive Health Section",
], size=34, color=GREY, align=PP_ALIGN.CENTER, space_after=0)
# bring the Liberty logo above the white title band
logo._element.getparent().remove(logo._element)
slide.shapes._spTree.append(logo._element)

# ---------------------------------------------------------------- left column
y = header(LEFT_X, TOP, LEFT_W, "Abstract")
abstract_h = 8.35
text(LEFT_X, y, LEFT_W, abstract_h, [
    "**Background:** Mayer-Rokitansky-Küster-Hauser (MRKH) syndrome is a rare congenital "
    "condition (1 in 4,500–5,000 female births) characterized by uterovaginal agenesis in "
    "individuals with a 46,XX karyotype and functional ovaries. Diagnosed during adolescence, "
    "MRKH is associated with significant psychosocial burden. Mental health outcomes and coping "
    "mechanisms remain insufficiently synthesized, limiting integration into clinical care and "
    "public health planning.",
    "**Methods:** Following Arksey and O'Malley's framework and PRISMA-ScR guidelines, we "
    "searched PubMed/MEDLINE, Scopus, PsycINFO, and CINAHL (January 2019–March 2026). Eligible "
    "studies included primary quantitative, qualitative, and mixed-methods research on "
    "psychological outcomes and/or coping mechanisms in MRKH populations.",
    f"**Results:** {N} studies met inclusion criteria. Depression and anxiety were most "
    f"frequently reported (n = {OUT['Depression & anxiety']}), followed by reduced QoL and body "
    f"image concerns (n = {OUT['Reduced QoL & body image']}), psychosexual challenges "
    f"(n = {OUT['Psychosexual & relational challenges']}), and psychological distress "
    f"(n = {OUT['Broader psychological distress']}). Coping mechanisms were documented in "
    f"{OUT['Coping mechanisms documented']} studies; healthcare gaps in "
    f"{OUT['Healthcare system gaps']}.",
    "**Conclusions:** MRKH-related psychosocial burden is substantial yet under-integrated into "
    "care models. Multidisciplinary, mental health-inclusive care and greater research "
    "investment are urgently needed.",
    "**Keywords:** MRKH syndrome; mental health; coping; psychosocial outcomes; quality of "
    "life; reproductive health",
], size=23, fill=WHITE, space_after=5)
y += abstract_h + 0.25

y = header(LEFT_X, y, LEFT_W, "Introduction and Research Question", size=40)
intro_h = 9.0
text(LEFT_X, y, LEFT_W, intro_h, [
    "MRKH syndrome is a rare Müllerian aplasia resulting in congenital absence of the uterus and "
    "upper two-thirds of the vagina in chromosomally female individuals (46,XX) with functional "
    "ovaries. It affects approximately 1 in 4,500–5,000 female births^{1,2} and is typically "
    "diagnosed during adolescence, often during evaluation for primary amenorrhea^{1}—a critical "
    "period for identity formation and social development.",
    "The diagnosis carries profound implications for fertility, psychosexual development, and "
    "self-image. Professional guidance identifies psychosocial counseling as a key component of "
    "care,^{1} yet psychosocial outcomes remain underexplored and insufficiently integrated into "
    "clinical and public health frameworks.",
    "**Research Question**",
    "What mental health outcomes and coping mechanisms are reported among individuals with MRKH "
    "syndrome, and what healthcare system gaps exist?",
    "**Learning Objectives**",
    "1. Identify key mental health outcomes—including depression, anxiety, reduced quality of "
    "life, and psychosexual challenges—reported among individuals with MRKH syndrome.",
    "2. Describe coping mechanisms and psychosocial responses, including adaptive and "
    "maladaptive strategies, documented in MRKH populations.",
], size=23, fill=WHITE, space_after=6)
y += intro_h + 0.25

y = header(LEFT_X, y, LEFT_W, "Methods")
methods = [
    ("Study Design", "Scoping review following Arksey & O'Malley's five-stage framework^{3}; "
                     "reported per PRISMA-ScR^{4}"),
    ("Databases", "PubMed; Scopus; EBSCOhost (MEDLINE, CINAHL, APA PsycInfo, Women's "
                  "Studies International)"),
    ("Years Included", "January 2019 – March 2026 (earlier records removed at screening); "
                       "searches run March 29, 2026"),
    ("Inclusion Criteria", "Primary quantitative, qualitative, and mixed-methods studies "
                           "reporting psychological outcomes and/or coping mechanisms in MRKH"),
    ("Exclusion Criteria", "Studies focused solely on anatomical, surgical, or fertility outcomes"),
    ("Screening", f"{P['identified']} records identified; {P['duplicates_removed']} duplicates "
                  f"removed; {P['screened']} screened; {P['excluded']} excluded; "
                  f"{P['included']} included"),
    ("Synthesis", "Descriptive frequency counts by outcome domain and thematic grouping of "
                  "coping mechanisms and healthcare gaps"),
]
tbl_h = BOTTOM - y
gt = slide.shapes.add_table(len(methods) + 1, 2, Inches(LEFT_X), Inches(y), Inches(LEFT_W),
                            Inches(tbl_h))
tbl = gt.table
tbl.columns[0].width = Inches(3.4)
tbl.columns[1].width = Inches(LEFT_W - 3.4)
tbl.first_row = True
for r, (a, b) in enumerate([("Category", "Description")] + methods):
    for c, val in enumerate((a, b)):
        cell = tbl.cell(r, c)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY if r == 0 else (WHITE if r % 2 else PANEL)
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        cell.margin_left = cell.margin_right = Inches(0.1)
        tf = cell.text_frame
        tf.word_wrap = True
        par = tf.paragraphs[0]
        add_runs(par, val, 20, WHITE if r == 0 else BLACK, bold=(r == 0 or c == 0))
for r in range(len(methods) + 1):
    tbl.rows[r].height = Inches(tbl_h / (len(methods) + 1))

# ---------------------------------------------------------------- centre panel (figures)
box(MID_X, TOP, MID_W, BOTTOM - TOP, fill=WHITE, line=WHITE)
cx = MID_X + 0.4
cw = MID_W - 0.8
y = TOP + 0.3

# MRKH at a glance strip
text(cx, y, cw, 0.75, ["**MRKH Syndrome at a Glance**"], size=32, color=NAVY,
     align=PP_ALIGN.CENTER, space_after=0)
y += 0.85
tiles = [("~1 in 5,000", "female births"), ("46,XX", "karyotype; functional ovaries"),
         ("Adolescence", "typical age at diagnosis"), ("No uterus", "uterovaginal agenesis")]
gap = 0.35
tw = (cw - 3 * gap) / 4
for k, (big, small) in enumerate(tiles):
    tx = cx + k * (tw + gap)
    box(tx, y, tw, 1.95, fill=PANEL, line=BLUE, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    text(tx, y + 0.12, tw, 0.9, [f"**{big}**"], size=38, color=NAVY, align=PP_ALIGN.CENTER,
         anchor=MSO_ANCHOR.MIDDLE, space_after=0)
    text(tx, y + 1.0, tw, 0.8, [small], size=22, color=GREY, align=PP_ALIGN.CENTER,
         space_after=0)
y += 2.35

# Row: PRISMA (left) | outcomes bar chart + coping (right)
row_top = y
pw, ph = image(FIG / "prisma_flow.png", cx, y, w=10.4)
caption(cx, y + ph + 0.1, pw, "Fig 1: PRISMA-ScR Flow Diagram",
        "(Adapted from Tricco et al., 2018)")
rx = cx + pw + 0.5
rw = cx + cw - rx
text(rx, y, rw, 0.7, ["**Key Findings From Included Studies (2019–2026)**"], size=28,
     color=NAVY, align=PP_ALIGN.CENTER, space_after=0)
bw, bh = image(FIG / "fig1_outcomes_bar.png", rx, y + 0.8, w=rw)
caption(rx, y + 0.8 + bh + 0.05, rw, "Fig 2: Frequency of Outcome Domains (N = 34)",
        "Studies could report more than one domain")
y2 = y + 0.8 + bh + 1.2
text(rx, y2, rw, 0.6, [f"**Coping Mechanisms Documented (n = "
                       f"{OUT['Coping mechanisms documented']} studies)**"],
     size=26, color=NAVY, align=PP_ALIGN.CENTER, space_after=0)
y2 += 0.7
chips = [("Peer & community support", False), ("Psychological counseling", False),
         ("Identity reconstruction", False), ("Spiritual coping", False),
         ("Adaptive acceptance", False), ("Avoidance (maladaptive)", True)]
chw = (rw - 2 * 0.25) / 3
for k, (label, bad) in enumerate(chips):
    chx = rx + (k % 3) * (chw + 0.25)
    chy = y2 + (k // 3) * 0.95
    box(chx, chy, chw, 0.78, fill=PANEL_WARM if bad else PANEL, line=ORANGE if bad else BLUE,
        shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    text(chx, chy, chw, 0.78, [label], size=21, color=ORANGE if bad else NAVY,
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, space_after=0, margin=0.05)
right_end = y2 + 2 * 0.95
y = max(row_top + ph + 1.2, right_end) + 1.3

# Row: map (left) | design donut (right)
mw, mh = image(FIG / "fig3_geographic_map.png", cx, y + 0.3, w=15.6)
caption(cx, y + 0.3 + mh + 0.1, mw, "Fig 3: Geographic Distribution of Included Studies",
        f"{REG['Europe'] + REG['North America']} of {N} studies (76%) from Europe or North "
        f"America; {REG['Africa'] + REG['South America']} from Africa or South America")
dx = cx + mw + 0.4
dw_, dh = image(FIG / "fig2_design_donut.png", dx, y + 1.3, w=cx + cw - dx)
caption(dx, y + 1.3 + dh + 0.1, dw_, "Fig 4: Study Design Distribution",
        "Cross-sectional studies (n = 11) are a subset of quantitative designs")
centre_end = y + 0.3 + mh + 1.2

# ---------------------------------------------------------------- right column
y = header(RIGHT_X, TOP, RIGHT_W, "Results, Discussion and Conclusion", size=38)
rdc_h = 11.3
text(RIGHT_X, y, RIGHT_W, rdc_h, [
    "**Results**",
    f"Of {P['identified']} records identified, {P['screened']} remained after deduplication and "
    f"{N} studies met inclusion criteria: {DES['Quantitative']} quantitative (11 "
    f"cross-sectional), {DES['Qualitative']} qualitative, and {DES['Mixed methods']} "
    f"mixed-methods. Depression and anxiety were reported in {OUT['Depression & anxiety']} "
    f"studies (76%), reduced QoL and body image in {OUT['Reduced QoL & body image']} (65%), "
    f"psychosexual and relational challenges in {OUT['Psychosexual & relational challenges']} "
    f"(56%), and broader distress in {OUT['Broader psychological distress']} (50%). "
    f"Healthcare system gaps were identified in {OUT['Healthcare system gaps']} studies (53%): "
    "delayed diagnosis without psychosocial support, limited multidisciplinary care, mental "
    "health insufficiently integrated into care models, and no standardized screening at "
    "diagnosis.",
    "**Discussion**",
    "These findings are consistent with earlier evidence of elevated distress, anxiety, and "
    "poorer mental health-related quality of life in MRKH^{5–7} and with a prior systematic "
    "review.^{8} Coping strategies were documented in most studies but remain unsupported by "
    "systematic clinical pathways, and 76% of studies came from Europe or North America, "
    "leaving low-resource settings underrepresented.",
    "**Conclusion**",
    "MRKH-related psychosocial burden is substantial yet under-integrated into care models. "
    "Multidisciplinary, mental health-inclusive care and greater research investment are "
    "urgently needed, particularly in underrepresented and low-resource settings.",
], size=25, fill=WHITE, space_after=6)
y += rdc_h + 0.25

y = header(RIGHT_X, y, RIGHT_W, "Limitations")
lim_h = 3.6
text(RIGHT_X, y, RIGHT_W, lim_h, [
    "Review limited to 2019–2026, potentially excluding earlier foundational research",
    "Heterogeneous designs and outcome measures limit direct comparisons",
    "Most studies from high-income countries, limiting global generalizability",
    "Some studies relied on self-reported mental health outcomes",
], size=24, fill=WHITE, bullet=True, space_after=4, align=PP_ALIGN.LEFT)
y += lim_h + 0.25

y = header(RIGHT_X, y, RIGHT_W, "Public Health Implications", size=40)
imp_h = 4.5
text(RIGHT_X, y, RIGHT_W, imp_h, [
    "Integrate mental health screening into MRKH diagnostic pathways",
    "Develop multidisciplinary care protocols including psychology and social work",
    "Expand research investment in LMIC and underrepresented settings",
    "Build peer support infrastructure within reproductive health services",
    "Train providers in psychosocially informed MRKH care",
], size=24, fill=WHITE, bullet=True, space_after=4, align=PP_ALIGN.LEFT)
y += imp_h + 0.25

y = header(RIGHT_X, y, RIGHT_W, "References")
text(RIGHT_X, y, RIGHT_W, BOTTOM - y, [
    "1. ACOG Committee Opinion No. 728. *Obstet Gynecol*. 2018;131(1):e35–e42.",
    "2. Herlin M, et al. *Hum Reprod*. 2016;31(10):2384–2390.",
    "3. Arksey H, O'Malley L. *Int J Soc Res Methodol*. 2005;8(1):19–32.",
    "4. Tricco AC, et al. *Ann Intern Med*. 2018;169(7):467–473.",
    "5. Heller-Boersma JG, et al. *Psychosomatics*. 2009;50(3):277–281.",
    "6. Laggari V, et al. *J Psychosom Obstet Gynaecol*. 2009;30(2):83–88.",
    "7. Liao LM, et al. *Am J Obstet Gynecol*. 2011;205(2):117.e1–6.",
    "8. Facchin F, et al. *J Health Psychol*. 2021;26(1):26–39.",
    "**Acknowledgements:** Mentorship by Dr. Paul Okojie and Dr. Robyn Anderson. "
    "No external funding.",
], size=18, fill=WHITE, space_after=2, align=PP_ALIGN.LEFT)

for name, end in (("centre", centre_end), ("right", y)):
    flag = "WARNING past bottom" if end > BOTTOM else "ok"
    print(f"{name}: {end:.2f} in ({flag})")

out = ROOT / "poster" / "MRKH_APHA2026_Poster.pptx"
prs.save(out)
print("wrote", out)
