# MRKH Scoping Review: Manuscript, Poster, and Figures

*Mental Health and Psychosocial Outcomes Among Individuals With Mayer-Rokitansky-Küster-Hauser
(MRKH) Syndrome: A Scoping Review.* Shobayo IP, Okojie P, Anderson R. Liberty University. APHA 2026.

| File | What it is |
|---|---|
| `manuscript/MRKH_Scoping_Review_Manuscript.docx` | Full journal-style manuscript: title page, abstract, IMRaD, 4 tables, 4 figures, verified references, and Appendices A–C (search strategy, included-studies table, PRISMA-ScR checklist). Yellow highlights mark items you must complete. |
| `poster/MRKH_APHA2026_Poster.pptx` | Editable 48 × 36 in poster (PowerPoint) |
| `manuscript/MRKH_Scoping_Review_Manuscript.pdf` | PDF preview of the manuscript |
| `poster/MRKH_APHA2026_Poster.pdf` | Print-ready PDF of the poster |
| `figures/` | PRISMA flow, Fig 1 bar chart, Fig 2 donut, Fig 3 world map (PNG at 300 dpi, plus SVG) |
| `REVIEW_NOTES.md` | **Read first.** Every correction made to the draft, and what you still need to confirm |
| `scripts/data.json` | The single source for every number in all outputs |

## Rebuilding after changing a number
```bash
pip install matplotlib python-docx python-pptx pillow
cd scripts && npm install && node make_map.js && cd ..
python3 scripts/make_figures.py
python3 scripts/make_poster.py
python3 scripts/make_manuscript.py
soffice --headless --convert-to pdf --outdir poster poster/MRKH_APHA2026_Poster.pptx
```
