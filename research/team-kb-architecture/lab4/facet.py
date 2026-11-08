import sys,os
sys.path.insert(0,os.path.dirname(__file__))
import numpy as np, corpus, queries, evalret as ev
u=corpus.build("L",ev.ALIAS); idx=ev.Index(u,True); by={x['uid']:x for x in u}
subj={}
for x in u:
    if x['kind']=='claim': subj.setdefault(x['subject'],[]).append(x['uid'])
for qid,qt,qtext,gold,stale in queries.Q:
    if qt!='M': continue
    for cfg in (("hybb",1),("hybb",1)):
        pass
    rk=ev.ranks(idx,idx.scores("hybb",qtext,ev.QX[qid]))
    top=rk[:8]; r0=len(set(top)&gold)/len(gold)
    topc=[t for t in rk[:5] if by[t]['kind']=='claim']
    ex=set(topc)
    for t in topc: ex|=set(subj[by[t]['subject']])
    r1=len(ex&gold)/len(gold)
    print(qid,qtext,f"rec@8={r0:.2f}  top5 後依 subject 展開 recall={r1:.2f} (展開後 {len(ex)} 條,gold {len(gold)})")
