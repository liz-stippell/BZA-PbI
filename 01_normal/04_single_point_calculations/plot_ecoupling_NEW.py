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
vbm_c4 = 128 #140 # PBI SYSTEM
cbm_c4=vbm_c4+1
act_sp_c4=list(range(vbm_c4-50-1,cbm_c4+50))
#-------------


rcParams = {}
params = {
   'axes.labelsize': 18, #12,
   'font.size': 18, #12,
   'legend.fontsize': 16, #14,
   'xtick.labelsize': 16, #12,
   'ytick.labelsize': 16, #12,
   'legend.handlelength': 3,
   'text.usetex': False,
   'lines.linewidth': 2,
   'axes.prop_cycle': cycler(color=['r', 'g', 'b', 'y']),
#   'figure.figsize': [12, 6],
   'figure.figsize': [6, 6],
   'mathtext.default': 'regular',
   'axes.linewidth' : 1 #,
#   'axes.titlesize': 14, 'font.family':'Arial'
   }
plt.rcParams.update(params)

window_path = "."

fig, ax = plt.subplots(1,1) #2, 3
print(ax)

fileout="ecoup-larger_fonts.png"

vbm=50-1; cbm=vbm+1 # no need to -1 below

#filename1="_V_FILES/_V21_1000.txt"; data1=np.loadtxt(filename1)[act_sp_c4,:][:,act_sp_c4]*au2ev; data1=np.abs(data1)

path = "_V_FILES/"

data_list = []
for i in range(1000, 4000):
    print(i)
    data = np.loadtxt(f"{path}_V21_{i}.txt")[act_sp_c4,:][:,act_sp_c4]*au2ev; data = np.abs(data)
    print(np.shape(data))
    data_list.append(data)

data_list = np.array(data_list)
data_average = np.mean(data_list, axis=0)
print(np.shape(data_average))

x_min = 0
x_max = 128 #140 #102
y_min = 0
y_max=  128 #140 #102


#vmin=0; vmax=10 # test vmax to make plot look better
vmin=0
vmax=50

#im=ax.imshow(np.flipud(data1*1000), cmap='hot', interpolation='none', vmin=vmin, vmax=vmax,  extent=(x_min,x_max,y_min,y_max))
im=ax.imshow(np.flipud(data_average*1000), cmap='hot', interpolation='none', vmin=vmin, vmax=vmax,  extent=(x_min,x_max,y_min,y_max))

ax.set_xlim(59, 70.25)
ax.set_ylim(59, 70.25)

#ax.set_ylim(64.5, 76.75)
#ax.set_xlim(64.5, 76.75)


       # plot cbar
#cbar=plt.colorbar(im, ax=ax[i,j], fraction=0.045, pad=0.045)#,ticks=[U.min(),(U.min()+U.max())/2.,U.max()] )#, format='%.2f')
cbar=plt.colorbar(im, ax=ax, fraction=0.045, pad=0.045)#,ticks=[U.min(),(U.min()+U.max())/2.,U.max()] )#, format='%.2f')

cbar.ax.locator_params(nbins=5)
#cbar.ax.tick_params(labelsize=12)
cbar.ax.tick_params(labelsize=16)

        #use scientific notion on color bar
#cbar.formatter.set_powerlimits((0, 0))
#cbar.formatter.set_useMathText(True)
cbar.set_label('V [meV]')

         # change the tick name
#        label=np.arange(46.5,54.5+1,2)

#label=np.arange(65,75.75+1,2.75)
#label = np.arange(58.5, 69.5, 2)
label = np.arange(59.5, 70.25, 2.5)

label_list = ['-4', '-2', '0', '2', "4"]
ax.set_xticks(label)
ax.set_yticks(label)
ax.set_xticklabels(label_list)
ax.set_yticklabels(label_list)


ax.set_ylabel('HOMO+$\it{j}$ [Layer1]')
ax.set_xlabel('HOMO+$\it{i}$ [Layer2]')


plt.tight_layout()
plt.savefig(fileout, dpi=800)
