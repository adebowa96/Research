import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
NAVY='#0A254E'; RED='#A31F34'; INK='#1F2937'; PALE='#EEF2F8'; PINK='#FDECEE'
plt.rcParams.update({'font.family':'Liberation Serif','font.size':10})
# Figure 1 PRISMA
fig,ax=plt.subplots(figsize=(7,7)); ax.set_xlim(0,10); ax.set_ylim(1.2,10.2); ax.axis('off')
def box(x,y,w,h,txt,fc=PALE,ec=NAVY,fs=10):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.02,rounding_size=0.12',fc=fc,ec=ec,lw=1.2))
    ax.text(x+w/2,y+h/2,txt,ha='center',va='center',fontsize=fs,color=INK,linespacing=1.3)
def arr(x1,y1,x2,y2): ax.annotate('',xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle='-|>',color=NAVY,lw=1.3))
for y,l in [(8.9,'Identification'),(6.9,'Screening'),(4.8,'Eligibility'),(2.6,'Included')]:
    ax.text(0.3,y,l,rotation=90,ha='center',va='center',fontsize=11,fontweight='bold',color=NAVY)
X,W=0.7,5.1; RX,RW=6.25,3.65
box(X,8.2,W,1.4,'Records identified through database searching\n(PubMed/MEDLINE, CINAHL, APA PsycInfo,\nAPA PsycArticles, Cochrane Library)\nn = 1,943')
box(RX,8.45,RW,0.9,'Duplicates removed\nn = 325',fc=PINK,ec=RED)
arr(X+W,8.9,RX,8.9); arr(X+W/2,8.2,X+W/2,7.4)
box(X,6.5,W,0.9,'Records screened (title and abstract)\nn = 1,618')
box(RX,6.0,RW,1.9,'Records excluded\nn = 1,554\nNot PMDD-focused or no\npsychosocial or coping aim;\nreview, intervention, animal\nor laboratory study',fc=PINK,ec=RED)
arr(X+W,6.95,RX,6.95); arr(X+W/2,6.5,X+W/2,5.3)
box(X,4.2,W,1.1,'Records assessed for eligibility\n(title and abstract)\nn = 64')
box(RX,4.2,RW,1.1,'Records excluded\nn = 20\nDid not meet inclusion criteria',fc=PINK,ec=RED)
arr(X+W,4.75,RX,4.75); arr(X+W/2,4.2,X+W/2,3.05)
box(X,2.15,W,0.9,'Studies included in the scoping review\nn = 44',fc='#D9E2F3')
plt.savefig('ms/figure1_prisma.png',dpi=300,bbox_inches='tight',facecolor='white')
# Figure 2 outcomes
D=[('Depression',39),('Psychological distress',24),('Interpersonal functioning',18),('Suicidal ideation or self-harm',14),('Quality of life',14),('Coping mechanisms',3)]
fig,ax=plt.subplots(figsize=(7,3.6))
lab=[d[0] for d in D][::-1]; val=[d[1] for d in D][::-1]
bars=ax.barh(lab,val,color=[RED]+[NAVY]*5,height=0.62)
for b,v in zip(bars,val): ax.text(v+0.6,b.get_y()+b.get_height()/2,str(v),va='center',fontsize=10,fontweight='bold',color=INK)
ax.set_xlim(0,44); ax.set_xlabel('Number of studies (n = 44; categories not mutually exclusive)',color=INK)
for s in ['top','right']: ax.spines[s].set_visible(False)
ax.spines['left'].set_color('#9CA3AF'); ax.spines['bottom'].set_color('#9CA3AF'); ax.tick_params(colors=INK,length=0)
plt.tight_layout(); plt.savefig('ms/figure2_outcomes.png',dpi=300,facecolor='white')
# Figure 3 period
fig,ax=plt.subplots(figsize=(6,3))
P=['2010–2013','2014–2017','2018–2021','2022–2025']; V=[6,6,5,27]
bars=ax.bar(P,V,color=[NAVY]*3+[RED],width=0.6)
for b,v in zip(bars,V): ax.text(b.get_x()+b.get_width()/2,v+0.6,str(v),ha='center',fontsize=10,fontweight='bold',color=INK)
ax.set_ylim(0,31); ax.set_ylabel('Number of studies',color=INK); ax.set_xlabel('Publication period',color=INK)
for s in ['top','right']: ax.spines[s].set_visible(False)
ax.spines['left'].set_color('#9CA3AF'); ax.spines['bottom'].set_color('#9CA3AF'); ax.tick_params(colors=INK,length=0)
plt.tight_layout(); plt.savefig('ms/figure3_period.png',dpi=300,facecolor='white')
