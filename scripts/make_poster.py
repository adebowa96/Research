"""Builds the 48 x 36 in APHA 2026 poster on the Liberty University poster template
(poster/template/liberty_poster_template.pptx, taken from the Liberty VPHA sample: title box,
logo, navy section headers, white text boxes, blue Methods table and centre figure panel).
Only the content is replaced; the template's layout and styling are kept.
Run make_figures.py and make_map.js first. Usage: python3 scripts/make_poster.py

Inline markup: **bold**, *italic*, ^{sup}."""
import json
import re
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_AUTO_SIZE, PP_ALIGN
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
COPE = dict(data["coping"])
FONT = "Times New Roman"
BLACK = RGBColor(0, 0, 0)
A_NS = "{http://schemas.openxmlformats.org/drawingml/2006/main}"


def pct(n):
    return f"{n / N:.0%}"


prs = Presentation(str(ROOT / "poster" / "template" / "liberty_poster_template.pptx"))
slide = prs.slides[0]


def find(name, shapes=None):
    for sh in shapes if shapes is not None else slide.shapes:
        if sh.name == name:
            return sh
        if sh.shape_type == 6:
            hit = find(name, sh.shapes)
            if hit is not None:
                return hit
    return None


TOKEN = re.compile(r"(\*\*.+?\*\*|\*.+?\*|\^\{.+?\})")


def add_runs(par, text, size, bold=False, color=BLACK):
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


def clear(tf):
    body = tf._txBody
    for p in list(body.findall(A_NS + "p"))[1:]:
        body.remove(p)
    for r in list(tf.paragraphs[0].runs):
        r._r.getparent().remove(r._r)


def fill(shape, paras, size=24, align=PP_ALIGN.JUSTIFY, space_after=4):
    """Replace a template text box's paragraphs, keeping the box itself (position, fill, border)."""
    tf = shape.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    clear(tf)
    for k, text in enumerate(paras):
        par = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
        par.alignment = PP_ALIGN.LEFT if text.startswith("•") else align
        par.space_after = Pt(space_after)
        par.line_spacing = 1.0
        add_runs(par, text, size)


def image_in(path, x, y, w, h):
    """Place an image centred inside the box (x, y, w, h), preserving aspect ratio."""
    with Image.open(path) as im:
        aspect = im.height / im.width
    iw, ih = (w, w * aspect) if w * aspect <= h else (h / aspect, h)
    slide.shapes.add_picture(str(path), Inches(x + (w - iw) / 2), Inches(y + (h - ih) / 2),
                             Inches(iw), Inches(ih))


def caption(x, y, w, h, text):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    add_runs(tf.paragraphs[0], text, 30)


# ------------------------------------------------------------------ title
tf = find("TextBox 3").text_frame
clear(tf)
lines = [("MENTAL HEALTH AND PSYCHOSOCIAL OUTCOMES AMONG INDIVIDUALS WITH", 52, True),
         ("MAYER-ROKITANSKY-KÜSTER-HAUSER (MRKH) SYNDROME: A SCOPING REVIEW", 52, True),
         ("Ifeoluwanimi P. Shobayo, BSc, MSPHc, Paul Okojie, PhD, Robyn Anderson, PhD", 44, False),
         ("Department of Public and Community Health, Liberty University", 34, False)]
for k, (text, size, bold) in enumerate(lines):
    par = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
    par.alignment = PP_ALIGN.CENTER
    par.line_spacing = 1.0
    add_runs(par, text, size, bold=bold)

# ------------------------------------------------------------------ left column
fill(find("TextBox 308"), [
    "**Background:** Mayer-Rokitansky-Küster-Hauser (MRKH) syndrome is a rare congenital "
    "condition (1 in 4,500–5,000 female births) characterized by uterovaginal agenesis in "
    "individuals with a 46,XX karyotype. Diagnosed in adolescence, it carries substantial "
    "psychosocial burden that remains insufficiently synthesized.",
    "**Methods:** Scoping review (Arksey & O'Malley; PRISMA-ScR) of PubMed, Scopus, and "
    "EBSCOhost databases, January 2019–March 2026.",
    f"**Results:** {N} studies were provisionally included. Psychosexual and relational "
    f"challenges were most frequent (n = {OUT['Psychosexual & relational challenges']}), "
    f"followed by psychological distress (n = {OUT['Broader psychological distress']}), reduced "
    f"QoL, body image and self-esteem (n = {OUT['QoL, body image & self-esteem']}), and "
    f"depression and anxiety (n = {OUT['Depression & anxiety']}). Coping was documented in "
    f"{OUT['Coping mechanisms documented']} studies; healthcare gaps in "
    f"{OUT['Healthcare system gaps']}.",
    "**Conclusion:** MRKH-related psychosocial burden is substantial yet under-integrated into "
    "care. *Results updated from the submitted abstract after final screening.*",
], size=24, space_after=4)

fill(find("TextBox 311"), [
    "**Introduction**",
    "MRKH syndrome is congenital absence of the uterus and upper vagina in individuals with a "
    "46,XX karyotype and functional ovaries, affecting about 1 in 4,500–5,000 female births.^{1,2} "
    "It is usually diagnosed in adolescence during evaluation for primary amenorrhea,^{1} a "
    "critical period for identity and social development. The diagnosis affects fertility, "
    "sexuality, and self-image, and psychosocial counseling is recommended as part of care,^{1} "
    "yet mental health outcomes remain insufficiently integrated into practice.",
    "**Objective**",
    "To map mental health outcomes, coping mechanisms, and healthcare system gaps reported in "
    "studies of individuals with MRKH published 2019–2026.",
    "**Research Question**",
    "What mental health outcomes and coping mechanisms are reported among individuals with "
    "MRKH syndrome, and what healthcare system gaps exist?",
], size=24, space_after=4)

methods = [
    ("METHOD", "DESCRIPTION"),
    ("Design", "Scoping review following Arksey & O'Malley's framework;^{3} reported per "
               "PRISMA-ScR^{4}"),
    ("Search", "PubMed; Scopus; EBSCOhost (MEDLINE, CINAHL, APA PsycInfo, Women's Studies "
               "International). Jan 2019–Mar 2026; run Mar 29, 2026"),
    ("Eligibility", "English-language primary quantitative, qualitative, or mixed-methods "
                    "studies reporting psychological outcomes or coping in MRKH; "
                    "surgical/fertility-only studies excluded"),
    ("Screening & Analysis", f"{P['identified']} records; {P['screened']} screened; "
                             f"{P['fulltext']} assessed; {N} included. AI-assisted screening "
                             "and abstract-level charting (verification in progress); "
                             "frequency counts and thematic grouping"),
]
table = find("Table 9").table
for r, (a, b) in enumerate(methods):
    for c, val in enumerate((a, b)):
        tfc = table.cell(r, c).text_frame
        clear(tfc)
        size = 30 if r == 0 else 23
        color = RGBColor(0xFF, 0xFF, 0xFF) if r == 0 else BLACK
        add_runs(tfc.paragraphs[0], val, size, bold=(r > 0 and c == 0), color=color)

# ------------------------------------------------------------------ right column
fill(find("Rectangle 326"), [
    "**Results**",
    f"Of {P['identified']} records, {P['screened']} were screened and {N} studies included: "
    f"{DES['Quantitative']} quantitative, {DES['Qualitative']} qualitative, "
    f"{DES['Mixed methods']} mixed-methods, 1 not reported. Studies came from Europe "
    f"({REG['Europe']}), Asia ({REG['Asia']}), North America ({REG['North America']}), Africa "
    f"({REG['Africa']}), and Oceania ({REG['Oceania']}); none from South America. "
    f"Psychosexual and relational challenges were most common "
    f"({pct(OUT['Psychosexual & relational challenges'])}); depression and anxiety were "
    f"measured least ({pct(OUT['Depression & anxiety'])}), with mixed findings.",
    "**Discussion**",
    "Findings align with earlier evidence^{5–7} and a prior review highlighting sexual esteem "
    "and genital image.^{8} Coping relied on peer support and self-management; only "
    f"{COPE['Psychological counseling/intervention']} studies tested interventions. Healthcare "
    "gaps included providers' limited knowledge of MRKH and insensitive communication at "
    "diagnosis.",
    "**Conclusion**",
    "Psychosocial burden in MRKH is substantial yet under-integrated into care; "
    "multidisciplinary, mental health–inclusive care is needed.",
], size=24, space_after=4)

fill(find("TextBox 13"), [
    "**Limitations**",
    "• Provisional: AI-assisted screening and abstract-level charting pending full-text "
    "verification",
    "• Review limited to 2019–2026; heterogeneous designs and measures",
    "• Few studies from Africa or Oceania; none from South America",
], size=23, space_after=3)

fill(find("TextBox 320"), [
    "**Public Health Implications**",
    "• Integrate psychosocial support and mental health screening at diagnosis",
    "• Build multidisciplinary teams with psychology and social work",
    "• Pair vaginal lengthening treatment with psychosexual counseling",
    "• Train providers in sensitive, non-stigmatizing communication",
    "**Future Work**",
    "• Longitudinal studies with validated measures",
    "• Trials of psychosocial interventions in routine care",
    "• Research in underrepresented and low-resource settings",
], size=24, space_after=3)

# References (text box in place of the sample's QR code)
refs = slide.shapes.add_textbox(Inches(37.28), Inches(30.3), Inches(10.0), Inches(5.3))
refs.fill.solid()
refs.fill.fore_color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
rtf = refs.text_frame
rtf.word_wrap = True
rtf.auto_size = MSO_AUTO_SIZE.NONE
rtf.margin_left = rtf.margin_right = Inches(0.12)
for k, ref in enumerate([
    "1. ACOG Committee Opinion No. 728. *Obstet Gynecol*. 2018;131(1):e35-e42.",
    "2. Herlin M, et al. *Hum Reprod*. 2016;31(10):2384-2390.",
    "3. Arksey H, O'Malley L. *Int J Soc Res Methodol*. 2005;8(1):19-32.",
    "4. Tricco AC, et al. *Ann Intern Med*. 2018;169(7):467-473.",
    "5. Heller-Boersma JG, et al. *Psychosomatics*. 2009;50(3):277-281.",
    "6. Laggari V, et al. *J Psychosom Obstet Gynaecol*. 2009;30(2):83-88.",
    "7. Liao LM, et al. *Am J Obstet Gynecol*. 2011;205(2):117.e1-117.e6.",
    "8. Facchin F, et al. *J Health Psychol*. 2021;26(1):26-39.",
    f"Full list of the {N} included studies available on request.",
    "**Acknowledgements:** Mentorship by Dr. Paul Okojie and Dr. Robyn Anderson. No external "
    "funding.",
]):
    par = rtf.paragraphs[0] if k == 0 else rtf.add_paragraph()
    par.space_after = Pt(2)
    add_runs(par, ref, 18)

# ------------------------------------------------------------------ centre figures
# slot geometry follows the sample poster's figure positions
image_in(FIG / "fig1_outcomes_bar.png", 12.3, 5.0, 23.9, 9.9)
caption(12.41, 15.0, 23.8, 0.7,
        f"Figure 1. Frequency of Outcome Domains Across Included Studies (N = {N}); studies "
        "could report more than one domain")
slots = [  # image box, caption box, figure file, caption
    ((12.22, 16.0, 11.2, 8.3), (12.22, 24.4, 11.2, 1.2), "prisma_flow.png",
     "Figure 2. PRISMA-ScR Flow Diagram of Study Selection (provisional)"),
    ((24.15, 16.3, 11.9, 7.9), (24.15, 24.4, 11.9, 1.2), "fig3_geographic_map.png",
     f"Figure 3. Geographic Distribution of Included Studies (N = {N})"),
    ((12.22, 26.0, 11.2, 8.0), (12.22, 34.1, 11.2, 1.2), "fig2_design_donut.png",
     f"Figure 4. Study Design Distribution (N = {N})"),
    ((24.15, 26.0, 11.9, 8.0), (24.15, 34.1, 11.9, 1.2), "fig5_coping_bar.png",
     f"Figure 5. Coping Mechanisms Documented ({OUT['Coping mechanisms documented']} studies)"),
]
for (ix, iy, iw, ih), (cx, cy, cw, ch), fname, text in slots:
    image_in(FIG / fname, ix, iy, iw, ih)
    caption(cx, cy, cw, ch, text)

out = ROOT / "poster" / "MRKH_APHA2026_Poster.pptx"
prs.save(out)
print("wrote", out)
