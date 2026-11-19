import os,json
from urllib.request import urlopen,Request
U=os.getenv('MAKEFUN_ENV_URL','')
def api(path,data):
 return json.load(urlopen(Request(U+path,json.dumps(data).encode(),{'Content-Type':'application/json'}),timeout=30))
N=(-21,-19,-12,-8,8,12,19,21);B=(-11,-9,9,11);R=(-10,-1,1,10);Q=B+R
V=(0,100,325,335,515,950,0)
def ix(s):return (10-int(s[1]))*10+ord(s[0])-96
def setup(fen):
 b=[99]*120
 for i in range(21,99):
  if 0<i%10<9:b[i]=0
 r,c=2,1
 for p in fen.split()[0]:
  if p=='/':r+=1;c=1
  elif p.isdigit():c+=int(p)
  else:b[r*10+c]=(' PNBRQK'.index(p.upper()))*(1 if p.isupper() else -1);c+=1
 x=fen.split();return b,1 if x[1]=='w' else -1,sum({'K':1,'Q':2,'k':4,'q':8}.get(t,0) for t in x[2]),ix(x[3]) if x[3]!='-' else 0
def attack(b,k,s):
 for d in N:
  if b[k+d]==2*s:return True
 for ds,targets in ((B,(3*s,5*s)),(R,(4*s,5*s))):
  for d in ds:
   j=k+d
   while b[j]==0:j+=d
   if b[j] in targets:return True
 for d in Q:
  if b[k+d]==6*s:return True
 return b[k+9*s]==s or b[k+11*s]==s
def king(b,s):return b.index(6*s)
def moves(b,s,c,e,cap=0):
 out=[]
 for i in range(21,99):
  if not 0<i%10<9 or b[i]*s<=0:continue
  p=abs(b[i])
  if p==1:
   t=i-10*s
   if not cap and b[t]==0:
    if t//10 in (2,9):out.extend((i,t,q*s) for q in (5,4,3,2))
    else:
     out.append((i,t,0))
     z=t-10*s
     if i//10==(8 if s==1 else 3) and b[z]==0:out.append((i,z,0))
   for z in (t-1,t+1):
    if b[z]==99 or abs(b[z])==6 or not (b[z]*s<0 or z==e):continue
    if z//10 in (2,9):out.extend((i,z,q*s) for q in (5,4,3,2))
    else:out.append((i,z,0))
  else:
   for d in (N if p==2 else Q if p in (5,6) else B if p==3 else R):
    j=i+d
    while b[j]!=99 and b[j]*s<=0:
     if (not cap or b[j]*s<0) and abs(b[j])!=6:out.append((i,j,0))
     if b[j] or p in (2,6):break
     j+=d
  if p==6 and not cap and not attack(b,i,-s):
   for bit,rook,th,dst,empty in ((1,98,96,97,(96,97)),(2,91,94,93,(92,93,94))) if s==1 else ((4,28,26,27,(26,27)),(8,21,24,23,(22,23,24))):
    if c&bit and b[rook]==4*s and all(b[j]==0 for j in empty) and not attack(b,th,-s) and not attack(b,dst,-s):out.append((i,dst,0))
 return out
def make(b,s,c,e,m):
 f,t,p=m;z=b[:];pc=z[f];z[f]=0;z[t]=p or pc
 if abs(pc)==1 and t==e:z[t+10*s]=0
 if abs(pc)==6 and abs(t-f)==2:
  a,d=(f+3,f+1) if t>f else (f-4,f-1)
  z[d]=z[a];z[a]=0
 for j in (f,t):c&={98:14,91:13,95:12,28:11,21:7,25:3}.get(j,15)
 if abs(pc)==6:c&=12 if s==1 else 3
 e=(t+f)//2 if abs(pc)==1 and abs(t-f)==20 else 0
 return z,-s,c,e
nd=0
class Stop(Exception):pass
def ev(b,s):
 sc=0
 for i in range(21,99):
  if not 0<i%10<9:continue
  p=b[i]
  if not p:continue
  a=abs(p);j=i%10;k=i//10
  bn=int((7-abs(j-4.5)-abs(k-5.5))*(8 if a in (2,3) else 2))
  sc+=(V[a]+bn)*(1 if p>0 else -1)
 return sc*s
def search(b,s,c,e,d,alpha,beta,q=0):
 global nd
 nd+=1
 if nd>9000:raise Stop()
 incheck=attack(b,king(b,s),-s)
 if d<=0 and not incheck:
  stand=ev(b,s)
  if stand>=beta:return stand
  alpha=max(alpha,stand)
  if q>2:return alpha
 if d<=0 and q>=6:return ev(b,s)
 lst=moves(b,s,c,e,d<=0 and not incheck)
 lst.sort(key=lambda m:V[abs(b[m[1]])]+1000*(m[2]!=0)-V[abs(b[m[0]])]//12,reverse=True)
 seen=0
 for m in lst:
  nb,ns,nc,ne=make(b,s,c,e,m)
  if attack(nb,king(nb,s),-s):continue
  seen+=1
  sc=-search(nb,ns,nc,ne,d-1,-beta,-alpha,q+1 if d<=0 else 0)
  if sc>alpha:alpha=sc
  if alpha>=beta:break
 if not seen and (d>0 or incheck):return -28000+q if incheck else 0
 return alpha
def choose(fen,opts):
 global nd
 b,s,c,e=setup(fen);ans=opts[0]
 for dp in (1,2,3,4):
  nd=0;best=-30001;cand=ans
  try:
   lst=sorted(opts,key=lambda a:V[abs(b[ix(a[2:4])])],reverse=True)
   for mv in lst:
    f,t=ix(mv[:2]),ix(mv[2:4]);prom=((' nbrq'.index(mv[4])+1)*s) if len(mv)==5 else 0
    nb,ns,nc,ne=make(b,s,c,e,(f,t,prom))
    sc=-search(nb,ns,nc,ne,dp-1,-30000,-best)
    if sc>best:best=sc;cand=mv
  except Stop:break
  ans=cand
 return ans
if __name__=='__main__' and U:
 while True:
  g=api('/game',{})
  if g['status']=='done':break
  while g['status']=='your_move':g=api('/move',{'game':g['game'],'move':choose(g['fen'],g['legal_moves'])})
