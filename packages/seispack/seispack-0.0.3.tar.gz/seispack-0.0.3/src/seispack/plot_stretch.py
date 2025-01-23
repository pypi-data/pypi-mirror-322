import numpy as _np
import matplotlib.pyplot as _plt
from .stretch import tau
from .stretch import tauOG
from .stretch import zeta

def plot_stretch(par_p, q, dpi,
                 nuobs, sigmaobs=[], numod=[], 
                 filename='', OG=False): #numax, DNu (in par_p), nu, etc. in µHz ; dpi in s or Ms
    """
    plot a stretched echelle diagramme from a frequency list
    """
    if(dpi > 1.): #second OR Mega-second?
        dps=dpi
        dp1=dpi*1.e-6
    else:
        dp1=dpi
        dps=dpi*1.e6

    if(type(numod) == tuple):
        numodt=numod
        if(len(numodt)>3): numodt=numodt[0:3]
    else:
        numodt=(numod,)
    col_mod=['red','orange','magenta']
    nmodel=len(numodt)

    t0=0.
    
    for imod in range(nmodel):
        nu=numodt[imod]
        n1=_np.size(nu)
        if(n1>0):
            nu1=_np.array(nu)
            nu1.resize(n1)
            nu1.sort()
            nu1=_np.flip(nu1)
        
            if(OG):
                t = tauOG(nu1,par_p,q,dp1)
            else:
                t=_np.zeros(n1)
                if(t0==0.): t0=1./nu1[0]
                t[0]=t0
                for i in range(n1-1):
                    t[i+1]=t[i]+tau(nu1[i+1],nu1[i],par_p,q,dp1)
            
            ts=t*1.e6
            _plt.plot(ts%dps,nu1,'o', mec=col_mod[imod], mfc='none')
            _plt.plot(ts%dps + dps,nu1,'o', mec=col_mod[imod], mfc='none')
            
        
    ax=_plt.xlim([0,2*dps])
    nu1=_np.array(nuobs)
    n1=_np.size(nuobs)
    nu1.resize(n1)
    sor=nu1.argsort()
    sor=_np.flip(sor)
    nu1=nu1[sor]
    
    if(_np.size(sigmaobs)==n1):
        sig=_np.array(sigmaobs)
        sig.resize(n1)
        sig=sig[sor]
    elif(_np.size(sigmaobs)==1):
        sig=_np.full(n1,sigmaobs)
    else:
        sig=0.
        
    err=sig/(zeta(nu1,par_p,q,dp1)*nu1*nu1)

    if(OG):
        t = tauOG(nu1,par_p,q,dp1)
    else:
        t=_np.zeros(n1)
        if(t0>0.):
            t[0]=t0+tau(nu1[0],1/t0,par_p,q,dp1)
        else:
            t[0]=1./nu1[0]
        for i in range(n1-1):
            t[i+1]=t[i]+tau(nu1[i+1],nu1[i],par_p,q,dp1)
        
    ts=t*1.e6
    errs=err*1.e6
    _plt.errorbar(ts%dps,nu1,fmt='b.',xerr=errs)
    _plt.errorbar(ts%dps + dps,nu1,fmt='b.',xerr=errs)
    _plt.axvline(x=dps,ls=':',c='k')
    _plt.xlabel(r'$\tau$ mod $\Delta\Pi_1$ ({:.2f} s)'.format(dps))
    _plt.ylabel(r'Frequency [$\mu$Hz]')
    _plt.xlim(0,2*dps)

    if filename == '':
        _plt.show()
    else:
        _plt.savefig(filename,dpi=200)
        _plt.close()

    return
