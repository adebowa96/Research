s=open('poster_final.py').read()
def rep(a,b):
    global s
    assert a in s, a[:80]; s=s.replace(a,b)
def repblock(start,end,new):
    global s
    i=s.index(start); j=s.index(end,i); s=s[:i]+new+s[j:]
repblock("header(LX,0.806,LW,0.199,'Abstract')","header(LX,2.62",'''header(LX,0.806,LW,0.199,'Abstract')
body(LX,1.03,LW,1.52,[
 [('Background: ',True,False),('Premenstrual dysphoric disorder (PMDD) is a DSM-5 depressive disorder affecting an estimated 31 million women and girls worldwide.¹ This scoping review examined psychosocial outcomes and coping mechanisms among women with PMDD and assessed the geographic distribution of the evidence.',False,False)],
 [('Methods: ',True,False),("Following Arksey and O’Malley’s framework and PRISMA-ScR guidance, we searched PubMed/MEDLINE, CINAHL, APA PsycInfo, APA PsycArticles and the Cochrane Library for peer-reviewed studies published 2010–2025. Eligible empirical and qualitative studies had PMDD as the primary population and at least one psychosocial outcome or coping mechanism as a primary aim.",False,False)],
 [('Results: ',True,False),("The search identified 1,943 records; 1,618 remained after deduplication and 44 studies met the inclusion criteria. Depression was most documented (n=39), followed by psychological distress (n=24), interpersonal functioning (n=18), suicidal ideation or self-harm (n=14) and quality of life (n=14). Only three studies examined coping mechanisms. Three studies (6.8%) originated from low- and middle-income countries (LMICs), including one from Nigeria.",False,False)],
 [('Conclusions: ',True,False),('Evidence on PMDD’s psychosocial burden is growing but geographically concentrated in high-income countries, revealing a critical LMIC evidence gap.',False,False)],
 [('Keywords: ',True,False),('premenstrual dysphoric disorder; psychosocial outcomes; coping mechanisms; LMICs; scoping review',False,True)]],size=4.35,align=PP_ALIGN.JUSTIFY,space=1.4)
''')
repblock("rows=[('Study Design'","top=4.69",'''rows=[('Study Design','Scoping review guided by Arksey and O’Malley’s framework³ and reported using PRISMA-ScR.⁴'),
('Databases','PubMed/MEDLINE, CINAHL, APA PsycInfo, APA PsycArticles and Cochrane Library.'),
('Publication Years','2010–2025.'),
('Inclusion Criteria','Peer-reviewed empirical or qualitative studies with PMDD as the primary population and at least one psychosocial outcome or coping mechanism as a primary aim.'),
('Exclusion Criteria','Animal studies, laboratory research, reviews, interventions and non-peer-reviewed publications.'),
('Screening Process','1,943 records identified; 325 duplicates removed; 1,618 titles and abstracts screened; 64 full-text articles assessed; 44 studies included.'),
('Evidence Mapping','Included studies categorized by psychosocial outcome, coping mechanism and geographic setting (country and income level).')]
''')
rep("""tiles=[(f"{P['identified_total']:,}",'records identified','across 7 databases',NAVY),(str(P['included']),'studies included','in the scoping review',NAVY),
       ('7','studies addressing coping','8.2% of 85',RED),('3','studies from sub-Saharan Africa','3.5% of 85',RED)]""",
"""tiles=[('1,943','records identified','across 5 databases',NAVY),('44','studies included','in the scoping review',NAVY),
       ('3','studies addressing coping','6.8% of 44',RED),('3','studies from LMICs','6.8% of 44',RED)]""")
repblock("rowsY=[","# inclusion criteria box",'''rowsY=[(1.98,0.4,'Identification'),(2.46,0.36,'De-duplication'),(2.9,0.4,'Screening'),(3.38,0.4,'Eligibility'),(3.86,0.4,'Included')]
for y,h,l in rowsY: stage(y,h,l)
pbox(bx,1.98,bw,0.4,['Records identified via database search','PubMed/MEDLINE · CINAHL · APA PsycInfo','APA PsycArticles · Cochrane Library','n = 1,943'],size=3.3)
arrow(bx+bw/2,2.38,bx+bw/2,2.46)
pbox(bx,2.46,bw,0.36,['Records after duplicate removal','325 duplicates removed','n = 1,618'],size=3.6)
arrow(bx+bw/2,2.82,bx+bw/2,2.9)
pbox(bx,2.9,bw,0.4,['Records screened','(title and abstract)','n = 1,618'],size=3.6)
pbox(rx,2.9,rw,0.4,['Excluded (n = 1,554)','Not PMDD-focused or no psychosocial/','coping aim; review, intervention,','animal or laboratory study'],fill=RGBColor(0xFD,0xEC,0xEE),line=RED,size=3.2)
arrow(bx+bw,3.1,rx,3.1)
arrow(bx+bw/2,3.3,bx+bw/2,3.38)
pbox(bx,3.38,bw,0.4,['Full-text articles assessed','for eligibility','n = 64'],size=3.6)
pbox(rx,3.38,rw,0.4,['Excluded (n = 20)','Did not meet inclusion','criteria at full text'],fill=RGBColor(0xFD,0xEC,0xEE),line=RED,size=3.3)
arrow(bx+bw,3.58,rx,3.58)
arrow(bx+bw/2,3.78,bx+bw/2,3.86)
pbox(bx,3.86,bw,0.4,['Studies included in','the scoping review','n = 44'],fill=RGBColor(0xD9,0xE2,0xF3),line=NAVY,size=4.2)
''')
repblock("D=sorted(S['domains']","write(tb(dx,4.82",'''D=[('Coping mechanisms',3),('Quality of life',14),('Suicidal ideation or self-harm',14),('Interpersonal functioning',18),('Psychological distress',24),('Depression',39)]
cd=CategoryChartData(); cd.categories=[k for k,_ in D]; cd.add_series('Studies',[v for _,v in D])
def style(ch,size,maxv):
    ch.has_title=False; ch.has_legend=False; ch.font.name=FONT; ch.font.size=Pt(size); ch.font.color.rgb=INK
    pl=ch.plots[0]; pl.gap_width=45; pl.has_data_labels=True; dl=pl.data_labels; dl.font.size=Pt(size); dl.font.bold=True; dl.font.name=FONT; dl.position=XL_LABEL_POSITION.OUTSIDE_END
    ser=pl.series[0]; ser.format.fill.solid(); ser.format.fill.fore_color.rgb=NAVY
    va=ch.value_axis; va.visible=False; va.has_major_gridlines=False; va.maximum_scale=maxv; va.minimum_scale=0
    ca=ch.category_axis; ca.tick_labels.font.size=Pt(size); ca.format.line.color.rgb=GRAY
    return ser
gf=s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED,Inches(dx),Inches(1.98),Inches(2.45),Inches(2.85),cd); ser=style(gf.chart,4.6,44)
pt=ser.points[0]; pt.format.fill.solid(); pt.format.fill.fore_color.rgb=RED
''')
rep("ib=tb(fx,4.33,2.47,0.62","ib=tb(fx,4.38,2.47,0.6")
rep("('Fig 2. Included Studies Reporting Each Outcome (of 85)',True,False)","('Fig 2. Included Studies Reporting Each Outcome (of 44)',True,False)")
repblock("# --- Fig 3 region ---","# ---------------- RIGHT COLUMN",'''# --- Fig 3 geography ---
gy=5.07
write(tb(fx,gy,5.0,0.16),[[('Fig 3. Geographic Setting of the 44 Included Studies',True,False)]],size=5.2,color=NAVY)
cd=CategoryChartData(); cd.categories=['High-income / other settings','Low- and middle-income countries']; cd.add_series('Studies',[41,3])
gf=s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED,Inches(fx),Inches(gy+0.25),Inches(2.9),Inches(1.2),cd); ser=style(gf.chart,5,48)
p_=ser.points[1]; p_.format.fill.solid(); p_.format.fill.fore_color.rgb=RED
call=tb(5.7,gy+0.3,1.9,1.1,fill=PALE,line=RED,shape=MSO_SHAPE.ROUNDED_RECTANGLE,anchor=MSO_ANCHOR.MIDDLE,lw=0.6)
write(call,[{'runs':[('6.8%',True,False,RED)],'size':20,'align':PP_ALIGN.CENTER,'space':0},{'runs':[('of included studies came from LMICs',False,False)],'size':5.5,'align':PP_ALIGN.CENTER,'space':1},{'runs':[('Sub-Saharan Africa: 1 study (Nigeria)',True,False,RED)],'size':5.5,'align':PP_ALIGN.CENTER,'space':0}])
write(tb(fx,6.55,5.0,0.5),[{'runs':[('41 of 44 studies (93.2%) were conducted in high-income or other non-LMIC settings; 3 (6.8%) came from LMICs, only one of them from sub-Saharan Africa. Evidence on PMDD’s psychosocial burden therefore reflects mainly high-income contexts.',False,True)],'align':PP_ALIGN.CENTER}],size=4.2,color=MUTED)
''')
repblock(" [('Results',True,False)],"," [('Limitations',True,False)],",''' [('Results',True,False)],
 "The database search identified 1,943 records. After 325 duplicates were removed, 1,618 records were screened by title and abstract; 64 articles underwent full-text assessment, 20 were excluded, and 44 studies were included (Fig. 1).",
 "Depression was the most documented outcome (n=39), followed by psychological distress (n=24), interpersonal functioning (n=18), suicidal ideation or self-harm (n=14) and quality of life (n=14). Only three studies examined coping mechanisms (Fig. 2).",
 "Geographic representation was critically skewed: three of the 44 studies (6.8%) originated from LMICs, including one from Nigeria, the only study from sub-Saharan Africa (Fig. 3).",
 [('Discussion',True,False)],
 "PMDD research consistently documents depression, distress, relationship difficulties and suicidality; large studies have linked PMDD with suicidal ideation and attempts.⁵,⁶ Yet coping mechanisms remain largely unexamined, and the near-absence of LMIC and African studies leaves the burden in these settings invisible to health systems.",
 [('Conclusion',True,False)],
 "Evidence on PMDD’s psychosocial burden is growing but geographically concentrated in high-income countries. Findings call for culturally responsive screening, integrated mental and reproductive health services, and Africa-centred research investment.",
''')
repblock(" B([('Screening stage: '"," B([('Coding overlap: '",''' B([('Search scope: ',True,False),('studies outside the five databases or the 2010–2025 period may have been missed.',False,False)]),
 B([('Study differences: ',True,False),('variation in design and outcome definitions limits direct comparison.',False,False)]),
''')
rep("('studies can address several domains, so counts should not be summed.',False,False)])],size=4.5","('a study could address more than one outcome, so counts should not be summed.',False,False)]),\n B([('Geographic coverage: ',True,False),('few LMIC studies limit conclusions about those settings.',False,False)])],size=4.6")
open('poster_abstract.py','w').write(s)
