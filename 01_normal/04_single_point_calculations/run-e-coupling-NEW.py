import sys
import cmath
import math
import os

import numpy as np
from TB2J_OpenMX.ffiparser import OpenmxWrapper
from ase.units import Ha, Bohr, Ry

import scipy.sparse as sp
from scipy.linalg import fractional_matrix_power
import scipy.linalg as sl

def  do_orthonormalization(H,S):
    #https://chemistry.stackexchange.com/questions/85484/how-to-do-lowdin-symmetric-orthonormalisation
    lam_s, l_s = np.linalg.eigh(S)
    lam_s = lam_s * np.eye(len(lam_s))
    lam_sqrt_inv = np.sqrt(np.linalg.inv(lam_s))
    symm_orthog = np.dot(l_s, np.dot(lam_sqrt_inv, l_s.T))
    H_orthonormalized = np.linalg.multi_dot([symm_orthog.T,  H,  symm_orthog])
    return H_orthonormalized



def ao_basis(i):
    tmp=-1
    #if i in H_ele:
        #tmp=H_ao
    if i in C_ele:
        tmp=C_ao
    elif i in N_ele:
        tmp = N_ao
    elif i in H_ele:
        tmp = H_ao
    elif i in Pb_ele:
        tmp = Pb_ao        
    elif i in I_ele:
        tmp = I_ao  
    else:
        pass
    return tmp

def act_sp(frag):
    tmp=[]
    for I in frag:
        for i in range(0,ao_basis(I)):
           local_i = trans(I) + i
           tmp.append(local_i)
    return tmp

def trans(t):
    cnt=0
    if t==1:
        pass
    else:
        for i in range(1,t):
            if i in H_ele:
               cnt+= H_ao
            elif i in N_ele:
                cnt+= N_ao
            elif i in C_ele:
                cnt+= C_ao
            elif i in Pb_ele:
                cnt+= Pb_ao
            elif i in I_ele:
                cnt+= I_ao
    return cnt

def check(a, b, ndim):
    tmp = a + b
    tmp1 = list(range(ndim))
    if set(tmp) == set(tmp1):
        print ("fine with fragment definition")

    else:
        print ("error with grouping")
        sys.exit(0)        

################################
C_ele=list(range(109,164+1)); C_ao = 13  #s2p2d1
H_ele=list(range(29,108+1)); H_ao = 5  #s2p1
N_ele=list(range(21,28+1)); N_ao = 13  #s2p2d1
Pb_ele=list(range(1,4+1)); Pb_ao = 3+6+10+7  #s3p2d2f1
I_ele=list(range(5,20+1)); I_ao = 3+6+10+7  #s3p2d2f1

ndim =  len(C_ele)*C_ao + len(H_ele)*H_ao + len(N_ele)*N_ao +  len(Pb_ele)*Pb_ao + len(I_ele)*I_ao #N, s2p2, H, 1s , NH3
print (ndim) # HOMO=212, nKS=612 in openmx

#ntot=156
ntot = 164
at = list(range(1,ntot+1))
#frag_a = [29,21,13,5,133,125,109,117,37, 45,61,53,77,69,101,93,85,28,20,12,4,132,108,124,116,44,36,52,60,68,76,100,84,92,30,102,86,94,22,70,78,54,62,14,6,46,38,134,110,118,126,27,83,99,91,19,75,67,11,51,59,3,43,35,131,115,107,123,155,154,139,148,140,150,142,141,149,147]

frag_a = [ 1, 13, 5, 14, 11, 4, 20, 6, 19, 12,    27, 43, 35, 51, 163, 107, 99, 115, 123, 59, 131, 67, 139, 75, 147, 83, 155, 91,    22, 38, 46, 30, 158, 94, 102, 110, 150, 86, 142, 78, 134, 70, 126, 62, 118, 54,    28, 44, 36, 52, 164, 108, 100, 116, 156, 92, 148, 84, 140, 76, 132, 68, 124, 60,     21, 29, 37, 45, 157, 93, 101, 109, 149, 85, 141, 77, 133, 69, 125, 61, 117, 53 ]
###############################
frag_b = []
for i in at:
    if i not in frag_a:
        frag_b.append(i)

h1_act_sp = act_sp(frag_a); h2_act_sp = act_sp(frag_b)

check(h1_act_sp, h2_act_sp, ndim)

kp=[0,0,0]
prefix="abc"

opt=1 # do Lowdin
#opt=0 # no Lowdin

#homo=108
# HOMO from OpenMX
homo = 128 #Confirm this - for each layer (half of total electrons)

start_indx=3053 #Change
end_indx=4000 #Change - last 2/3 ps

for i in range(start_indx, end_indx+1):

#    E_adi_fname = "_E_adi_"+str(i)+".txt"
#    E_dia1_fname = "_E_dia1_"+str(i)+".txt"
#    E_dia2_fname = "_E_dia2_"+str(i)+".txt"

# Above not important (E_dia)

    V21_fname = "_V21_"+str(i)+".txt" # most important

#    dir=os.getcwd()+"/../run/"+str(i)

    dir=os.getcwd()+"/run/"+str(i) #make run directory
    if not os.path.exists(dir):
        os.makedirs(dir)

    print(dir)
    print(prefix)

    openmx=OpenmxWrapper(dir,prefix)
    h, s = openmx.HSE_k(np.array(kp))

    print ("\n========= now begin ========= \n")

    if opt==1:
        print ("\n now do block diagonalization with Lowdin\n")
        h=do_orthonormalization(h, s)
        eva, evc = sl.eigh(h)
        eva1, evc1 = sl.eigh(h[h1_act_sp,:][:,h1_act_sp])
        eva2, evc2 = sl.eigh(h[h2_act_sp,:][:,h2_act_sp])

    #print (" \n ========= e-coupling V21 ========= \n")
    V21 = np.linalg.multi_dot([evc2.T,  h[h2_act_sp,:][:,h1_act_sp],  evc1])

    #print ("\n ========= H' take the following form ======== \n")
    #H = np.block([[np.diag(eva1.real), V21.real.T],[V21.real,np.diag(eva2.real)]])

    #print ("\n ========= now diagonalize H' without S ======== \n")
    #eva3, evc3 = sl.eigh(H)
    #print (eva3.real); #print ("\n"); print (evc3.real)

#    np.savetxt(E_adi_fname, eva.real.T)
#    np.savetxt(E_dia1_fname, eva1.real.T)
#    np.savetxt(E_dia2_fname, eva2.real.T)
    #np.savetxt(E_finalH_fname, eva3.real.T)

#   V21_fname = os.path.join("_V_FILES", V21_fname)
    np.savetxt(V21_fname, V21.real )
