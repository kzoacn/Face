import math
import hashlib


class BW:
    @staticmethod
    def add(v1,v2):
        v=[]
        for i in range(len(v1)):
            v.append(v1[i]+v2[i])
        return v
    @staticmethod
    def sub(v1,v2):
        v=[]
        for i in range(len(v1)):
            v.append(v1[i]-v2[i])
        return v
    @staticmethod
    def dis(v1,v2):
        s=0
        for i in range(len(v1)):
            s+=(v1[i]-v2[i])*(v1[i]-v2[i])
        return math.sqrt(s)
    @staticmethod
    def rot(y,t):
        x=[]
        if t==-1:
            for i in range(0,len(y),2):
                x.append((y[i]+y[i+1])/2)
                x.append((y[i]-y[i+1])/2)
        else:
            for i in range(0,len(y),2):
                x.append(y[i]+y[i+1])
                x.append(y[i]-y[i+1])
        return x


    @staticmethod
    def round(x,t):
        x=round(x)
        if x%t < t/2:
            return x-x%t
        else:
            return x-x%t+t

    @staticmethod
    def decode(y,t):
        n=len(y)
        x=[]
        if n==2:
            x.append(BW.round(y[0],t))
            x.append(BW.round(y[1],t))
            return x
        y1=y[0:n//2]
        y2=y[n//2:n]
        u1=BW.decode(y1,t)
        u2=BW.decode(y2,t)

        v1=BW.rot(BW.decode(BW.rot(BW.sub(y1,u2),-1),t),1)
        v2=BW.rot(BW.decode(BW.rot(BW.sub(y2,u1),-1),t),1)

        x1=u1+BW.add(u1,v2)
        x2=BW.add(u2,v1)+u2

        if BW.dis(x1,y) < BW.dis(x2,y):
            return x1
        else:
            return x2

class SS:

    def __init__(self,n,t):
        self.n=n
        self.t=t
        self.scale=int(t/(math.sqrt(n)/2)+1)

    def Gen(self,w):
        v=BW.decode(w,self.scale)
        e=BW.sub(v,w)
        return e

    def Rec(self,s,w_):
        w=BW.sub(BW.decode(BW.add(w_,s),self.scale),s)
        return w

    def Err(self,s,w_):
        w=BW.sub(BW.decode(BW.add(w_,s),self.scale),s)
        return BW.dis(w,w_)/self.scale

class FuzzyExtractor:

    def __init__(self,n,t):
        self.ss=SS(n,t)
        
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
        return self.ss.Err(P,w_)
