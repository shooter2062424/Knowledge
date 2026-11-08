"""量化小實驗(numpy):①尺子與離群值(整張表一把尺 vs 每 32 個一組)②玩具 MLP 上 PTQ vs QAT(STE)。

用法:python q.py。只用 numpy;玩具資料,結果只示範機制,不可外推到 LLM。
"""
import numpy as np
rng=np.random.default_rng(0)
# ① 離群值
n=1_200_000
w=rng.laplace(0,0.01/np.sqrt(2),n); w[0]=0.21
def mm_quant(x,bits):  # 非對稱 min-max,2^bits 個刻度
    lo,hi=x.min(),x.max(); L=2**bits-1; s=(hi-lo)/L
    return np.round((x-lo)/s)*s+lo
def group_quant(x,bits,g=32):
    x=x[:len(x)//g*g].reshape(-1,g); lo=x.min(1,keepdims=True); hi=x.max(1,keepdims=True); L=2**bits-1
    s=np.where(hi>lo,(hi-lo)/L,1); return (np.round((x-lo)/s)*s+lo).ravel()
for name,q in (("整張表一把尺 4bit",mm_quant(w,4)),("每32個一組 4bit",group_quant(w,4))):
    x=w[:len(q)]
    vals,cnt=np.unique(np.round(q,7),return_counts=True); modal=cnt.max()/len(q)
    # 「變 0」:量化後與零的距離小於半個原始標準差且原值非零→看被壓成同一個值的比例
    uniq=len(np.unique(np.round(q,6)))
    print(f"{name}: 均方誤差 {np.mean((x-q)**2):.2e}, 最常出現的單一值佔 {modal:.1%}, 不同值個數 {uniq}")
# ② 玩具 MLP:PTQ vs QAT
def make(seed,d=64,k=10,N=6000,noise_seed=0):
    """合成 10 類高斯混合:類別中心由 seed 決定,噪聲由 noise_seed 決定(訓練與測試用不同噪聲)。"""
    C=np.random.default_rng(seed).normal(0,1.0,(k,d)); r=np.random.default_rng(10_000*noise_seed+seed)
    y=r.integers(0,k,N); return C[y]+r.normal(0,2.2,(N,d)),y
def init(seed,sizes):
    r=np.random.default_rng(seed); return [r.normal(0,np.sqrt(2/a),(a,b)) for a,b in zip(sizes[:-1],sizes[1:])]
def q_w(W,bits,g=32,tern=False):
    shp=W.shape; x=W.reshape(-1,g)
    if tern:
        s=np.abs(x).mean(1,keepdims=True)+1e-8; return (np.clip(np.round(x/s),-1,1)*s).reshape(shp)
    L=2**(bits-1)-1; s=np.abs(x).max(1,keepdims=True)/L+1e-12; return (np.clip(np.round(x/s),-L,L)*s).reshape(shp)
def fwd(Ws,X,qf):
    hs=[X]; h=X
    for i,W in enumerate(Ws):
        Wq=qf(W); h=h@Wq
        if i<len(Ws)-1: h=np.maximum(h,0)
        hs.append(h)
    return hs
def acc(Ws,X,y,qf): return np.mean(np.argmax(fwd(Ws,X,qf)[-1],1)==y)
def train(Ws,X,y,qf,ep,lr,seed=0):
    r=np.random.default_rng(seed); N=len(X)
    for e in range(ep):
        idx=r.permutation(N)
        for b in range(0,N,128):
            xb,yb=X[idx[b:b+128]],y[idx[b:b+128]]
            Wq=[qf(W) for W in Ws]; hs=[xb]; h=xb
            for i,W in enumerate(Wq):
                h=h@W
                if i<len(Wq)-1: h=np.maximum(h,0)
                hs.append(h)
            p=np.exp(hs[-1]-hs[-1].max(1,keepdims=True)); p/=p.sum(1,keepdims=True); p[np.arange(len(yb)),yb]-=1; g=p/len(yb)
            for i in range(len(Ws)-1,-1,-1):
                gW=hs[i].T@g           # STE:對量化後權重的梯度直接當作對浮點權重的梯度
                if i>0: g=(g@Wq[i].T)*(hs[i]>0)
                Ws[i]-=lr*gW
    return Ws
ident=lambda W:W
sizes=[64,256,256,10]
rows=[]
for seed in range(5):
    X,y=make(seed); Xt,yt=make(seed,noise_seed=1)
    base=train(init(seed,sizes),X,y,ident,20,0.01,seed)
    res={"fp":acc(base,Xt,yt,ident)}
    for name,qf in (("4bit",lambda W:q_w(W,4)),("3bit",lambda W:q_w(W,3)),("2bit",lambda W:q_w(W,2)),("ternary",lambda W:q_w(W,2,tern=True))):
        res["PTQ "+name]=acc(base,Xt,yt,qf)
        qat=train([W.copy() for W in base],X,y,qf,8,0.005,seed)   # 從 FP 權重繼續訓練,前向用量化
        res["QAT "+name]=acc(qat,Xt,yt,qf)
    rows.append(res)
keys=list(rows[0])
print("玩具 MLP(5 個種子平均,測試準確率;隨機猜 10%)")
for k in keys: print(f"{k:14s} {np.mean([r[k] for r in rows]):.3f} ± {np.std([r[k] for r in rows]):.3f}")
