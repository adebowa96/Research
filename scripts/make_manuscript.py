"""Builds the full manuscript (manuscript/MRKH_Scoping_Review_Manuscript.docx).
Run make_figures.py and make_map.js first. Usage: python3 scripts/make_manuscript.py

Inline markup: **bold**, *italic*, ^{sup} superscript, [[...]] = yellow-highlighted
placeholder the authors must complete or confirm before submission."""
import json
import re
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

HERE = Path(__file__).parent
ROOT = HERE.parent
FIG = ROOT / "figures"
data = json.loads((HERE / "data.json").read_text())
N = data["total_included"]
P = data["prisma"]
OUT = dict(data["outcomes"])
DES = {name: (n, note) for name, n, note in data["designs"]}
REG = {name: n for name, n, _ in data["regions"]}


def pct(n, d=N, digits=1):
    return f"{100 * n / d:.{digits}f}%"


doc = Document()
for s in doc.sections:
    s.left_margin = s.right_margin = s.top_margin = s.bottom_margin = Inches(1)

normal = doc.styles["Normal"]
normal.font.name = "Times New Roman"
normal.font.size = Pt(12)
normal.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
normal.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE
normal.paragraph_format.space_after = Pt(0)
for lvl, size in ((1, 14), (2, 12), (3, 12)):
    st = doc.styles[f"Heading {lvl}"]
    st.font.name = "Times New Roman"
    rfonts = st.element.rPr.rFonts
    rfonts.set(qn("w:eastAsia"), "Times New Roman")
    for attr in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
        rfonts.attrib.pop(qn(attr), None)  # theme fonts would override Times New Roman
    st.font.size = Pt(size)
    st.font.bold = True
    st.font.italic = lvl == 3
    st.font.color.rgb = RGBColor(0, 0, 0)
    st.paragraph_format.space_before = Pt(12)
    st.paragraph_format.space_after = Pt(6)
    st.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE

# page numbers in footer
fp = doc.sections[0].footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
for tag, text in (("begin", None), (None, "PAGE"), ("end", None)):
    run = fp.add_run()
    if tag:
        el = OxmlElement("w:fldChar")
        el.set(qn("w:fldCharType"), tag)
    else:
        el = OxmlElement("w:instrText")
        el.set(qn("xml:space"), "preserve")
        el.text = text
    run._r.append(el)

TOKEN = re.compile(r"(\*\*.+?\*\*|\*.+?\*|\^\{.+?\}|\[\[.+?\]\])")
BODY_WORDS = []  # words in main text (Introduction through Conclusions) for the word count
counting = {"on": False}


def add_runs(par, text, size=None, bold=False):
    for piece in TOKEN.split(text):
        if not piece:
            continue
        b, i, sup, hl = bold, False, False, False
        if piece.startswith("**"):
            piece, b = piece[2:-2], True
        elif piece.startswith("[["):
            piece, hl = "[" + piece[2:-2] + "]", True
        elif piece.startswith("^{"):
            piece, sup = piece[2:-1], True
        elif piece.startswith("*"):
            piece, i = piece[1:-1], True
        r = par.add_run(piece)
        r.bold, r.italic = b, i
        if sup:
            r.font.superscript = True
        if hl:
            r.font.highlight_color = WD_COLOR_INDEX.YELLOW
        if size:
            r.font.size = Pt(size)
        if counting["on"] and not sup:
            BODY_WORDS.extend(piece.split())


def para(text, align=None, indent=True, size=None, bold=False, style=None, spacing=None):
    p = doc.add_paragraph(style=style)
    if align is not None:
        p.alignment = align
    if indent and style is None and align is None:
        p.paragraph_format.first_line_indent = Inches(0.5)
    if spacing is not None:
        p.paragraph_format.line_spacing_rule = spacing
    add_runs(p, text, size=size, bold=bold)
    return p


def bullets(items, style="List Bullet"):
    for it in items:
        p = doc.add_paragraph(style=style)
        add_runs(p, it)


def heading(text, level=1):
    h = doc.add_heading(level=level)
    if pending_break["on"]:
        h.paragraph_format.page_break_before = True
        pending_break["on"] = False
    add_runs(h, text)
    return h


pending_break = {"on": False}


def page_break():
    # applied as "page break before" on the next heading, so a full page never
    # leaves a stray break paragraph that creates a blank page
    pending_break["on"] = True


def set_cell_shading(cell, hex_fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_fill)
    tcPr.append(shd)


def table(caption, header, rows, widths=None, note=None, size=10):
    was, counting["on"] = counting["on"], False  # tables are excluded from the word count
    cp = doc.add_paragraph()
    cp.paragraph_format.keep_with_next = True
    cp.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    cp.paragraph_format.space_before = Pt(12)
    cp.paragraph_format.space_after = Pt(4)
    add_runs(cp, caption)
    t = doc.add_table(rows=1, cols=len(header))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    for j, h in enumerate(header):
        c = t.rows[0].cells[j]
        c.text = ""
        add_runs(c.paragraphs[0], h, size=size, bold=True)
        set_cell_shading(c, "D9E2F3")
    for row in rows:
        cells = t.add_row().cells
        for j, v in enumerate(row):
            cells[j].text = ""
            add_runs(cells[j].paragraphs[0], str(v), size=size)
    for row in t.rows:
        for j, c in enumerate(row.cells):
            for p in c.paragraphs:
                p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
                p.paragraph_format.first_line_indent = None
            if widths:
                c.width = Inches(widths[j])
    if widths:
        for j, col in enumerate(t.columns):
            col.width = Inches(widths[j])
    if note:
        np_ = doc.add_paragraph()
        np_.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
        np_.paragraph_format.space_after = Pt(12)
        add_runs(np_, note, size=10)
    counting["on"] = was
    return t


def figure(path, caption, width=6.0):
    was, counting["on"] = counting["on"], False
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(str(path), width=Inches(width))
    cp = doc.add_paragraph()
    cp.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    cp.paragraph_format.space_after = Pt(12)
    add_runs(cp, caption, size=10)
    counting["on"] = was


# ====================================================================== TITLE PAGE
para("**Mental Health and Psychosocial Outcomes Among Individuals With "
     "Mayer-Rokitansky-Küster-Hauser (MRKH) Syndrome: A Scoping Review**",
     align=WD_ALIGN_PARAGRAPH.CENTER, size=14)
para("**Running title:** Mental health in MRKH syndrome: a scoping review",
     align=WD_ALIGN_PARAGRAPH.CENTER)
para("Ifeoluwanimi P. Shobayo, BSc, MSPHc^{1}; Paul Okojie, PhD^{1}; Robyn Anderson, PhD^{1}",
     align=WD_ALIGN_PARAGRAPH.CENTER)
para("^{1}Department of Public and Community Health, Liberty University, Lynchburg, Virginia, USA",
     align=WD_ALIGN_PARAGRAPH.CENTER)
para("", indent=False)
para("**Corresponding author:** Ifeoluwanimi P. Shobayo, Department of Public and Community "
     "Health, Liberty University, Lynchburg, VA, USA. Email: [[corresponding author email]]",
     indent=False)
para("**Word count (main text):** {WORDCOUNT}   **Tables:** 4   **Figures:** 4   "
     "**Supplementary material:** Appendices A–C", indent=False)
para("**Prior presentation:** An abstract of this work was submitted to the American Public "
     "Health Association (APHA) 2026 Annual Meeting & Expo, Sexual and Reproductive Health "
     "Section, and accepted for poster presentation.",
     indent=False)
para("**Keywords:** Mayer-Rokitansky-Küster-Hauser syndrome; Müllerian agenesis; mental health; "
     "coping; psychosocial outcomes; quality of life; reproductive health", indent=False)
page_break()

# ====================================================================== ABSTRACT
heading("Abstract")
abstract = [
    "**Background:** Mayer-Rokitansky-Küster-Hauser (MRKH) syndrome is a rare congenital "
    "condition, affecting approximately 1 in 4,500–5,000 female births, characterized by "
    "uterovaginal agenesis in individuals with a 46,XX karyotype and functional ovaries. "
    "Typically diagnosed during adolescence, MRKH is associated with significant psychosocial "
    "burden, yet mental health outcomes and coping mechanisms remain insufficiently synthesized, "
    "limiting their integration into clinical care and public health planning. This scoping "
    "review mapped the mental health outcomes, coping mechanisms, and healthcare system gaps "
    "reported among individuals with MRKH.",
    "**Methods:** Following Arksey and O'Malley's framework and the PRISMA Extension for Scoping "
    "Reviews (PRISMA-ScR), we searched PubMed, Scopus, and (via EBSCOhost) MEDLINE, CINAHL, APA "
    "PsycInfo, and Women's Studies International for studies published between January 2019 "
    "and March 2026. Eligible studies were primary quantitative, "
    "qualitative, and mixed-methods research reporting psychological outcomes and/or coping "
    "mechanisms in MRKH populations.",
    f"**Results:** Of {P['identified']} records identified ({P['screened']} after "
    f"deduplication), {N} studies met inclusion criteria. Depression and anxiety were the most "
    f"frequently reported outcomes (n = {OUT['Depression & anxiety']}; "
    f"{pct(OUT['Depression & anxiety'], digits=0)}), followed by reduced quality of life and "
    f"body image concerns (n = {OUT['Reduced QoL & body image']}; "
    f"{pct(OUT['Reduced QoL & body image'], digits=0)}), psychosexual and relational challenges "
    f"(n = {OUT['Psychosexual & relational challenges']}; "
    f"{pct(OUT['Psychosexual & relational challenges'], digits=0)}), and broader psychological "
    f"distress (n = {OUT['Broader psychological distress']}; "
    f"{pct(OUT['Broader psychological distress'], digits=0)}). Coping mechanisms were documented "
    f"in {OUT['Coping mechanisms documented']} studies and healthcare system gaps in "
    f"{OUT['Healthcare system gaps']}. Most studies originated from Europe "
    f"(n = {REG['Europe']}) and North America (n = {REG['North America']}).",
    "**Conclusions:** MRKH-related psychosocial burden is substantial yet under-integrated into "
    "care models. Multidisciplinary, mental health–inclusive care and greater research "
    "investment, particularly in underrepresented and low-resource settings, are urgently needed.",
]
for a in abstract:
    para(a, indent=False)
page_break()

# ====================================================================== MAIN TEXT
counting["on"] = True
heading("Introduction")
para("Mayer-Rokitansky-Küster-Hauser (MRKH) syndrome, also termed Müllerian agenesis or "
     "Müllerian aplasia, is a congenital condition characterized by absence of the uterus and "
     "upper two-thirds of the vagina in individuals with a 46,XX karyotype, functional ovaries, "
     "and typical secondary sexual development. It affects approximately 1 in 4,500–5,000 "
     "female births^{1}; a nationwide Danish registry study estimated a prevalence of 1 in 4,982 "
     "live female births.^{2} MRKH is classified as type I (isolated uterovaginal aplasia) or "
     "type II (accompanied by extragenital anomalies, most often renal, skeletal, auditory, or "
     "cardiac).^{3} Diagnosis is usually made in adolescence during evaluation for primary "
     "amenorrhea,^{1,3} a developmental period that is critical for identity formation, body "
     "image, and social relationships.")
para("The diagnosis carries profound implications for fertility, psychosexual development, and "
     "self-image. Management commonly includes vaginal dilation as first-line treatment, surgical "
     "creation of a neovagina when indicated, and fertility options such as gestational "
     "surrogacy and, more recently, uterus transplantation.^{1,3} The American College of "
     "Obstetricians and Gynecologists identifies psychosocial counseling as one of the most "
     "important components of effective management.^{1} Earlier studies documented elevated "
     "psychological distress and lower self-esteem among women with MRKH compared with "
     "controls,^{4} higher anxiety scores among affected adolescents,^{5} and poorer "
     "mental health–related quality of life, higher anxiety, and impaired sexual wellness "
     "relative to normative data.^{6} A review of this early literature concluded that creating a "
     "neovagina alone does not ensure a good psychological outcome and that psychological "
     "support at critical times can be helpful,^{7} while qualitative work described how young "
     "women manage intimacy, a sensitivity to difference, and threats to identity after "
     "diagnosis.^{8} More recent qualitative studies describe emotional turmoil at diagnosis, "
     "challenges to sexual identity and intimate relationships, the profound impact of "
     "infertility,^{9} and reduced self-esteem and sexual wellbeing.^{10}")
para("Two systematic reviews have since synthesized the psychological, quality-of-life, and "
     "sexual outcomes of MRKH.^{11,12} However, to our knowledge, the more recent literature has "
     "not been mapped with a public health lens that jointly considers mental health outcomes, "
     "the coping mechanisms individuals use, and the healthcare system gaps that shape access to "
     "psychosocial support. As a result, psychosocial outcomes remain insufficiently integrated "
     "into clinical and public health frameworks for this population.")
para("A scoping review is well suited to mapping a heterogeneous body of quantitative, "
     "qualitative, and mixed-methods evidence and identifying gaps for future research and "
     "practice.^{13,14} This scoping review therefore addressed the following research question: "
     "*What mental health outcomes and coping mechanisms are reported among individuals with MRKH "
     "syndrome, and what healthcare system gaps exist?*")

heading("Methods")
heading("Study Design", 2)
para("This scoping review followed Arksey and O'Malley's five-stage methodological "
     "framework^{13}—(1) identifying the research question; (2) identifying relevant studies; "
     "(3) selecting studies; (4) charting the data; and (5) collating, summarizing, and reporting "
     "the results—and is reported in accordance with the PRISMA Extension for Scoping Reviews "
     "(PRISMA-ScR; Appendix C),^{14} informed by published guidance on the steps of conducting a "
     "scoping review.^{15} A review protocol was not registered.")
heading("Eligibility Criteria", 2)
para("Eligibility was defined using the Population–Concept–Context approach. The *population* "
     "was individuals diagnosed with MRKH syndrome; the *concepts* were psychological or mental "
     "health outcomes and coping mechanisms; and the *context* was any healthcare or community "
     "setting in any country. We included primary quantitative, qualitative, and mixed-methods "
     "studies published between January 2019 and March 2026 that reported psychological "
     "outcomes and/or coping mechanisms among individuals with MRKH. Studies focused solely on "
     "anatomical, surgical, or fertility outcomes were excluded, as were records published "
     "before January 2019. [[Confirm any additional criteria applied, e.g., language (English "
     "only?), peer-reviewed publications only, and exclusion of reviews, case reports, "
     "editorials, and conference abstracts.]]")
heading("Information Sources and Search Strategy", 2)
para("Searches were run and exported on March 29, 2026, in PubMed, Scopus, and EBSCOhost "
     "[[confirm the PubMed search was also run on this date]]. "
     "The EBSCOhost search covered MEDLINE Ultimate, CINAHL Ultimate, APA PsycInfo, and Women's "
     "Studies International, and APA PsycInfo was also exported separately (Appendix A). Date "
     "limits were not applied identically across interfaces: the Scopus search was limited to "
     "2019–2026, the PubMed export covered 2021–2026 (MEDLINE records from 2019–2020 were "
     "captured through the EBSCOhost MEDLINE search), and EBSCOhost results were exported "
     "without a date limit. Records published before January 2019 were therefore removed during "
     "title and abstract screening. Search strategies combined controlled "
     "vocabulary and free-text terms for MRKH (e.g., “Mayer-Rokitansky-Küster-Hauser,” “MRKH,” "
     "“Müllerian agenesis,” “vaginal agenesis”) with terms for mental health and coping (e.g., "
     "“depression,” “anxiety,” “psychological distress,” “quality of life,” “body image,” "
     "“coping”). Records retrieved from each source are reported in Appendix A. [[Verify that "
     "the example terms above match the search you ran; recover exact strings from your "
     "PubMed, Scopus, and EBSCOhost search histories if saved.]]")
heading("Study Selection", 2)
para(f"Records were exported to [[reference manager/screening software, e.g., Zotero, "
     f"Covidence, Rayyan]], and {P['duplicates_removed']} duplicates were removed. The remaining "
     f"{P['screened']} records were screened against the eligibility criteria "
     f"[[by two independent reviewers; disagreements resolved through discussion or by a third "
     f"reviewer — edit to reflect your actual process]]. [[Report the number of full-text "
     f"articles assessed for eligibility and the reasons for full-text exclusion; PRISMA-ScR "
     f"item 14 requires this.]]")
heading("Data Charting", 2)
para("Data were charted using a standardized form capturing author, year, country, study "
     "design, sample characteristics, outcome measures, reported mental health outcomes, coping "
     "mechanisms, and healthcare system gaps. [[Confirm charted items and whether charting was "
     "piloted or completed in duplicate.]]")
heading("Synthesis", 2)
para("Findings were collated using a descriptive numerical summary—the number and proportion of "
     "included studies reporting each outcome domain—and a qualitative content analysis that "
     "grouped findings into mental health outcome domains, coping mechanisms, and healthcare "
     "system gaps. Because a single study could report multiple domains, domain counts are not "
     "mutually exclusive. Consistent with scoping review methodology, a formal critical appraisal "
     "of study quality was not performed.^{13,14} Ethical approval was not required because this review analyzed "
     "published data.")

heading("Results")
heading("Selection of Sources of Evidence", 2)
para(f"The database searches identified {P['identified']} records. After removal of "
     f"{P['duplicates_removed']} duplicates, {P['screened']} records were screened, of which "
     f"{P['excluded']} were excluded for not meeting inclusion criteria. A total of {N} studies "
     f"were included in the review (Figure 1).")
figure(FIG / "prisma_flow.png",
       "**Figure 1.** PRISMA-ScR flow diagram of study selection. [[Add a full-text assessment "
       "box (number assessed and number excluded with reasons) if full-text screening was "
       "conducted as a separate stage.]]", width=5.2)

heading("Characteristics of Included Studies", 2)
q_n, q_note = DES["Quantitative"]
para(f"The {N} included studies comprised {q_n} quantitative studies ({pct(q_n)}), "
     f"{DES['Qualitative'][0]} qualitative studies ({pct(DES['Qualitative'][0])}), and "
     f"{DES['Mixed methods'][0]} mixed-methods studies ({pct(DES['Mixed methods'][0])}); "
     f"11 of the quantitative studies used a cross-sectional design (Table 1; Figure 2). "
     f"Studies were concentrated in high-income regions: {REG['Europe']} ({pct(REG['Europe'])}) "
     f"originated in Europe and {REG['North America']} ({pct(REG['North America'])}) in North "
     f"America, together accounting for {REG['Europe'] + REG['North America']} of {N} studies "
     f"({pct(REG['Europe'] + REG['North America'], digits=0)}). Five studies "
     f"({pct(REG['Asia'])}) were conducted in Asia, {REG['Africa']} ({pct(REG['Africa'])}) in "
     f"Africa, and {REG['South America']} ({pct(REG['South America'])}) in South America; no "
     f"included study originated in Oceania (Figure 3). Characteristics of each included study "
     f"are summarized in Appendix B. [[Add the range of sample sizes, participant ages, and "
     f"publication years from your extraction table.]]")
table("**Table 1.** Study design and geographic distribution of included studies (N = 34)",
      ["Characteristic", "n", "%"],
      [["**Study design**", "", ""],
       [f"Quantitative (incl. 11 cross-sectional)", q_n, pct(q_n)],
       ["Qualitative", DES["Qualitative"][0], pct(DES["Qualitative"][0])],
       ["Mixed methods", DES["Mixed methods"][0], pct(DES["Mixed methods"][0])],
       ["**Region**", "", ""]]
      + [[name, n, pct(n)] for name, n, _ in data["regions"]],
      widths=[3.6, 0.8, 1.0],
      note="Percentages are of all included studies (N = 34) and may not total 100% because of "
           "rounding. [[Verify design classifications against your extraction table.]]")
figure(FIG / "fig2_design_donut.png",
       "**Figure 2.** Distribution of included studies by design (N = 34). Cross-sectional "
       "studies (n = 11) are a subset of quantitative designs.", width=4.8)
figure(FIG / "fig3_geographic_map.png",
       "**Figure 3.** Geographic distribution of included studies by region (N = 34). Darker "
       "shading indicates more studies; no included study originated in Oceania.", width=6.3)

heading("Mental Health and Psychosocial Outcomes", 2)
d = OUT["Depression & anxiety"]
q = OUT["Reduced QoL & body image"]
s = OUT["Psychosexual & relational challenges"]
g = OUT["Broader psychological distress"]
para(f"Four outcome domains were identified (Table 2; Figure 4). Depression and anxiety were "
     f"the most frequently reported outcomes, appearing in {d} of {N} studies ({pct(d)}). "
     f"Reduced quality of life and body image concerns were reported in {q} studies "
     f"({pct(q)}), psychosexual and relational challenges in {s} ({pct(s)}), and broader "
     f"psychological distress in {g} ({pct(g)}). These outcomes frequently co-occurred within "
     f"the same studies, indicating that the psychosocial impact of MRKH extends across "
     f"emotional, relational, and identity-related dimensions rather than being confined to a "
     f"single domain.")
table("**Table 2.** Mental health and psychosocial outcome domains reported in included studies "
      "(N = 34)",
      ["Outcome domain", "Description", "Studies, n (%)"],
      [["Depression and anxiety", "Depressive and/or anxiety symptoms or diagnoses",
        f"{d} ({pct(d)})"],
       ["Reduced quality of life and body image", "Lower overall or mental health–related "
        "quality of life; negative body or genital image; self-esteem concerns", f"{q} ({pct(q)})"],
       ["Psychosexual and relational challenges", "Sexual function and sexual self-esteem "
        "difficulties; concerns about intimacy, partner relationships, and disclosure",
        f"{s} ({pct(s)})"],
       ["Broader psychological distress", "General distress, grief and loss, shame, "
        "isolation, and identity-related distress", f"{g} ({pct(g)})"]],
      widths=[1.9, 3.3, 1.2],
      note="Studies could report more than one domain; counts are therefore not mutually "
           "exclusive. [[Check that the domain descriptions match how studies were coded in "
           "your extraction.]]")
figure(FIG / "fig1_outcomes_bar.png",
       "**Figure 4.** Number of included studies reporting each outcome domain, coping "
       "mechanisms, and healthcare system gaps (N = 34). Studies could contribute to more "
       "than one category.", width=6.3)

heading("Coping Mechanisms", 2)
c = OUT["Coping mechanisms documented"]
para(f"Coping mechanisms were documented in {c} studies ({pct(c)}). Six categories were "
     f"identified (Table 3). Five were adaptive—peer and community support, psychological "
     f"counseling, identity reconstruction, spiritual coping, and adaptive acceptance—and one, "
     f"avoidance, was maladaptive. Consistent with the healthcare system gaps described below, "
     f"these coping mechanisms were not supported by systematic clinical pathways.")
table("**Table 3.** Coping mechanisms documented in included studies",
      ["Coping mechanism", "Type", "Description"],
      [["Peer and community support", "Adaptive",
        "Connection with others with MRKH through support groups, online communities, and "
        "advocacy networks"],
       ["Psychological counseling", "Adaptive",
        "Professional psychological support, including individual or group therapy"],
       ["Identity reconstruction", "Adaptive",
        "Redefining femininity, womanhood, and self-concept independent of reproductive anatomy"],
       ["Spiritual coping", "Adaptive", "Drawing on faith, religious practice, or spirituality "
        "to find meaning and resilience"],
       ["Adaptive acceptance", "Adaptive",
        "Gradual acceptance of the diagnosis and its implications for fertility and sexuality"],
       ["Avoidance", "Maladaptive", "Avoiding discussion of the diagnosis, concealment, and "
        "withdrawal from intimate relationships or care"]],
      widths=[1.9, 1.1, 3.4],
      note="[[Confirm that the descriptions reflect the included studies; optionally add the "
           "number of studies reporting each coping mechanism from your extraction table.]]")

heading("Healthcare System Gaps", 2)
h = OUT["Healthcare system gaps"]
para(f"Healthcare system gaps were identified in {h} studies ({pct(h)}; Table 4). These "
     f"included delayed diagnosis in adolescence without concurrent psychosocial support; limited "
     f"access to multidisciplinary care teams that include psychology, social work, and "
     f"gynecology; insufficient integration of mental health into MRKH care models; and the "
     f"absence of standardized mental health screening protocols at diagnosis. In addition, the "
     f"geographic distribution of the evidence base itself (Figure 3) reveals a research gap: "
     f"only {REG['Africa'] + REG['South America']} of {N} studies originated in Africa or "
     f"South America.")
table("**Table 4.** Healthcare system gaps identified and corresponding public health implications",
      ["Gap identified", "Public health implication"],
      [["Delayed diagnosis in adolescence without concurrent psychosocial support",
        "Integrate mental health screening into standard MRKH diagnostic pathways"],
       ["Limited access to multidisciplinary care teams (psychology, social work, gynecology)",
        "Develop multidisciplinary care protocols that include psychology and social work"],
       ["Mental health insufficiently integrated into MRKH care models",
        "Train providers in psychosocially informed MRKH care; build peer support "
        "infrastructure within reproductive health services"],
       ["Lack of standardized mental health screening protocols at diagnosis",
        "Adopt validated screening instruments at diagnosis and follow-up"],
       ["Underrepresentation of low- and middle-income settings in the evidence base "
        "(research gap)", "Expand research investment in underrepresented and low-resource "
        "settings"]],
      widths=[3.2, 3.2])

heading("Discussion")
heading("Summary of Evidence", 2)
para(f"This scoping review mapped {N} studies published between 2019 and 2026 on the mental "
     f"health and psychosocial outcomes of individuals with MRKH syndrome. Depression and "
     f"anxiety were reported in about three of every four included studies, and reduced quality "
     f"of life, body image concerns, psychosexual challenges, and broader psychological distress "
     f"were each reported in at least half. Coping mechanisms were documented in about three "
     f"in five studies, yet they appeared to operate largely outside systematic clinical "
     f"pathways, and more than half of the studies identified healthcare system gaps that limit "
     f"access to psychosocial support.")
para("These findings are consistent with earlier evidence. Before 2019, women with MRKH were "
     "shown to have greater psychological distress and lower self-esteem than controls,^{4} "
     "adolescents with MRKH had higher anxiety scores than healthy peers,^{5} and adult women "
     "reported poorer mental health–related quality of life and sexual wellness than normative "
     "samples.^{6} Prior systematic reviews similarly concluded that MRKH may be associated with "
     "psychological symptoms and impaired quality of life, particularly poor sexual esteem and "
     "genital image.^{11,12} The present review indicates that these concerns remain prominent in "
     "the recent literature and extends earlier syntheses by mapping coping mechanisms and "
     "healthcare system gaps alongside outcomes.")
heading("Coping and Psychosocial Support", 2)
para("The coping strategies identified—peer and community support, psychological counseling, "
     "identity reconstruction, spiritual coping, and acceptance—suggest that many individuals "
     "develop considerable resilience after diagnosis. Identity reconstruction aligns with "
     "qualitative accounts in which young women with MRKH worked to manage threats to identity "
     "and intimacy.^{8} At the same time, avoidance was documented as a maladaptive response that "
     "may delay help-seeking and treatment engagement. Evidence that structured psychological "
     "intervention can help is available: a randomized controlled trial of a cognitive-behavioural "
     "group intervention improved psychological outcomes among women with MRKH compared with a "
     "waiting-list control.^{16} The persistence of self-directed coping in the recent literature "
     "suggests that such evidence-based support has not been consistently translated into "
     "routine care.")
heading("Healthcare System Gaps and Equity", 2)
para("Although professional guidance identifies psychosocial counseling as central to MRKH "
     "management,^{1} the gaps identified in this review—diagnosis without concurrent "
     "psychosocial support, limited multidisciplinary care, and no standardized mental health "
     "screening—indicate a gap between recommendations and practice. The concentration of "
     f"evidence in Europe and North America ({REG['Europe'] + REG['North America']} of {N} "
     "studies) further limits understanding of how MRKH is experienced where cultural "
     "expectations regarding fertility, marriage, and womanhood, as well as access to "
     "specialized care, may differ substantially. The scarcity of studies from Africa and South "
     "America represents both a research gap and a likely inequity in diagnosis, support, and "
     "long-term outcomes. Recent studies from Türkiye and Japan^{9,17} show that such work is "
     "feasible and that cultural context shapes experiences of diagnosis, disclosure, and "
     "infertility.")
heading("Implications for Practice, Policy, and Research", 2)
para("Five priorities emerge from this review. First, mental health screening should be "
     "integrated into standard MRKH diagnostic pathways, beginning at the time of diagnosis. "
     "Second, multidisciplinary care protocols should include psychology and social work alongside "
     "gynecology. Third, peer support infrastructure should be embedded within reproductive health "
     "services, building on the coping strategies individuals already use. Fourth, providers "
     "should be trained in psychosocially informed MRKH care, including sensitive communication "
     "about fertility and sexuality. Fifth, research investment should be expanded in "
     "low- and middle-income and underrepresented settings. Future studies should use "
     "standardized, validated mental health measures, longitudinal designs that follow "
     "individuals from diagnosis into adulthood, and trials of psychosocial interventions "
     "delivered within routine care.")
heading("Strengths and Limitations", 2)
para("Strengths of this review include the use of an established methodological framework, "
     "reporting according to PRISMA-ScR, a search of multiple biomedical, nursing, psychological, "
     "and women's studies databases, and inclusion of quantitative, qualitative, and mixed-methods evidence. Several "
     "limitations should be noted. The review was limited to studies published from 2019 to "
     "2026 and may therefore exclude earlier foundational research. Heterogeneity in study "
     "designs and outcome measures limits direct comparison across studies. Most studies came "
     "from high-income countries, limiting global generalizability, and some studies relied on "
     "self-reported mental health outcomes. Consistent with scoping review methodology, study "
     "quality was not formally appraised, and the counts reported here reflect how frequently "
     "outcomes were studied, not their prevalence. Date limits were applied inconsistently across "
     "database interfaces at the search stage and were enforced during screening. [[Add, if applicable: English-language "
     "restriction; grey literature not searched.]]")
heading("Conclusions", 2)
para("MRKH-related psychosocial burden is substantial yet under-integrated into care models. "
     "Depression, anxiety, reduced quality of life, and psychosexual challenges are frequently "
     "reported and often co-occurring, while coping mechanisms—though documented—remain "
     "unsupported by systematic clinical pathways. Multidisciplinary, mental health–inclusive "
     "care and greater research investment are urgently needed, particularly in underrepresented "
     "and low-resource settings, to address persistent inequities in diagnosis, support, and "
     "long-term outcomes.")
counting["on"] = False

# ====================================================================== DECLARATIONS
heading("Declarations")
decl = [
    "**Acknowledgements:** This scoping review was conducted under the mentorship of Dr. Paul "
    "Okojie and Dr. Robyn Anderson, Department of Public and Community Health, Liberty University.",
    "**Funding:** No external funding was received.",
    "**Conflicts of interest:** [[The authors declare no conflicts of interest. — confirm with "
    "all authors.]]",
    "**Author contributions:** [[e.g., I.P.S.: conceptualization, search, screening, data "
    "charting, analysis, writing—original draft; P.O. and R.A.: supervision, methodology, "
    "writing—review and editing. Edit to reflect actual contributions (CRediT taxonomy).]]",
    "**Ethics approval:** Not applicable; this review analyzed published studies.",
    "**Data availability:** The data charting form and extracted data are available from the "
    "corresponding author on reasonable request.",
    "**Use of AI tools:** Generative AI (Claude, Anthropic) was used to assist with drafting and "
    "editing the manuscript, verifying reference details, and preparing figures. The authors "
    "reviewed and verified all content and take full responsibility for the work. [[Confirm "
    "wording against the target journal's AI policy.]]",
]
for dtext in decl:
    para(dtext, indent=False)

# ====================================================================== REFERENCES
heading("References")
refs = [
    "American College of Obstetricians and Gynecologists' Committee on Adolescent Health Care. "
    "ACOG Committee Opinion No. 728: Müllerian agenesis: diagnosis, management, and treatment. "
    "*Obstet Gynecol*. 2018;131(1):e35-e42. doi:10.1097/AOG.0000000000002458",
    "Herlin M, Bjørn AMB, Rasmussen M, Trolle B, Petersen MB. Prevalence and patient "
    "characteristics of Mayer-Rokitansky-Küster-Hauser syndrome: a nationwide registry-based "
    "study. *Hum Reprod*. 2016;31(10):2384-2390. doi:10.1093/humrep/dew220",
    "Herlin MK, Petersen MB, Brännström M. Mayer-Rokitansky-Küster-Hauser (MRKH) syndrome: a "
    "comprehensive update. *Orphanet J Rare Dis*. 2020;15(1):214. "
    "doi:10.1186/s13023-020-01491-9",
    "Heller-Boersma JG, Schmidt UH, Edmonds DK. Psychological distress in women with "
    "uterovaginal agenesis (Mayer-Rokitansky-Kuster-Hauser syndrome, MRKH). *Psychosomatics*. "
    "2009;50(3):277-281. doi:10.1176/appi.psy.50.3.277",
    "Laggari V, Diareme S, Christogiorgos S, et al. Anxiety and depression in adolescents with "
    "polycystic ovary syndrome and Mayer-Rokitansky-Küster-Hauser syndrome. *J Psychosom Obstet "
    "Gynaecol*. 2009;30(2):83-88. doi:10.1080/01674820802546204",
    "Liao LM, Conway GS, Ismail-Pratt I, Bikoo M, Creighton SM. Emotional and sexual wellness "
    "and quality of life in women with Rokitansky syndrome. *Am J Obstet Gynecol*. "
    "2011;205(2):117.e1-117.e6. doi:10.1016/j.ajog.2011.03.013",
    "Bean EJ, Mazur T, Robinson AD. Mayer-Rokitansky-Küster-Hauser syndrome: sexuality, "
    "psychological effects, and quality of life. *J Pediatr Adolesc Gynecol*. "
    "2009;22(6):339-346. doi:10.1016/j.jpag.2008.11.006",
    "Patterson CJ, Crawford R, Jahoda A. Exploring the psychological impact of "
    "Mayer-Rokitansky-Küster-Hauser syndrome on young women: an interpretative phenomenological "
    "analysis. *J Health Psychol*. 2016;21(7):1228-1240. doi:10.1177/1359105314551077",
    "Güner P, Ulukaya T, Pehlivan Sarıbudak T. \u201cI felt like a woman\u201d: a phenomenological "
    "qualitative study of disease-related experiences in Mayer-Rokitansky-Küster-Hauser syndrome "
    "(MRKH syndrome). *J Health Psychol*. Published online 2025. "
    "doi:10.1177/13591053241305941 [[add volume/issue/pages from the journal page]]",
    "Rajesh Z, Marshall N, Hunker KE, et al. Understanding the impact of "
    "Mayer-Rokitansky-Küster-Hauser syndrome on sexual wellbeing—a qualitative study. *J Sex "
    "Med*. 2026;23(1):qdaf309. doi:10.1093/jsxmed/qdaf309",
    "Facchin F, Francini F, Ravani S, et al. Psychological impact and health-related "
    "quality-of-life outcomes of Mayer-Rokitansky-Küster-Hauser syndrome: a systematic review "
    "and narrative synthesis. *J Health Psychol*. 2021;26(1):26-39. "
    "doi:10.1177/1359105319901308",
    "Tsarna E, Eleftheriades A, Eleftheriades M, Kalampokas E, Liakopoulou MK, Christopoulos P. "
    "The impact of Mayer-Rokitansky-Küster-Hauser syndrome on psychology, quality of life, and "
    "sexual life of patients: a systematic review. *Children (Basel)*. 2022;9(4):484. "
    "doi:10.3390/children9040484",
    "Arksey H, O'Malley L. Scoping studies: towards a methodological framework. *Int J Soc Res "
    "Methodol*. 2005;8(1):19-32. doi:10.1080/1364557032000119616",
    "Tricco AC, Lillie E, Zarin W, et al. PRISMA Extension for Scoping Reviews (PRISMA-ScR): "
    "checklist and explanation. *Ann Intern Med*. 2018;169(7):467-473. doi:10.7326/M18-0850",
    "Mak S, Thomas A. Steps for conducting a scoping review. *J Grad Med Educ*. "
    "2022;14(5):565-567. doi:10.4300/JGME-D-22-00621.1",
    "Heller-Boersma JG, Schmidt UH, Edmonds DK. A randomized controlled trial of a "
    "cognitive-behavioural group intervention versus waiting-list control for women with "
    "uterovaginal agenesis (Mayer-Rokitansky-Küster-Hauser syndrome: MRKH). *Hum Reprod*. "
    "2007;22(8):2296-2301. doi:10.1093/humrep/dem167",
    "Okunomiya A, Tsuyuki K, Ohsuga T, et al. Long-term psychosocial outcomes in Japanese "
    "Mayer-Rokitansky-Küster-Hauser syndrome: a single-center study. *J Obstet Gynaecol Res*. "
    "2026;52(5). doi:10.1111/jog.70291 [[add article number/pages]]",
]
for i, r in enumerate(refs, 1):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    p.paragraph_format.first_line_indent = Inches(-0.35)
    add_runs(p, f"{i}.\t{r}")
para("[[Add citations for the 34 included studies (numbered in order of first citation, e.g., "
     "in Appendix B) per the target journal's style.]]", indent=False)

# ====================================================================== APPENDICES
page_break()
heading("Appendix A. Search Strategy")
para("Searches were exported on March 29, 2026. Record counts below are taken from the export "
     "files and total 516, matching Figure 1. [[Paste the exact search string for each database "
     "if it can be recovered from your search history.]]", indent=False)
para("[[Suggested PubMed/MEDLINE string for comparison. Replace it with the string you actually "
     "ran; do not report a search you did not run:]]", indent=False)
para("(\"Mayer-Rokitansky-Kuster-Hauser\"[tiab] OR \"Mayer-Rokitansky-Küster-Hauser\"[tiab] OR "
     "MRKH[tiab] OR Rokitansky[tiab] OR \"Mullerian agenesis\"[tiab] OR \"Mullerian aplasia\"[tiab] "
     "OR \"vaginal agenesis\"[tiab] OR \"uterovaginal agenesis\"[tiab] OR "
     "\"Mullerian Ducts/abnormalities\"[Mesh]) AND (depress*[tiab] OR anxiety[tiab] OR "
     "\"mental health\"[tiab] OR psycholog*[tiab] OR distress[tiab] OR \"quality of life\"[tiab] "
     "OR \"body image\"[tiab] OR \"self-esteem\"[tiab] OR coping[tiab] OR psychosocial[tiab] OR "
     "\"Mental Health\"[Mesh] OR \"Adaptation, Psychological\"[Mesh] OR \"Quality of Life\"[Mesh]) "
     "AND (\"2019/01/01\"[dp] : \"2026/03/31\"[dp])", indent=False, size=10)
para("[[Scopus: TITLE-ABS-KEY(...) with the same two concept blocks; PsycINFO and CINAHL: the "
     "same keywords plus each database's own subject headings (e.g., APA Thesaurus “Coping "
     "Behavior”; CINAHL Headings “Quality of Life”).]]", indent=False)
table("**Table A1.** Records retrieved by database",
      ["Database", "Platform", "Date searched", "Records retrieved"],
      [["MEDLINE Ultimate; CINAHL Ultimate; Women's Studies International; APA PsycInfo "
        "(combined export: 145; 39; 15; 8)", "EBSCOhost", "Mar 29, 2026", "207"],
       ["APA PsycInfo (separate export)", "EBSCOhost", "Mar 29, 2026", "20"],
       ["MEDLINE (publications 2021–2026)", "PubMed", "[[Mar 29, 2026?]]", "146"],
       ["Scopus (publications 2019–2026)", "Scopus", "Mar 29, 2026", "143"],
       ["**Total**", "", "", f"**{P['identified']}**"]],
      widths=[2.9, 1.1, 1.2, 1.2],
      note="Records published before 2019 (n = 100, all from the EBSCOhost exports) were excluded "
           "at title and abstract screening and are counted among the 327 exclusions.")

page_break()
heading("Appendix B. Characteristics of Included Studies")
para("[[Complete one row per included study from your data-charting form. Column totals must "
     "match the counts reported in the Results.]]", indent=False)
table("**Table B1.** Characteristics of included studies (N = 34)",
      ["#", "Author (year)", "Country", "Design", "Sample (n; age)", "Mental health outcomes",
       "Coping mechanisms", "Healthcare gaps"],
      [[str(i), "", "", "", "", "", "", ""] for i in range(1, N + 1)],
      widths=[0.3, 1.0, 0.7, 0.8, 0.8, 1.1, 0.9, 0.8], size=8)

page_break()
heading("Appendix C. PRISMA-ScR Checklist")
prisma_items = [
    ("Title", "1", "Title page"),
    ("Structured summary", "2", "Abstract"),
    ("Rationale", "3", "Introduction"),
    ("Objectives", "4", "Introduction (research question)"),
    ("Protocol and registration", "5", "Methods: Study Design [[complete]]"),
    ("Eligibility criteria", "6", "Methods: Eligibility Criteria"),
    ("Information sources", "7", "Methods: Information Sources; Appendix A"),
    ("Search", "8", "Appendix A [[complete]]"),
    ("Selection of sources of evidence", "9", "Methods: Study Selection"),
    ("Data charting process", "10", "Methods: Data Charting"),
    ("Data items", "11", "Methods: Data Charting"),
    ("Critical appraisal of individual sources of evidence (optional)", "12",
     "Methods: Synthesis (not performed)"),
    ("Synthesis of results", "13", "Methods: Synthesis"),
    ("Selection of sources of evidence", "14", "Results; Figure 1 [[add full-text stage]]"),
    ("Characteristics of sources of evidence", "15", "Results; Table 1; Appendix B"),
    ("Critical appraisal within sources of evidence (optional)", "16", "Not applicable"),
    ("Results of individual sources of evidence", "17", "Appendix B"),
    ("Synthesis of results", "18", "Results; Tables 2–4; Figures 2–4"),
    ("Summary of evidence", "19", "Discussion: Summary of Evidence"),
    ("Limitations", "20", "Discussion: Strengths and Limitations"),
    ("Conclusions", "21", "Discussion: Conclusions"),
    ("Funding", "22", "Declarations"),
]
table("**Table C1.** PRISMA-ScR checklist (Tricco et al., 2018)",
      ["Section / topic", "Item", "Reported in"],
      [[a, b, c] for a, b, c in prisma_items], widths=[3.0, 0.6, 2.8])

# fill in the word count on the title page
wc = len(BODY_WORDS)
for p in doc.paragraphs:
    for r in p.runs:
        if "{WORDCOUNT}" in r.text:
            r.text = r.text.replace("{WORDCOUNT}", f"{wc:,}")

out = ROOT / "manuscript" / "MRKH_Scoping_Review_Manuscript.docx"
out.parent.mkdir(exist_ok=True)
doc.save(out)
print(f"wrote {out} (main text ≈ {wc} words)")

# ====================================================================== SEPARATE REFERENCE LIST
ref_doc = Document()
for sec in ref_doc.sections:
    sec.left_margin = sec.right_margin = sec.top_margin = sec.bottom_margin = Inches(1)
st = ref_doc.styles["Normal"]
st.font.name = "Times New Roman"
st.font.size = Pt(12)
st.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
doc_backup, doc = doc, ref_doc  # reuse para()/add_runs() helpers on the reference document
counting["on"] = False
para("**References (AMA 11th edition)**", align=WD_ALIGN_PARAGRAPH.CENTER, size=14,
     spacing=WD_LINE_SPACING.SINGLE)
para("*Mental Health and Psychosocial Outcomes Among Individuals With "
     "Mayer-Rokitansky-Küster-Hauser (MRKH) Syndrome: A Scoping Review*",
     align=WD_ALIGN_PARAGRAPH.CENTER, spacing=WD_LINE_SPACING.SINGLE)
para("Numbered in order of first citation in the manuscript. In-text citations are superscript "
     "numerals, placed after periods and commas and before colons and semicolons.",
     indent=False, size=10, spacing=WD_LINE_SPACING.SINGLE)
for i, r in enumerate(refs, 1):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    p.paragraph_format.first_line_indent = Inches(-0.35)
    p.paragraph_format.space_after = Pt(6)
    add_runs(p, f"{i}.\t{r}")
para("**Poster reference list** (poster numbering; shortened AMA format)", indent=False,
     spacing=WD_LINE_SPACING.SINGLE)
poster_map = [1, 2, 13, 14, 4, 5, 6, 11]  # poster ref n -> manuscript ref number
for i, m in enumerate(poster_map, 1):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    p.paragraph_format.first_line_indent = Inches(-0.35)
    add_runs(p, f"{i}.\t{refs[m - 1]}")
doc = doc_backup
ref_out = ROOT / "manuscript" / "References_AMA.docx"
ref_doc.save(ref_out)
print("wrote", ref_out)
