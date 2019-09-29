#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 11:22:11 2019

@author: Eric Chen, Graduate Center, CUNY

@ Prof. Kurtzman's Lab
"""

# This code is for Amber 18 gist output, in which 

# dTStrans-dens: Colume 7( starting from 0 in C++)

# dTSorient-dens: Colume 9

# Esw-dens: cloume 13

# Eww-dens: column 15, unit: Kcal/(mol*A3)



import os 

print(os.getcwd())

#os.chdir("/Users/eric/Desktop/TI-Water/gist-displacement/70_70_70/pure_water/")

os.chdir("/Users/eric/Desktop/TI-Water/gist-displacement/100ns")

import subprocess

# set up the gistpp command 

gistpp="/Users/eric/software/gist-post-processing-master/gistpp"

command1=[gistpp,"-i", "100ns-dTStrans-dens.dx","-op","multconst", "-opt", "const","0.125","-o","dTStrans.dx"]

command2=[gistpp,"-i", "gist-dTSorient-dens.dx","-op","multconst", "-opt", "const","0.125","-o","dTSorient.dx"]


command3=[gistpp,"-i", "gist-Esw-dens.dx","-op","multconst", "-opt", "const","0.125","-o","Esw.dx"]

command4=[gistpp,"-i", "gist-Eww-dens.dx","-op","multconst", "-opt", "const","0.125","-o","Eww.dx"]


p1=subprocess.Popen(command1)
p2=subprocess.Popen(command2)
p3=subprocess.Popen(command3)
p4=subprocess.Popen(command4)



dist=15 # the farest distance

r=1 # Starting from 1 vdw radius 

log=open("log.txt","w+")

import numpy as np


from gridData import Grid

voxel_num=[]

steps=np.arange(1,dist,0.5)

for r in steps:
    
    log.write("Displaced vdw within {0}".format(r))
    vdw=[gistpp,"-i","100ns-dTStrans-dens.dx","-i2","water_ligand.pdb","-op","defbp", "-opt","const",str(r),"-o","vdw.dx"]
    
    s1=subprocess.Popen(vdw)
    subprocess.Popen.wait(s1)
    
    
    #calculate the number of voxel that displaced
    
    g=Grid("vdw.dx")
    n=g.grid
    displace_voxel_num=np.count_nonzero(n==1)
    
    voxel_num.append(displace_voxel_num)
    
    
    
    
    
    
    

    
    for file in ["dTStrans.dx"]:
        
        f=file.split(".")[0]+"_displaced.dx"
        
        #print(f)
        
        displace=[gistpp,"-i","vdw.dx","-i2",file,"-op","mult","-o",f]
        
        s2=subprocess.Popen(displace)
        
        subprocess.Popen.wait(s2)
        
        displace_sum=[gistpp,"-i",f,"-op","sum"]
        
        
        s3=subprocess.Popen(displace_sum,stdout=log)
        
        subprocess.Popen.wait(s3)
        
        
    
log.close()
    
  
dTStrans_displace=[]
dTSorient_displace=[]

Esw_displace=[]
Eww_displace=[]
gO_displace=[]

output=open("log.txt","r").readlines()

for line in output:
    if "sum" in line:
        value=float(line.split()[-1])
        if "dTStrans" in line:
            
            dTStrans_displace.append(value)
        elif "dTSorient" in line:
            dTSorient_displace.append(value)
        elif "Esw" in line:
            Esw_displace.append(value)
        elif "Eww" in line:
            Eww_displace.append(value)
            
        elif "gO" in line:
            gO_displace.append(value)
            
average_gO=np.divide(np.array(gO_displace),np.array(voxel_num))

#print(average_gO)
import matplotlib.pyplot as plt

plt.subplot(221)
plt.plot(steps,dTStrans_displace,"r",label="dTStrans")
#plt.plot(steps,dTSorient_displace,"g",label="dTSorient")
#plt.plot(steps,Esw_displace,"grey",label="Esw")
#plt.plot(steps,Eww_displace,"blue",label="Eww")
plt.xlabel("displaced vdw radius in Å ")
plt.ylabel("Kcal/mol")
plt.legend()
plt.savefig("dTStrans100ns.png",dpi=400)
plt.show()

print(dTStrans_displace)

volume=[float(4/3)*3.14159*i for i in steps]

import numpy
numpy.divide(np.array(dTStrans_displace),np.array(volume))

plt.subplot(223)

plt.plot(steps,Eww_displace,"orange",label="Eww")
plt.xlabel("displaced vdw radius in Å ")
plt.ylabel("Energy in Kcal/mol")
plt.legend()

plt.subplot(222)
plt.plot(steps,average_gO,"black",label="averaged gO")
plt.xlabel("displaced vdw radius in Å ")
plt.ylabel("water density relative to bulk")
plt.legend()

plt.tight_layout()
plt.savefig("gist_displaced_radius_20.png", dpi=400)
plt.show()


print(dTStrans_displace)

g_dTStrans=Grid("gist-dTStrans-dens.dx").grid
values=[]
for i in range(70):
    for j in range(70):
        for k in range(70):
            values.append(g_dTStrans[i,j,k])
points=[ p for p in range(len(values))]

total_dTStrans=sum(values)*0.125

print(total_dTStrans)
plt.hist(values,50,facecolor="blue")

plt.xlabel("Voxels")
plt.ylabel("dTStrans")
plt.show()
         
print(dTStrans_displace)
