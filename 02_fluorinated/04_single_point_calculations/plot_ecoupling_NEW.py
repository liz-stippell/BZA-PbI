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
vbm_c4 = 140 # PBI SYSTEM
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

fileout="ecoup-1ps_TEST.png"

vbm=50-1; cbm=vbm+1 # no need to -1 below

filename1="_V_COMBINED.txt"; data1=np.loadtxt(filename1)[act_sp_c4,:][:,act_sp_c4]*au2ev; data1=np.abs(data1)

x_min = 0
x_max = 70 #102
y_min = 0
y_max=  70 #102


#vmin=0; vmax=10 # test vmax to make plot look better
vmin=0
vmax=100

im=ax.imshow(np.flipud(data1*1000), cmap='hot', interpolation='none', vmin=vmin, vmax=vmax,  extent=(x_min,x_max,y_min,y_max))


#ax.set_xlim(59, 68)
#ax.set_ylim(59, 68)
ax.set_ylim(27, 36)
ax.set_xlim(27, 36)


       # plot cbar
#cbar=plt.colorbar(im, ax=ax[i,j], fraction=0.045, pad=0.045)#,ticks=[U.min(),(U.min()+U.max())/2.,U.max()] )#, format='%.2f')
cbar=plt.colorbar(im, ax=ax, fraction=0.045, pad=0.045)#,ticks=[U.min(),(U.min()+U.max())/2.,U.max()] )#, format='%.2f')

cbar.ax.locator_params(nbins=5)
cbar.ax.tick_params(labelsize=12)

        #use scientific notion on color bar
cbar.formatter.set_powerlimits((0, 0))
cbar.formatter.set_useMathText(True)
cbar.set_label('V [meV]')

         # change the tick name
#        label=np.arange(46.5,54.5+1,2)
#label=np.arange(59.5,67.5+1,2)
label = np.arange(27.5, 35.5+1, 2)

label_list = ['-4', '-2', '0', '2', "4"]
ax.set_xticks(label)
ax.set_yticks(label)
ax.set_xticklabels(label_list)
ax.set_yticklabels(label_list)


ax.set_ylabel('LUCO+$\it{j}$ [Layer1]')
ax.set_xlabel('LUCO+$\it{i}$ [Layer2]')


plt.tight_layout()
plt.savefig(fileout, dpi=800)
