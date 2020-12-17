import face_recognition
import numpy as np
import extractor
import math
import os
import csv

face_list=[]
di=os.listdir('../CASIA')
for s in di:
    if s[-4:]=='.bmp':
        face_list.append(s)
vec=[]
cnt=0

print(len(face_list))

name=[]
for f in face_list:
    face=face_recognition.load_image_file('../CASIA/'+f)
    features=face_recognition.api.face_encodings(face)
    if len(features)==0:
        continue
    feature=features[0]
    #print(feature)
    name.append(f[:-4])
    vec.append(feature)
    cnt+=1
    print(cnt)

with open('caisa','w') as f:
    for i in range(len(vec)):
        f.write(name[i]+' ')
        for x in vec[i]:
            f.write(str(x)+' ')
        f.write('\n')