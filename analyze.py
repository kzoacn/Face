import os 
import numpy as np 
import math
import bw
d=os.listdir('./lfw')



name_list=[]
for f in d:
    if f[-4:]=='.jpg':
        name_list.append(f[0:-4])

fin=open('vec','r')

def toZp(v,p):
    vec=[]
    for x in v:
        vec.append(math.floor(min(max(0,x+1),2)*p/2))
    return vec

n=128
p=2**31-1
t=math.floor(0.53*p/2)

#[-1,1] -> [0,q)
# eps -> q/2*eps

FE=bw.FuzzyExtractor(n,t)

helper=[]
randomness=[]


f=fin.readlines()

#f=f[:100]

name_list=[]
vec=[]
cnt=0
for l in f:
    v=l.split()
    name=v[0]
    vv=toZp([float(x) for x in v[1:129]],p)
    R,P=FE.Ext(vv)
    name_list.append(name)
    vec.append(vv)
    helper.append(P)
    randomness.append(R)
    cnt+=1
    print(cnt,len(f))

#print(name_list)


allyes=0
allno=0
falseN=0
falseP=0

cnt=0

n=len(name_list)

for i in range(len(name_list)):
    for j in range(i+1,len(name_list)):
        flag=False
        if name_list[i][:-4]==name_list[j][:-4]:
            flag=True
            allyes+=1
        else:
            flag=False
            allno+=1

        R_=FE.Rep(helper[i],vec[j])
        if randomness[i]==R_:
            if not flag:
                falseP+=1
        else:
            if flag:
                falseN+=1
        cnt+=1
        if cnt%100==0 and allno>0 and allyes>0:
            print(cnt/(n*(n-1)/2)*100,falseP/allno*100,falseN/allyes*100)


"""
fout=open('vec','w')
cnt=0
for name in name_list:
    cnt+=1
    face=face_recognition.load_image_file('./lfw/'+name+'.jpg')
    reg=face_recognition.api.face_encodings(face)
    if len(reg)==0:
        continue
    vec=reg[0]

    fout.write(name+' ')
    for v in vec:
        fout.write(str(v)+' ')
    fout.write('\n')
    print(str(cnt)+'/'+str(len(name_list)))
"""
