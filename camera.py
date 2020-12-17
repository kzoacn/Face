import face_recognition
import cv2
import numpy as np
#import extractor
import bw
import math
# This is a super simple (but slow) example of running face recognition on live video from your webcam.
# There's a second example that's a little more complicated but runs faster.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

name_list=['kaiyi','hongrui','jiangwen','jiangwu','liudehua','biden','yuyu']

known_face_encodings = []
known_face_names = []

def toZp(v,p):
    vec=[]
    for x in v:
        vec.append(math.floor(min(max(0,x+1),2)*p/2))
    return vec

n=128
p=2**31-1
t=math.floor(0.30*p/2)
q=(2*t+1)**(n+1)

#[-1,1] -> [0,q)
# eps -> q/2*eps

FE=bw.FuzzyExtractor(n,t)

helper=[]
randomness=[]


for name in name_list:
    image=face_recognition.load_image_file(name+'.jpg')
    face_encoding = face_recognition.face_encodings(image)[0]    
    R,P=FE.Ext(toZp(face_encoding,p)) 
    helper.append(P)
    randomness.append(R)

known_face_names = name_list


while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = frame[:, :, ::-1]

    # Find all the faces and face enqcodings in the frame of video
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Loop through each face in this frame of video
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)


        

        name = ''

        for i in range(len(randomness)):
            R=randomness[i]
            P=helper[i]
            w_=toZp(face_encoding,p)
            R_=FE.Rep(P,w_)
            if R==R_:
                print('Found '+name_list[i])
                print('Prob '+str(FE.Err(P,w_)))
                print(face_encoding[0:5])
                print(hex(hash(R)))
                name+=name_list[i]+','
        if name=='':
            name='Unknown'

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom + 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left , bottom +30), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
