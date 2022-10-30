# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 09:39:09 2021

@author: Ghosty
"""

import numpy as np
from scipy.optimize import minimize, root
from miepythoncylinder import i_unpolarized_cyl
from numba import njit, int32, float64, complex128


def getCentreX(x,y):
    _xs = x[np.where(y>=0.999*max(y))]
    xcentre = 0.5*(_xs[0]+_xs[-1])
    return xcentre

def getFraunDiameter(dTheta,wavelength,m=1):
    return m*wavelength/1000/np.sin(dTheta)

def getFraunDThetaM(diameter,wavelength,m=1):
    return m*wavelength/diameter/1000

# def getMieDThetaM(diameter,wavelength,relref,m=1):
#     scaleParam = np.pi*diameter/wavelength*1000
#     getIntensity = lambda theta: i_unpolarized_cyl(relref,scaleParam,np.cos(theta))
#     minima = minimize(getIntensity,m*np.pi/scaleParam,method='Nelder-Mead',options={'xatol':1E-8}).x[0]
#     return minima

def getMieDThetaM(diameter,wavelength,relref,m=1):
    scaleParam = np.pi*diameter/wavelength*1000
    getIntensity = lambda theta: i_unpolarized_cyl(relref,scaleParam,np.cos(theta))
    minimaM = minimize(getIntensity,m*np.pi/scaleParam,method='Nelder-Mead',options={'xatol':1E-8}).x[0]
    return minimaM

# def getMieDiameter(dTheta1,wavelength,relref):
#     #Fraunhofer approximation
#     #wavelength (nm)
#     #tan dTheta = x/z
#     #D = (1)λ/sinθ1
#     #scaleParam0 = πD/λ = π/sinθ1 ~ π/θ1
#     scaleParam0 = np.pi/dTheta1
#     getIntensity = lambda theta, scaleParam: i_unpolarized_cyl(relref,scaleParam,np.cos(theta))[0]
#     getDTheta1 = lambda scaleParam: minimize(getIntensity,np.pi/scaleParam,args=(scaleParam[0],),
#                                               method='Nelder-Mead',options={'xatol':1E-8}).x[0]
#     scaleParam_opt = root(lambda scaleParam: dTheta1-getDTheta1(scaleParam),scaleParam0).x[0]
#     diameter = scaleParam_opt/np.pi*wavelength/1000
#     return diameter

def getMieDiameter(dTheta,wavelength,relref,m=1):
    #Fraunhofer approximation
    #wavelength (nm)
    #tan dTheta = x/z
    #D = (1)λ/sinθ1
    #scaleParam0 = πD/λ = π/sinθ1 ~ π/θ1
    scaleParam0 = m*np.pi/np.sin(dTheta)
    getIntensity = lambda theta, scaleParam: i_unpolarized_cyl(relref,scaleParam,np.cos(theta))[0]
    getDThetaM = lambda scaleParam: minimize(getIntensity,m*np.pi/scaleParam,args=(scaleParam[0],),
                                              method='Nelder-Mead',options={'xatol':1E-8}).x[0]
    scaleParam_opt = root(lambda scaleParam: dTheta-getDThetaM(scaleParam),scaleParam0).x[0]
    diameter = scaleParam_opt/np.pi*wavelength/1000
    return diameter

def getMRange(xdata,screenZ,diameter,wavelength,cPos=None):
    print(cPos)
    #diameter in microns
    #wavelength in nm
    #screenZ in cm
    #x in mm
    get_dm = lambda deltaX: int(np.sign(deltaX)*round(diameter/wavelength*1000/(1+(screenZ*10/deltaX)**2)**0.5,0))
    if cPos is None: cPos = (max(xdata)+min(xdata))/2
    deltaXr = max(xdata)-cPos
    m_max = get_dm(deltaXr)
    m_max = max(m_max,1)
    deltaXl = min(xdata)-cPos
    m_min = get_dm(deltaXl)
    m_min = min(m_min,-1)
    return m_min,m_max

if __name__ == "__main__":
    from miepythoncylinder import mie_S1_S2_cyl
    from matplotlib import pyplot as plt
    diameter = 10 #microns
    wavelength = 532 #nm
    scaleParam = np.pi*diameter/wavelength*1000
    thetas = np.linspace(-45,45,360)/180*np.pi
    mu = np.cos(thetas)
    m = 2.27-0.64j
    S1, S2 = mie_S1_S2_cyl(m,scaleParam,mu)
    plt.plot(thetas,S1**2,label="S1")
    plt.plot(thetas,S2**2,label="S2")
    I = (S1**2+S2**2)/2
    plt.plot(thetas,I,label="unpol")
    plt.legend()