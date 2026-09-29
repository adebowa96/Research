import pandas as pd, re
m=pd.read_pickle('master.pkl')
u=m[~m.is_duplicate].copy()
def lang_en(l): return l.strip().lower() in ('english','eng','')
nonpr=re.compile(r'dissertation|chapter|book|letter|editorial|comment|erratum|errata|conference|proceeding|news|database|electronic collection|periodical|case report',re.I)
rev_title=re.compile(r'\breview\b|meta-?analy|systematic|overview|scoping|\bupdate on\b|guideline|consensus|recommendations',re.I)
def s1(r):
    if r.year<2010 or r.year>2025: return 'Excluded: published outside 2010–2025'
    if not lang_en(r.language): return 'Excluded: non-English full text'
    if nonpr.search(r.doc_type) or str(r.peer_reviewed)=='False': return 'Excluded: ineligible publication type (book, chapter, dissertation, letter, editorial, comment, case report, or non-peer-reviewed)'
    if r.export=='Cochrane Library export' or re.search(r'\breview\b',r.doc_type,re.I) or rev_title.search(r.title): return 'Excluded: review/meta-analysis/guideline (not primary empirical study)'
    return ''
u['stage1']=u.apply(s1,axis=1)
print(u.stage1.value_counts())
rest=u[u.stage1=='']
pm=re.compile(r'premenstrual dysphoric|pre-menstrual dysphoric|\bPMDD\b|late luteal phase dysphoric|LLPDD|\bPMDs?\b|premenstrual disorder',re.I)
rest=rest.assign(pmdd_mention=rest.apply(lambda r: bool(pm.search(r.title+' '+r.abstract+' '+r.subjects)),axis=1))
print('remaining',len(rest),'pmdd mention',rest.pmdd_mention.sum(), 'no abstract',(rest.abstract.str.len()<50).sum())
u.to_pickle('stage1.pkl'); rest.to_pickle('rest.pkl')
