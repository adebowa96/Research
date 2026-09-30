"""Data extraction for the 35 included studies.

AI-ASSISTED: 30 of 35 rows were checked against the full-text PDF (see note column);
5 rows (MISSING_FULL_TEXT) are still coded from title/abstract only. The review team
should confirm all entries before publication.

Domain codes (a study can have several):
  D  Depression and/or anxiety (symptoms or diagnoses)
  Q  Quality of life, body/genital image, or self-esteem
  S  Psychosexual and relational (sexual esteem/distress/wellbeing, intimacy, relationships)
  P  Broader psychological distress (distress, shame, identity disruption, psychopathology)
  C  Coping mechanisms documented
  H  Healthcare system gaps reported
Coping categories: peer (peer/family/social support), counsel (psychological counseling or
intervention), identity (identity reconstruction / positive reappraisal), spiritual,
accept (acceptance), avoid (avoidance / concealment, maladaptive), advocate (self-advocacy)
"""
import csv
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent

# record_id: (first author, year, country, region, design, detail, n, domains, coping, note)
STUDIES = {
    "R002": ("Lei", 2024, "China", "Asia", "Quantitative", "Longitudinal case series (2 survey rounds)", "53", "DQS", "", "Full text checked"),
    "R003": ("Weijenborg", 2019, "Netherlands", "Europe", "Quantitative", "Case-control", "54 (+79 controls)", "DQSP", "", "Full text checked; SCL-90 and HADS did not differ from controls; lower sexual esteem and genital self-image"),
    "R004": ("Khairudin", 2026, "Malaysia", "Asia", "Quantitative", "Cross-sectional", "77", "D", "", "Full text checked; GAD-7 anxiety 37.7%, PHQ-9 depression 32.5%"),
    "R010": ("Di Mattei", 2026, "Italy", "Europe", "Qualitative", "Thematic analysis of online forum", "NR", "SPH", "", "Abstract only (full text not obtained); online 2024; country from affiliations"),
    "R011": ("Güner", 2025, "Türkiye", "Asia", "Qualitative", "Phenomenological interviews", "10", "SP", "", "Full text checked"),
    "R012": ("Kang", 2020, "China", "Asia", "Quantitative", "Cross-sectional (dilation vs surgery)", "133", "QS", "", "Full text checked; FSFI and WHODAS 2.0"),
    "R013": ("Gilfillan", 2024, "United Kingdom", "Europe", "Qualitative", "Interpretative phenomenological analysis", "13", "PCH", "accept,avoid", "Full text checked"),
    "R014": ("Jensen", 2024, "Denmark", "Europe", "Qualitative", "Semi-structured interviews (life course)", "18", "SPCH", "peer", "Abstract only (full text not obtained)"),
    "R017": ("Rajesh", 2026, "Canada", "North America", "Qualitative", "Semi-structured interviews", "12", "QSC", "identity", "Full text checked"),
    "R020": ("Karpel", 2025, "France", "Europe", "Quantitative", "Cross-sectional (uterus transplant candidates)", "16 recipients (+16 partners, 16 donors)", "DQSP", "", "Full text checked; HADS: no depression and low anxiety in recipients"),
    "R021": ("Rall", 2021, "Germany", "Europe", "Quantitative", "Prospective cohort (pre/post surgery)", "82", "DQSPC", "peer", "Full text checked; depression screening added (D)"),
    "R032": ("Güner", 2026, "Türkiye", "Asia", "Qualitative", "Descriptive phenomenological interviews", "10", "SPC", "avoid,identity,spiritual,peer", "Full text checked"),
    "R034": ("Sabatucci", 2019, "Italy", "Europe", "Quantitative", "Descriptive longitudinal", "39", "QS", "", "Full text checked; FSFI and PGWBI"),
    "R038": ("Shao", 2022, "China", "Asia", "Quantitative", "Prospective pre/post intervention", "30", "DC", "counsel", "Full text checked"),
    "R040": ("Jensen", 2024, "Denmark", "Europe", "Qualitative", "Semi-structured interviews", "18", "QSP", "", "Full text checked; same Danish interview cohort as R267"),
    "R052": ("Sorouri Khorashad", 2025, "United States", "North America", "Quantitative", "Retrospective cohort (EHR, matched referents)", "101 MA (60 uterovaginal agenesis) + 63 CAIS", "DP", "", "Full text checked; MA cohort reported separately from CAIS"),
    "R057": ("Le", 2024, "Vietnam", "Asia", "Qualitative", "In-depth interviews", "20", "CH", "avoid", "Full text checked; religion reported as a barrier to surrogacy, not as coping"),
    "R060": ("Mao", 2024, "China", "Asia", "Quantitative", "Retrospective (with controls)", "42 (+30 controls)", "QS", "", "Abstract only (full text not obtained)"),
    "R063": ("Stepanow", 2023, "Austria", "Europe", "Qualitative", "Semi-structured interviews", "10 (+20 controls)", "QSC", "accept", "Full text checked"),
    "R073": ("Marshall", 2025, "United States/Canada", "North America", "Qualitative", "Semi-structured interviews", "12", "CH", "advocate", "Full text checked"),
    "R084": ("Song", 2020, "China", "Asia", "Quantitative", "Cross-sectional (with controls)", "141 (+178 controls)", "DS", "", "Full text checked; GAD-7 24.1% moderate-severe; associated with sexual dysfunction"),
    "R086": ("Jha", 2022, "India", "Asia", "Quantitative", "Case-control", "NR", "DQS", "", "Abstract only (full text not obtained); country from affiliations"),
    "R091": ("Beisert", 2022, "Poland", "Europe", "Quantitative", "Case-control", "32 (+32 controls)", "DQSP", "", "Full text checked"),
    "R094": ("Tsitoura", 2021, "Greece", "Europe", "Qualitative", "Semi-structured interviews", "7", "SPCH", "avoid,peer", "Full text checked"),
    "R104": ("Chen", 2020, "China", "Asia", "Quantitative", "Cross-sectional (with controls)", "141 (+178 controls)", "DS", "", "Full text checked; same sample as Song 2020 (R084)"),
    "R105": ("Carroll", 2020, "Multinational", "Multinational", "Quantitative", "Cross-sectional online survey", "263", "QPC", "peer,identity", "Full text checked"),
    "R112": ("Pennesi", 2023, "Multinational (40 countries)", "Multinational", "Mixed methods", "Cross-sectional mixed-methods survey", "616", "SPH", "", "Full text checked"),
    "R131": ("Vosoughi", 2022, "Iran", "Asia", "Quantitative", "Randomized controlled trial", "38", "QSC", "counsel", "Full text checked"),
    "R149": ("Hatim", 2021, "Malaysia", "Asia", "Mixed methods", "Qualitative with quantitative component", "12", "DQSPCH", "peer,avoid", "Full text checked; RSE self-esteem low-moderate; 2 participants depressed"),
    "R227": ("Arsy", 2019, "Indonesia", "Asia", "Not reported", "Not reported in export (no abstract)", "NR", "Q", "", "Title only (full text not obtained); design and country need verification"),
    "R267": ("Lou", 2024, "Denmark", "Europe", "Qualitative", "In-depth interviews", "18", "PCH", "peer", "Full text checked; same Danish interview cohort as R040"),
    "R001": ("Pittman", 2025, "Australia", "Oceania", "Quantitative", "Cross-sectional survey (congenital vs acquired uterine factor infertility)", "39 (31 MRKH)", "DQP", "", "Full text checked; MRKH results reported separately; DASS-21 and FertiQoL"),
    "R223": ("Ngoumou", 2022, "Cameroon, Côte d'Ivoire, Senegal", "Africa", "Qualitative", "In-depth interviews", "5", "QSPCH", "avoid", "Full text checked; family secrecy; religious beliefs limited dilation"),
    "R234": ("Järvholm", 2020, "Sweden", "Europe", "Qualitative", "Interviews after uterus transplantation", "9 (8 MRKH)", "QSP", "", "Full text checked; 8 of 9 recipients had MRKH"),
    "R244": ("Scollo", 2020, "Italy", "Europe", "Quantitative", "Retrospective (MMPI-2; uterus transplant candidates)", "19 (18 MRKH)", "DP", "", "Full text checked"),
}
MISSING_FULL_TEXT = {rid for rid, s in STUDIES.items() if not s[9].startswith("Full text checked")}

DOMAINS = [("D", "Depression & anxiety"), ("Q", "Reduced QoL, body image & self-esteem"),
           ("S", "Psychosexual & relational challenges"), ("P", "Broader psychological distress"),
           ("C", "Coping mechanisms documented"), ("H", "Healthcare system gaps")]
COPING = [("peer", "Peer, family & social support"), ("counsel", "Psychological counseling/intervention"),
          ("identity", "Identity reconstruction / positive reappraisal"), ("spiritual", "Spiritual coping"),
          ("accept", "Acceptance"), ("avoid", "Avoidance / concealment (maladaptive)"),
          ("advocate", "Self-advocacy")]

assert len(STUDIES) == 35
records = {r["record_id"]: r for r in csv.DictReader(open(HERE / "records_unique.csv", encoding="utf-8"))}

rows = []
for rid, (au, yr, country, region, design, detail, n, dom, cop, note) in STUDIES.items():
    r = records[rid]
    rows.append({"record_id": rid, "study": f"{au} {yr}", "title": r["title"], "journal": r["journal"],
                 "doi": r["doi"], "country": country, "region": region, "design": design,
                 "design_detail": detail, "sample_n": n,
                 **{name: ("yes" if code in dom else "") for code, name in DOMAINS},
                 "coping_types": "; ".join(dict(COPING)[c] for c in cop.split(",") if c),
                 "full_text_checked": "no" if rid in MISSING_FULL_TEXT else "yes",
                 "verification_note": note})

with open(HERE / "extraction_provisional.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(sorted(rows, key=lambda x: x["study"]))

N = len(rows)
dom_counts = [(name, sum(1 for s in STUDIES.values() if code in s[7])) for code, name in DOMAINS]
cop_counts = [(name, sum(1 for s in STUDIES.values() if code in s[8].split(","))) for code, name in COPING]
design_counts = Counter(s[4] for s in STUDIES.values())
region_counts = Counter(s[3] for s in STUDIES.values())

print("Domains:")
for name, n in dom_counts:
    print(f"  {name:<42}{n:>3} ({n / N:.0%})")
print("Coping types:", cop_counts)
print("Designs:", dict(design_counts))
print("Regions:", dict(region_counts))

summary = {"domains": dom_counts, "coping": cop_counts, "designs": dict(design_counts),
           "regions": dict(region_counts), "n": N,
           "full_text_checked": N - len(MISSING_FULL_TEXT), "missing_full_text": sorted(MISSING_FULL_TEXT)}
(HERE / "extraction_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
