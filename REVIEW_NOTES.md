# MRKH Scoping Review: Accuracy Check and Corrections

Read this before you submit the manuscript or print the poster. It lists every factual
or numerical problem found in the draft text, what was changed, and what only you can
confirm from your screening and data-extraction records.

Everything numeric in the poster and manuscript comes from one file,
`scripts/data.json`. If a number changes, edit it there and rebuild (see README).

---

## 1. Errors corrected

### 1a. Four of your seven references had the wrong journal, volume, or pages (checked against PubMed and the publishers)

| Draft citation | Problem | Corrected citation |
|---|---|---|
| Heller-Boersma JG, et al. *J Psychosom Obstet Gynaecol.* 2009;30(4):247–254 | Wrong journal, volume, and pages | Heller-Boersma JG, Schmidt UH, Edmonds DK. Psychological distress in women with uterovaginal agenesis (MRKH). ***Psychosomatics.* 2009;50(3):277–281** |
| Liao LM, et al. "Long-term outcomes in women with vaginal agenesis." *BJOG.* 2011;118(13):1596–1601 | Wrong title, journal, and pages | Liao LM, Conway GS, Ismail-Pratt I, et al. Emotional and sexual wellness and quality of life in women with Rokitansky syndrome. ***Am J Obstet Gynecol.* 2011;205(2):117.e1–117.e6** |
| Bean EJ, et al. "A qualitative study of women's experiences." *Eur J Obstet Gynecol.* 2009;144(2):172–176 | Wrong title, journal, and pages; it is a literature review, not a qualitative study | Bean EJ, Mazur T, Robinson AD. MRKH syndrome: sexuality, psychological effects, and quality of life. ***J Pediatr Adolesc Gynecol.* 2009;22(6):339–346** |
| Laggari V, et al. *J Pediatr Adolesc Gynecol.* 2009;22(1):37–43 | Wrong journal and pages; title also covers PCOS | Laggari V, et al. Anxiety and depression in adolescents with polycystic ovary syndrome and MRKH. ***J Psychosom Obstet Gynaecol.* 2009;30(2):83–88** |
| Herlin M, et al. *Hum Reprod.* 2016;31(10):2384–2390 | Correct | No change (reports a prevalence of 1 in 4,982) |
| Arksey & O'Malley 2005; Tricco 2018 | Correct | No change |

New references added and checked: ACOG Committee Opinion No. 728 (2018), the source
for the "1 in 4,500–5,000" figure; Herlin et al. 2020 (*Orphanet J Rare Dis*);
Patterson et al. 2016 (*J Health Psychol*); Facchin et al. 2021 (*J Health Psychol*);
Tsarna et al. 2022 (*Children*); Heller-Boersma et al. 2007 (*Hum Reprod*, group CBT trial).

### 1b. The study-design percentages were impossible
Draft: Quantitative ~47%, Cross-sectional ~32%, Qualitative ~32%, Mixed ~21%. That adds
up to **132%**. Cross-sectional is a *type* of quantitative study, so it was counted twice.
With N = 34, the only split that matches your percentages is:

| Design | n | % |
|---|---|---|
| Quantitative (11 of them cross-sectional) | 16 | 47.1% |
| Qualitative | 11 | 32.4% |
| Mixed methods | 7 | 20.6% |
| **Total** | **34** | **100%** |

➡ **Confirm these counts against your extraction table.** Fig 2 and Table 1 use them.

### 1c. "Most studies (n=34) originate from Europe and North America"
This is wrong as written, because n = 34 is *all* studies. It now reads: **26 of 34 (76%)
came from Europe (18) or North America (8)**; only 3 (9%) came from Africa (2) or South
America (1). The regional counts add up to 34. ✔

### 1d. "Underrepresentation of LMIC settings" was listed as a *healthcare system* gap
This is a gap in the research literature, which your review found from the geographic
data. It was not a finding of the 18 studies that reported healthcare gaps. On the poster
it now appears with the map. In the manuscript it is labeled as a research gap in Table 4.

### 1e. Wording that implied prevalence
A scoping review counts how many **studies** reported an outcome. It does not measure
how many **people** have it. So "Depression, anxiety … are *prevalent*" was changed to
"are *frequently reported* and often co-occurring". The manuscript's limitations now
state this explicitly.

---

## 2. Checked and correct as submitted
- PRISMA arithmetic: 516 − 155 = 361 ✔; 361 − 327 = 34 ✔
- All outcome percentages (of 34): 26 = 76%, 22 = 65%, 21 = 62%, 19 = 56%, 18 = 53%, 17 = 50% ✔
- Regions add up to 34 ✔
- The submitted APHA abstract matches every number in the poster and manuscript ✔

---

## 3. Only you can confirm these (highlighted **yellow** in the manuscript)
1. **PRISMA full-text stage.** Your flow goes straight from 361 screened to 34 included.
   PRISMA-ScR (item 14) expects the number of full-text articles assessed and the
   reasons they were excluded. Add these if you have them. Reviewers often ask.
2. **Study-design split** (16 / 11 / 7; see 1b).
3. **Date the final search was run** and the **exact search strings** for each database
   (Appendix A). The per-database counts must add up to 516.
4. **Screening process**: how many reviewers screened, how disagreements were resolved,
   and which software you used.
5. **Other eligibility limits**, e.g., English only, or whether reviews and case reports
   were excluded.
6. **Protocol registration** (for example OSF), or a statement that there was none.
7. **Critical appraisal**: the manuscript says none was done, which is standard for
   scoping reviews. Change this if you did one.
8. **Appendix B**: one row per included study. Also add the 34 study citations to the
   reference list.
9. **Descriptions of the domains and coping mechanisms** in Tables 2–3. These are
   general definitions. Check that they match how you coded the studies.
10. **Corresponding-author email, conflicts of interest, CRediT author contributions,
    AI-use disclosure, and presentation status** (accepted or presented at APHA).

---

## 4. Poster notes
- Size: **48 × 36 in, landscape**. This is the most common APHA print size. If your
  session asks for a different size, tell me and I'll rebuild it.
- I could not see the three sample posters you mentioned. They are not in this
  repository and did not come through in the chat. The layout follows standard APHA
  poster conventions. If you upload the samples, I can match their style.
- No university or APHA logos were added. Insert official logo files from Liberty
  University and APHA if your program allows them.
