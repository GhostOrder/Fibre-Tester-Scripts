# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 02:14:49 2022

@author: Ghosty
"""

from matplotlib import pyplot as plt
import numpy as np
from scipy.optimize import minimize
import pandas as pd

file = r'G:/My Drive/Msc. in Materials Engineering/Thesis/Tensile Specimens/Tensile Data/621e55b6/005.csv'
df = pd.read_csv(file)

positions = df.iloc[:,0].to_numpy()
loads = df.iloc[:,1].to_numpy()

plt.plot(positions,loads,linewidth=1)

max_force_0 = loads[0]
max_disp_0 = positions[0]
for i in range(1,positions.size):
    if loads[i] > max_force_0:
        max_force_0 = loads[i]
        max_disp_0 = positions[i]
offset_0 = 0.02
background_0 = -10

# max_disp_0 = 0.027-offset_0
# max_force_0 = max_force_0-background_0

margin = 0.001
weights = np.ones_like(positions)
#weights[np.where(loads<max_force_0*1)]=0
weights[np.where(positions<0.025)]=0
# weights[np.where((positions>0.023984)&(positions<0.028))]=0
# weights[np.where((positions>=0.028))]=1
weights[np.where(positions>offset_0+max_disp_0+margin)] = 1
weights[np.where((positions>offset_0+max_disp_0)&(positions<=offset_0+max_disp_0+margin))]=0
weights = weights/sum(weights)

def func_objective(posArr,loadsArr,max_force,max_disp,background,offset):
    estim = func_tensCurve(posArr,max_force,max_disp,background,offset)
    resid = loadsArr-estim
    objective = np.dot(weights,resid**2)
    return objective


def func_tensCurve(posArr,max_force,max_disp,background,offset):
    slope = max_force/max_disp
    loadArr = np.ones_like(posArr)*background
    for i in range(loadArr.size):
        if posArr[i] > offset and posArr[i] < offset+max_disp: 
            loadArr[i] = background + slope*(posArr[i]-offset)
    return loadArr

def wrapper_func_objective(params,posArr,loadsArr):
    max_force, max_disp, background, offset = params
    return func_objective(posArr,loadsArr,max_force,max_disp,background,offset)

params0 = np.array([max_force_0,max_disp_0,background_0,offset_0])
res = minimize(wrapper_func_objective,params0,args=(positions,loads),method='Nelder-Mead')
max_force_1,max_disp_1,background_1,offset_1 = res.x
estimates = func_tensCurve(positions,max_force_1,max_disp_1,background_1,offset_1)

#max_force_1 is in lb
# max_force_mN = max_force_1*4.4482216153*1000
# max_disp_mm = max_disp_1*25.4
# offset_mm = offset_1*25.4

# print("Max Force: {:.6f} mN".format(max_force_mN))
# print("Displacement: {:.6f} mm".format(max_disp_mm))
# print("Offset: {:.6f} mm".format(offset_mm))

print("Max Stress: {:.6f} MPa".format(max_force_1))
print("Elongation: {:.6f} mm/mm".format(max_disp_1))
print("Offset: {:.6f} mm/mm".format(offset_1))

gauge_length = 5
print("Corrected length: {:.6f} mm".format((1+offset_1)*gauge_length))

plt.plot(positions,estimates,linewidth=1)