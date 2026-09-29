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

## 3. Status of the open items

**Done**
- Protocol: "A review protocol was not registered." (you confirmed)
- Critical appraisal: none, which is standard for scoping reviews (you confirmed)
- APHA status: "accepted for poster presentation" (you confirmed)
- AI-use disclosure: statement drafted. Check it against your target journal's policy.
- AMA in-text citations: superscript numerals, numbered in order of first citation, placed
  after periods and commas and before colons and semicolons. Two misplaced citations fixed.
- References: DOIs added, full author lists where AMA requires them (up to 6 authors,
  otherwise 3 + et al.), and 3 recent sources added (2025–2026). The full list is in
  `manuscript/References_AMA.docx`.
- Appendix A: suggested PubMed search string included for comparison.

**Fixed from your search export files (September 29)**
- Databases now listed as actually searched: PubMed; Scopus; EBSCOhost (MEDLINE Ultimate,
  CINAHL Ultimate, APA PsycInfo, Women's Studies International). Updated in the Methods,
  the manuscript abstract, the PRISMA figure and the poster Methods table. The APHA abstract
  on the poster is left exactly as submitted.
- Search date: March 29, 2026 (the export date).
- Appendix A table filled in: 207 + 20 + 146 + 143 = 516.
- Date limits described honestly: they were applied unevenly when searching, so the 100
  pre-2019 records were removed at screening and count among the 327 exclusions.
- Mak & Thomas (2022) added as a methods citation (reference 15).

**Cannot be recovered from the export files (still highlighted)**
1. Screening process (reviewers and software). **Ask Dr. Okojie and Dr. Anderson, and check
   whether you have a Rayyan, Covidence or Zotero account or library holding this project.**
   That tool also holds your screening decisions and duplicate count.
2. Full-text screening numbers and exclusion reasons.
3. The 34 included studies (Appendix B and their citations) and the 16/11/7 design split.
   These came from your data-extraction spreadsheet. Search your email, OneDrive/Google
   Drive and Canvas for a file with "MRKH" or "extraction" in the name.
4. Whether the PubMed search was also run on March 29, 2026.
5. Duplicate count: your 155 versus about 192 from automated matching (see SEARCH_AUDIT.md).
6. Corresponding-author email, conflicts of interest, and CRediT author contributions.
7. Whether Güner 2025, Rajesh 2026 and Okunomiya 2026 are among your 34 studies.

## 4. Poster notes
- Built on the Liberty University sample poster you provided
  (`poster/template/liberty_template.pptx`: navy background and Liberty logo only).
  It uses the same 48 × 36 in size, three-column layout, navy Times New Roman section
  headers and white centre figure panel.
- Poster figure numbers (Fig 1 PRISMA, Fig 2 outcomes, Fig 3 map, Fig 4 design) differ
  from the manuscript's (Figure 1 PRISMA, 2 design, 3 map, 4 outcomes), because each
  document numbers figures in the order they are first cited. This is expected.
- The sample posters had a QR code in the References box. This poster lists the
  references as text instead. Add a QR code if you have a link to point it to.
