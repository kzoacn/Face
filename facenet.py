from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image
import numpy as np
# If required, create a face detection pipeline using MTCNN:
mtcnn = MTCNN()

# Create an inception resnet (in eval mode):
resnet = InceptionResnetV1(pretrained='vggface2').eval()



name_list=[]

name_list=name_list+['./cai/c'+str(i)+'.jpg' for i in range(1,4)]
name_list=name_list+['./jw/jw'+str(i)+'.jpg' for i in range(1,5)]
name_list=name_list+['./xk/xk'+str(i)+'.jpg' for i in range(1,4)]

print(name_list)

vec=[]
for name in name_list:
    img = Image.open(name)
    img_cropped = mtcnn(img)
    img_embedding = resnet(img_cropped.unsqueeze(0))
    vec.append(img_embedding)

#print(len(vec[0].detach().numpy()[0]))

for v in vec:
    print((v-vec[2]).norm())