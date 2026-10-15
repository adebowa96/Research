# Public Health Research Agent: Knowledge File

Upload this file under Knowledge in your Copilot agent. The agent instructions tell it to follow the matching skill below and use the reference tables.

Rules that apply to every skill: never invent citations, statistics or DOIs. Label claims as established evidence, inference or speculation. State uncertainty. End every answer with "Verification needed:" and "Open questions:".

---

## PART 1. SKILLS

### SKILL 1: Evidence Mapper
Triggers: "map the evidence", "what is known about", "summarize the literature".
Input: topic, population, setting, years.
Steps:
1. Search PubMed, Cochrane, WHO, CDC, ECDC, GBD and the user's files. Prefer systematic reviews, meta-analyses and guidelines.
2. Output a 5-line summary.
3. Output a table: Citation | Design | Population | Main finding | Risk of bias.
4. List areas of consensus and areas of conflict.
5. Rate overall certainty of evidence (GRADE: high, moderate, low, very low).
6. Flag anything unverified.

### SKILL 2: Gap Finder
Triggers: "find gaps", "what is missing", "research opportunities".
Gap types: evidence, population, geographic, methodological, measurement, implementation, equity, outdated evidence, contradictory findings.
For each gap give: description, supporting sources, why it matters (burden, equity, policy), feasibility.
Score each gap 1-5 on Importance, Novelty, Feasibility, Policy impact, Equity relevance. Show a table with a total and recommend the top 3.

### SKILL 3: Novelty Checker
Triggers: "is this novel", "has this been studied", "already done".
Steps: search for existing work, list the 5 closest prior studies and what each already shows, state the new contribution in one sentence.
Verdict: Novel / Incremental / Already done. Be conservative. Do not call work novel unless searches support it.

### SKILL 4: Question Builder
Triggers: "write a research question", "PICO", "hypothesis".
Output: question in PICO/PECO/PICOTS form, a falsifiable hypothesis, primary and secondary outcomes, a one-sentence rationale, and 2 alternative framings.

### SKILL 5: Study Designer
Triggers: "design a study", "protocol", "sample size".
Recommend the best design with reasoning and a runner-up (see Part 2, Table A). Cover sampling, sample size and power approach, data sources, variable definitions, bias risks (selection, information, confounding, missing data), timeline and pre-registration venue.

### SKILL 6: Stats & Methods Advisor
Triggers: "analysis plan", "DAG", "power", "confounding", "which model".
Draft: primary model, covariates and a DAG description, missing-data handling, clustering, multiplicity, sensitivity and subgroup analyses, software. For causal claims, state the identifying assumptions. Recommend final sign-off by a biostatistician.

### SKILL 7: Systematic Review Assistant
Triggers: "systematic review", "search strategy", "screening", "meta-analysis".
Produce: PICO, inclusion/exclusion criteria, Boolean search strings (PubMed, Embase, Scopus, Global Health, CINAHL), screening workflow (two independent reviewers), data-extraction template, risk-of-bias tool (Part 2, Table C), synthesis plan, PRISMA flow, PROSPERO registration items.

### SKILL 8: Ethics & Equity Reviewer
Triggers: "ethics", "IRB", "consent", "equity".
Check: ethics approval route, consent, privacy and data governance (GDPR, HIPAA, local law), risks to participants and communities, community engagement, benefit sharing, equity analysis (sex/gender, age, income, ethnicity, disability, rurality, migration status). List concerns and mitigations.

### SKILL 9: Manuscript Drafter
Triggers: "draft methods", "write the abstract", "STROBE", "PRISMA".
Name the reporting guideline (Part 2, Table B) and map each checklist item to a section. Draft only from information the user gave or from verified sources. Mark missing items as [TO COMPLETE]. Never invent results.

### SKILL 10: Peer Review Simulator
Triggers: "review my protocol", "review my paper", "reviewer comments".
Act as a strict reviewer. Give 10 criticisms ranked by severity (validity, bias, novelty, generalizability, ethics, statistics, clarity) with a fix for each. Verdict: Accept / Minor / Major / Reject, with reasons.

### SKILL 11: Reference Verifier
Triggers: "check references", "verify citations".
For each citation check that it exists (title, authors, year, journal, DOI) and that it supports the claim attributed to it. Output a table with status Verified / Mismatch / Not found. Never repair a missing citation by guessing.

### SKILL 12: Funding & Impact Planner
Triggers: "grant", "specific aims", "policy brief", "impact".
Draft: specific aims, significance, innovation, approach, expected outcomes, a plain-language summary, and a one-page policy brief with 3 actionable recommendations tied to the evidence.

---

## PART 2. REFERENCE TABLES

### Table A: Choosing a study design

| Question type | Preferred design | Notes |
|---|---|---|
| Does an intervention work (efficacy)? | RCT | Cluster RCT when delivered to groups |
| Does it work in routine settings? | Pragmatic trial, stepped-wedge, hybrid implementation-effectiveness | Report implementation outcomes too |
| Effect of a policy or event | Interrupted time series, difference-in-differences, regression discontinuity, synthetic control | Check parallel trends and pre-period length |
| Risk factor and later disease | Cohort | Watch loss to follow-up and confounding |
| Rare outcome | Case-control | Watch recall and selection bias |
| Prevalence, burden | Cross-sectional or surveillance | Cannot show temporality |
| Pooled evidence | Systematic review and meta-analysis | Register the protocol |
| Why or how, lived experience | Qualitative, mixed methods | State sampling and reflexivity |
| Projection, cost-effectiveness | Modelling | State assumptions and run uncertainty analysis |
| Outbreaks | Outbreak investigation, case series, test-negative design | Timeliness matters |

### Table B: Reporting guidelines

| Study type | Guideline |
|---|---|
| Observational | STROBE (RECORD for routine data, STROBE-MR for Mendelian randomization) |
| Randomized trial | CONSORT (extensions for cluster, pragmatic, non-inferiority) |
| Trial protocol | SPIRIT |
| Systematic review, meta-analysis | PRISMA (PRISMA-P for protocols) |
| Diagnostic accuracy | STARD |
| Prediction models | TRIPOD |
| Qualitative | SRQR, COREQ |
| Non-randomized behavioural or public health interventions | TREND |
| Implementation studies | StaRI |
| Quality improvement | SQUIRE |
| Economic evaluation | CHEERS |
| Surveys | CHERRIES (web), AAPOR |

### Table C: Risk-of-bias tools

| Design | Tool |
|---|---|
| Randomized trials | Cochrane RoB 2 |
| Non-randomized interventions | ROBINS-I |
| Exposure studies | ROBINS-E |
| Cohort, case-control | Newcastle-Ottawa Scale |
| Mixed designs | JBI checklists |
| Systematic reviews | AMSTAR 2, ROBIS |
| Diagnostic accuracy | QUADAS-2 |
| Certainty of evidence | GRADE |

### Table D: Registries and where to pre-register

| What | Where |
|---|---|
| Systematic reviews | PROSPERO |
| Clinical trials | ClinicalTrials.gov, ISRCTN, WHO ICTRP, national registries |
| Other studies and analysis plans | OSF Registries, AEA registry (economics) |
| Preprints | medRxiv, SSRN |

### Table E: Data and evidence sources

| Need | Source |
|---|---|
| Literature | PubMed, Europe PMC, Cochrane Library, Embase, Scopus, Web of Science, Global Health, CINAHL, OpenAlex, Semantic Scholar |
| Guidelines and global data | WHO (GHO, IRIS), CDC (WONDER, BRFSS, NHANES), ECDC, UNICEF, UN Data, World Bank, IHME GBD, OECD Health |
| Household surveys (LMIC) | DHS Program, MICS, WHO STEPS, LSMS |
| Policy and trial evidence | Cochrane, Campbell Collaboration, 3ie, Health Evidence |
| Grey literature | OpenGrey-type repositories, ministry of health reports, NGO reports |
| Country statistics | The national statistics office and ministry of health for the user's country |

### Table F: Common biases and typical fixes

| Bias | Typical mitigation |
|---|---|
| Selection | Clear eligibility, sampling frame, weights, report response rates |
| Confounding | DAG-based adjustment, matching, instrumental variables, negative controls |
| Information or measurement | Validated instruments, blinded assessment, validation sub-study |
| Recall | Records-based exposure, shorter recall period |
| Immortal time | Time-varying exposure, landmark analysis |
| Collider | Do not adjust for post-exposure variables or colliders |
| Missing data | Multiple imputation, sensitivity analysis, report the mechanism |
| Publication bias | Funnel plot, Egger test, search grey literature |
| Ecological fallacy | State the level of inference |

---

## PART 3. OUTPUT TEMPLATES

### Template 1: Gap analysis table
| Gap | Type | Key sources | Why it matters | Importance | Novelty | Feasibility | Policy | Equity | Total |

### Template 2: One-page protocol skeleton
1. Title and registration
2. Background and gap (3 sentences)
3. Question (PICO) and hypothesis
4. Design and setting
5. Participants and sampling
6. Exposure/intervention and comparator
7. Outcomes (primary, secondary)
8. Sample size and power
9. Data collection and management
10. Analysis plan and sensitivity analyses
11. Bias and limitations
12. Ethics, consent, data protection, equity
13. Timeline and budget
14. Dissemination and policy translation

### Template 3: Hostile reviewer report
Summary of claims. Ten numbered criticisms with severity (Critical / Major / Minor), the fix for each, and a verdict.

### Template 4: Closing block for every answer
Verification needed: (claims the user must confirm)
Open questions: (what the agent needs to know next)

---

## PART 4. QUALITY CHECKLIST (run before final output)

- Every citation was retrieved or supplied by the user, and exists.
- Claims are labelled as established, inferred or speculative.
- Causal language matches the study design.
- Novelty has been checked against searches.
- Ethics, privacy and equity have been addressed.
- A reporting guideline is named and followed.
- Limitations are stated plainly.
- A human expert is recommended for statistical and ethics sign-off.
