import numpy as np
import os
import sys
import math
from copy import deepcopy

##### needs be specified ####
min_indx=1000 #which period of trajectory (start)
max_indx=4000 #end

#Noccup=[4,1,5,7,14] #used in openMX input - outmost valence electrons for elements
Noccup=[14, 7, 5, 1, 4]
templ_filename="nbt.dat"
prefix="PbI"
###########################

wd="wd"
# Read the template file
f_templ = open(templ_filename,"r")
T = f_templ.readlines()
f_templ.close()

if os.path.isdir(wd):
    pass
else:
    os.system("mkdir %s" % wd)

inp = [line for line in open("XDATCAR") if line.strip()]

scale = float(inp[1])
cell = np.array([line.split() for line in inp[2:5]], dtype=float)
cell *= scale

element_names = inp[5].split()
element_numbers = inp[6].split()
Natom = np.array(element_numbers, dtype=int)
Nions = np.sum(Natom)


Ntype = len(element_names)
Nname=[]
Noccup1=[]; Noccup2=[]
for t in range(Ntype):
    for i in range(int(element_numbers[t])):
        Nname.append(element_names[t])
        Noccup1.append(Noccup[t]*0.5)
        Noccup2.append(Noccup[t]*0.5)

pos = np.array([line.split() for line in inp[7:] if not line.split()[0].isalpha()], dtype=float)
position = pos.ravel().reshape((-1, Nions, 3))
Niter = position.shape[0]
#print (position[-1,:,:])
print (position.shape)
#print(Ntype,Nions)
#for i in range(len(Nname)):
#    print (Nname[i],Noccup1[i])

#print (cell[0][0])
#sys.exit(0)

f_prev=np.zeros([Nions,3])
f_next=np.zeros([Nions,3])

for i in range(0,Niter):
    f_next = position[i,:,:]
    for j in range(0,Nions):
        for x in range(3):
            if(f_next[j,x]-f_prev[j,x]<-0.5):
                f_next[j,x]+=1
            elif(f_next[j,x]-f_prev[j,x]>0.5):
                f_next[j,x]-=1
    f_prev=deepcopy(f_next)
    position[i,:,:] = f_next

#change direct to car
for i in range(0,Niter):
    position[i,:,:] = np.dot(position[i,:,:], cell)

for i in range(min_indx,max_indx+1):
    f_t = open("%s/%s.%d.dat" % (wd,prefix,i), "w")
        
    for b in T:
        f_t.write(b)

    # Write the header for positions        
    f_t.write("<Atoms.SpeciesAndCoordinates\n")
    for atom in range(0,Nions):
        f_t.write(str(atom+1)+" "+Nname[atom]+" "+str(position[i-1,atom,0])+" "+str(position[i-1,atom,1])+" "+str(position[i-1,atom,2])+" "+str(Noccup1[atom])+" "+str(Noccup2[atom])+ "\n")
    f_t.write("Atoms.SpeciesAndCoordinates>\n")



