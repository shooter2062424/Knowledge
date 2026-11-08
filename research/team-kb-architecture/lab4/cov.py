import sys,os,pickle
sys.path.insert(0,os.path.dirname(__file__))
import numpy as np, corpus, queries, evalret as ev
res={}
for sc in "SML":
    u0=corpus.build(sc,ev.ALIAS); idx={0:ev.Index(u0,False),1:ev.Index(u0,True)}
    for m in ("grep","bm25b","bm25c","hybb","hybc"):
        for a in (0,1):
            for x in (0,1):
                if m=="grep" and (a or x): continue
                h5=[];mrr=[];g=[]
                for qid,qt,qtext,gold,stale in queries.Q:
                    sc_=idx[a].scores(m,qtext,ev.QX[qid] if x else None)
                    rk=ev.ranks(idx[a],sc_); met=ev.metrics(rk,ev.gold_expand(u0,gold),gold,stale)
                    h5.append(met['h5']);mrr.append(met['mrr'])
                    if qt=='G': g.append(met['h5'])
                print(sc,m,'alias' if a else '-','qx' if x else '-',f"h5={np.mean(h5):.2f} mrr={np.mean(mrr):.2f} G={np.mean(g):.2f}")
