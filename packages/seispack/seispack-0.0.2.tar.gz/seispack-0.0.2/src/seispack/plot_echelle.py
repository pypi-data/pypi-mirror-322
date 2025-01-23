import numpy as _np
import matplotlib.pyplot as _plt

def plot_echelle(dnu,nuobs,lobs=[],sigmaobs=[],numod=[],lmod=[],shift=0,filename=''):
    """
    plot an echelle diagramme from a frequency list
    """

    if(type(numod) == tuple):
        numodt=numod
        lmodt=lmod
        if(len(numodt)>3): numodt=numodt[0:3]
    else:
        numodt=(numod,)
        lmodt=(lmod,)
    col=['red','orange','magenta']

    nmodel=len(numodt)
    for imod in range(nmodel):
        num = _np.array(numodt[imod])
        if len(lmodt)==nmodel:
            lm  = _np.array(lmodt[imod])
        else:
            lm = _np.array([])
            
        if(_np.size(num)>0):
            if(_np.size(lm) != _np.size(num)):
                _plt.plot((num+shift)%dnu,num,'o', mfc='none', mec=col[imod])
            else:
                nu=num[lm == 0]
                _plt.plot((nu+shift)%dnu,nu,'v', mfc='none', mec=col[imod])
                nu=num[lm == 1]
                _plt.plot((nu+shift)%dnu,nu,'o', mfc='none', mec=col[imod])
                nu=num[lm > 1]
                _plt.plot((nu+shift)%dnu,nu,'.', mfc='none', mec=col[imod])

    if(_np.size(lobs) != _np.size(nuobs)):

        _plt.errorbar((nuobs+shift)%dnu,nuobs,fmt='b.',xerr=sigmaobs)
    else:
        
        if(_np.size(sigmaobs)==1):
            sig=_np.full(_np.size(nuobs),sigmaobs)
        elif(_np.size(sigmaobs)==_np.size(nuobs)):
            sig=_np.array(sigmaobs)
        else:
            sig=_np.zeros(_np.size(nuobs))
            
        nu=nuobs[lobs == 0]
        err=sig[lobs == 0]
        _plt.errorbar((nu+shift)%dnu,nu,fmt='bv', mec='none',xerr=err)
        nu=nuobs[lobs == 1]
        err=sig[lobs == 1]
        _plt.errorbar((nu+shift)%dnu,nu,fmt='b.',xerr=err)
        nu=nuobs[lobs > 1]
        err=sig[lobs > 1]
        _plt.errorbar((nu+shift)%dnu,nu,fmt='bx',xerr=err)
    _plt.xlabel(r'$\nu$ mod $\Delta\nu$ ({:.2f} $\mu$Hz)'.format(dnu))
    _plt.ylabel(r'Frequency [$\mu$Hz]')
    _plt.xlim(0,dnu)

    if filename == '':
        _plt.show()
    else:
        _plt.savefig(filename,dpi=200)
        _plt.close()
    
