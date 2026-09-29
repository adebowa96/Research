import json, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
plt.rcParams.update({'font.family':'Liberation Sans','font.size':10})
S=json.load(open('stats.json')); G=json.load(open('prisma_groups.json')); P=S['prisma']
NAVY='#0A254E'; INK='#1F2937'; MUTED='#6B7280'; GRID='#E5E7EB'; ACC='#C2410C'
# ---------- Figure 1 PRISMA-ScR ----------
fig,ax=plt.subplots(figsize=(8.5,8.4)); ax.set_xlim(0,100); ax.set_ylim(26,120); ax.axis('off')
def box(x,y,w,h,txt,fc='#FFFFFF',ec=NAVY,fs=9.5,bold=False,align='center'):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.4,rounding_size=1.2',fc=fc,ec=ec,lw=1.4))
    ax.text(x+(w/2 if align=='center' else 1.5),y+h/2,txt,ha=align,va='center',fontsize=fs,color=INK,fontweight='bold' if bold else 'normal',wrap=True,linespacing=1.35)
def arrow(x1,y1,x2,y2): ax.annotate('',xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle='-|>',color=NAVY,lw=1.4))
for y,lab in [(100,'Identification'),(60,'Screening'),(30,'Included')]:
    ax.add_patch(FancyBboxPatch((0,y),7,16 if lab!='Screening' else 36,boxstyle='round,pad=0.3,rounding_size=1',fc=NAVY,ec=NAVY))
    ax.text(3.5,y+(8 if lab!='Screening' else 18),lab,rotation=90,ha='center',va='center',color='white',fontweight='bold',fontsize=10)
dbs=P['identified_by_database']
dbtxt='\n'.join(f'{k}: {v:,}' for k,v in dbs.items())
box(11,100,40,16,f"Records identified from databases\n(n = {P['identified_total']:,})",bold=True)
box(56,97,42,22,dbtxt,fs=8,align='left',fc='#F3F4F6',ec='#9CA3AF')
arrow(31,100,31,92)
box(11,82,40,10,f"Records after duplicates removed\n(n = {P['screened']:,})")
box(56,84,42,8,f"Duplicates removed (n = {P['duplicates_removed']:,})",fs=9,fc='#F3F4F6',ec='#9CA3AF')
arrow(51,87,56,88)
arrow(31,82,31,74)
box(11,62,40,12,f"Records screened\n(title, abstract, subject terms)\n(n = {P['screened']:,})")
ex=sorted(G.items(),key=lambda x:-x[1])
short={'PMDD not the primary study population':'PMDD not the primary population',
 'Published outside 2010–2025':'Published outside 2010–2025',
 'Reviews, meta-analyses, guidelines, commentaries':'Reviews, guidelines, commentaries',
 'Other ineligible publication types (books, chapters, dissertations, letters, editorials, case reports, conference abstracts)':'Other ineligible publication types*',
 'Non-English full text':'Non-English',
 'Intervention or treatment study':'Intervention/treatment studies',
 'Laboratory/biological study':'Laboratory/biological studies',
 'No psychosocial outcome or coping mechanism as a primary aim':'No psychosocial/coping primary aim',
 'Instrument development/validation study':'Instrument validation studies',
 'Animal study':'Animal studies'}
extxt=f"Records excluded (n = {P['excluded_total']:,})\n"+'\n'.join(f'• {short[k]}: {v}' for k,v in ex)
box(56,52,42,28,extxt,fs=8.3,align='left',fc='#FEF2F2',ec='#B91C1C')
arrow(51,68,56,68)
arrow(31,62,31,46)
box(11,30,40,16,f"Studies included in the\nscoping review\n(n = {P['included']})",fc='#ECFDF5',ec='#047857',bold=True,fs=11)
ax.text(56,46,'*Books, chapters, dissertations, letters,\neditorials, case reports, conference abstracts.\n\nEligibility judged on title, abstract and subject\nterms; full-text verification pending.',fontsize=7.5,color=MUTED,va='top')
ax.set_title('Figure 1. PRISMA-ScR flow of records',loc='left',fontsize=12,fontweight='bold',color=INK)
fig.savefig('fig1_prisma.png',dpi=300,bbox_inches='tight'); plt.close(fig)
# ---------- Figure 2 domains ----------
D=sorted(S['domains'].items(),key=lambda x:x[1])
fig,ax=plt.subplots(figsize=(8,5.6))
y=range(len(D)); ax.barh(list(y),[v for _,v in D],color=NAVY,height=0.62)
ax.set_yticks(list(y)); ax.set_yticklabels([k for k,_ in D],color=INK)
for i,(k,v) in enumerate(D): ax.text(v+0.4,i,f'{v} ({100*v/85:.0f}%)',va='center',fontsize=9,color=INK)
ax.set_xlim(0,34); ax.xaxis.grid(True,color=GRID); ax.set_axisbelow(True)
for s in ['top','right','left']: ax.spines[s].set_visible(False)
ax.spines['bottom'].set_color('#9CA3AF'); ax.tick_params(axis='y',length=0); ax.tick_params(axis='x',colors=MUTED)
ax.set_xlabel('Number of included studies (n = 85; studies can map to more than one domain)',color=MUTED)
ax.set_title('Figure 2. Psychosocial domains examined in PMDD studies',loc='left',fontsize=12,fontweight='bold',color=INK)
fig.savefig('fig2_domains.png',dpi=300,bbox_inches='tight'); plt.close(fig)
# ---------- Figure 3 geography ----------
order=['High income','Upper-middle income','Lower-middle income','Low income','Not classifiable (online/multinational/not reported)']
lab={'Not classifiable (online/multinational/not reported)':'Online /\nmultinational /\nnot reported'}
inc=S['income']
fig,(a1,a2)=plt.subplots(1,2,figsize=(11,4.6),gridspec_kw=dict(width_ratios=[1,1.15]))
vals=[inc.get(k,0) for k in order]; cols=[NAVY,ACC,ACC,ACC,'#9CA3AF']
a1.bar(range(len(order)),vals,color=cols,width=0.62)
a1.set_xticks(range(len(order))); a1.set_xticklabels([lab.get(k,k.replace(' income','\nincome')) for k in order],fontsize=8.5,color=INK)
for i,v in enumerate(vals): a1.text(i,v+0.8,f'{v} ({100*v/85:.0f}%)',ha='center',fontsize=9,color=INK)
a1.set_ylim(0,66); a1.yaxis.grid(True,color=GRID); a1.set_axisbelow(True)
for s in ['top','right','left']: a1.spines[s].set_visible(False)
a1.tick_params(axis='y',colors=MUTED,length=0); a1.tick_params(axis='x',length=0)
a1.set_title('A. World Bank income group (FY2027)',loc='left',fontsize=10.5,fontweight='bold',color=INK)
R=sorted(S['region'].items(),key=lambda x:x[1])
Rl={'Europe & Central Asia':'Europe & Central Asia\n(incl. Türkiye)','Online / multinational / not reported':'Online / multinational / NR'}
a2.barh(range(len(R)),[v for _,v in R],color=[ACC if k=='Sub-Saharan Africa' else NAVY for k,_ in R],height=0.62)
a2.set_yticks(range(len(R))); a2.set_yticklabels([Rl.get(k,k) for k,_ in R],fontsize=9,color=INK)
for i,(k,v) in enumerate(R): a2.text(v+0.3,i,str(v),va='center',fontsize=9,color=INK)
a2.set_xlim(0,33); a2.xaxis.grid(True,color=GRID); a2.set_axisbelow(True)
for s in ['top','right','left']: a2.spines[s].set_visible(False)
a2.tick_params(axis='y',length=0); a2.tick_params(axis='x',colors=MUTED)
a2.set_title('B. Region of study setting',loc='left',fontsize=10.5,fontweight='bold',color=INK)
fig.suptitle('Figure 3. Geographic distribution of included studies (n = 85)',x=0.01,ha='left',fontsize=12,fontweight='bold',color=INK)
fig.tight_layout(); fig.savefig('fig3_geography.png',dpi=300,bbox_inches='tight'); plt.close(fig)
print('ok')
