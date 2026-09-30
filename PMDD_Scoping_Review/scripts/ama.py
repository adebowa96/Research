import pandas as pd, re
m=pd.read_pickle('/root/work/pmdd/master.pkl').set_index('record_id')
JA={"PLoS ONE":"PLoS One","The Lancet Psychiatry":"Lancet Psychiatry","Women's Reproductive Health":"Womens Reprod Health (Phila)","Women’s Reproductive Health":"Womens Reprod Health (Phila)","JAMA Network Open":"JAMA Netw Open","Clinical Psychology & Psychotherapy":"Clin Psychol Psychother","Healthcare (2227-9032)":"Healthcare (Basel)","Journal of Affective Disorders":"J Affect Disord","Women & Health":"Women Health","Journal of Nervous and Mental Disease":"J Nerv Ment Dis","Klinik Psikiyatri Dergisi: The Journal of Clinical Psychiatry":"Klin Psikiyatri Derg","Asian Journal of Psychiatry":"Asian J Psychiatr","Behavioral Psychology":"Behav Psychol","Psychiatry Research":"Psychiatry Res","BMC Psychiatry":"BMC Psychiatry","British Journal of Occupational Therapy":"Br J Occup Ther","Journal of Women's Health (15409996)":"J Womens Health (Larchmt)","BMC Medicine":"BMC Med","Behaviour Research and Therapy":"Behav Res Ther","Advances in Nursing & Midwifery":"Adv Nurs Midwifery","Journal of Reproductive & Infant Psychology":"J Reprod Infant Psychol","Psychological Medicine":"Psychol Med","Archives of Women's Mental Health":"Arch Womens Ment Health","Journal of Obstetrics & Gynaecology":"J Obstet Gynaecol","Gender & Behaviour":"Gend Behav","International Journal of Psychiatry in Medicine":"Int J Psychiatry Med","Social Psychiatry and Psychiatric Epidemiology: The International Journal for Research in Social and Genetic Epidemiology and Mental Health Services":"Soc Psychiatry Psychiatr Epidemiol","Health & Quality of Life Outcomes":"Health Qual Life Outcomes","The Patient: Patient-Centered Outcomes Research":"Patient"}
PAGES={1031:'e0321097',1083:'e0322314',1250:'e0148653',424:'e70062',336:'2862',1173:'103355',1162:'114381',1186:'199',1318:'60',1137:'548',1258:'103613',976:'1',485:'e2533823'}
PROPER={'sweden','swedish','korean','korea','nigeria','ibadan','lebanese','bangladesh','canada','japanese','taiwan','chinese','hong','kong','turkish','iranian','iran','jordan','spanish','polish','ethiopia','africa','african','mexico','brazil','dsm-5','dsm-iv','icd-11'}
def sentence(t):
    t=re.sub(r'<[^>]+>','',t).strip().rstrip('.')
    out=[]; cap=True
    for w in t.split(' '):
        core=re.sub(r'[^\w\-’\']','',w)
        if not core: out.append(w); continue
        if cap:
            parts=w.split('-'); w='-'.join([parts[0]]+[p if (p.isupper() and len(p)>1) else p.lower() for p in parts[1:]]); out.append(w)
        elif (core.isupper() and len(core)>1) or any(ch.isdigit() for ch in core) or re.search(r'[a-z][A-Z]',core) or core.lower().strip('’\'s') in PROPER or core.lower() in PROPER:
            out.append(w)
        else: out.append(w.lower())
        cap = w.endswith('?')
    s=' '.join(out)
    s=re.sub(r'\bpmdd\b','PMDD',s); s=re.sub(r'\bpms\b','PMS',s)
    return s
def ini(first):
    first=first.replace('.',' ')
    return ''.join(''.join(q[0].upper() for q in p.split('-') if q) for p in first.split() if p)
def author(n):
    n=n.strip().replace('‐','-')
    if ',' in n:
        last,first=n.split(',',1); return f"{last.strip()} {ini(first)}"
    return n
def authors(a):
    L=[x for x in (a.split(';') if ';' in a else a.split(', ')) if x.strip()]
    L=[author(x) for x in L]
    return ', '.join(L) if len(L)<=6 else ', '.join(L[:3])+', et al'
def ama(rid,override=None):
    r=m.loc[rid].to_dict(); r.update(override or {})
    A=authors(r['authors']); T=sentence(r['title']); J=JA.get(r['journal'],r['journal'])
    v=str(r['volume']).replace('.0','') if str(r['volume']) not in ('','nan') else ''
    i=str(r['issue']).replace('.0','') if str(r['issue']) not in ('','nan') else ''
    p=PAGES.get(rid, str(r['pages']).replace('-nan',''))
    if p in ('nan',): p=''
    s=f"{A}. {T}. {J}. {r['year']}"
    if v: s+=f";{v}"+(f"({i})" if i else '')
    if p: s+=f":{p}"
    s+='.'
    if r['doi'] and str(r['doi'])!='nan': s+=f" doi:{r['doi']}"
    return s
