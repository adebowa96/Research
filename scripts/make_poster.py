"""Builds the 48 x 36 in APHA 2026 poster on the Liberty University poster template
(poster/template/liberty_poster_template.pptx, taken from the Liberty VPHA sample: title box,
logo, navy section headers, white text boxes, blue Methods table and centre figure panel).
The template's styling is kept; the right column is re-spaced to fit the text and references.
Run make_figures.py and make_map.js first. Usage: python3 scripts/make_poster.py

Inline markup: **bold**, *italic*, ^{sup}. Citations are written ^{@key} and numbered in AMA
style in order of first appearance on the poster (separately from the manuscript); the
References box lists them in the same order. Also writes poster/Poster_Full_Reference_List.docx
(poster references plus every included study) for the QR code."""
import json
import re
import sys
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.util import Inches, Pt

HERE = Path(__file__).parent
ROOT = HERE.parent
FIG = ROOT / "figures"
sys.path.insert(0, str(HERE))
from citations import Citer  # noqa: E402

data = json.loads((HERE / "data.json").read_text())
N = data["total_included"]
P = data["prisma"]
OUT = dict(data["outcomes"])
DES = {name: n for name, n, _ in data["designs"]}
REG = {name: n for name, n, _ in data["regions"]}
COPE = dict(data["coping"])
FT = data["full_text_checked"]
FONT = "Times New Roman"
BODY = 22
BLACK = RGBColor(0, 0, 0)
A_NS = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
CITER = Citer()

assert COPE["Peer, family & social support"] == 7 and COPE["Psychological counseling/intervention"] == 2


def pct(n):
    return f"{n / N:.0%}"


prs = Presentation(str(ROOT / "poster" / "template" / "liberty_poster_template.pptx"))
slide = prs.slides[0]


def ungroup_all():
    """Move grouped template shapes onto the slide, converting their coordinates, so the
    right-column boxes can be re-spaced."""
    tree = slide.shapes._spTree
    for g in [sh for sh in slide.shapes if sh.shape_type == 6]:
        gx = g._element.grpSpPr.find(A_NS + "xfrm")
        off, ext, choff, chext = (gx.find(A_NS + t) for t in ("off", "ext", "chOff", "chExt"))
        ox, oy = int(off.get("x")), int(off.get("y"))
        sx = int(ext.get("cx")) / int(chext.get("cx"))
        sy = int(ext.get("cy")) / int(chext.get("cy"))
        cx0, cy0 = int(choff.get("x")), int(choff.get("y"))
        idx = list(tree).index(g._element)
        for ch in list(g.shapes):
            xf = ch._element.find(".//" + A_NS + "xfrm")
            o, e = xf.find(A_NS + "off"), xf.find(A_NS + "ext")
            o.set("x", str(round(ox + (int(o.get("x")) - cx0) * sx)))
            o.set("y", str(round(oy + (int(o.get("y")) - cy0) * sy)))
            e.set("cx", str(round(int(e.get("cx")) * sx)))
            e.set("cy", str(round(int(e.get("cy")) * sy)))
            tree.insert(idx, ch._element)
            idx += 1
        tree.remove(g._element)


ungroup_all()


def find(name):
    for sh in slide.shapes:
        if sh.name == name:
            return sh
    raise KeyError(name)


def place(shape, x, y, w, h):
    shape.left, shape.top, shape.width, shape.height = Inches(x), Inches(y), Inches(w), Inches(h)


TOKEN = re.compile(r"(\*\*.+?\*\*|\*.+?\*|\^\{.+?\})")


def add_runs(par, text, size, bold=False, color=BLACK):
    text = CITER.resolve(text)
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


def fill(shape, paras, size=BODY, align=PP_ALIGN.JUSTIFY, space_after=4):
    """Replace a template text box's paragraphs, keeping the box itself (position, fill, border).
    Paragraphs starting with '• ' become hanging-indent bullets."""
    tf = shape.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.vertical_anchor = MSO_ANCHOR.TOP
    clear(tf)
    for k, text in enumerate(paras):
        par = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
        par.space_after = Pt(space_after)
        par.line_spacing = 1.0
        if text.startswith("• "):
            par.alignment = PP_ALIGN.LEFT
            pPr = par._p.get_or_add_pPr()
            pPr.set("marL", str(Inches(0.3)))
            pPr.set("indent", str(-Inches(0.3)))
            text = "• " + text[2:]
        else:
            par.alignment = align
        add_runs(par, text, size)


def set_header(shape, text):
    """Change a navy section header's text, keeping the template's run formatting."""
    tf = shape.text_frame
    body = tf._txBody
    for p in list(body.findall(A_NS + "p"))[1:]:
        body.remove(p)
    runs = tf.paragraphs[0].runs
    runs[0].text = text
    runs[0].font.name, runs[0].font.size = FONT, Pt(48)
    for r in runs[1:]:
        r._r.getparent().remove(r._r)
    for br in tf.paragraphs[0]._p.findall(A_NS + "br"):
        tf.paragraphs[0]._p.remove(br)


def image_in(path, x, y, w, h):
    """Place an image centred inside the box (x, y, w, h), preserving aspect ratio."""
    with Image.open(path) as im:
        aspect = im.height / im.width
    iw, ih = (w, w * aspect) if w * aspect <= h else (h / aspect, h)
    slide.shapes.add_picture(str(path), Inches(x + (w - iw) / 2), Inches(y + (h - ih) / 2),
                             Inches(iw), Inches(ih))


def caption(x, y, w, h, text, size=26):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    add_runs(tf.paragraphs[0], text, size)


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
    "individuals with a 46,XX karyotype. Usually diagnosed in adolescence, it affects fertility, "
    "sexuality, and identity, yet its mental health consequences remain insufficiently "
    "synthesized.",
    "**Methods:** Scoping review (Arksey & O'Malley; PRISMA-ScR) of PubMed, Scopus, and "
    "EBSCOhost databases (MEDLINE, CINAHL, APA PsycInfo, Women's Studies International), "
    "January 2019–March 2026.",
    f"**Results:** Of {P['identified']} records, {N} studies were included. Psychosexual and "
    f"relational challenges were most frequent (n = {OUT['Psychosexual & relational challenges']}), "
    f"followed by psychological distress (n = {OUT['Broader psychological distress']}), reduced "
    f"QoL, body image, and self-esteem (n = {OUT['QoL, body image & self-esteem']}), and "
    f"depression and anxiety (n = {OUT['Depression & anxiety']}). Coping was documented in "
    f"{OUT['Coping mechanisms documented']} studies, mostly peer support; healthcare gaps in "
    f"{OUT['Healthcare system gaps']}.",
    "**Conclusion:** MRKH-related psychosocial burden is substantial yet under-integrated into "
    "care. Psychosocial screening, psychosexual counseling, and peer support belong in MRKH "
    "care pathways.",
])

fill(find("TextBox 311"), [
    "**Introduction**",
    "MRKH syndrome is the congenital absence of the uterus and upper vagina in individuals with "
    "a 46,XX karyotype and functioning ovaries, affecting about 1 in 4,500–5,000 female "
    "births.^{@acog,@herlin16} It is usually diagnosed in adolescence during evaluation of "
    "primary amenorrhea,^{@acog} a sensitive period for identity, sexuality, and relationships. "
    "Earlier studies linked MRKH with psychological distress, anxiety, and reduced quality of "
    "life,^{@hb09,@laggari,@liao} and guidelines recommend psychosocial counseling as part of "
    "care.^{@acog} Prior reviews focused on psychological and sexual outcomes;^{@facchin,@tsarna} "
    "coping and healthcare system gaps have not been mapped across the growing recent literature. "
    "Mapping this evidence can guide psychosocial care, provider training, and research priorities.",
    "**Objective**",
    "To map mental health and psychosocial outcomes, coping mechanisms, and healthcare system "
    "gaps reported in studies of individuals with MRKH published 2019–2026.",
    "**Research Question**",
    "What mental health outcomes and coping mechanisms are reported among individuals with "
    "MRKH syndrome, and what healthcare system gaps exist?",
])

methods = [
    ("METHOD", "DESCRIPTION"),
    ("Design", "Scoping review using Arksey & O'Malley's five-stage framework^{@arksey} and "
               "PRISMA-ScR reporting guidance.^{@tricco} Framed by population (individuals "
               "with MRKH), concept (mental health, coping, care gaps), and context (any "
               "setting). No quality appraisal, consistent with scoping methodology."),
    ("Search", "PubMed; Scopus; EBSCOhost (MEDLINE, CINAHL, APA PsycInfo, Women's Studies "
               "International). January 2019–March 2026; exported March 29, 2026. Terms "
               "combined MRKH and Müllerian agenesis with mental health, psychosocial, and coping "
               "concepts."),
    ("Eligibility", "**Included:** English-language primary quantitative, qualitative, or "
                    "mixed-methods studies reporting psychological outcomes or coping in MRKH; "
                    "mixed samples only if MRKH results were reported separately or ≥80% had MRKH. "
                    "**Excluded:** reviews, case reports, and studies of surgical, anatomical, or "
                    "fertility outcomes only."),
    ("Screening & Analysis", f"{P['identified']} records; {P['duplicates_removed']} duplicates "
                             f"removed; {P['screened']} titles and abstracts screened; "
                             f"{P['fulltext']} assessed; {N} included (Figure 2). AI-assisted "
                             f"screening and charting, checked against full text for {FT} of "
                             f"{N} studies. Charted design, country, sample, outcomes, coping, "
                             "and healthcare gaps; synthesized with frequency counts and "
                             "thematic grouping into 6 domains (Figure 1)."),
]
table = find("Table 9").table
table.columns[0].width = Inches(2.55)
table.columns[1].width = Inches(7.91)
for r, h in enumerate([0.66, 2.62, 2.2, 3.0, 3.1]):
    table.rows[r].height = Inches(h)
for r, (a, b) in enumerate(methods):
    for c, val in enumerate((a, b)):
        tfc = table.cell(r, c).text_frame
        tfc.word_wrap = True
        clear(tfc)
        size = 28 if r == 0 else 24
        color = RGBColor(0xFF, 0xFF, 0xFF) if r == 0 else BLACK
        tfc.paragraphs[0].alignment = PP_ALIGN.LEFT
        add_runs(tfc.paragraphs[0], val, size, bold=(r > 0 and c == 0), color=color)

# ------------------------------------------------------------------ right column
X, W = 37.19, 10.12
S, Q, G, D = (OUT["Psychosexual & relational challenges"], OUT["QoL, body image & self-esteem"],
              OUT["Broader psychological distress"], OUT["Depression & anxiety"])
C, H = OUT["Coping mechanisms documented"], OUT["Healthcare system gaps"]

set_header(find("TextBox 325"), "Results and Discussion")
place(find("TextBox 325"), X, 4.62, W, 0.95)
place(find("TextBox 324"), X, 5.57, W, 14.33)
place(find("Rectangle 326"), X + 0.12, 5.62, W - 0.24, 14.23)
fill(find("Rectangle 326"), [
    "**Key Findings**",
    f"{N} studies from 2019–2026 were included ({DES['Quantitative']} quantitative, "
    f"{DES['Qualitative']} qualitative, {DES['Mixed methods']} mixed-methods), with samples of "
    f"5 to 616 participants (Figures 1–5).",
    f"• **Psychosexual and relational ({pct(S)}):** lower sexual esteem and more negative genital "
    "self-image than controls, even after neovagina creation.^{@R003,@R091}",
    f"• **Psychological distress ({pct(G)}):** shock, grief, shame, and secrecy at diagnosis; "
    "the diagnostic process itself was described as upsetting and potentially "
    "traumatizing.^{@R011,@R267}",
    f"• **QoL, body image, and self-esteem ({pct(Q)}):** impaired mental health–related quality "
    "of life,^{@R021} and higher distress with lower self-esteem than population norms.^{@R105}",
    f"• **Depression and anxiety ({pct(D)}):** depressive symptoms in 75.2% of 141 Chinese "
    "patients;^{@R104} anxiety in 37.7% and depression in 32.5% of 77 Malaysian women.^{@R004} "
    "Findings were mixed: uterus transplant candidates in France showed few symptoms.^{@R020}",
    f"• **Coping ({pct(C)}):** peer and online support most common; avoidance and concealment "
    f"also frequent, and one study traced a shift from avoidance to empowerment.^{{@R032}} Only {COPE['Psychological counseling/intervention']} "
    "intervention studies were found, both reporting benefit.^{@R038,@R131}",
    f"• **Healthcare gaps ({pct(H)}):** delayed diagnosis, providers unfamiliar with MRKH, and "
    "patients forced to self-advocate.^{@R073,@R149}",
    "**Discussion**",
    "Findings echo earlier evidence of distress and reduced quality of life in MRKH^{@hb09,@liao} "
    "and extend prior reviews by mapping coping and health-system gaps. Structured support can "
    "help (group cognitive-behavioral therapy improved psychological outcomes in an earlier "
    "trial^{@hb07}), yet few recent studies tested interventions. Psychosexual concerns "
    "dominate the recent literature, whereas depression and anxiety were measured in fewer than "
    f"half of studies. Evidence is concentrated in Europe ({REG['Europe']}) and Asia "
    f"({REG['Asia']}); {REG['Africa']} study came from Africa and none from South America, "
    "where expectations about fertility and marriage may shape experiences differently.",
    "**Limitations:** AI-assisted screening and charting (full text checked for "
    f"{FT} of {N} studies); English-language studies from 2019–2026 only; heterogeneous designs "
    "and measures; some reports may share samples; counts show how often outcomes were studied, "
    "not their prevalence.",
])

TextBox13 = find("TextBox 13")
TextBox13._element.getparent().remove(TextBox13._element)

set_header(find("TextBox 321"), "Implications and Conclusion")
place(find("TextBox 321"), X, 20.0, W, 0.95)
place(find("TextBox 320"), X, 20.95, W, 8.1)
fill(find("TextBox 320"), [
    "**Public Health Implications**",
    "• Integrate psychosocial screening and support into MRKH diagnostic pathways^{@acog}",
    "• Build multidisciplinary teams that include psychology and social work",
    "• Pair vaginal lengthening treatment with psychosexual counseling",
    "• Train providers in sensitive, non-stigmatizing communication",
    "• Expand peer support networks, including online communities",
    "**Future Research**",
    "• Longitudinal studies using validated mental health measures",
    "• Trials of psychosocial interventions delivered in routine care",
    "• Studies in Africa, South America, and other low-resource settings",
    "**Conclusion**",
    "MRKH carries a substantial psychosocial burden that remains under-integrated into care. "
    "Mental health–inclusive, multidisciplinary care is needed to close this gap.",
    "*Acknowledgements: mentorship by Dr. Paul Okojie and Dr. Robyn Anderson; no external "
    "funding.*",
], space_after=3)

set_header(find("TextBox 322"), "References")
poster_refs = CITER.reference_list()
# QR code spot in the sample poster's position and size (its Picture 2): paste the QR code over it
qr = slide.shapes.add_shape(1, Inches(39.6), Inches(30.21), Inches(5.53), Inches(5.53))
qr.name = "QR code spot"
qr.fill.solid()
qr.fill.fore_color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
qr.line.color.rgb = RGBColor(0xBF, 0xBF, 0xBF)
qr.line.width = Pt(1.5)
qtf = qr.text_frame
qtf.word_wrap = True
qtf.vertical_anchor = MSO_ANCHOR.MIDDLE
for k, (text, size) in enumerate([("Paste QR code here", 28),
                                  ("(5.53 × 5.53 in; links to the full reference list)", 18)]):
    qp = qtf.paragraphs[0] if k == 0 else qtf.add_paragraph()
    qp.alignment = PP_ALIGN.CENTER
    add_runs(qp, text, size, color=RGBColor(0x59, 0x59, 0x59))

# ------------------------------------------------------------------ centre figures
# slot geometry follows the sample poster's figure positions; captions state the takeaway
image_in(FIG / "fig1_outcomes_bar.png", 12.3, 4.9, 23.9, 9.45)
caption(12.41, 14.4, 23.8, 1.15,
        f"**Figure 1.** Psychosexual and relational challenges were the most frequently reported "
        f"outcome ({S} of {N} studies); depression and anxiety were the least often assessed of "
        f"the four outcome domains ({D} of {N}). Studies could report more than one domain.")
slots = [  # image box, caption box, figure file, caption
    ((12.22, 15.75, 11.2, 7.75), (12.22, 23.6, 11.2, 1.6), "prisma_flow.png",
     f"**Figure 2.** PRISMA-ScR flow diagram: {P['identified']} records identified, "
     f"{P['screened']} screened, {P['fulltext']} assessed for eligibility, and {N} included."),
    ((24.15, 16.0, 11.9, 7.4), (24.15, 23.6, 11.9, 1.6), "fig3_geographic_map.png",
     f"**Figure 3.** Europe and Asia contributed {REG['Europe']} studies each, Africa and "
     f"Oceania {REG['Africa']} each, and South America none ({REG['Multinational']} "
     "multinational studies not mapped)."),
    ((12.22, 25.5, 11.2, 7.7), (12.22, 33.35, 11.2, 1.6), "fig2_design_donut.png",
     f"**Figure 4.** Study designs: {DES['Quantitative']} quantitative "
     f"({pct(DES['Quantitative'])}), {DES['Qualitative']} qualitative "
     f"({pct(DES['Qualitative'])}), {DES['Mixed methods']} mixed-methods, and "
     f"{DES['Not reported']} not reported."),
    ((24.15, 25.5, 11.9, 7.7), (24.15, 33.35, 11.9, 1.6), "fig5_coping_bar.png",
     f"**Figure 5.** Coping mechanisms in {C} studies: peer, family, and social support was most "
     f"common ({COPE['Peer, family & social support']}), followed by avoidance and concealment "
     f"({COPE['Avoidance / concealment (maladaptive)']})."),
]
for (ix, iy, iw, ih), (cx, cy, cw, ch), fname, text in slots:
    image_in(FIG / fname, ix, iy, iw, ih)
    caption(cx, cy, cw, ch, text, size=24)

out = ROOT / "poster" / "MRKH_APHA2026_Poster.pptx"
prs.save(out)
print("wrote", out, f"({len(poster_refs)} references on the poster)")

# ------------------------------------------------------------------ full reference list (QR code)
from docx import Document  # noqa: E402
from docx.shared import Pt as DPt  # noqa: E402

doc = Document()
st = doc.styles["Normal"]
st.font.name, st.font.size = FONT, DPt(11)


def ama_par(text, prefix=""):
    par = doc.add_paragraph()
    par.paragraph_format.space_after = DPt(4)
    if prefix:
        par.add_run(prefix)
    for piece in re.split(r"(\*.+?\*)", text):
        if piece:
            run = par.add_run(piece.strip("*") if piece.startswith("*") else piece)
            run.italic = piece.startswith("*")
    return par


doc.add_heading("Mental Health and Psychosocial Outcomes Among Individuals With "
                "Mayer-Rokitansky-Küster-Hauser (MRKH) Syndrome: A Scoping Review", 1)
doc.add_paragraph("Ifeoluwanimi P. Shobayo, BSc, MSPHc; Paul Okojie, PhD; Robyn Anderson, PhD. "
                  "Department of Public and Community Health, Liberty University. "
                  "APHA 2026 Annual Meeting poster — full reference list (AMA style).")
doc.add_heading("A. References cited on the poster", 2)
doc.add_paragraph("Numbered as they appear on the poster.")
for k, ref in enumerate(poster_refs, 1):
    ama_par(ref, f"{k}. ")

cited = set(CITER.order)
included = [(k, v) for k, v in CITER.lib.items() if re.fullmatch(r"R\d{3}", k)]
included.sort(key=lambda kv: kv[1].lower())
doc.add_heading(f"B. All {N} studies included in the scoping review", 2)
doc.add_paragraph("Listed alphabetically by first author. Studies also cited on the poster "
                  "show their poster reference number in brackets.")
assert len(included) == N
for k, ref in included:
    tag = f" [poster ref {CITER.order.index(k) + 1}]" if k in cited else ""
    ama_par(ref + tag, "• ")

extra = [k for k in ("herlin20", "bean", "patterson", "tsarna", "mak", "hb07", "okunomiya",
                     "laggari", "facchin")
         if k not in cited]
if extra:
    doc.add_heading("C. Additional background references (manuscript)", 2)
    for k in extra:
        ama_par(CITER.lib[k], "• ")
ref_out = ROOT / "poster" / "Poster_Full_Reference_List.docx"
doc.save(ref_out)
print("wrote", ref_out)
