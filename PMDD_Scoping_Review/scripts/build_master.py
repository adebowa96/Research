import pandas as pd, re, glob, json
W='/root/work/'
src_names={'37b3f2fb':'EBSCO export 1 (CINAHL)','7416e639':'EBSCO export 2 (CINAHL)',
 'b8928d61':'EBSCO export 3 (APA PsycInfo/CINAHL/PsycArticles)','285fb757':'EBSCO export 4 (MEDLINE/CINAHL/WSI/PsycInfo)'}
rows=[]
for f in sorted(glob.glob(W+'*_2.csv')):
    d=pd.read_csv(f); k=f.split('/')[-1][:8]
    for _,r in d.iterrows():
        rows.append(dict(export=src_names[k],database=r.longDBName,accession=str(r.an),title=str(r.title).strip(),
            abstract='' if pd.isna(r.abstract) else str(r.abstract),year=int(str(r.publicationDate)[:4]),
            authors='' if pd.isna(r.contributors) else str(r.contributors),journal='' if pd.isna(r.source) else str(r.source),
            doc_type=f"{r.docTypes} | {r.pubTypes}",language='' if pd.isna(r.language) else str(r.language),
            peer_reviewed=r.peerReviewed,doi='' if pd.isna(r.doi) else str(r.doi).strip(),
            volume='' if pd.isna(r.volume) else str(r.volume),issue='' if pd.isna(r.issue) else str(r.issue),
            pages=('' if pd.isna(r.pageStart) else str(r.pageStart))+('' if pd.isna(r.pageEnd) else '-'+str(r.pageEnd)),
            subjects='' if pd.isna(r.subjects) else str(r.subjects), link=r.plink))
c=pd.read_csv(W+'4085f4f0-citation-export_1.csv')
for _,r in c.iterrows():
    rows.append(dict(export='Cochrane Library export',database='Cochrane Database of Systematic Reviews',accession=r['Cochrane Review ID'],
        title=r.Title,abstract=r.Abstract,year=int(r.Year),authors=r['Author(s)'],journal=r.Source,doc_type='Cochrane systematic review',
        language='English',peer_reviewed=True,doi=r.DOI,volume='',issue=str(r.Issue),pages='',subjects=str(r.Keywords),link=r.URL))
t=open(W+'c1687b0e-summary-premenstru-set_4.txt').read()
for blk in re.split(r'\n\s*\n',t.strip()):
    b=' '.join(blk.split()); b=re.sub(r'^\d+:\s*','',b)
    auth,rest=b.split('. ',1); title,rest2=rest.split('. ',1)
    yr=int(re.search(r'(20\d\d)',rest2).group(1)); doi=re.search(r'doi: (\S+?)\.\s',b).group(1)
    pmid=re.search(r'PMID: (\d+)',b).group(1)
    rows.append(dict(export='PubMed export',database='PubMed/MEDLINE',accession='PMID '+pmid,title=title,abstract='',year=yr,
        authors=auth,journal=rest2.split('.')[0],doc_type='Journal Article',language='English',peer_reviewed=True,doi=doi,
        volume='',issue='',pages='',subjects='',link='https://pubmed.ncbi.nlm.nih.gov/'+pmid))
m=pd.DataFrame(rows)
m['doi_n']=m.doi.str.lower().str.replace(r'^https?://(dx\.)?doi\.org/','',regex=True).str.strip()
m['title_n']=m.title.str.lower().str.replace(r'<[^>]+>','',regex=True).str.replace(r'[\W_]','',regex=True)
# duplicate grouping: union of DOI and normalized title
parent=list(range(len(m)))
def find(i):
    while parent[i]!=i: parent[i]=parent[parent[i]]; i=parent[i]
    return i
for key in ['doi_n','title_n']:
    first={}
    for i,v in enumerate(m[key]):
        if not v or len(v)<8: continue
        if v in first: parent[find(i)]=find(first[v])
        else: first[v]=i
m['group']=[find(i) for i in range(len(m))]
# choose primary record per group: prefer one with abstract, MEDLINE/PsycInfo
pri={'PubMed/MEDLINE':0,'MEDLINE Ultimate':1,'APA PsycInfo':2,'CINAHL Ultimate':3}
m['_len']=m.abstract.str.len()
m['_p']=m.database.map(pri).fillna(5)
m=m.sort_values(['group','_len','_p'],ascending=[True,False,True])
m['is_duplicate']=m.duplicated('group')
m['record_id']=range(1,len(m)+1)
m.drop(columns=['_len','_p']).to_pickle(W+'pmdd/master.pkl')
print('total',len(m),'duplicates',m.is_duplicate.sum(),'unique',(~m.is_duplicate).sum())
print(m.groupby('export').size())
