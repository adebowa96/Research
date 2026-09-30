"""AMA reference list with automatic numbering in order of first citation.

In manuscript text write citations as ^{@key} or ^{@key1,@key2}; resolve() replaces them with
superscript numbers (ranges collapsed, e.g. 4–6) the first time each key is cited.
Keys are short names for background sources and record IDs (e.g. R104) for included studies."""
import csv
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESCREEN = ROOT / "rescreen"

BACKGROUND = {
    "acog": "American College of Obstetricians and Gynecologists' Committee on Adolescent Health "
            "Care. ACOG Committee Opinion No. 728: Müllerian agenesis: diagnosis, management, and "
            "treatment. *Obstet Gynecol*. 2018;131(1):e35-e42. doi:10.1097/AOG.0000000000002458",
    "herlin16": "Herlin M, Bjørn AMB, Rasmussen M, Trolle B, Petersen MB. Prevalence and patient "
                "characteristics of Mayer-Rokitansky-Küster-Hauser syndrome: a nationwide "
                "registry-based study. *Hum Reprod*. 2016;31(10):2384-2390. doi:10.1093/humrep/dew220",
    "herlin20": "Herlin MK, Petersen MB, Brännström M. Mayer-Rokitansky-Küster-Hauser (MRKH) "
                "syndrome: a comprehensive update. *Orphanet J Rare Dis*. 2020;15(1):214. "
                "doi:10.1186/s13023-020-01491-9",
    "hb09": "Heller-Boersma JG, Schmidt UH, Edmonds DK. Psychological distress in women with "
            "uterovaginal agenesis (Mayer-Rokitansky-Kuster-Hauser syndrome, MRKH). "
            "*Psychosomatics*. 2009;50(3):277-281. doi:10.1176/appi.psy.50.3.277",
    "laggari": "Laggari V, Diareme S, Christogiorgos S, et al. Anxiety and depression in "
               "adolescents with polycystic ovary syndrome and Mayer-Rokitansky-Küster-Hauser "
               "syndrome. *J Psychosom Obstet Gynaecol*. 2009;30(2):83-88. "
               "doi:10.1080/01674820802546204",
    "liao": "Liao LM, Conway GS, Ismail-Pratt I, Bikoo M, Creighton SM. Emotional and sexual "
            "wellness and quality of life in women with Rokitansky syndrome. *Am J Obstet "
            "Gynecol*. 2011;205(2):117.e1-117.e6. doi:10.1016/j.ajog.2011.03.013",
    "bean": "Bean EJ, Mazur T, Robinson AD. Mayer-Rokitansky-Küster-Hauser syndrome: sexuality, "
            "psychological effects, and quality of life. *J Pediatr Adolesc Gynecol*. "
            "2009;22(6):339-346. doi:10.1016/j.jpag.2008.11.006",
    "patterson": "Patterson CJ, Crawford R, Jahoda A. Exploring the psychological impact of "
                 "Mayer-Rokitansky-Küster-Hauser syndrome on young women: an interpretative "
                 "phenomenological analysis. *J Health Psychol*. 2016;21(7):1228-1240. "
                 "doi:10.1177/1359105314551077",
    "facchin": "Facchin F, Francini F, Ravani S, et al. Psychological impact and health-related "
               "quality-of-life outcomes of Mayer-Rokitansky-Küster-Hauser syndrome: a systematic "
               "review and narrative synthesis. *J Health Psychol*. 2021;26(1):26-39. "
               "doi:10.1177/1359105319901308",
    "tsarna": "Tsarna E, Eleftheriades A, Eleftheriades M, Kalampokas E, Liakopoulou MK, "
              "Christopoulos P. The impact of Mayer-Rokitansky-Küster-Hauser syndrome on "
              "psychology, quality of life, and sexual life of patients: a systematic review. "
              "*Children (Basel)*. 2022;9(4):484. doi:10.3390/children9040484",
    "arksey": "Arksey H, O'Malley L. Scoping studies: towards a methodological framework. *Int J "
              "Soc Res Methodol*. 2005;8(1):19-32. doi:10.1080/1364557032000119616",
    "tricco": "Tricco AC, Lillie E, Zarin W, et al. PRISMA Extension for Scoping Reviews "
              "(PRISMA-ScR): checklist and explanation. *Ann Intern Med*. 2018;169(7):467-473. "
              "doi:10.7326/M18-0850",
    "mak": "Mak S, Thomas A. Steps for conducting a scoping review. *J Grad Med Educ*. "
           "2022;14(5):565-567. doi:10.4300/JGME-D-22-00621.1",
    "hb07": "Heller-Boersma JG, Schmidt UH, Edmonds DK. A randomized controlled trial of a "
            "cognitive-behavioural group intervention versus waiting-list control for women with "
            "uterovaginal agenesis (Mayer-Rokitansky-Küster-Hauser syndrome: MRKH). *Hum Reprod*. "
            "2007;22(8):2296-2301. doi:10.1093/humrep/dem167",
    "okunomiya": "Okunomiya A, Tsuyuki K, Ohsuga T, et al. Long-term psychosocial outcomes in "
                 "Japanese Mayer-Rokitansky-Küster-Hauser syndrome: a single-center study. *J "
                 "Obstet Gynaecol Res*. 2026;52(5):e70291. doi:10.1111/jog.70291",
}

JOURNAL_ABBREV = {
    "R003": "Hum Reprod", "R012": "Fertil Steril", "R021": "J Clin Med", "R034": "BJOG",
    "R063": "J Sex Med", "R073": "J Pediatr Adolesc Gynecol", "R084": "Chin Med J (Engl)",
    "R104": "Orphanet J Rare Dis", "R105": "J Pediatr Adolesc Gynecol",
    "R149": "J Pediatr Adolesc Gynecol", "R164": "Evol Psychiatr",
    "R227": "Indian J Public Health Res Dev", "R223": "Pan Afr Med J", "R234": "Hum Reprod",
    "R244": "Ital J Gynaecol Obstet",
}
# corrections checked against the full-text PDFs (export metadata was wrong or incomplete)
AUTHOR_FIX = {
    "R223": "Ngoumou RD",
    "R003": "Weijenborg PTM, Kluivers KB, Dessens AB, ten Kate-Booij MJ, Both S",
}
TITLE_FIX = {
    "R004": ("Kϋster", "Küster"),
    "R017": ("wellbeing-a", "wellbeing—a"),
    "R234": ("'complete' woman-a", '"complete" woman—a'),
    "R244": ("Uterus Transplantation", "uterus transplantation"),
    "R052": ("Aplasia/Agenesis", "aplasia/agenesis"),
    "R010": ("Hauser Syndrome (MRKH)", "Hauser syndrome (MRKH)"),
    "R223": ("(MRKH) Syndrome", "(MRKH) syndrome"),
}
PAGE_FIX = {"R021": "1269"}  # article number (export listed page range 1-33)


def _initials(given):
    parts = re.split(r"[\s.]+", given.strip())
    out = ""
    for p in parts:
        if not p:
            continue
        out += "".join(s[0].upper() for s in p.split("-") if s) if not p.isupper() or len(p) > 3 else p
    return out


def ama_authors(raw):
    raw = raw.strip()
    if ";" in raw:
        names = [a.strip() for a in raw.split(";") if a.strip()]
    else:  # PubMed style "Lou S, Jensen AH, ..."
        names = [a.strip() for a in raw.split(",") if a.strip()]
    out = []
    for n in names:
        if "," in n:
            last, given = [x.strip() for x in n.split(",", 1)]
            out.append(f"{last} {_initials(given)}".strip())
        else:
            m = re.match(r"(.+?)\s+([A-Z][A-Z.]*\.?)$", n)
            out.append(f"{m.group(1)} {m.group(2).replace('.', '')}" if m else n)
    if len(out) > 6:
        out = out[:3] + ["et al"]
    return ", ".join(out)


KEEP_CAPS = {"Mayer", "Rokitansky", "Küster", "Kuster", "Kuester", "Hauser", "Rokitansky's",
             "Müllerian", "Mullerian", "Denmark", "Malaysia", "Vecchietti", "Canada", "Vietnam",
             "Türkiye", "Wharton", "Sheares", "George", "McIndoe", "Abbé", "Chinese", "Japanese",
             "Interceed", "Rokitansky-Küster-Hauser", "I"}


def sentence_case(title):
    words = title.split(" ")
    caps = sum(1 for w in words if w[:1].isupper())
    if caps / max(len(words), 1) < 0.5:  # already sentence case
        return title
    out = []
    for i, w in enumerate(words):
        core = re.sub(r"[^\wÀ-ſ'-]", "", w)
        prev = out[-1] if out else ""
        keep = (i == 0 or prev.endswith(":") or prev.endswith(".") or core.isupper() and len(core) > 1
                or any(part in KEEP_CAPS for part in re.split(r"[-()]", core))
                or re.search(r"[A-Z][A-Z]", core))
        out.append(w if keep else re.sub(r"(^|[-(\"“])([A-ZÀ-Þ])", lambda m: m.group(1) + m.group(2).lower(), w))
    return " ".join(out)


def lower_after_colon(title):
    """AMA: in article titles the first word after a colon is lowercase unless it is a proper
    noun or abbreviation."""
    def repl(m):
        word = m.group(2)
        if word in KEEP_CAPS or re.search(r"[A-Z].*[A-Z]", word):
            return m.group(0)
        return m.group(1) + word[0].lower() + word[1:]
    return re.sub(r"(:\s+)([A-Z][\w'-]*)", repl, title)


def included_reference(rec):
    rid = rec["record_id"]
    title = html.unescape(re.sub(r"<[^>]+>", "", rec["title"])).strip().rstrip(".")
    if rid in TITLE_FIX:
        title = title.replace(*TITLE_FIX[rid])
    title = lower_after_colon(sentence_case(title))
    end = "" if title.endswith(("?", "!")) else "."
    journal = JOURNAL_ABBREV.get(rid) or rec["journal_abbrev"] or rec["journal"]
    vol, iss = rec["volume"], rec["issue"]
    pages = PAGE_FIX.get(rid, rec["pages"])
    vi = f"{vol}({iss})" if vol and iss else vol
    loc = f"{rec['year']};{vi}:{pages}" if vi and pages else f"{rec['year']};{vi}" if vi else rec["year"]
    doi = f" doi:{rec['doi']}" if rec["doi"] else ""
    authors = AUTHOR_FIX.get(rid) or ama_authors(rec["authors"])
    return f"{authors}. {title}{end} *{journal}*. {loc}.{doi}"


def load_included():
    recs = {r["record_id"]: r for r in csv.DictReader(open(RESCREEN / "records_unique.csv", encoding="utf-8"))}
    ids = re.findall(r'"(R\d{3})": \(', (RESCREEN / "extraction.py").read_text())
    return {rid: included_reference(recs[rid]) for rid in ids}


class Citer:
    def __init__(self):
        self.lib = dict(BACKGROUND)
        self.lib.update(load_included())
        self.order = []

    def number(self, key):
        if key not in self.lib:
            raise KeyError(f"unknown citation key {key}")
        if key not in self.order:
            self.order.append(key)
        return self.order.index(key) + 1

    def resolve(self, text):
        def repl(m):
            nums = sorted(self.number(k.strip().lstrip("@")) for k in m.group(1).split(","))
            parts, i = [], 0
            while i < len(nums):
                j = i
                while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
                    j += 1
                parts.append(f"{nums[i]}–{nums[j]}" if j - i >= 2 else
                             ",".join(str(n) for n in nums[i:j + 1]))
                i = j + 1
            return "^{" + ",".join(parts) + "}"
        return re.sub(r"\^\{(@[^}]+)\}", repl, text)

    def reference_list(self):
        return [self.lib[k] for k in self.order]
