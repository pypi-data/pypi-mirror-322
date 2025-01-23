"""
this file gathers functions for stretching frequencies of mixed p-g modes
"""

import numpy as _np
from scipy.integrate import quad as _quad

def zeta(nu,par_p,q,dpi1): #par_p=[numax, Dnu, eps_p, a2_p, d01]
    nmax=par_p[0]/par_p[1]-par_p[2]
    n_proxy=_np.floor((nu+par_p[4])/par_p[1]-0.5-par_p[2])
    n_p = _np.arange(_np.min(n_proxy)-2,_np.max(n_proxy)+3)

    nup=par_p[1]*(n_p+0.5+par_p[2]+0.5*par_p[3]*(n_p-nmax)**2)-par_p[4]

    i0=_np.searchsorted(nup, nu)-1
    nup0=nup[i0]
    dnup=nup[i0+1]-nup[i0]
    
    theta=_np.pi*(nu-nup0)/dnup

    tmp=_np.sin(theta)**2 + (_np.cos(theta)*q)**2

    tmp = 1. + q * nu**2 * dpi1/dnup/tmp

    return 1./tmp

def zetabis(nu,par_p,q,dpi1):
    nmax=par_p[0]/par_p[1]-par_p[2]
    n_proxy=_np.floor((nu+par_p[4])/par_p[1]-0.5-par_p[2])

    nup0=par_p[1]*(n_proxy+0.5+par_p[2]+0.5*par_p[3]*(n_proxy-nmax)**2)-par_p[4]
    dnup=par_p[1]*(1.+par_p[3]*(n_proxy-nmax+0.5))
    
    theta=_np.pi*(nu-nup0)/dnup

    tmp=_np.sin(theta)**2 + (_np.cos(theta)*q)**2

    tmp = 1. + q * nu**2* dpi1/dnup/tmp

    return 1./tmp

def dtaudnu(nu,par_p,q,dp1):
    z=zeta(nu,par_p,q,dp1)
    dtau=1./(z*nu*nu)
    return dtau

def tau(nu,nu0,par_p,q,dpi1): #tau(nu) where nu0 is the reference for tau=0
    r,_ = _quad(dtaudnu,nu,nu0,args=(par_p,q,dpi1))
    return r

def tauOG(nu,par_p,q,dpi1): #tau(nu) where nu0 is the reference for tau=0
    nmax=par_p[0]/par_p[1]-par_p[2]
    n_proxy=_np.floor((nu+par_p[4])/par_p[1]-0.5-par_p[2])
    n_p = _np.arange(_np.min(n_proxy)-2,_np.max(n_proxy)+3)

    nup=par_p[1]*(n_p+0.5+par_p[2]+0.5*par_p[3]*(n_p-nmax)**2)-par_p[4]

    i0=_np.searchsorted(nup, nu)-1
    nup0=nup[i0]
    dnup=nup[i0+1]-nup[i0]
    
    theta=_np.pi*(nu-nup0)/dnup

    r = 1./nu + dpi1/_np.pi * _np.arctan(q/_np.tan(theta))
    
    return r

