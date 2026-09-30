"""Methods (selection onward), Results, and Discussion text for the manuscript.
Imported by make_manuscript.py; `build(ctx)` writes the sections using its helpers."""


def build(ctx):
    para, heading, table, figure = ctx["para"], ctx["heading"], ctx["table"], ctx["figure"]
    P, N, OUT, DES, REG, FIG, pct = (ctx[k] for k in ("P", "N", "OUT", "DES", "REG", "FIG", "pct"))
    COPE = dict(ctx["data"]["coping"])
    assert COPE["Psychological counseling/intervention"] == 2
    ext = ctx["extraction"]
    FT = ctx["data"]["full_text_checked"]
    NFT = P["included"] - FT

    heading("Study Selection", 2)
    para(f"The original screening records could not be recovered, so study selection was repeated "
         f"from the original export files. Records from all sources were merged and "
         f"{P['duplicates_removed']} duplicates were identified by matching DOIs and normalized "
         f"titles, leaving {P['screened']} unique records. Titles and abstracts were screened in "
         f"two steps: objective criteria (publication year and article type) were applied first, "
         f"and each remaining record was then read against the eligibility criteria. An AI tool "
         f"(Claude, Anthropic) proposed a decision and reason for every record; "
         f"[[the first author and a second reviewer independently verified each decision, and "
         f"disagreements were resolved by discussion — complete once verification is done]]. "
         f"Records that could not be classified from the exported title and abstract were assessed "
         f"for eligibility using the published abstract; studies with mixed samples were included "
         f"only if results were reported separately for participants with MRKH or at least 80% of "
         f"participants had MRKH. Full texts were then obtained for {FT} of the {P['included']} included studies and checked against the same criteria; at this stage one study of adults with differences of sex development was excluded because only 2 of its 15 participants had MRKH and their findings were not analyzed separately. The full texts of the remaining {NFT} studies could not be obtained; their inclusion rests on the published abstract or title. The screening workbook, with a decision and reason for every record, "
         f"is available as supplementary material.")
    heading("Data Charting", 2)
    para("For each included study, data were charted on author, year, country, study design, "
         "sample size, reported mental health and psychosocial outcomes, coping mechanisms, and "
         "healthcare system gaps. Charted items were checked against the full text for "
         f"{FT} of {P['included']} studies; the remaining {NFT} were charted from the title and "
         "abstract. Outcomes were coded into "
         "four domains—depression and anxiety; quality of life, body image, and self-esteem; "
         "psychosexual and relational challenges; and broader psychological distress—and coping "
         "mechanisms into seven categories.")
    heading("Synthesis", 2)
    para("Findings were collated using a descriptive numerical summary—the number and proportion of "
         "included studies reporting each outcome domain—and a qualitative content analysis that "
         "grouped findings into outcome domains, coping mechanisms, and healthcare system gaps. "
         "Because a single study could report multiple domains, domain counts are not mutually "
         "exclusive. Consistent with scoping review methodology, a formal critical appraisal of "
         "study quality was not performed.^{@arksey,@tricco} Ethical approval was not required "
         "because this review analyzed published data.")

    # ------------------------------------------------------------------ RESULTS
    heading("Results")
    heading("Selection of Sources of Evidence", 2)
    reasons = "; ".join(f"{r.lower()} (n = {n})" for r, n in P["reasons"])
    para(f"The searches identified {P['identified']} records. After removal of "
         f"{P['duplicates_removed']} duplicates, {P['screened']} records were screened and "
         f"{P['excluded']} were excluded: {reasons}. Of the {P['fulltext']} records assessed for "
         f"eligibility, {P['excluded_eligibility']} were excluded ("
         + "; ".join(f"{r.lower()}, n = {n}" for r, n in P["eligibility_reasons"])
         + f"), and {P['included']} studies were included (Figure 1).")
    figure(FIG / "prisma_flow.png",
           "**Figure 1.** PRISMA-ScR flow diagram of study selection. Counts are pending "
           "confirmation by the review team.", width=5.4)

    heading("Characteristics of Included Studies", 2)
    para(f"The {N} included studies were published between 2019 and 2026 and comprised "
         f"{DES['Quantitative'][0]} quantitative studies ({pct(DES['Quantitative'][0])}), "
         f"{DES['Qualitative'][0]} qualitative studies ({pct(DES['Qualitative'][0])}), and "
         f"{DES['Mixed methods'][0]} mixed-methods studies ({pct(DES['Mixed methods'][0])}); the "
         f"design of 1 study could not be determined because only its title was available (Table 1; Figure 2). "
         f"Quantitative designs included cross-sectional surveys, case-control comparisons, "
         f"cohort and pre–post studies, and 1 randomized controlled trial.^{{@R131}} Most studies "
         f"came from Europe (n = {REG['Europe']}) and Asia (n = {REG['Asia']}), followed by North "
         f"America (n = {REG['North America']}), Africa (n = {REG['Africa']}), and Oceania (n = "
         f"{REG['Oceania']}); {REG['Multinational']} studies recruited internationally, and none "
         f"came from South America (Figure 3). China contributed the most studies (n = 6). Sample "
         f"sizes, where reported, ranged from 5 to 616 participants. Two Chinese "
         f"reports appear to draw on the same sample of 141 patients.^{{@R084,@R104}} "
         f"Characteristics of each study are listed in Appendix B.")
    table("**Table 1.** Study design and geographic distribution of included studies (N = {N_INCLUDED})",
          ["Characteristic", "n", "%"],
          [["**Study design**", "", ""]]
          + [[name, n, pct(n)] for name, (n, _) in DES.items()]
          + [["**Region**", "", ""]]
          + [[name, n, pct(n)] for name, n, _ in ctx["data"]["regions"]],
          widths=[3.6, 0.8, 1.0],
          note="Percentages are of all included studies (N = {N_INCLUDED}) and may not total 100% because "
               "of rounding. Five studies were charted from the abstract or title only.")
    figure(FIG / "fig2_design_donut.png",
           "**Figure 2.** Distribution of included studies by design (N = {N_INCLUDED}).", width=4.8)
    figure(FIG / "fig3_geographic_map.png",
           "**Figure 3.** Geographic distribution of included studies by region (N = {N_INCLUDED}). Darker "
           "shading indicates more studies; 2 multinational studies are not mapped.", width=6.3)

    heading("Mental Health and Psychosocial Outcomes", 2)
    s_, q_, g_, d_ = (OUT["Psychosexual & relational challenges"],
                      OUT["QoL, body image & self-esteem"],
                      OUT["Broader psychological distress"], OUT["Depression & anxiety"])
    para(f"Psychosexual and relational challenges were the most frequently reported domain "
         f"({s_} of {N} studies; {pct(s_)}), followed by quality of life, body image, and "
         f"self-esteem ({q_}; {pct(q_)}), broader psychological distress ({g_}; {pct(g_)}), and "
         f"depression and anxiety ({d_}; {pct(d_)}) (Table 2; Figure 4).")
    para("*Psychosexual and relational challenges.* Compared with controls, women with MRKH "
         "reported lower sexual esteem, a more negative genital self-image, and more sexual "
         "distress, even after neovagina creation.^{@R003,@R091} Qualitative studies described "
         "insecurity about the neovagina, low sexual confidence, and anxiety about disclosing "
         "the diagnosis to partners.^{@R040,@R063,@R094,@R017} One randomized trial found that "
         "e-learning psychosexual education improved genital self-image and reduced sexual "
         "distress.^{@R131} In an African qualitative study, cultural and religious expectations about "
         "virginity discouraged vaginal dilation.^{@R223}")
    para("*Quality of life, body image, and self-esteem.* A prospective study found impaired "
         "mental health–related quality of life despite normal body image,^{@R021} and an "
         "international survey of 263 patients reported higher distress and lower self-esteem "
         "than the general population.^{@R105} Low self-esteem was also reported in a further "
         "study.^{@R227} Others found similar quality of life across treatment "
         "approaches^{@R012} or improvements in well-being and body image after "
         "treatment.^{@R034,@R060}")
    para("*Broader psychological distress.* Qualitative studies described shock, anger, "
         "sadness, shame, and secrecy around the diagnosis, and portrayed diagnosis as a turning "
         "point that disrupted imagined futures and female identity.^{@R011,@R013,@R014} The "
         "diagnostic process itself was experienced as upsetting and potentially "
         "traumatizing.^{@R267} Uterus transplant recipients described changes in "
         "self-perception, body, and sexuality.^{@R234}")
    para("*Depression and anxiety.* Where measured with validated scales, findings were mixed. "
         "Depressive symptoms were reported in 75.2% of 141 Chinese patients (34.0% moderate to "
         "severe),^{@R104} moderate-to-severe anxiety in 24.1%,^{@R084} and depression and anxiety "
         "in 32.5% and 37.7% of 77 Malaysian women.^{@R004} After vaginoplasty, 45.3% of 53 "
         "women reported mild-to-moderate depression and 34.0% mild anxiety.^{@R002} A US cohort found anxiety and "
         "depressive disorders about twice as common as in male, but not female, "
         "referents.^{@R052} In contrast, some samples after neovagina creation or awaiting "
         "uterus transplantation showed few depressive symptoms.^{@R020,@R086} Among other uterus "
         "transplant candidates, however, MMPI-2 profiles showed elevated depression scales,^{@R244} "
         "and women with congenital uterine absence more often reported severe depression and "
         "anxiety symptoms than women with acquired uterine absence.^{@R001}")
    table("**Table 2.** Mental health and psychosocial outcome domains reported in included studies "
          "(N = {N_INCLUDED})",
          ["Outcome domain", "Description", "Studies, n (%)"],
          [["Psychosexual and relational challenges", "Sexual esteem, sexual distress and "
            "wellbeing, intimacy, partner relationships, disclosure", f"{s_} ({pct(s_)})"],
           ["Quality of life, body image and self-esteem", "Overall or mental health–related "
            "quality of life; body or genital image; global self-esteem", f"{q_} ({pct(q_)})"],
           ["Broader psychological distress", "Distress, shame, identity disruption, "
            "psychopathology", f"{g_} ({pct(g_)})"],
           ["Depression and anxiety", "Depressive and/or anxiety symptoms or diagnoses",
            f"{d_} ({pct(d_)})"]],
          widths=[1.9, 3.3, 1.2],
          note="Studies could report more than one domain; counts are not mutually exclusive.")
    figure(FIG / "fig1_outcomes_bar.png",
           "**Figure 4.** Number of included studies reporting each outcome domain, coping "
           "mechanisms, and healthcare system gaps (N = {N_INCLUDED}). Studies could contribute to more "
           "than one category.", width=6.3)

    heading("Coping Mechanisms", 2)
    c_ = OUT["Coping mechanisms documented"]
    para(f"Coping mechanisms were documented in {c_} studies ({pct(c_)}; Table 3). Peer, family, "
         f"and social support was most common,^{{@R014,@R021,@R032,@R094,@R105,@R149,@R267}} including "
         f"MRKH support groups and online communities. Avoidance and concealment—such as "
         f"pretending to menstruate or hiding the diagnosis—were the most frequently documented "
         f"maladaptive strategies.^{{@R013,@R032,@R057,@R094,@R149,@R223}} One qualitative study traced a "
         f"shift from avoidance to empowerment through positive reappraisal and spiritual "
         f"coping,^{{@R032}} and illness coherence and positive affect appeared protective for "
         f"psychological adjustment.^{{@R105}} Structured psychological or psychosexual "
         f"interventions were evaluated in only {COPE['Psychological counseling/intervention']} "
         f"studies.^{{@R038,@R131}}")
    table("**Table 3.** Coping mechanisms documented in included studies",
          ["Coping mechanism", "Type", "Studies, n"],
          [[name, "Maladaptive" if "Avoidance" in name else "Adaptive", n]
           for name, n in sorted(ctx["data"]["coping"], key=lambda x: -x[1])],
          widths=[3.4, 1.4, 1.2],
          note="A study could document more than one coping mechanism.")

    heading("Healthcare System Gaps", 2)
    h_ = OUT["Healthcare system gaps"]
    para(f"Healthcare system gaps were reported in {h_} studies ({pct(h_)}; Table 4). Participants "
         f"described providers with limited knowledge of MRKH and the need to advocate for "
         f"themselves,^{{@R013,@R073}} delayed diagnosis and insensitive communication at "
         f"diagnosis, including stigmatizing language,^{{@R149,@R267,@R094}} confusion after "
         f"medical encounters in several African countries,^{{@R223}} scarce information, "
         f"psychological support, and fertility counseling,^{{@R057,@R149,@R010}} and variable "
         f"counseling around vaginal lengthening treatment.^{{@R112}}")
    table("**Table 4.** Healthcare system gaps identified and corresponding public health implications",
          ["Gap identified", "Public health implication"],
          [["Providers' limited knowledge of MRKH; patients must self-advocate",
            "Train providers in psychosocially informed MRKH care"],
           ["Delayed diagnosis and insensitive communication at diagnosis",
            "Integrate psychosocial support and mental health screening into diagnostic pathways"],
           ["Scarce information, psychological support, and fertility counseling",
            "Develop multidisciplinary protocols including psychology and social work; build peer "
            "support infrastructure"],
           ["Variable counseling around vaginal lengthening treatment",
            "Standardize counseling and shared decision-making for treatment"],
           ["Few studies from Africa and none from South America (research gap)",
            "Expand research investment in underrepresented and low-resource settings"]],
          widths=[3.2, 3.2])

    # ------------------------------------------------------------------ DISCUSSION
    heading("Discussion")
    heading("Summary of Evidence", 2)
    para(f"This scoping review mapped {N} studies published between 2019 and 2026 on the mental "
         f"health and psychosocial outcomes of individuals with MRKH syndrome. Psychosexual and "
         f"relational challenges were the most frequently reported outcome, reported in about "
         f"two of every three studies, while broader psychological distress and quality of life, "
         f"body image, and self-esteem were each reported in about half. Depression and anxiety "
         f"were measured less often, and results were mixed. Coping was documented in more than "
         f"one in three studies and relied largely on peer support and self-management, and more than one in four "
         f"studies described healthcare system gaps.")
    para("These findings are consistent with earlier evidence that women with MRKH experience "
         "greater psychological distress and lower self-esteem than controls,^{@hb09} higher "
         "anxiety in adolescence,^{@laggari} and poorer mental health–related quality of life and "
         "sexual wellness.^{@liao} Prior systematic reviews likewise highlighted poor sexual esteem "
         "and genital image.^{@facchin,@tsarna} The present review indicates that psychosexual "
         "concerns remain central in the recent literature and extends earlier syntheses by "
         "mapping coping mechanisms and healthcare system gaps.")
    heading("Coping and Psychosocial Support", 2)
    para("Peer support, reappraisal, and spiritual coping suggest considerable resilience after "
         "diagnosis, consistent with earlier qualitative accounts of women managing threats to "
         "identity and intimacy.^{@patterson} At the same time, avoidance and concealment were "
         "common and may delay help-seeking. Evidence that structured intervention helps is "
         "available—a randomized trial of group cognitive-behavioural therapy improved "
         "psychological outcomes,^{@hb07} and recent studies of psychological support and "
         "psychosexual education reported benefits^{@R038,@R131}—yet only a few studies evaluated "
         "such support, suggesting it has not been translated into routine care.")
    heading("Healthcare System Gaps and Equity", 2)
    para("Although professional guidance identifies psychosocial counseling as central to MRKH "
         "management,^{@acog} participants described providers unfamiliar with the condition, "
         "insensitive communication, and scarce psychological and fertility counseling, indicating "
         "a gap between recommendations and practice. The evidence base is more geographically "
         "diverse than earlier literature—Asia contributed nearly as many studies as Europe—yet "
         "only 1 study came from Africa and none from South America, where expectations regarding "
         "fertility, marriage, and womanhood and access to specialized care may differ "
         "substantially. Studies from Türkiye, Vietnam, and Japan illustrate how cultural context "
         "shapes experiences of diagnosis, disclosure, and infertility.^{@R011,@R057,@okunomiya}")
    heading("Implications for Practice, Policy, and Research", 2)
    para("Five priorities emerge. First, psychosocial support and mental health screening should "
         "be integrated into MRKH diagnostic pathways. Second, multidisciplinary care protocols "
         "should include psychology and social work alongside gynecology. Third, psychosexual "
         "counseling should accompany vaginal lengthening treatment, given the prominence of "
         "sexual esteem and genital image concerns. Fourth, providers should be trained in "
         "sensitive, non-stigmatizing communication. Fifth, research investment should be "
         "expanded in underrepresented and low-resource settings. Future studies should use "
         "validated measures, longitudinal designs, and trials of psychosocial interventions "
         "delivered within routine care.")
    heading("Strengths and Limitations", 2)
    para("Strengths include an established methodological framework, PRISMA-ScR reporting, a "
         "search of biomedical, nursing, psychological, and women's studies databases, and "
         "inclusion of quantitative, qualitative, and mixed-methods evidence. The most important "
         "limitation is that the original screening records were lost and selection was repeated "
         "from the original exports with AI-assisted screening and charting. Charting was checked "
         f"against the full text for {FT} of the {P['included']} included studies, but the "
         f"remaining {NFT} rest on abstracts or titles. Two Danish reports and two Chinese reports appear to share samples. In addition, the review was "
         "limited to 2019–2026, date limits were applied inconsistently across database "
         "interfaces and enforced at screening, designs and measures were heterogeneous, and "
         "other studies may also share samples. Consistent with scoping methodology, study quality was "
         "not appraised, and counts reflect how often outcomes were studied, not their "
         "prevalence. Grey literature was not searched, and many included studies had small, single-center samples, which limits generalizability.")
    heading("Conclusions", 2)
    para("MRKH-related psychosocial burden is substantial yet under-integrated into care models. "
         "Psychosexual and relational challenges, reduced quality of life and self-esteem, and "
         "psychological distress are frequently reported, while coping relies largely on peer "
         "support and self-management rather than systematic clinical pathways. Multidisciplinary, "
         "mental health–inclusive care and greater research investment are urgently needed, "
         "particularly in underrepresented and low-resource settings.")
