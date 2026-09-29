import pandas as pd, re
def initials(first):
    out=[]
    for part in first.replace('.',' ').split():
        if '-' in part: out.append('-'.join(p[0]+'.' for p in part.split('-') if p))
        elif part: out.append(part[0]+'.')
    return ' '.join(out)
def fmt_name(n):
    n=n.strip().strip(',').replace('‐','-')
    if ',' in n:
        last,first=n.split(',',1); return f"{last.strip()}, {initials(first.strip())}"
    parts=n.split()
    if len(parts)>=2 and parts[-1].isupper() and len(parts[-1])<=3:
        return f"{' '.join(parts[:-1])}, {' '.join(c+'.' for c in parts[-1])}"
    return n
def split_authors(a):
    if ';' in a: return [x for x in a.split(';') if x.strip()]
    return [x for x in a.split(', ') if x.strip()]
def surname(n):
    n=n.strip().replace('‐','-')
    if ',' in n: return n.split(',')[0].strip()
    parts=n.split(); return ' '.join(parts[:-1]) if len(parts)>1 else n
SURNAME_FIX={1224:'Fernández',1800:'Kibralew'}
def intext(rid,authors,year,suffix=''):
    au=split_authors(authors); s=SURNAME_FIX.get(rid,surname(au[0]))
    if len(au)==1: return f"{s}, {year}{suffix}"
    if len(au)==2: return f"{s} & {surname(au[1])}, {year}{suffix}"
    return f"{s} et al., {year}{suffix}"
def clean_journal(j):
    j=re.sub(r'\s*\((?:\d{4}-?\d{3}[\dX]|\d{8}|John Wiley.*?|Wiley.*?)\)','',j); return j.replace('®','').strip()
def clean_num(v):
    v=str(v)
    return '' if v in ('','nan','None') else re.sub(r'\.0$','',v)
def apa(r, suffix=''):
    au=[fmt_name(x) for x in split_authors(r['authors'])]
    if len(au)>20: au=au[:19]+['. . . '+au[-1]]
    if len(au)==1: A=au[0]
    elif au[-1].startswith('. . .'): A=', '.join(au[:-1])+', '+au[-1]
    else: A=', '.join(au[:-1])+', & '+au[-1]
    t=re.sub(r'<[^>]+>','',r['title']).strip().rstrip('.')
    j=clean_journal(r['journal']); v=clean_num(r.get('volume','')); i=clean_num(r.get('issue','')); p=clean_num(r.get('pages','')).replace('-nan','')
    s=f"{A} ({r['year']}{suffix}). {t}. "
    parts=[j]; vi=''
    if v: vi=v+(f"({i})" if i else '')
    return s, j, vi, p, r['doi']
