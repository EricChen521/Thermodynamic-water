#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 10:49:36 2019

@author: Eric Chen, Graduate Center, CUNY

@ Prof. Kurtzman's Lab
"""

import os 

os.chdir("/Users/eric/Desktop/TI-Water/small_solvation/NPT")

# calculate water_lig solvation energy 

from gridData import Grid

import numpy as np

E_bulk=0.125*np.sum(Grid("pure_water-gist-Eww-dens.dx").grid)

Eww_bulk=Grid("pure_water-gist-Eww-dens.dx").grid

mean_E_bulk=np.mean(Grid("pure_water-gist-Eww-dens.dx").grid)

std_E_bulk=np.std(Grid("pure_water-gist-Eww-dens.dx").grid)

lower1=mean_E_bulk - 3*std_E_bulk
higher1=mean_E_bulk + 3*std_E_bulk

ori_bulk=0.125*np.sum(Grid("pure_water-gist-dTSorient-dens.dx").grid)

mean_ori_bulk=np.mean(Grid("pure_water-gist-dTSorient-dens.dx").grid)

std_ori_bulk=np.std(Grid("pure_water-gist-dTSorient-dens.dx").grid)

lower2=mean_ori_bulk - 3* std_ori_bulk
higher2=mean_ori_bulk + 3*std_ori_bulk

trans_bulk=0.125*np.sum(Grid("pure_water-gist-dTStrans-dens.dx").grid)

mean_trans_bulk=np.mean(Grid("pure_water-gist-dTStrans-dens.dx").grid)
std_trans_bulk=np.std(Grid("pure_water-gist-dTStrans-dens.dx").grid)

lower3=mean_trans_bulk - 3 *std_trans_bulk
higher3=mean_trans_bulk + 3 *std_trans_bulk


E_sw_water_lig=0.125*np.sum(Grid("water_lig_gist-Esw-dens.dx").grid)
E_ww_water_lig=0.125*np.sum(Grid("water_lig_gist-Eww-dens.dx").grid)

ori_water_lig=0.125*np.sum(Grid("water_lig_gist-dTSorient-dens.dx").grid)
trans_water_lig=0.125*np.sum(Grid("water_lig_gist-dTStrans-dens.dx").grid)


delta_E = E_sw_water_lig + E_ww_water_lig - E_bulk

delta_S = ori_water_lig + trans_water_lig - ori_bulk - trans_bulk

delta_G= delta_E - delta_S

print(delta_G)

#filter the values in mean +/- 3*std

import copy
E_ww_lig=Grid("water_lig_gist-Eww-dens.dx").grid

np.sum(E_ww_lig)

temp1=copy.deepcopy(E_ww_lig)

temp1[(temp1>lower1) & (temp1<higher1)]=0

filtered_Eww_water_lig=0.125*np.sum(temp1)


ori_lig=Grid("water_lig_gist-dTSorient-dens.dx").grid

temp2=copy.deepcopy(ori_lig)

temp2[(temp2>lower2) & (temp2<higher2)]=0

filtered_ori=0.125*np.sum(temp2)




trans_lig=Grid("water_lig_gist-dTStrans-dens.dx").grid

temp3=copy.deepcopy(trans_lig)

temp3[(temp3>lower3) & (temp3<higher3)]=0

filtered_trans=0.125*np.sum(temp3)


filtered_delta_S= filtered_trans + filtered_ori

filtered_delta_E=E_sw_water_lig + filtered_Eww_water_lig

filtered_delta_G=filtered_delta_E - filtered_delta_S

print(filtered_delta_G)


# filter the bulk voxels by energy, oxygen density, ori, trans 


O_bulk=Grid("pure_water-gist-gO.dx").grid

mean_O=np.mean(O_bulk)
std_O=np.std(O_bulk)

lower4=mean_O - 3*std_O

higher4=mean_O + 3 * std_O

O_lig=Grid("water_lig_gist-gO.dx").grid

four_filtered_voxels=[]
three_filtered_voxels=[]
one_filtered_voxels=[]

np.max(E_ww_lig)
np.min(E_ww_lig)

np.max(ori_lig)
np.min(ori_lig)

for i in range(50):
    
    for j in range(50):
        
        for k in range(50):
            
            
            
            if lower1<=E_ww_lig[i,j,k]<= higher1 and lower2<=ori_lig[i,j,k]<=higher2 and \
            lower3<=trans_lig[i,j,k]<=higher3 and lower4<=O_lig[i,j,k]<=higher4:
                #print("love")
                four_filtered_voxels.append((i,j,k))
                
            if  lower2<=ori_lig[i,j,k]<=higher2 and lower3<=trans_lig[i,j,k]<=higher3 and lower4<=O_lig[i,j,k]<=higher4  :
                three_filtered_voxels.append((i,j,k))
                
            if lower1<=E_ww_lig[i,j,k]<= higher1 :
                
                one_filtered_voxels.append((i,j,k))
                
  


              
import matplotlib.pyplot as plt   

plt.subplot(121)
plt.hist(E_ww_lig.reshape(-1),bins=100,color="blue",label= "restrained_single_water")
plt.xlabel("Eww-dens")
plt.legend()

plt.subplot(122)

plt.hist(Eww_bulk.reshape(-1),bins=100,color="orange",label= "pure water")
plt.xlabel("Eww-dens")

plt.legend()

plt.tight_layout()
plt.show()        
                
np.sum(E_ww_lig) * 0.125    

np.sum(Eww_bulk)  * 0.125

            



