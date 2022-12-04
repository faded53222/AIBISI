import os
import math
import cv2
import numpy as np
import random
import openslide
from skimage import io
from openslide.deepzoom import DeepZoomGenerator

NAME='stad'

def D_img(file_paths,num):
	for file_path in file_paths:
		file_name=file_path.split('/')[-1][:-4]
		print(file_name)
		slide=openslide.open_slide(file_path)
		data_gen=DeepZoomGenerator(slide,tile_size=512,overlap=0,limit_bounds=False)
		count=0
		while 1:
			l=data_gen.level_count-1
			p_i=random.randint(0,math.floor(data_gen.level_dimensions[data_gen.level_count-1][0]/512)-1)
			p_j=random.randint(0,math.floor(data_gen.level_dimensions[data_gen.level_count-1][1]/512)-1)
			img=np.array(data_gen.get_tile(l,(p_i,p_j)))
			edges=cv2.Canny(img,100,200)
			if edges.mean()<4:
				continue
			fname=file_name+'_'+str(l)+'_'+str(p_i)+'_'+str(p_j)+'_'+NAME+'.png'
			io.imsave(os.path.join('s_cuts_'+NAME,fname),img)
			count+=1
			if count==num:
				break

labels=[]
with open('data_labels/'+NAME+'_labels.txt') as f:
	lines=f.readlines()
	for line in lines:
		items=line.split()
		labels.append((items[0],int(items[1])))
files=[]
with open('data_labels/'+NAME+'_use.txt','r') as f:
	lines=f.readlines()[1:]
	for line in lines:
		items=line.split()
		for each in labels:
			if each[0]==items[1][:-4]:
				file=os.path.join('download/'+NAME,items[0],each[0]+'.svs')
				files.append(file)
				break

#print(files)
D_img(files,20)
def get_labels(file_name,place):
    with open(file_name,'w') as f:
        for each in os.listdir(place):
            for label in labels:
                if label[0]==each.split('_')[0]:
                    f.write(each+'\t'+str(label[1])+'\n')
                    break
get_labels('s_labels_'+NAME+'.txt','s_cuts_'+NAME)
