import face_recognition
import numpy as np
import extractor
import math

vec=[]


name_list=['kaiyi','hongrui','jiangwen','jiangwu','liudehua','biden']


face=face_recognition.load_image_file('./lixiaolong.jpeg')
vec.append(face_recognition.api.face_encodings(face)[0])

for name in name_list:
    face=face_recognition.load_image_file('./'+name+'.jpg')
    vec.append(face_recognition.api.face_encodings(face)[0])



 
def toZp(v,p):
    vec=[]
    for x in v:
        vec.append(math.floor(min(max(0,x+1),2)*p/2))
    return vec

n=len(vec[0])
p=2**31-1
t=math.floor(0.11*p/2)
q=(2*t+1)**(n+1)

#[-1,1] -> [0,q)
# eps -> q/2*eps

FE=extractor.FuzzyExtractor(n,q,t)

R,P=FE.Ext(toZp(vec[0],p))
print(n,t,len(P))
print(n*math.log(p,2),math.log(q,2))

print(R)

for v in vec:
    R_=FE.Rep(P,toZp(v,p))
    print(R==R_,max(abs(v-vec[0])),np.linalg.norm(v-vec[0]),np.dot(v-vec[0],v-vec[0]))
#    print(max(abs(v-vec[0])))


