import pandas as pd, json, re, sys
sys.path.insert(0,'.')
from refs import *
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
S=json.load(open('stats.json')); G=json.load(open('prisma_groups.json')); P=S['prisma']
m=pd.read_pickle('master.pkl').set_index('record_id'); T=pd.read_pickle('table.pkl').set_index('record_id')
N=85
def pct(n): return f"{100*n/N:.1f}%"
# ---------- in-text citation helper ----------
SUFFIX={1323:'a',1061:'b'}
def c(*ids):
    out=[]
    for i in ids:
        r=m.loc[i]; out.append(intext(i,r.authors,r.year,SUFFIX.get(i,'')))
    return '('+'; '.join(out)+')'
def cn(i):  # narrative citation "Author et al. (2019)"
    r=m.loc[i]; t=intext(i,r.authors,r.year,SUFFIX.get(i,'')); a,y=t.rsplit(', ',1); return f"{a} ({y})"
# ---------- document ----------
doc=Document()
st=doc.styles['Normal']; st.font.name='Times New Roman'; st.font.size=Pt(12)
st.element.rPr.rFonts.set(qn('w:eastAsia'),'Times New Roman')
pf=st.paragraph_format; pf.line_spacing_rule=WD_LINE_SPACING.DOUBLE; pf.space_after=Pt(0)
for s in doc.sections: s.left_margin=s.right_margin=s.top_margin=s.bottom_margin=Inches(1)
# page numbers
def add_page_number(section):
    p=section.footer.paragraphs[0]; p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    r=p.add_run(); f1=OxmlElement('w:fldChar'); f1.set(qn('w:fldCharType'),'begin'); it=OxmlElement('w:instrText'); it.set(qn('xml:space'),'preserve'); it.text='PAGE'; f2=OxmlElement('w:fldChar'); f2.set(qn('w:fldCharType'),'end')
    r._r.append(f1); r._r.append(it); r._r.append(f2)
add_page_number(doc.sections[0])
def para(text='',bold=False,italic=False,align=None,indent=True,size=None,color=None,spacing=None,keep=False):
    p=doc.add_paragraph()
    if indent: p.paragraph_format.first_line_indent=Inches(0.5)
    if align=='center': p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    if spacing: p.paragraph_format.line_spacing_rule=spacing
    add_runs(p,text,bold,italic,size,color)
    if keep: p.paragraph_format.keep_with_next=True
    return p
def add_runs(p,text,bold=False,italic=False,size=None,color=None):
    # supports *italic* and **bold** markup
    for tok in re.split(r'(\*\*.+?\*\*|\*.+?\*)',text):
        if not tok: continue
        b=bold; it=italic
        if tok.startswith('**'): tok=tok[2:-2]; b=True
        elif tok.startswith('*'): tok=tok[1:-1]; it=True
        r=p.add_run(tok); r.bold=b; r.italic=it
        if size: r.font.size=Pt(size)
        if color: r.font.color.rgb=RGBColor.from_string(color)
def H(text,level=1):
    p=doc.add_paragraph(); p.paragraph_format.keep_with_next=True
    if level==1: p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    r=p.add_run(text); r.bold=True
    if level==3: r.italic=True
    return p
def note(text):
    p=para(text,indent=False,size=11,color='B45309'); return p
# ---------- TITLE PAGE ----------
para('Psychosocial Outcomes and Coping Mechanisms Among Women with Premenstrual Dysphoric Disorder: A Global Scoping Review',bold=True,align='center',indent=False)
para('')
para('Ifeoluwanimi P. Shobayo, MSPH, Chelsea R. Mazonde, MPH, Marylyn O. Oduneye, MSPH, Tahirou Diallo, MSPH, Fadzai G. Nyarugwe, MSPH, and Cynthia C. Ilechukwu, MSPH',align='center',indent=False)
para('Liberty University',align='center',indent=False)
note('[AUTHOR NOTE – before submission: add department, city and country, corresponding-author contact, ORCID iDs and word count.]')
para('')
para('Running head: PMDD PSYCHOSOCIAL OUTCOMES: A SCOPING REVIEW',indent=False)
para('Keywords: premenstrual dysphoric disorder; psychosocial outcomes; coping; suicidality; quality of life; low- and middle-income countries; sub-Saharan Africa; scoping review',indent=False)
doc.add_page_break()
# ---------- ABSTRACT ----------
H('Abstract')
LMIC=S['income'].get('Upper-middle income',0)+S['income'].get('Lower-middle income',0)+S['income'].get('Low income',0)
LLI=S['income'].get('Lower-middle income',0)+S['income'].get('Low income',0)
D=S['domains']
abs_txt=[
('Background: ',f"Premenstrual dysphoric disorder (PMDD) is a DSM-5 depressive disorder with an estimated confirmed community prevalence of 1.6%, equivalent to roughly 31 million women and girls worldwide. PMDD is associated with depression, suicidality and impaired functioning, yet the global distribution of evidence on its psychosocial burden, and on how affected women cope, has not been mapped."),
('Methods: ',f"Following Arksey and O'Malley's framework and PRISMA-ScR, records exported from CINAHL Ultimate, APA PsycInfo, APA PsycArticles, MEDLINE Ultimate, Women's Studies International, PubMed and the Cochrane Library were screened against pre-specified criteria: peer-reviewed empirical studies (2010–2025, English) with PMDD as a defined population and at least one psychosocial outcome or coping mechanism as a primary aim. Animal, laboratory, intervention, review and instrument-validation studies were excluded. Data were charted for design, setting, World Bank income group, PMDD ascertainment and psychosocial domain."),
('Results: ',f"Of {P['identified_total']:,} records, {P['duplicates_removed']} were duplicates; {P['screened']:,} were screened and {N} studies met inclusion criteria. Depression was the most frequently examined domain (n = {D['Depression / depressive symptoms']}), followed by mood and emotion regulation (n = {D['Mood & emotion regulation']}), psychiatric comorbidity (n = {D['Psychiatric comorbidity']}), psychological distress (n = {D['Psychological distress & perceived stress']}), suicidality and self-harm (n = {D['Suicidal ideation, attempts & self-harm']}), academic/occupational functioning (n = {D['Academic & occupational functioning']}), interpersonal functioning (n = {D['Interpersonal & relational functioning']}), quality of life (n = {D['Quality of life']}) and coping or resilience (n = {D['Coping strategies & resilience']}). Only {S['ascertainment']['Prospective symptom ratings (confirmed)']} studies ({pct(S['ascertainment']['Prospective symptom ratings (confirmed)'])}) confirmed PMDD with prospective daily ratings. Two-thirds of studies ({S['income']['High income']}; {pct(S['income']['High income'])}) came from high-income countries; {LMIC} ({pct(LMIC)}) came from low- and middle-income countries (LMICs), but only {LLI} ({pct(LLI)}) from low- or lower-middle-income countries and {S['region']['Sub-Saharan Africa']} ({pct(S['region']['Sub-Saharan Africa'])}) from sub-Saharan Africa (Ethiopia, n = 2; Nigeria, n = 1)."),
('Conclusions: ',"Evidence on the psychosocial burden of PMDD is growing but remains concentrated in high-income settings, relies heavily on provisional diagnoses, and rarely examines coping or lived experience. Culturally responsive screening, integration of PMDD into sexual, reproductive and mental health services, and Africa-centred research investment are needed.")]
for lab,t in abs_txt:
    p=para('',indent=False); r=p.add_run(lab); r.bold=True; add_runs(p,t)
note('[Word count of abstract ≈ 330 words; trim to the target journal limit. Note that the counts above supersede those in the APHA abstract submitted before full screening—see the cover note.]')
doc.add_page_break()
# ---------- INTRODUCTION ----------
H('Introduction')
para("Premenstrual dysphoric disorder (PMDD) is a cyclical, hormone-linked mood disorder in which marked affective symptoms—irritability, affective lability, depressed mood and anxiety—together with behavioural and physical symptoms emerge in the late luteal phase of the menstrual cycle and remit shortly after the onset of menses (American Psychiatric Association [APA], 2013). PMDD was placed in the depressive disorders chapter of the *Diagnostic and Statistical Manual of Mental Disorders* (5th ed.; DSM-5) in 2013 and is also recognised in the *International Classification of Diseases, 11th Revision* (ICD-11), which came into effect in 2022 (APA, 2013; World Health Organization [WHO], 2022). Its diagnostic validity nevertheless continues to be debated (Naik et al., 2023).")
para("Estimates of how common PMDD is depend heavily on how it is diagnosed. A meta-analysis of 44 studies (50,659 participants) estimated a pooled point prevalence of 3.2% for confirmed diagnoses—which require prospective daily symptom ratings over at least two cycles—and 7.7% for provisional diagnoses based on retrospective report; restricted to community samples with confirmed diagnosis, prevalence was 1.6% (Reilly et al., 2024), equivalent to roughly 31 million women and girls worldwide (University of Oxford, 2024). Premenstrual symptoms more broadly are highly prevalent in Africa: a meta-analysis of 16 African studies reported a pooled premenstrual syndrome (PMS) prevalence of 47.0% (Andualem et al., 2024).")
para("Because PMDD recurs every month across the reproductive years, its consequences extend well beyond symptom counts. Studies have linked PMDD with depression, suicidal ideation and behaviour, strained relationships, lost productivity and reduced quality of life, and have begun to examine how affected women cope. However, this evidence is dispersed across psychiatry, gynaecology, nursing and psychology journals, and it is unclear which psychosocial outcomes have been studied, with what methods, and in which parts of the world. This matters for public health: in many low- and middle-income countries (LMICs), and particularly in sub-Saharan Africa, menstrual health remains under-prioritised and mental health services are scarce, so a condition whose burden is undocumented is unlikely to be recognised by health systems [add supporting citation, e.g., WHO Mental Health Atlas].")
para("We therefore conducted a scoping review to map the global evidence on psychosocial outcomes and coping mechanisms among women with PMDD. The review addressed four questions: (1) Which psychosocial outcomes and coping mechanisms have been examined among women with PMDD? (2) How are these studies distributed across countries, regions and income settings? (3) What study designs and diagnostic approaches characterise this evidence? (4) What gaps exist, particularly for LMICs and sub-Saharan Africa?")
# ---------- METHODS ----------
H('Methods')
H('Design',2)
para("This scoping review followed the five-stage framework of Arksey and O'Malley (2005), with the methodological refinements proposed by Levac et al. (2010), and is reported according to the Preferred Reporting Items for Systematic Reviews and Meta-Analyses extension for Scoping Reviews (PRISMA-ScR; Tricco et al., 2018). Consistent with scoping-review methodology, the aim was to map the extent and nature of the evidence rather than to appraise study quality or pool effect estimates.")
note('[State whether a protocol was registered (e.g., Open Science Framework) and give the registration DOI/date, or state that no protocol was registered.]')
H('Information Sources and Search',2)
para(f"Records were retrieved from CINAHL Ultimate, APA PsycInfo, APA PsycArticles, MEDLINE Ultimate and Women's Studies International (via EBSCOhost), PubMed and the Cochrane Library. Search strategies combined terms for premenstrual dysphoric disorder (e.g., “premenstrual dysphoric disorder”, “PMDD”, “premenstrual disorder*”) with psychosocial and coping concepts. The exported records ({P['identified_total']:,} in total) formed the screening set; the publication-date limit (January 2010 to December 2025) was applied at screening because some exports contained records outside this range.")
note('[Insert the exact search string, limits and search date for each database in Appendix A. The PubMed export provided contributed 6 records; if the full PubMed search yielded more, add those records and re-run deduplication so that the PRISMA counts match.]')
H('Eligibility Criteria',2)
para("Eligibility was defined using the Population–Concept–Context framework. *Population:* women and people who menstruate with PMDD defined by DSM-IV, DSM-5 or ICD criteria, whether provisional (retrospective screening instruments such as the Premenstrual Symptoms Screening Tool) or confirmed (prospective daily ratings), including studies of premenstrual disorders that reported a distinct PMDD group or diagnosis. *Concept:* at least one psychosocial outcome or correlate (e.g., depression, anxiety, mood and emotion regulation, psychological distress, interpersonal functioning, suicidality or self-harm, quality of life, academic or occupational functioning) or a coping mechanism as a primary aim. *Context:* any country or setting. Eligible sources were peer-reviewed primary empirical studies (quantitative, qualitative or mixed methods) published in English between 2010 and 2025. We excluded animal studies; laboratory and biological studies (neuroimaging, hormonal, genetic or physiological aims); intervention and treatment studies; reviews, meta-analyses, guidelines and commentaries; instrument development or validation studies; case reports; books, chapters, dissertations, letters, editorials and conference abstracts; and studies of PMS without a PMDD group.")
H('Selection of Sources of Evidence',2)
para("All exports were merged into a single library. Duplicates were identified by digital object identifier and by normalised title (Unicode-aware, so that non-Latin titles were matched), and near-identical titles were reviewed manually. Records were then screened in two steps: (a) application of the date, language and publication-type criteria using database metadata, and (b) title, abstract and subject-term screening of every remaining record against the population, concept and study-design criteria. Every decision and exclusion reason was recorded in a screening log (Supplementary File).")
note('[Describe the reviewers: title/abstract screening and data charting were performed with AI assistance (Claude, Anthropic) and must be verified by two independent human reviewers, with disagreements resolved by discussion or a third reviewer. Full-text retrieval and eligibility confirmation are in progress; update the PRISMA-ScR diagram with full-text counts once complete. Declare AI assistance according to the target journal\'s policy.]')
H('Data Charting',2)
para("For each included study we charted the author, year, country, study design, sample size, population, method of PMDD ascertainment and the psychosocial domains examined. Country was taken from the abstract or, where not stated, from the study setting described by the authors. Countries were grouped by World Bank region and income group using the fiscal-year 2027 classification (World Bank, 2026); consistent with World Bank usage, LMICs comprise low-, lower-middle- and upper-middle-income economies. Psychosocial outcomes were coded into 13 domains developed iteratively during charting; a study could contribute to more than one domain.")
H('Synthesis',2)
para("Results were summarised numerically (frequencies and percentages) and narratively by psychosocial domain, with particular attention to the geographic distribution of evidence and to LMIC and sub-Saharan African settings.")
# ---------- RESULTS ----------
H('Results')
H('Selection of Sources of Evidence',2)
ex=sorted(G.items(),key=lambda x:-x[1])
extxt='; '.join(f"{k.lower() if not k.startswith('PMDD') else k} (n = {v})" for k,v in ex)
para(f"The database exports contained {P['identified_total']:,} records. After {P['duplicates_removed']} duplicates were removed, {P['screened']:,} records were screened and {P['excluded_total']:,} were excluded: {extxt}. In total, {N} studies met the inclusion criteria (Figure 1).")
doc.add_picture('fig1_prisma.png',width=Inches(5.8)); doc.paragraphs[-1].alignment=WD_ALIGN_PARAGRAPH.CENTER
H('Characteristics of Included Studies',2)
per=S['period']; des=S['design']; asc=S['ascertainment']
para(f"The {N} included studies were published between 2010 and 2025, with almost half ({per['2020–2025']}; {pct(per['2020–2025'])}) published since 2020 and {S['by_year']['2025']} ({pct(S['by_year']['2025'])}) in 2025 alone (Table 1). Most were cross-sectional ({des['Cross-sectional']}; {pct(des['Cross-sectional'])}) or case-control ({des['Case-control']}; {pct(des['Case-control'])}) designs; {des['Prospective daily ratings / EMA']} used prospective daily ratings or ecological momentary assessment, {des['Cohort / registry']} were cohort or registry studies, {des['Prospective observational']} were other prospective observational studies, {des['Retrospective record review']} were retrospective record reviews and only {des['Qualitative']} were qualitative. Sample sizes ranged from 10 to 1,472,379 participants (median 266). Samples most often comprised community women (n = 17), university or college students (n = 14) and school-age adolescents (n = 7); others involved population cohorts, psychiatric and gynaecological patients, women with bipolar disorder, attention-deficit/hyperactivity disorder (ADHD) or rheumatoid arthritis, pregnant and perimenopausal women, suicide attempters and online PMDD communities.")
para(f"Methods of identifying PMDD varied considerably. The largest group of studies ({asc['Retrospective screening / self-report (provisional)']}; {pct(asc['Retrospective screening / self-report (provisional)'])}) relied on retrospective screening instruments or self-report, yielding provisional diagnoses; {asc['Prospective symptom ratings (confirmed)']} ({pct(asc['Prospective symptom ratings (confirmed)'])}) confirmed PMDD with prospective daily ratings, {asc['Structured/psychiatric interview']} used structured or psychiatric interviews, {asc['Clinical/DSM-criteria diagnosis']} used clinical or DSM-criteria diagnoses and {asc['Clinical/registry diagnosis']} used registry diagnoses.")
# Table 1
def table(rows,header,widths,fs=9,title=None):
    if title: para(title,bold=False,indent=False,keep=True)
    t=doc.add_table(rows=1,cols=len(header)); t.style='Table Grid'; t.alignment=WD_TABLE_ALIGNMENT.CENTER
    for i,h in enumerate(header):
        cell=t.rows[0].cells[i]; cell.text=''; r=cell.paragraphs[0].add_run(h); r.bold=True; r.font.size=Pt(fs)
        sh=OxmlElement('w:shd'); sh.set(qn('w:val'),'clear'); sh.set(qn('w:fill'),'D9E2F3'); cell._tc.get_or_add_tcPr().append(sh)
    for row in rows:
        cells=t.add_row().cells
        for i,v in enumerate(row):
            cells[i].text=''; p=cells[i].paragraphs[0]; add_runs(p,str(v),size=fs,bold=str(v).startswith('§'))
            if str(v).startswith('§'): p.runs[0].text=p.runs[0].text[1:]
    for row in t.rows:
        for i,w in enumerate(widths):
            row.cells[i].width=Inches(w)
            for p in row.cells[i].paragraphs: p.paragraph_format.line_spacing_rule=WD_LINE_SPACING.SINGLE
    # repeat header
    trPr=t.rows[0]._tr.get_or_add_trPr(); th=OxmlElement('w:tblHeader'); th.set(qn('w:val'),'true'); trPr.append(th)
    return t
rows=[]
def blk(title,d,order=None):
    rows.append((f'§{title}','',''))
    items=[(k,d[k]) for k in order] if order else sorted(d.items(),key=lambda x:-x[1])
    for k,v in items: rows.append(('    '+k,v,pct(v)))
blk('Publication period',per,['2010–2014','2015–2019','2020–2025'])
blk('Study design',des)
blk('PMDD ascertainment',asc)
blk('World Bank income group (FY2027)',S['income'],['High income','Upper-middle income','Lower-middle income','Low income','Not classifiable (online/multinational/not reported)'])
blk('World Bank region',S['region'])
para('')
table(rows,['Characteristic','n','%'],[4.4,0.7,0.9],title='**Table 1** *Characteristics of Included Studies (N = 85)*')
para('Note. Percentages are of 85 included studies. Income groups follow the World Bank FY2027 classification (effective 1 July 2026).',indent=False,size=10)
H('Geographic Distribution',2)
inc=S['income']
para(f"Studies were conducted in 31 countries and territories; a further seven were online, multinational or did not report a country. The United States contributed the most studies (n = 13; 15.3%), followed by Japan, Sweden and Taiwan (n = 6 each), Türkiye (n = 5) and Germany and Iran (n = 4 each). Two-thirds of studies ({inc['High income']}; {pct(inc['High income'])}) came from high-income economies (Figure 3). Under the World Bank definition, {LMIC} studies ({pct(LMIC)}) were from LMICs, but most of these ({inc['Upper-middle income']}) were from upper-middle-income countries (Türkiye, n = 5; Iran, n = 4; Jordan, Mexico and mainland China, n = 2 each; Brazil, n = 1). Only {LLI} studies ({pct(LLI)}) came from lower-middle-income (Bangladesh, Lebanon, Nigeria) or low-income (Ethiopia) countries. Sub-Saharan Africa contributed three studies ({pct(3)}): a survey of 985 secondary-school adolescents in Ibadan, Nigeria {c(1421)}, and two studies from Ethiopia—one of 529 university students {c(452)} and one of 548 high-school students {c(1800)}.")
para(f"The LMIC evidence also differed in kind. Only one of the {LMIC} LMIC studies (Jordan) confirmed PMDD with prospective daily ratings {c(387)}; none of the qualitative or lived-experience studies came from an LMIC; and only one of the seven studies examining coping was conducted in an LMIC {c(443)}. No study from sub-Saharan Africa examined suicidality, quality of life, interpersonal functioning or coping as a primary aim.")
doc.add_picture('fig3_geography.png',width=Inches(6.3)); doc.paragraphs[-1].alignment=WD_ALIGN_PARAGRAPH.CENTER
H('Psychosocial Domains',2)
para(f"Figure 2 shows the number of studies examining each psychosocial domain. Depression was the most frequently examined domain (n = {D['Depression / depressive symptoms']}; {pct(D['Depression / depressive symptoms'])}), followed by mood and emotion regulation and psychiatric comorbidity (n = 18 each), psychological distress and perceived stress (n = 16), anxiety, suicidality and academic or occupational functioning (n = 13 each), interpersonal and relational functioning (n = 12), quality of life (n = 8), personality, trauma and adversity, and coping and resilience (n = 7 each), and lived experience, stigma and help-seeking (n = 5).")
doc.add_picture('fig2_domains.png',width=Inches(6.0)); doc.paragraphs[-1].alignment=WD_ALIGN_PARAGRAPH.CENTER
H('Depression and Psychiatric Comorbidity',3)
para(f"Women with PMDD reported more depressive symptoms than women with PMS or controls {c(711,738,1053)}, and PMDD was more common among young women with a history of major depression {c(798)}. Longitudinally, a Taiwanese national-insurance cohort of 8,222 women with PMDD and 32,888 matched controls found higher risks of unipolar depression (hazard ratio [HR] 2.58) and bipolar disorder (HR 2.50) after a PMDD diagnosis {c(1173)}. PMDD was also associated with antenatal depression (odds ratio [OR] 3.54) {c(1074)}, perinatal depression (OR up to 3.05) {c(1079)} and perimenopausal depression {c(848)}. Comorbidity studies linked PMDD with ADHD—provisional PMDD affected 31.4% of women with a clinical ADHD diagnosis versus 9.8% of a non-ADHD group {c(1036)}; see also {cn(286)} and {cn(1277)}—and with bipolar disorder, where comorbid PMDD was associated with earlier onset and greater illness burden {c(1312,1095,1515)}. PMDD was associated with bulimia nervosa (OR 7.2) {c(510)} and Internet use disorder {c(1323)}, and in a Korean national sample 59.3% of women with PMDD had at least one other psychiatric disorder, compared with 21.8% of women without PMDD {c(1378)}.")
H('Mood, Emotion Regulation and Personality',3)
para(f"Women with PMDD reported greater difficulties in emotion regulation {c(553,628,208,1053)}, more rumination and repetitive negative thinking {c(1258,1037,455,1314)} and more self-focused attention {c(698,1400)}, as well as higher anger and aggression {c(1490,1250,1285)}. Ecological momentary assessment studies from Germany showed that favourable habitual emotion-regulation strategies were linked to better everyday mood but did not protect against premenstrual mood deterioration {c(242)}, whereas momentary rumination and present-moment awareness predicted late-luteal mood {c(1037)}. Personality studies consistently reported higher neuroticism and related traits {c(350,1472,1224,1464)}, as well as anxious and cyclothymic temperaments {c(1159)} and differences in reinforcement sensitivity {c(1061)}.")
H('Psychological Distress and Anxiety',3)
para(f"PMDD was associated with psychological distress in a Swiss population survey {c(290)} and PMDD or premenstrual symptom severity was associated with higher perceived stress in Jordan, Spain, Saudi Arabia and Ethiopia {c(443,1224,336,1800)}; women with PMDD in Germany reported particularly high daily-life stress in the late luteal phase {c(1205)}; in a Spanish case-control study, high perceived stress was associated with more than five-fold higher odds of PMDD (OR 5.79) {c(1224)}. In Ethiopian high-school students, depressive symptoms and high perceived stress were among the factors associated with PMDD {c(1800)}. Anxiety was elevated in several samples {c(288,455,1031)}, including higher health anxiety and anxiety sensitivity among college women with provisional PMDD {c(1275)}.")
H('Suicidality and Self-Harm',3)
para(f"Thirteen studies examined suicidality. In a nationally representative US sample, PMDD was associated with suicidal ideation (OR 2.22), plans (OR 2.27) and attempts (OR 2.10) after adjustment for psychiatric comorbidity {c(695)}. Among Bangladeshi university students, PMDD was associated with suicidal ideation (adjusted OR [AOR] 5.42) and attempts (AOR 4.07) {c(1031)}. In a global survey of 599 people with prospectively diagnosed PMDD, 72% reported lifetime active suicidal ideation, 34% a suicide attempt and 51% non-suicidal self-injury {c(1186)}, and 39.1% of Swedish women with confirmed PMDD reported current suicidal ideation in the late luteal phase {c(1158)}. Among women with mood disorders in Taiwan, PMDD was independently associated with lifetime suicide attempts (OR 3.46) {c(693)}; PMDD was more frequent among Iranian suicide attempters than matched controls {c(1267)}; and 23% of women hospitalised after a suicide attempt in France met PMDD criteria {c(1250)}; and a Swedish population cohort found a higher risk of suicidal behaviour (HR 2.26) among women with clinically recognised premenstrual disorders {c(1354)}.")
H('Functioning, Relationships and Quality of Life',3)
para(f"PMDD was associated with presenteeism and absenteeism in a nationwide Japanese workforce survey {c(1141)}, with absenteeism from clinical training among Kuwaiti nursing students {c(1347)}, with differences in academic self-determination among Jordanian university students {c(387)} and with lower occupational competence in Türkiye {c(1189)}; in contrast, an Ethiopian study found no significant association between premenstrual symptoms and academic performance {c(452)}. PMDD was associated with relationship disruption among married or cohabiting women in a Swedish cohort (incidence rate ratio 1.22) {c(1041)}, and both people with PMDD and their partners reported lower relationship quality {c(1083)}. Quality of life was consistently lower: in a Swedish cohort of 17,284 women, the association with reduced quality of life was stronger for PMDD than for PMS {c(485)}; untreated Japanese patients had a mean EQ-5D score of 0.795, corresponding to an estimated lifetime loss of about three quality-adjusted life years {c(445)}; and Iranian adolescents with PMDD scored lower on all SF-36 domains except physical functioning {c(976)}.")
H('Trauma, Adversity and Discrimination',3)
para(f"Adverse childhood experiences were associated with premenstrual disorders in a dose-dependent manner in Iceland (prevalence ratio 2.46 for four or more experiences), more strongly for PMDD than PMS {c(1318)}, and four or more such experiences were associated with PMDD among Japanese working women (AOR 5.61) {c(1111)}; school bullying was associated with premenstrual disorders among Chinese adolescents, more strongly for PMDD than PMS {c(1038)}; 83% of Australian clinic patients with PMDD reported early-life trauma {c(1162)}; and perceived discrimination was associated with PMDD among US minority women {c(1338)}. In Lebanon, depression mediated the association between childhood abuse and PMDD {c(1137)}.")
H('Coping and Lived Experience',3)
para(f"Only seven studies examined coping or resilience. Jordanian women with PMS or PMDD most often self-treated by taking analgesics, drinking hot fluids, wearing warm clothing and lying on the abdomen {c(443)}; Canadian women with PMDD used cannabis more pre-menstrually and menstrually, partly for coping motives {c(483)}; women with premenstrual disorders in the United States reported more maladaptive coping styles than controls {c(698)}; and in a Spanish case-control study, higher use of most coping strategies was associated with increased odds of PMDD {c(1224)}. Coping styles were also measured alongside rumination in a US study {c(1314)}. Resilience potentially moderated associations between high-risk PMDD and anxiety, depression and loneliness among Hong Kong students {c(288)}, and members of an online PMDD community described peer support and knowledge as sources of agency {c(1116)}. Five studies, all from high-income or online settings, explored lived experience and help-seeking, describing misdiagnosis and “lost decades” {c(296)}, medical mistrust and masking {c(311)}, variable provider knowledge across specialties {c(1200)} and patient priorities for PMDD-tailored mental health care, including suicidality and relationships {c(1117)}.")
# ---------- DISCUSSION ----------
H('Discussion')
para(f"This scoping review mapped {N} empirical studies of psychosocial outcomes and coping among women with PMDD. Three findings stand out. First, the literature is growing quickly—half of the studies were published since 2020—and it consistently links PMDD with depression, psychiatric comorbidity, suicidality, impaired functioning and reduced quality of life. The suicidality findings are particularly striking and span nationally representative surveys, clinical samples and population registries, supporting calls for routine suicide-risk screening in people with PMDD. Second, the evidence is narrow in scope: coping (n = 7) and lived experience (n = 5) were rarely primary aims, and no study examined adaptive coping longitudinally. Third, the evidence base is geographically concentrated: two-thirds of studies came from high-income countries, only five came from low- or lower-middle-income countries, and just three came from sub-Saharan Africa.")
para(f"Methodological features limit what the evidence can tell us. Fewer than one in four studies confirmed PMDD with prospective daily ratings, and over two in five relied on provisional, retrospective diagnoses. Provisional diagnoses substantially overestimate prevalence (Reilly et al., 2024), and in one study self-reported PMDD (51.8%) far exceeded clinically assessed PMDD (5.9%) {c(1175)}. Associations with psychosocial outcomes based on provisional diagnoses may therefore conflate PMDD with PMS or with premenstrual exacerbation of other disorders. The problem is sharpest in LMICs, where only one study used prospective ratings; the high prevalence (33.0%) reported among Ethiopian high-school students from a single cross-sectional DSM-5-based assessment {c(1800)} illustrates the need for validated, prospectively confirmed assessment. Notably, none of the 11 instrument-validation studies identified (and excluded) during screening was conducted in an African setting.")
para(f"The scarcity of evidence from sub-Saharan Africa is not evidence of a small burden. Premenstrual symptoms are common across Africa (Andualem et al., 2024), and a community-based study of adolescent girls in southwest Ethiopia—excluded here because PMDD was a covariate rather than the study population—found PMDD independently associated with suicidal ideation (Segon et al., 2025). Research on premenstrual coping in Ethiopia has so far focused on PMS rather than PMDD (Eshetu et al., 2022). Together these observations suggest that PMDD’s psychosocial burden in the region is real but largely invisible to health systems.")
H('Implications for Public Health Practice and Research',2)
para("For practice, the consistent association between PMDD and suicidality supports routine screening for suicidal ideation in people presenting with premenstrual mood symptoms, and vice versa. PMDD screening could be integrated into existing sexual and reproductive health, school-health and university health services, which reach the adolescents and students who dominate the LMIC evidence. Provider training should address the diagnostic delays and dismissive care that patients describe. For research, priorities include prospectively confirmed studies in LMICs; qualitative research on lived experience, stigma and help-seeking in African contexts; validation of PMDD instruments in African languages; and longitudinal studies of coping and of interventions that strengthen adaptive coping.")
H('Strengths and Limitations',2)
para("This review screened records from seven databases, documented every decision in an auditable log and applied the World Bank’s current income classification. Several limitations apply. First, eligibility was judged on titles, abstracts and subject terms; full-text review is ongoing and may change the final set of studies. Second, screening and charting were AI-assisted and require independent verification by two human reviewers. Third, restricting to English excluded 65 records (most commonly Persian, French, Korean, German and Turkish), and the databases searched did not include regional sources such as African Journals Online, Embase, Scopus or grey literature, so the geographic gap may be partly an artefact of database coverage. Fourth, some studies combined PMS and PMDD, country was occasionally inferred from the study setting, and domains were coded from abstracts, so domain counts are approximate.")
H('Conclusions',2)
para("Evidence on the psychosocial burden of PMDD is growing and points to substantial effects on mental health, suicidality, functioning, relationships and quality of life. It remains concentrated in high-income countries, relies heavily on provisional diagnoses and rarely examines coping or lived experience. Culturally responsive screening, integration of PMDD into reproductive and mental health services, and Africa-centred research investment are needed for a condition whose burden remains largely invisible to health systems globally.")
H('Declarations',2)
note('[Funding: state funding or “none”. Conflicts of interest: declare. Author contributions (CRediT): complete. AI use: describe AI assistance with screening, charting and drafting per journal policy. Data availability: screening log and charting table provided as Supplementary File.]')
doc.add_page_break()
# ---------- REFERENCES ----------
H('References')
bg=[
("American Psychiatric Association. (2013). *Diagnostic and statistical manual of mental disorders* (5th ed.). American Psychiatric Publishing. https://doi.org/10.1176/appi.books.9780890425596"),
("Andualem, F., Melkam, M., Takelle, G. M., Nakie, G., Tinsae, T., Fentahun, S., Rtbey, G., Seid, J., Gedef, G. M., Bitew, D. A., & Godana, T. N. (2024). Prevalence of premenstrual syndrome and its associated factors in Africa: A systematic review and meta-analysis. *Frontiers in Psychiatry, 15*, Article 1338304. https://doi.org/10.3389/fpsyt.2024.1338304"),
("Arksey, H., & O’Malley, L. (2005). Scoping studies: Towards a methodological framework. *International Journal of Social Research Methodology, 8*(1), 19–32. https://doi.org/10.1080/1364557032000119616"),
("Eshetu, N., Abebe, H., Fikadu, E., Getaye, S., Jemal, S., Geze, S., Mesfin, Y., Abebe, S., Tsega, D., Tefera, B., & Tesfaye, W. (2022). Premenstrual syndrome, coping mechanisms and associated factors among Wolkite university female regular students, Ethiopia, 2021. *BMC Women’s Health, 22*(1), Article 88. https://doi.org/10.1186/s12905-022-01658-5"),
("Levac, D., Colquhoun, H., & O’Brien, K. K. (2010). Scoping studies: Advancing the methodology. *Implementation Science, 5*, Article 69. https://doi.org/10.1186/1748-5908-5-69"),
("Naik, S. S., Nidhi, Y., Kumar, K., & Grover, S. (2023). Diagnostic validity of premenstrual dysphoric disorder: Revisited. *Frontiers in Global Women’s Health, 4*, Article 1181583. https://doi.org/10.3389/fgwh.2023.1181583"),
("Reilly, T. J., Patel, S., Unachukwu, I. C., Knox, C.-L., Wilson, C. A., Craig, M. C., Schmalenberger, K. M., Eisenlohr-Moul, T. A., & Cullen, A. E. (2024). The prevalence of premenstrual dysphoric disorder: Systematic review and meta-analysis. *Journal of Affective Disorders, 349*, 534–540. https://doi.org/10.1016/j.jad.2024.01.066"),
("Segon, T., Dule, A., Alemayehu, D., Aderaw, M., Melkam, M., Tinsae, T., Nakie, G., Kibralew, G., Tadesse, G., Wondie, T., Seid, E., Kassa, M., Kassie, G. M., Belayneh, Z., Ali, Y., & Molla, A. (2025). Suicidal ideation, attempts and help-seeking behaviors among adolescent girls in Southwest Ethiopia: A community-based cross-sectional study. *Child and Adolescent Psychiatry and Mental Health, 19*(1), Article 146. https://doi.org/10.1186/s13034-025-00996-0"),
("Tricco, A. C., Lillie, E., Zarin, W., O’Brien, K. K., Colquhoun, H., Levac, D., Moher, D., Peters, M. D. J., Horsley, T., Weeks, L., Hempel, S., Akl, E. A., Chang, C., McGowan, J., Stewart, L., Hartling, L., Aldcroft, A., Wilson, M. G., Garritty, C., . . . Straus, S. E. (2018). PRISMA extension for scoping reviews (PRISMA-ScR): Checklist and explanation. *Annals of Internal Medicine, 169*(7), 467–473. https://doi.org/10.7326/M18-0850"),
("University of Oxford. (2024, January 30). *New data shows prevalence of premenstrual dysphoric disorder (PMDD)*. https://www.ox.ac.uk/news/2024-01-30-new-data-shows-prevalence-premenstrual-dysphoric-disorder"),
("World Bank. (2026). *World Bank country classifications by income level for FY2027*. https://datahelpdesk.worldbank.org/knowledgebase/articles/906519-world-bank-country-and-lending-groups"),
("World Health Organization. (2022). *International classification of diseases, 11th revision (ICD-11)*. https://icd.who.int/"),
]
FIX={1224:{'authors':'Fernández, María del Mar ; Regueira-Méndez, Carlos ; Takkouche, Bahi'},
     1800:{'journal':'Frontiers in Psychiatry','volume':'15','pages':'Article 1362118'}}
inc=[]
for rid in T.index:
    r=m.loc[rid].to_dict(); r.update(FIX.get(rid,{}))
    s,j,vi,p,doi=apa(r,SUFFIX.get(rid,''))
    if rid==1224: s=s.replace('Fernández, M. d. M.','Fernández, M. del M.')
    p=p.replace('N.PAG-N.PAG','').replace('N.PAG','')
    txt=s+f"*{j}*"
    if vi: 
        v=re.match(r'(\d+)(\(.*\))?',vi); txt+=f", *{v.group(1)}*{v.group(2) or ''}"
    if p: txt+=f", {p.replace('-','–')}" if not p.startswith('Article') else f", {p}"
    txt+='.'
    if doi: txt+=f" https://doi.org/{doi}"
    key=re.sub(r'[^a-z]','',unicodedata_normalize(s.lower())) if False else s.lower()
    inc.append((s,txt))
allrefs=[(x.lower(),x) for x in bg]+[(k.lower(),t) for k,t in inc]
import unicodedata
def sk(x): return unicodedata.normalize('NFKD',x).encode('ascii','ignore').decode().lower()
for _,t in sorted(allrefs,key=lambda x:sk(x[1])):
    p=doc.add_paragraph(); p.paragraph_format.left_indent=Inches(0.5); p.paragraph_format.first_line_indent=Inches(-0.5); add_runs(p,t)
doc.add_page_break()
# ---------- APPENDIX TABLE ----------
H('Supplementary Table S1')
para('*Characteristics of the 85 Included Studies*',indent=False,align='center')
LAB={'DEP':'Depression','ANX':'Anxiety','MER':'Mood/emotion regulation','PD':'Distress/stress','IF':'Interpersonal','SUI':'Suicidality/self-harm','QOL':'Quality of life','COP':'Coping/resilience','FUN':'Academic/occupational functioning','TRA':'Trauma/adversity','COM':'Psychiatric comorbidity','PER':'Personality','EXP':'Lived experience/help-seeking'}
rows=[]
for rid,r in T.sort_values('year').iterrows():
    mm=m.loc[rid]; a=intext(rid,mm.authors,mm.year,SUFFIX.get(rid,'')).rsplit(', ',1)
    rows.append((f"{a[0]} ({a[1]})",r.country.replace('Turkey','Türkiye'),r.design,r.sample_size,r.population,r.pmdd_ascertainment,'; '.join(LAB[d] for d in r.domain_codes.split())))
sec=doc.sections[-1]
from docx.enum.section import WD_ORIENT, WD_SECTION
ns=doc.add_section(WD_SECTION.NEW_PAGE); ns.orientation=WD_ORIENT.LANDSCAPE; ns.page_width,ns.page_height=sec.page_height,sec.page_width
table(rows,['Study','Country','Design','N','Population','PMDD ascertainment','Psychosocial domains'],[1.4,1.0,1.5,0.6,1.5,1.5,1.5],fs=8)
para('Note. NR = not reported in the abstract. Country was taken from the abstract or study setting. Full screening decisions for all 1,801 records are in the Supplementary File (Excel).',indent=False,size=10)
doc.save('PMDD_Scoping_Review_Manuscript.docx'); print('saved')
