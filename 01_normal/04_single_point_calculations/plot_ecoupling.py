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
#vbm_c4=108 #C4
vbm_c4 = 256 #236 # PBI SYSTEM
cbm_c4=vbm_c4+1
act_sp_c4=list(range(vbm_c4-50,cbm_c4+50+1))

#vbm_c8=156 #C8
#cbm_c8=vbm_c8+1
#act_sp_c8=list(range(vbm_c8-50,cbm_c8+50+1))

#vbm_c12=204 #C12
#cbm_c12=vbm_c12+1
#act_sp_c12=list(range(vbm_c12-50,cbm_c12+50+1))
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
   'figure.figsize': [12, 6],
   'mathtext.default': 'regular',
   'axes.linewidth' : 1 #,
#   'axes.titlesize': 14, 'font.family':'Arial'
   }
plt.rcParams.update(params)

window_path = "."
 
fig, ax = plt.subplots(2,3) #2, 3
print(ax)

fileout="ecoup-larger_fonts.png"
#title = ["C4PbI", "C8PbI", "C12PbI"]
title = ["BZA-PbI"] # figure out what we're naming the systems...

vbm=50-1; cbm=vbm+1 # no need to -1 below
#vbm = 237-1; cbm=vbm+1 # FOR MY SYSTEM

filename1="V2000.txt"; data1=np.loadtxt(filename1)[act_sp_c4,:][:,act_sp_c4]*au2ev; data1=np.abs(data1)
print(np.loadtxt(filename1)[act_sp_c4,:][:,act_sp_c4])
#filename2="V2000.txt"; data2=np.loadtxt(filename2)[act_sp_c4,:][:,act_sp_c4]*au2ev; data2=np.abs(data2)

#filename1="c4_V21.txt"; data1=np.loadtxt(filename1)[act_sp_c4,:][:,act_sp_c4]*au2ev; data1=np.abs(data1)
#filename2="c8_V21.txt"; data2=np.loadtxt(filename2)[act_sp_c8,:][:,act_sp_c8]*au2ev; data2=np.abs(data2)
#filename3="c12_V21.txt"; data3=np.loadtxt(filename3)[act_sp_c12,:][:,act_sp_c12]*au2ev; data3=np.abs(data3)

# unit in thermal averaged already in eV
#filename2="c4_V21.txt"; data2=np.loadtxt(filename2)[act_sp_c4,:][:,act_sp_c4]; data2=np.abs(data2)

#filename4="c4_average_abs_V_lowdin.dat"; data4=np.loadtxt(filename4)[act_sp_c4,:][:,act_sp_c4]; data4=np.abs(data4)
#filename5="c8_average_abs_V_lowdin.dat"; data5=np.loadtxt(filename5)[act_sp_c8,:][:,act_sp_c8]; data5=np.abs(data5)
#filename6="c12_average_abs_V-lowdin.dat"; data6=np.loadtxt(filename6)[act_sp_c12,:][:,act_sp_c12]; data6=np.abs(data6)

#print (np.loadtxt(filename1)[vbm_c4-1-2, vbm_c4-1+1]*au2ev)
#print (data1[vbm, vbm])
#print (data2[vbm, vbm])
#print (data3[vbm, vbm])

x_min = 0
x_max = 128 #102
y_min = 0
y_max=  128 #102
#z_min = 0

#x_min = 40
#x_max = 60
#y_min = 40
#y_max=  60


for i in range(1): # 2
    for j in range(1): # 3
        if i==0 and j==0:
            data=data1

        elif i==0 and j==1:
            data = data2
        elif i==0 and j==2:
            data=data3

        elif i==1 and j==0:
          data=data4

        elif i==1 and j==1:
          data=data5

        elif i==1 and j==2:
          data=data6

            #ax[i,j].set_clim(0,2.5e-1)
        if i==0:
          if j==0:
            vmin=0; vmax=10;
          elif j==1:
            vmin=0; vmax=1;
          elif j==2:
            vmin=0; vmax=0.1;

        elif i==1:
          if j==0:
            vmin=0; vmax=10;
          elif j==1:
            vmin=0; vmax=1;
          elif j==2:
            vmin=0; vmax=0.1;

        #im=ax[i,j].imshow(np.flipud(data*1000), cmap='hot', interpolation='none', vmin=vmin, vmax=vmax),  extent=(x_min,x_max,y_min,y_max))#,
        im=ax[i,j].imshow(np.flipud(data*1000), cmap='hot', interpolation='none', vmin=vmin, vmax=vmax,  extent=(x_min,x_max,y_min,y_max))

        if i==0:
          ax[i,j].set_title(title[j])
        #if i==1:
        #    im=ax[i,j].imshow(np.flipud(data), cmap='hot',  interpolation='none',  vmin=0, vmax=0.5, extent=(x_min,x_max,y_min,y_max))#,
         
       
#        ax[i,j].set_xlim(46,55)
#        ax[i,j].set_ylim(46,55)
 
        ax[i,j].set_xlim(59, 68)
        ax[i,j].set_ylim(59, 68)

       # plot cbar
        cbar=plt.colorbar(im, ax=ax[i,j], fraction=0.045, pad=0.045)#,ticks=[U.min(),(U.min()+U.max())/2.,U.max()] )#, format='%.2f')
        cbar.ax.locator_params(nbins=5)
        cbar.ax.tick_params(labelsize=12)

        #use scientific notion on color bar
        cbar.formatter.set_powerlimits((0, 0))
        cbar.formatter.set_useMathText(True)
        cbar.set_label('V [meV]')

         # change the tick name
#        label=np.arange(46.5,54.5+1,2)
        label=np.arange(59.5,67.5+1,2)

        label_list = ['-4', '-2', '0', '2', "4"]
        ax[i,j].set_xticks(label)
        ax[i,j].set_yticks(label)
        ax[i,j].set_xticklabels(label_list)
        ax[i,j].set_yticklabels(label_list)
 
       #ax[c].set_yticklabels(label_list)

        if j==0:
          ax[i,j].set_ylabel('LUCO+$\it{j}$ [Layer1]')

        if i==1:
          ax[i,j].set_xlabel('LUCO+$\it{i}$ [Layer2]')


#plt.colorbar().ax.set_title('eV', fontsize=10)
#plt.text(0, 10, "0K", fontsize=14)
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=.1, hspace=.1)
plt.tight_layout()
plt.savefig(fileout, dpi=800)
