import sys
import cmath
import math
import os

import numpy as np
from TB2J_OpenMX.ffiparser import OpenmxWrapper
from ase.units import Ha, Bohr, Ry

from scipy.linalg import fractional_matrix_power


import scipy.sparse as sp

#if sys.platform=="cygwin":
#    from cyglibra_core import *
#elif sys.platform=="linux" or sys.platform=="linux2":

if sys.platform=="linux" or sys.platform=="linux2":
    from liblibra_core import *

from libra_py import data_conv


#### use for peroid system

def find_dup(l):
    l1=[]
    for i in l:
        if i not in l1:
            l1.append(i)
        else:
            print("found duplicate atom index %d  \n" %i)

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
            #elif i in O_ele:
            #   cnt+= O_ao
            elif i in Pb_ele:
                cnt+= Pb_ao
            elif i in I_ele:
                cnt+= I_ao
    return cnt

def ao_basis(i):
    tmp=-1
    #if i in H_ele:
        #tmp=H_ao
    if i in C_ele:
        tmp=C_ao
    elif i in N_ele:
        return N_ao
    elif i in H_ele:
        return H_ao
    #elif i in O_ele:
    #    return O_ao
    elif i in Pb_ele:
        return Pb_ao        
    elif i in I_ele:
        return I_ao  
    else:
        pass
    return tmp
    # need to add more in case if there is a need

def dia_mat_to_file(X, outfile):
    col=X.num_of_cols; row=X.num_of_rows
    f=open(outfile, "w")
    for i in range(0,col):
	    for j in range(0,row):
		    if i==j:
			    f.write(" %f \n  " % X.get(i,j))


    f.close()


def do_orthonormalization(H,S):
    U = fractional_matrix_power(S,-1/2)
    H_orthonormalized = np.linalg.multi_dot([U.transpose(), H, U])
    return H_orthonormalized



def act_sp(frag):
    tmp=[]
    for I in frag:
        for i in range(0,ao_basis(I)):
           local_i = trans(I) + i
           tmp.append(local_i)
    return tmp

def make_matrix(filename_in, opt=1):
    if opt==1:
        look_up='Ham in AO'
    elif opt==2:
        look_up='Overlap in AO'

    A=MATRIX(ndim,ndim)
    #A.show_matrix()
    with open(filename_in,'r') as fo:
        while True:
            try:
                line=next(fo)
                #print (line)
                if line.find(look_up) >= 0:
                    tmp=line.split()
                    I=int(tmp[3]); J=int(tmp[4])
                    for i in range(0,ao_basis(I)):
                        local_i = trans(I) + i
                        tmp=next(fo).split()
                        for j in range(0,ao_basis(J)):
                            local_j = trans(J) + j
                            #print (tmp, local_i,local_j)
                            A.set(local_i,local_j, float(tmp[j]))
            except StopIteration:
                break
    return A


def check_at_list(at_list, li):
    cnt=-1
    if not at_list:
        cnt = 0
    elif li in at_list:
        cnt = 1
    else:
        cnt = 0

    return cnt



def make_matrix2(filename_in, opt=1):
    if opt==1:
        look_up='rHam in AO'
    elif opt==2:
        look_up='rOverlap in AO'

    at_list = []
    A=MATRIX(ndim,ndim)
    #A.show_matrix()
    with open(filename_in,'r') as fo:
        while True:
            try:
                line=next(fo)
                if line.find(look_up) >= 0:
                    tmp=line.split()
                    I=int(tmp[3]); J=int(tmp[4])
                    li=[I,J]
                    if check_at_list(at_list,li) == 0:
                        for i in range(0,ao_basis(I)):
                            local_i = trans(I) + i
                            tmp=next(fo).split()
                            #print (tmp)
                            for j in range(0,ao_basis(J)):
                                local_j = trans(J) + j
                                A.set(local_i,local_j,float(tmp[j]))
                        at_list.append(li)
                    elif check_at_list(at_list,li) == 1:
                        for i in range(0,ao_basis(I)):
                            local_i = trans(I) + i
                            tmp=next(fo).split()
                            #print (tmp)
                            for j in range(0,ao_basis(J)):
                                local_j = trans(J) + j
                                A.add(local_i,local_j,float(tmp[j]))                        
            except StopIteration:
                break
    #print (at_list)
    return A

# s-1, p-3, d-5, f-7
#atom list and AO, starting from 1
################################
#C_ele=list(range(1,32+1)); C_ao = 13  #s2p2d1
#H_ele=list(range(33,128+1)); H_ao = 5  #s2p1
#N_ele=list(range(129,136+1)); N_ao = 13  #s2p2d1
#Pb_ele=list(range(153,156+1)); Pb_ao = 3+6+10+7  #s3p2d2f1
#I_ele=list(range(137,152+1)); I_ao = 3+6+10+7  #s3p2d2f1

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

#print(frag_a)
#print(frag_b)

find_dup(frag_a); find_dup(frag_b)

if len(C_ele)+len(H_ele) + len(N_ele) + len(Pb_ele) + len(I_ele) != ntot:
   print ("atoms list not correct!\n")
   sys.exit(0)

if len(frag_a) + len(frag_b) != ntot:
    print ("atom groups not correct \n")
    sys.exit(0)

if len(frag_a) != len(frag_b):
    print ("atom groups not correct! \n")
    sys.exit(0)

# nrows=19; ncols=19
# a_list = [1,2,3,4]
# b_list = [5,6,7,8,9]
# frag_a = a_list
# frag_b = b_list

# #atom list and AO, starting from 1
# C_ele=[5]; C_ao = 4  #s1p1
# H_ele=[2,3,4,6,7,8,9]; H_ao = 1  #s1
# N_ele=[1]; N_ao = 8 #s2p2


# size of the big matrix

#h = make_matrix2(filename_in,1)
#s = make_matrix2(filename_in,2)





#params=[[[0.5,0,0], "X"], \
#    [[0.5,0,0.5], "U"]]
#params=[[[0,0,0], "G"], \
#    [[0.5,0.5,0.5], "A"], \
#    [[0.5,0.5,0], "M"], \
#    [[0,0.5,0.5], "R"], \
#    [[0,0.5,0], "X"], \
#    [[0,0,0.5], "Z"] ]

#homo=108-1
#homo = 256 - 1
homo = 237 - 1
 
#prefix="c4"
prefix = "abc"

start_indx=1000 #which period to calc e-coupling (start)
end_indx = 2000 #end

for i in range(start_indx, end_indx+1):
    dir=os.getcwd()+"/run/"+str(i) #make run directory
    if not os.path.exists(dir):
        os.makedirs(dir)

    kp=[0,0,0]
#    kp=[0, 0]

    filenameV_re="_V_"+str(i)+"_re.txt"
    filenameV_im="_V_"+str(i)+"_im.txt"
    filenameE="_E_"+str(i)+"_.txt"
    filenameE1="_E1_"+str(i)+"_.txt"
    filenameE2="_E2_"+str(i)+"_.txt"

    openmx=OpenmxWrapper(dir,prefix)
    #print(np.array(kp)) 
    h, s = openmx.HSE_k(np.array(kp))
    #print (h)
    h= do_orthonormalization(h, s)
    h=CMATRIX(data_conv.nparray2MATRIX(h.real), data_conv.nparray2MATRIX(h.imag))
    s=CMATRIX(data_conv.nparray2MATRIX(s.real), data_conv.nparray2MATRIX(s.imag))

    # try diagonalize the eigenvalues anyway
    H=CMATRIX(ndim, ndim); S=CMATRIX(ndim, ndim); U=CMATRIX(ndim, ndim); E=CMATRIX(ndim, ndim)
    solve_eigen(h, E, U,0)

    h1_act_sp = act_sp(frag_a); h2_act_sp = act_sp(frag_b)

    sz_a = len(h1_act_sp); sz_b=len(h2_act_sp)

    h1 = CMATRIX(sz_a, sz_a); h2 = CMATRIX(sz_b, sz_b)
    v21 = CMATRIX(sz_b, sz_a); v12 = CMATRIX(sz_a, sz_b)

    #s1 = CMATRIX(sz_a, sz_a); s2 = CMATRIX(sz_b, sz_b)

    U1 = CMATRIX(sz_a, sz_a); U2 = CMATRIX(sz_b, sz_b)
    E1 = CMATRIX(sz_a, sz_a); E2 = CMATRIX(sz_b, sz_b)

    #print (h1.num_of_cols)

    pop_submatrix(h, h1, list(h1_act_sp), list(h1_act_sp))
    pop_submatrix(h, h2, list(h2_act_sp), list(h2_act_sp))
    pop_submatrix(h, v21, list(h2_act_sp), list(h1_act_sp))
    pop_submatrix(h, v12, list(h1_act_sp), list(h2_act_sp))

    #pop_submatrix(s, s1, list(h1_act_sp), list(h1_act_sp))
    #pop_submatrix(s, s2, list(h2_act_sp), list(h2_act_sp))

    solve_eigen(h1,  E1, U1,0)
    solve_eigen(h2,  E2, U2,0)

    V21=U2.T()*v21*U1
    #V12=U1.T()*v12*U2


    #print ("final outputs")
    #V21_=data_conv.MATRIX2scipynpz(V21)
    V21.real().show_matrix(filenameV_re)
    #V21.imag().show_matrix(filenameV_im)
    # print ("homo-homo (eV)")
    # print (np.sqrt(V21.get(homo,homo).real**2 +  V21.get(homo,homo).imag**2)*27.211)
    # print ("lumo-lumo (eV")
    # print (np.sqrt(V21.get(homo+1,homo+1).real**2 +  V21.get(homo+1,homo+1).imag**2)*27.211)

    dia_mat_to_file(E.real(), filenameE)
    dia_mat_to_file(E1.real(), filenameE1)
    dia_mat_to_file(E2.real(), filenameE2)





