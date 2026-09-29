# Re-screening (September 2026)

The original Rayyan screening records could not be recovered, so screening is being redone
from the original search exports (`exports/`, dated March 29, 2026).

1. `build_records.py` merges the 516 exported records and removes duplicates (DOI or title),
   leaving 324 unique records.
2. `screen.py` proposes title/abstract decisions (objective rules, then a documented reading
   of each remaining record) and writes `MRKH_rescreening_workbook.xlsx`.

The proposed decisions are AI-assisted and **not final**. Two human screeners must record
independent decisions in the workbook, resolve disagreements, and complete full-text
screening before any counts go into the manuscript or poster.
