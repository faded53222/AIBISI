import numpy as np

with open('./data_labels/bacter.txt',encoding='utf-8') as f:
	bac_items=f.readline().split()[1:]
	for i in range(len(bac_items)):
		bac_items[i]=bac_items[i][:-1]
		
print('total',len(bac_items),'bacter labels')
use_labels1={}
'''
comps=['stad','ucec','brca','kirc','gbm','lusc','luad','lgg','ov'\
,'coad','hnsc','prad','thca','skcm','blca','sarc','lihc','kirp','cesc'\
,'read','paad','tgct','esca','pcpg','kich','acc','thym','meso','ucs'\
,'uvm','chol','dlbc']
'''
comps=['stad']
count=0
C2=[]
for comp in comps:
	with open('./data_labels/'+comp+'.txt',encoding='utf-8') as f:
		lines=f.readlines()[1:]
		temp=[]
		for line in lines:
			temp.append(line.split()[1][:15])
		common=np.intersect1d(bac_items,temp)
		if len(common)!=0:
			u_pos=[]
			u_neg=[]
			u=[]
			t=[]
			with open('./data_labels/'+comp+'.txt') as f:
				lines=f.readlines()[1:]
				for line in lines:
					items=line.split()
					t.append(items[1][:-4])
					if items[1][:15] in common:
						u_pos.append(items[1][:-4])
						u.append((items[1][:-4],1))
			
			u_pos=np.array(u_pos)
			u_neg=np.random.choice(list(set(t)-set(u_pos)),len(u_pos),replace=False)
			for each in u_neg:
				u.append((each,0))
			print(len(common),'labels lays in',comp,' within ',len(temp))
			C=[]
			for each in common:
				if each not in C:
					C.append(each)
					if each not in C2:
						C2.append(each)
					else:
						print(each)
					count+=1
			u0=[]
			for each in u:
				u0.append(each[0])
			with open('./data_labels/'+comp+'_use'+'.txt','w') as f:
				with open('./data_labels/'+comp+'.txt') as f2:
					lines=f2.readlines()
					f.write(lines[0])
					for line in lines[1:]:
						items=line.split()
						if items[1][:-4] in u0:
							f.write(line)
			with open('./data_labels/'+comp+'_labels'+'.txt','w') as f:
				for each in u:
					f.write(each[0]+'\t'+str(each[1])+'\n')
print(count)
