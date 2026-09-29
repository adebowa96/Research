"""Merge the four search exports (516 records), identify duplicates by DOI or normalized
title, and write records_all.csv (every record, with duplicate flags) and
records_unique.csv (one row per unique record, abstract kept when any source has one)."""
import csv
import re
from pathlib import Path

HERE = Path(__file__).parent
EXP = HERE / "exports"
csv.field_size_limit(10**9)


def norm_title(t):
    return re.sub(r"[^a-z0-9]", "", (t or "").lower())[:90]


def norm_doi(d):
    d = (d or "").strip().lower()
    d = re.sub(r"^https?://(dx\.)?doi\.org/", "", d)
    return d.rstrip(".")


records = []


def add(source, db, title, authors, year, journal, doi, doctype, language, abstract, pmid="",
        volume="", issue="", pages=""):
    records.append(dict(source=source, database=db, title=(title or "").strip(),
                        authors=(authors or "").strip(), year=str(year or "").strip()[:4],
                        journal=(journal or "").strip(), doi=norm_doi(doi),
                        doctype=(doctype or "").strip(), language=(language or "").strip(),
                        abstract=(abstract or "").strip(), pmid=pmid, volume=(volume or "").strip(),
                        issue=(issue or "").strip(), pages=(pages or "").strip()))


for name, label in (("ebsco_multi_2026-03-29.csv", "EBSCOhost combined export"),
                    ("ebsco_psycinfo_2026-03-29.csv", "EBSCOhost PsycInfo export")):
    for r in csv.DictReader(open(EXP / name, encoding="utf-8-sig")):
        add(label, r["longDBName"], r["title"], r["contributors"], r["publicationDate"],
            r["source"], r.get("doi"), r["docTypes"], r["language"], r["abstract"],
            volume=r.get("volume"), issue=r.get("issue"),
            pages="-".join(x for x in (r.get("pageStart"), r.get("pageEnd")) if x))

for r in csv.DictReader(open(EXP / "scopus_2026-03-29.csv", encoding="utf-8-sig")):
    add("Scopus export", "Scopus", r["Title"], r["Authors"], r["Year"], r["Source title"],
        r["DOI"], r["Document Type"], "", "", volume=r["Volume"], issue=r["Issue"],
        pages="-".join(x for x in (r["Page start"], r["Page end"]) if x) or r["Art. No."])

# PubMed "Summary (text)" format: numbered citations separated by blank lines
txt = (EXP / "pubmed_summary.txt").read_text(encoding="utf-8")
for blk in re.split(r"\n\s*\n(?=\d+: )", txt.strip()):
    b = " ".join(blk.split())
    body = re.sub(r"^\d+: ", "", b)
    authors, rest = body.split(". ", 1) if ". " in body else ("", body)
    # title ends at the first ". " followed by the journal abbreviation
    m = re.match(r"(.+?[.?!\]])\s+(.+?)\. (\d{4})", rest)
    vip = re.search(r"\d{4}(?: [A-Z][a-z]{2}(?: \d{1,2})?)?;(\d+)(?:\(([^)]+)\))?:([^.\s]+)", b)
    title, journal, year = (m.group(1), m.group(2), m.group(3)) if m else (rest, "", "")
    doi = re.search(r"doi: (\S+?)\.?(?= |$)", b)
    pmid = re.search(r"PMID: (\d+)", b)
    lang = re.search(r"\. (French|German|Chinese|Spanish|Polish)\. ", b)
    add("PubMed export", "PubMed", title.rstrip("."), authors, year, journal,
        doi.group(1) if doi else "", "", lang.group(1) if lang else "", "",
        pmid.group(1) if pmid else "", volume=vip.group(1) if vip else "",
        issue=(vip.group(2) or "") if vip else "", pages=vip.group(3) if vip else "")

assert len(records) == 516, len(records)

# duplicate detection: a record is a duplicate if its DOI or normalized title was seen before
groups = []
key_to_group = {}
for i, r in enumerate(records):
    keys = [k for k in (("doi:" + r["doi"]) if r["doi"] else "",
                        ("t:" + norm_title(r["title"])) if norm_title(r["title"]) else "") if k]
    g = next((key_to_group[k] for k in keys if k in key_to_group), None)
    if g is None:
        g = len(groups)
        groups.append([])
    groups[g].append(i)
    for k in keys:
        key_to_group[k] = g
    r["group"] = g

for g, members in enumerate(groups):
    for n, i in enumerate(members):
        records[i]["record_id"] = f"R{g + 1:03d}"
        records[i]["duplicate"] = "no" if n == 0 else "yes"

fields = ["record_id", "duplicate", "source", "database", "title", "authors", "year", "journal",
          "doi", "pmid", "doctype", "language", "abstract", "volume", "issue", "pages"]
with open(HERE / "records_all.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
    w.writeheader()
    w.writerows(records)

unique = []
for g, members in enumerate(groups):
    rs = [records[i] for i in members]
    best = max(rs, key=lambda r: (bool(r["abstract"]), bool(r["doi"]), bool(r["doctype"])))
    u = dict(best)
    u["sources"] = "; ".join(sorted({r["database"] for r in rs}))
    u["doi"] = next((r["doi"] for r in rs if r["doi"]), "")
    u["pmid"] = next((r["pmid"] for r in rs if r["pmid"]), "")
    u["doctype"] = " | ".join(sorted({r["doctype"] for r in rs if r["doctype"]}))
    u["language"] = next((r["language"] for r in rs if r["language"]), "")
    u["year"] = next((r["year"] for r in rs if r["year"]), "")
    # prefer PubMed citation details (standard abbreviations), then any source with pages
    cite = sorted(rs, key=lambda r: (r["database"] != "PubMed", not r["pages"]))[0]
    for k in ("volume", "issue", "pages"):
        u[k] = cite[k] or next((r[k] for r in rs if r[k]), "")
    u["journal_abbrev"] = next((r["journal"] for r in rs if r["database"] == "PubMed"), "")
    u["authors_all"] = " || ".join(r["authors"] for r in rs)
    unique.append(u)

with open(HERE / "records_unique.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["record_id", "sources"] + fields[4:] + ["journal_abbrev", "authors_all"],
                       extrasaction="ignore")
    w.writeheader()
    w.writerows(unique)

print(f"records: {len(records)}  unique: {len(unique)}  duplicates removed: "
      f"{len(records) - len(unique)}  with abstract: {sum(1 for u in unique if u['abstract'])}")
