#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 11:21:34 2019

@author: Eric Chen, Graduate Center, CUNY

@ Prof. Kurtzman's Lab
"""

import os

os.chdir("/Users/eric/Desktop/TI-Water/power-law-fit/gist_ref/amber14")


from gridData import Grid
import numpy as np

simulation_time=[1,2,5,10,20,40,60,80,100]

dTStrans=[]
dTSorient=[]

dTStrans_file=[str(i)+"ns-dTStrans-dens.dx" for i in simulation_time]

for f_trans in dTStrans_file:
    
    g=Grid(f_trans).grid
    
    total=np.sum(g)*0.125
    dTStrans.append(total)

dTSorient_file=[str(i)+"ns-dTSorient-dens.dx" for i in simulation_time]

for f_ori in dTSorient_file:
    g=Grid(f_ori).grid
    total=np.sum(g)*0.125
    dTSorient.append(total)
    
dTSsix_file=[str(i)+"ns-dTSsix-dens.dx" for i in simulation_time]

dTSsix=[]
for f_six in dTSsix_file:
    g=Grid(f_six).grid
    total=np.sum(g)*0.125
    dTSsix.append(total)

    


print(dTStrans)
print(dTSorient)








def powerlaw(x,a,b,c):
    return a*(x**b)+c

from scipy.optimize import curve_fit

pars,covar=curve_fit(powerlaw,simulation_time,dTSorient,p0=[-2,0,0])
print(pars)
print(covar)

p,c=curve_fit(powerlaw,simulation_time,dTStrans,p0=[-1,10,1])

print(p)


import matplotlib.pyplot as plt

plt.plot(simulation_time,dTStrans,"blue",label="dTStrans")

plt.plot(simulation_time,dTSorient,"orange",label="dTSorient")

#plt.plot(simulation_time,dTSsix,"black",label="dTSsix")


plt.xlabel("Simulation time in ns(sample every 1ps)")
plt.ylabel("Kcal/mol")

times=[ i for i in range(1,101)]
plt.plot(times,powerlaw(times,*pars),"r--",label="Y=[223.28*X**(-0.54)]+21.22")

plt.legend()
plt.savefig("pure_water_fiting.png",dpi=400)
plt.show()

import numba



print(dTStrans)

print(dTSorient)

fit_dTsori=[powerlaw(i,*pars) for i in simulation_time]

diff=[ dTSorient[i]-fit_dTsori[i] for i in range(len(dTSorient))]

print(diff)

g_dTSori=Grid("100ns-dTSorient-dens.dx").grid

e_dTSori=Grid("100ns-dTSorient-dens.dx").edges

print(e_dTSori[2])

np.sum(g_dTSori)*0.125

values=[]
for i in range(60):
    for j in range(60):
        for k in range(60):
            values.append(g_dTSori[i,j,k])
points=[ p for p in range(len(values))]

total_dTStrans=sum(values)*0.125

print(total_dTStrans)


bins=np.arange(np.min(g_dTSori),np.max(g_dTSori)+0.00015,0.00015)

print(bins)
plt.hist(values,bins=bins,facecolor="orange")

plt.xlabel("dTSorient(Kcal/mol)")
plt.ylabel("frequency")

plt.savefig("100_ns_dTSorient.png",dpi=400)

plt.show()

edge_dTStrans=Grid("100ns-dTStrans-dens.dx").edges

edge_dTStrans[0]

import numpy

g_dTStrans=Grid("100ns-dTStrans-dens.dx").grid


values=[]

indexs=[]
for i in range(60):
    for j in range(60):
        for k in range(60):
            
                values.append(g_dTStrans[i,j,k])
               
bins=np.arange(np.min(g_dTStrans),np.max(g_dTStrans)+0.00015,0.00015)
plt.hist(values,bins=bins,facecolor="orange")


edges=Grid("100ns-dTStrans-dens.dx").edges

for i in range(5):
    for j in range(5):
        print((edges[0][0],edges[1][i],edges[2][j]))
        print(g_dTStrans[0][i][j])

print(edges[0])

print


 






               
len(indexs) 
type(indexs)
print(indexs[0:10])
g_gO=Grid("100ns-gO.dx").grid

gO_values=[]
import math
for i in range(len(indexs)):
    temp=indexs[i]
    t=g_gO[temp[0],temp[1],temp[2]]
    
    trans=g_dTStrans[temp[0],temp[1],temp[2]]
    
    print(t)
    print(trans)
    print(t*math.log(t))
    
    gO_values.append(t)
print(gO_values[0:10])     




g_max=np.max(g_dTStrans)
g_min=np.min(g_dTStrans)
bin_width=(g_max-g_min)/100



g_values=[]
d_values=[]
for i in range(60):
    for j in range(60):
        for k in range(60):
            d=g_dTStrans[i,j,k]
            
            
            d_values.append(d)


d_nozero=[t for t in d_values if t!=0]       
plt.hist(d_nozero,np.arange(float(g_min),float(g_max)+0.00015,0.00015),facecolor="blue")

plt.xlabel("dTStrans(Kcal/mol)")
plt.ylabel("Frequency")
plt.savefig("100_ns_dTStrans.png",dpi=400)

plt.show()

print(np.arange(float(g_min),float(g_max)+0.00015,0.00015))
       

temp=[x for x in d_values if -0.00011161<x<0.00003839]  

temp.count(0)   


            

