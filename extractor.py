import math
import hashlib

class SS:


    def __init__(self,n,q,t):
        self.n=n
        self.q=q
        self.t=t
        self.b=2*t+1
        self.m=math.floor(math.log(q,self.b))
        self.k=math.ceil(n/self.m)

    def Gen(self,w):
        n=self.n
        q=self.q
        t=self.t
        b=self.b
        m=self.m
        k=self.k
        assert len(w)==n
       # print(n,q,t,b,m,k)
        s=[0 for i in range(k)]
        for i in range(n):
            s[i//m]=(s[i//m]+(w[i])*(b**(i%m)))%q
        return s

    def Rec(self,s,w_):
        n=self.n
        q=self.q
        t=self.t
        b=self.b
        m=self.m
        k=self.k
        Hw_=self.Gen(w_)
        eq=[]
        for i in range(k):
            eq.append((Hw_[i]-s[i])%q)
        #print(eq)
        e=[] 
        for x in eq:
            x=(x+t*(b**m-1)//(b-1))%q 
            for i in range(m):
                e.append(x%b-t)
                x//=b
        e=e[0:n]
        w=[]
        for i in range(n):
            w.append((w_[i]-e[i])%q)
        return w



class FuzzyExtractor:

    def __init__(self,n,q,t):
        self.ss=SS(n,q,t)
        

    def Ext(self,w): 
        P=self.ss.Gen(w)
        hash=hashlib.sha256()
        hash.update(str(w).encode())
        R=hash.digest()
        return (R,P)

    def Rep(self,P,w_): 
        w=self.ss.Rec(P,w_)
        hash=hashlib.sha256()
        hash.update(str(w).encode())
        R=hash.digest()
        return R

    def Err(self,P,w_): 
        w=self.ss.Rec(P,w_)
        s=0
        sw=0
        sw_=0
        for i in range(len(w)):
            s+=(w[i]*w_[i])
            sw+=w[i]**2
            sw_+=w_[i]**2
        return s/math.sqrt(sw)/math.sqrt(sw_)
