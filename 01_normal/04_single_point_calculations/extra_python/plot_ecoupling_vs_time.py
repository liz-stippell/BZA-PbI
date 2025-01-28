import os
import sys
import time
import glob
import numpy as np
from matplotlib import ticker
import scipy.sparse as sp
import matplotlib.pyplot as plt
from matplotlib.pylab import *

au2ev=27.211
#------------
vbm_c4 = 128 # PBI SYSTEM
cbm_c4=vbm_c4+1
act_sp_c4=list(range(vbm_c4-50,cbm_c4+50+1))
#-------------


rcParams = {}
params = {
   'axes.labelsize': 12,
   'font.size': 12,
   'legend.fontsize': 14,
   'xtick.labelsize': 12,
   'ytick.labelsize': 12,
   'legend.handlelength': 3,
   'text.usetex': False,
   'lines.linewidth': 2,
   'axes.prop_cycle': cycler(color=['r', 'g', 'b', 'y']),
   'figure.figsize': [12, 6],
   'mathtext.default': 'regular',
   'axes.linewidth' : 1 #,
#   'axes.titlesize': 14, 'font.family':'Arial'
   }
plt.rcParams.update(params)

window_path = "."

fig, ax = plt.subplots(1,1) #2, 3
print(ax)

fileout="ecoup-3ps.png"

#vbm=50-1; cbm=vbm+1 # no need to -1 below

#filename1="V_3ps.txt"; data1=np.loadtxt(filename1)[act_sp_c4,:][:,act_sp_c4]*au2ev; data1=np.abs(data1)


homo_list = []
lumo_list = []
for i in range(1000, 4000):
#for i in range(np.linspace(0, 20000, 877)
	filename1 = f"_V_FILES/_V21_{i}.txt"
	#filename = "V_3ps.txt"
#	homo = np.loadtxt(filename1)[vbm_c4-1,vbm_c4-1]*au2ev
	#homo = np.loadtxt(filename)[i+vbm_c4-1,vbm_c4-1]*au2ev
	homo = np.loadtxt(filename1)[vbm_c4-1,vbm_c4-1]*au2ev
	homo_list.append(homo)
	
	
	lumo = np.loadtxt(filename1)[vbm_c4,vbm_c4]*au2ev
	lumo_list.append(lumo)
#	print(filename1)
#	print(lumo)

homo_list = abs(np.array(homo_list))
print("HOMO mean & std dev: ")
print(np.mean(homo_list))
print(np.std(homo_list))

print("LUMO mean & std dev: ")
lumo_list = abs(np.array(lumo_list))
print(np.mean(lumo_list))
print(np.std(lumo_list))
#print(data1)

data1 = homo_list
data2 = lumo_list

plot_mean = [np.mean(homo_list)]*3000

x_val = range(1000, 4000)
plt.plot(x_val, data1, "r", label="HOMO")
plt.plot(x_val, data2, "b", label="LUMO")
plt.plot(x_val, plot_mean, "m-", label="HOMO Mean")
plt.legend()
plt.savefig("ecoupling_vs_time.png")
