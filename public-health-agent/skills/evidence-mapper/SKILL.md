---
name: "evidence-mapper"
description: "Maps what is known on a public health topic: key studies, consensus, conflicts and certainty of evidence. Use when asked to map evidence, summarize literature, or say what is known about a topic."
---

# Evidence Mapper
Input: topic, population, setting, years (ask if missing).
1. Search PubMed, Cochrane, WHO, CDC, ECDC, GBD and user files. Prefer systematic reviews, meta-analyses and guidelines.
2. Give a 5-line summary.
3. Table: Citation | Design | Population | Main finding | Risk of bias.
4. List areas of consensus and areas of conflict.
5. Rate overall certainty (GRADE: high, moderate, low, very low).
6. Flag anything unverified.

## Rules (always apply)
- Never invent citations, statistics, DOIs or quotes. Cite only sources retrieved or supplied by the user; otherwise write "unverified".
- Label claims as established evidence, inference, or speculation. State uncertainty.
- Do not give individual clinical advice. Do not process identifiable health data.
- End every answer with "Verification needed:" and "Open questions:".
