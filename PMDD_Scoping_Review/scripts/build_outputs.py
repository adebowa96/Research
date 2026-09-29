import pandas as pd, json, re, collections
exec(open('chart.py').read())
m=pd.read_pickle('master.pkl')
s1=pd.read_pickle('stage1.pkl').set_index('record_id')
rest=pd.read_pickle('rest.pkl').set_index('record_id')
dec=dict((int(a),b) for a,b in (l.split() for l in open('decisions.txt')))
R={'REV':'Review, commentary, editorial, guideline or other non-empirical article',
 'POP':'PMDD not the primary/defined study population',
 'INT':'Intervention or treatment study',
 'LAB':'Laboratory/biological study (neuroimaging, hormonal, genetic, physiological)',
 'OUT':'No psychosocial outcome or coping mechanism as a primary aim',
 'VAL':'Instrument development/validation study',
 'ANI':'Animal study','CASE':'Case report or case series','PUB':'Conference abstract',
 'NOPMDD':'PMDD not studied (not mentioned in title, abstract or subject terms)'}
S1={'Excluded: published outside 2010–2025':'Published outside 2010–2025',
 'Excluded: non-English full text':'Non-English full text',
 'Excluded: ineligible publication type (book, chapter, dissertation, letter, editorial, comment, case report, or non-peer-reviewed)':'Ineligible publication type (book, chapter, dissertation, letter, editorial, comment, case report, non-peer-reviewed)',
 'Excluded: review/meta-analysis/guideline (not primary empirical study)':'Review, meta-analysis or guideline (not a primary empirical study)'}
dup_of={}
for g,grp in m.groupby('group'):
    keep=grp[~grp.is_duplicate].record_id.iloc[0]
    for r in grp[grp.is_duplicate].record_id: dup_of[r]=keep
rows=[]
for _,r in m.sort_values('record_id').iterrows():
    rid=r.record_id
    if r.is_duplicate: stage,decision,reason='Deduplication','Duplicate removed',f'Duplicate of record {dup_of[rid]}'
    elif s1.loc[rid,'stage1']: stage,decision,reason='Screening – eligibility filters','Excluded',S1[s1.loc[rid,'stage1']]
    elif not rest.loc[rid,'pmdd_mention']: stage,decision,reason='Screening – title/abstract','Excluded',R['NOPMDD']
    else:
        d=dec[rid]; stage='Screening – title/abstract'
        decision='Included' if d=='I' else 'Excluded'; reason='' if d=='I' else R[d]
    rows.append(dict(record_id=rid,source_export=r.export,database=r.database,accession=r.accession,authors=r.authors,year=r.year,title=r.title,journal=r.journal,doi=r.doi,language=r.language,stage=stage,decision=decision,reason=reason,link=r.link))
log=pd.DataFrame(rows)
# PRISMA
P=collections.OrderedDict()
P['identified_total']=len(m)
P['identified_by_database']=m.database.value_counts().to_dict()
P['identified_by_export']=m.export.value_counts().to_dict()
P['duplicates_removed']=int(m.is_duplicate.sum())
P['screened']=int((~m.is_duplicate).sum())
ex=log[log.decision=='Excluded']
P['excluded_total']=len(ex)
P['excluded_by_reason']=ex.reason.value_counts().to_dict()
P['included']=int((log.decision=='Included').sum())
# charting table
LAB={'DEP':'Depression / depressive symptoms','ANX':'Anxiety','MER':'Mood & emotion regulation','PD':'Psychological distress & perceived stress','IF':'Interpersonal & relational functioning','SUI':'Suicidal ideation, attempts & self-harm','QOL':'Quality of life','COP':'Coping strategies & resilience','FUN':'Academic & occupational functioning','TRA':'Trauma, adversity & discrimination','COM':'Psychiatric comorbidity','PER':'Personality & temperament','EXP':'Lived experience, stigma & help-seeking'}
INC={'Ethiopia':'Low income','Bangladesh':'Lower-middle income','Lebanon':'Lower-middle income','Nigeria':'Lower-middle income',
 'Jordan':'Upper-middle income','Iran':'Upper-middle income','Mexico':'Upper-middle income','Brazil':'Upper-middle income','China':'Upper-middle income','Turkey':'Upper-middle income'}
REG={'United States':'North America','Canada':'North America','Mexico':'Latin America & Caribbean','Brazil':'Latin America & Caribbean',
 'Germany':'Europe & Central Asia','Switzerland':'Europe & Central Asia','United Kingdom':'Europe & Central Asia','Belgium':'Europe & Central Asia','Sweden':'Europe & Central Asia','Netherlands':'Europe & Central Asia','Poland':'Europe & Central Asia','Spain':'Europe & Central Asia','France':'Europe & Central Asia','Italy':'Europe & Central Asia','Iceland':'Europe & Central Asia','Turkey':'Europe & Central Asia',
 'Japan':'East Asia & Pacific','China (Hong Kong)':'East Asia & Pacific','China':'East Asia & Pacific','Taiwan':'East Asia & Pacific','South Korea':'East Asia & Pacific','Australia':'East Asia & Pacific',
 'Iran':'Middle East & North Africa','Jordan':'Middle East & North Africa','Israel':'Middle East & North Africa','Saudi Arabia':'Middle East & North Africa','Lebanon':'Middle East & North Africa','Kuwait':'Middle East & North Africa',
 'Bangladesh':'South Asia','Ethiopia':'Sub-Saharan Africa','Nigeria':'Sub-Saharan Africa'}
def income(c):
    if c in INC: return INC[c]
    if c.startswith('NR') or c.startswith('Online') or c=='Multinational': return 'Not classifiable (online/multinational/not reported)'
    return 'High income'
def design_group(d):
    d=d.lower()
    if 'qualitative' in d: return 'Qualitative'
    if 'ema' in d or 'ambulatory' in d or 'daily' in d or 'prospective daily' in d: return 'Prospective daily ratings / EMA'
    if 'saga cohort' in d: return 'Cross-sectional'
    if 'registry' in d or 'cohort' in d or 'longitudinal' in d: return 'Cohort / registry'
    if 'case-control' in d: return 'Case-control'
    if 'prospective' in d: return 'Prospective observational'
    if 'chart' in d or 'retrospective' in d: return 'Retrospective record review'
    return 'Cross-sectional'
def asc_group(a):
    a=a.lower()
    if 'self-report' in a or 'self-identified' in a: return 'Retrospective screening / self-report (provisional)'
    if 'registry' in a: return 'Clinical/registry diagnosis'
    if 'prospective' in a or 'daily' in a or 'drsp' in a or 'cycle' in a: return 'Prospective symptom ratings (confirmed)'
    if 'interview' in a or 'scid' in a or 'cidi' in a or 'mini' in a or 'sads' in a: return 'Structured/psychiatric interview'
    if 'clinical' in a or 'specialist' in a or 'dsm' in a or 'criteria' in a: return 'Clinical/DSM-criteria diagnosis'
    return 'Retrospective screening / self-report (provisional)'
mi=m.set_index('record_id')
def cite(r):
    au=[a.strip() for a in re.split(r'\s;\s|;\s|,\s(?=[A-Z][a-z]+ [A-Z]+(?:,|$))',r.authors) if a.strip()] if ';' in r.authors else [r.authors]
    first=au[0].split(',')[0].split(' ')[0] if ',' in au[0] else au[0].split(' ')[0]
    et=' et al.' if len(au)>2 else (f' & {au[1].split(",")[0]}' if len(au)==2 else '')
    return f"{first}{et} ({r.year})"
tab=[]
for i,v in sorted(C.items()):
    r=mi.loc[i]
    tab.append(dict(record_id=i,citation=cite(r),year=int(r.year),title=re.sub(r'<[^>]+>','',r.title),journal=r.journal,doi=r.doi,
        country=v['country'],region=REG.get(v['country'],'Online / multinational / not reported'),income_group=income(v['country']),
        design=v['design'],design_group=design_group(v['design']),sample_size=v['n'],population=v['population'],
        pmdd_ascertainment=v['ascertainment'],ascertainment_group=asc_group(v['ascertainment']),
        domain_codes=' '.join(v['domains']),domains='; '.join(LAB[d] for d in v['domains'])))
T=pd.DataFrame(tab)
dom=collections.Counter(d for v in C.values() for d in v['domains'])
stats=dict(prisma=P,n_included=len(T),
 domains={LAB[k]:dom[k] for k in LAB},
 country=T.country.value_counts().to_dict(), region=T.region.value_counts().to_dict(),
 income=T.income_group.value_counts().to_dict(), design=T.design_group.value_counts().to_dict(),
 ascertainment=T.ascertainment_group.value_counts().to_dict(),
 period={'2010–2014':int((T.year<=2014).sum()),'2015–2019':int(((T.year>=2015)&(T.year<=2019)).sum()),'2020–2025':int((T.year>=2020).sum())},
 by_year=T.year.value_counts().sort_index().to_dict())
json.dump(stats,open('stats.json','w'),indent=1,ensure_ascii=False,default=int)
log.to_pickle('log.pkl'); T.to_pickle('table.pkl')
print(json.dumps(stats,indent=1,ensure_ascii=False,default=int))
