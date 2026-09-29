"""Abstract-level data extraction for the 34 provisionally included studies.

AI-ASSISTED AND PROVISIONAL: each row was coded from the study's title and abstract only.
Every entry must be verified against the full text by the review team before publication.

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
    "R002": ("Lei", 2024, "China", "Asia", "Quantitative", "Longitudinal case series (2 survey rounds)", "53", "DQS", "", ""),
    "R003": ("Weijenborg", 2019, "Netherlands", "Europe", "Quantitative", "Case-control", "54 (+79 controls)", "QSP", "", "Country from author affiliations; verify"),
    "R004": ("Khairudin", 2026, "Malaysia", "Asia", "Quantitative", "Cross-sectional", "77", "D", "", ""),
    "R007": ("Magdoud", 2024, "Tunisia", "Africa", "Quantitative", "Retrospective comparative (with controls)", "30", "QS", "", "French-language article"),
    "R010": ("Di Mattei", 2026, "Italy", "Europe", "Qualitative", "Thematic analysis of online forum", "NR", "SPH", "", "Online 2024; country from affiliations"),
    "R011": ("Güner", 2025, "Türkiye", "Asia", "Qualitative", "Phenomenological interviews", "10", "SP", "", ""),
    "R012": ("Kang", 2020, "China", "Asia", "Quantitative", "Cross-sectional", "133", "QS", "", ""),
    "R013": ("Gilfillan", 2024, "United Kingdom", "Europe", "Qualitative", "Interpretative phenomenological analysis", "13", "PCH", "accept,avoid", "Country from affiliations; verify"),
    "R014": ("Jensen", 2024, "Denmark", "Europe", "Qualitative", "Semi-structured interviews (life course)", "18", "SPCH", "peer", ""),
    "R017": ("Rajesh", 2026, "Canada", "North America", "Qualitative", "Semi-structured interviews", "12", "QSC", "identity", ""),
    "R020": ("Karpel", 2025, "France", "Europe", "Quantitative", "Cross-sectional (uterus transplant candidates)", "16 (incl. partners, donors)", "DQSP", "", ""),
    "R021": ("Rall", 2021, "Germany", "Europe", "Quantitative", "Prospective cohort (pre/post surgery)", "82", "QSPC", "peer", ""),
    "R032": ("Güner", 2026, "Türkiye", "Asia", "Qualitative", "Descriptive phenomenological interviews", "10", "SPC", "avoid,identity,spiritual,peer", ""),
    "R034": ("Sabatucci", 2019, "Italy", "Europe", "Quantitative", "Descriptive longitudinal", "39", "QS", "", ""),
    "R038": ("Shao", 2022, "China", "Asia", "Quantitative", "Prospective pre/post intervention", "30", "DC", "counsel", ""),
    "R040": ("Jensen", 2024, "Denmark", "Europe", "Qualitative", "Semi-structured interviews", "18", "QSP", "", ""),
    "R052": ("Sorouri Khorashad", 2025, "United States", "North America", "Quantitative", "Retrospective cohort", "NR", "DP", "", ""),
    "R057": ("Le", 2024, "Vietnam", "Asia", "Qualitative", "In-depth interviews", "20", "CH", "avoid,spiritual", ""),
    "R060": ("Mao", 2024, "China", "Asia", "Quantitative", "Retrospective (with controls)", "42 (+30 controls)", "QS", "", ""),
    "R063": ("Stepanow", 2023, "Austria", "Europe", "Qualitative", "Semi-structured interviews", "10 (+20 controls)", "QSC", "accept", "Country from affiliations; verify"),
    "R065": ("Schäffeler", 2022, "Germany", "Europe", "Quantitative", "Quasi-experimental pre/post", "53", "DQSPC", "counsel", "German-language article"),
    "R073": ("Marshall", 2025, "United States/Canada", "North America", "Qualitative", "Semi-structured interviews", "NR", "CH", "advocate", ""),
    "R084": ("Song", 2020, "China", "Asia", "Quantitative", "Cross-sectional (with controls)", "141 (+178 controls)", "D", "", ""),
    "R086": ("Jha", 2022, "India", "Asia", "Quantitative", "Case-control", "NR", "DQS", "", "Country from affiliations; verify"),
    "R091": ("Beisert", 2022, "Poland", "Europe", "Quantitative", "Case-control", "32 (+32 controls)", "DQSP", "", "Country from affiliations; verify"),
    "R094": ("Tsitoura", 2021, "Greece", "Europe", "Qualitative", "Semi-structured interviews", "7", "SPCH", "avoid,peer", "Country from affiliations; verify"),
    "R104": ("Chen", 2020, "China", "Asia", "Quantitative", "Cross-sectional (with controls)", "141 (+178 controls)", "DS", "", "Same sample as Song 2020 (R084); verify"),
    "R105": ("Carroll", 2020, "Multinational", "Multinational", "Quantitative", "Cross-sectional online survey", "263", "QPC", "peer,identity", ""),
    "R112": ("Pennesi", 2023, "Multinational (40 countries)", "Multinational", "Mixed methods", "Cross-sectional mixed-methods survey", "616", "SPH", "", ""),
    "R131": ("Vosoughi", 2022, "Iran", "Asia", "Quantitative", "Randomized controlled trial", "38", "QSC", "counsel", ""),
    "R149": ("Hatim", 2021, "Malaysia", "Asia", "Mixed methods", "Qualitative with quantitative component", "12", "SPCH", "peer", ""),
    "R164": ("Blanc", 2019, "France", "Europe", "Mixed methods", "Qualitative and quantitative (clinical interviews)", "17", "QSP", "", "French-language article"),
    "R227": ("Arsy", 2019, "Indonesia", "Asia", "Not reported", "Not reported in export (no abstract)", "NR", "Q", "", "No abstract available; design and country need full-text verification"),
    "R267": ("Lou", 2024, "Denmark", "Europe", "Qualitative", "Interview study", "NR", "PH", "", "No abstract in export; coded from published summary"),
}

DOMAINS = [("D", "Depression & anxiety"), ("Q", "Reduced QoL, body image & self-esteem"),
           ("S", "Psychosexual & relational challenges"), ("P", "Broader psychological distress"),
           ("C", "Coping mechanisms documented"), ("H", "Healthcare system gaps")]
COPING = [("peer", "Peer, family & social support"), ("counsel", "Psychological counseling/intervention"),
          ("identity", "Identity reconstruction / positive reappraisal"), ("spiritual", "Spiritual coping"),
          ("accept", "Acceptance"), ("avoid", "Avoidance / concealment (maladaptive)"),
          ("advocate", "Self-advocacy")]

assert len(STUDIES) == 34
records = {r["record_id"]: r for r in csv.DictReader(open(HERE / "records_unique.csv", encoding="utf-8"))}

rows = []
for rid, (au, yr, country, region, design, detail, n, dom, cop, note) in STUDIES.items():
    r = records[rid]
    rows.append({"record_id": rid, "study": f"{au} {yr}", "title": r["title"], "journal": r["journal"],
                 "doi": r["doi"], "country": country, "region": region, "design": design,
                 "design_detail": detail, "sample_n": n,
                 **{name: ("yes" if code in dom else "") for code, name in DOMAINS},
                 "coping_types": "; ".join(dict(COPING)[c] for c in cop.split(",") if c),
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
           "regions": dict(region_counts), "n": N}
(HERE / "extraction_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
