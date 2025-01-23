import numpy as np
import matplotlib.pyplot as plt

def plot_echelle_image(nu, sp, Dnu, numax, *, 
                       Norder=(11,11), nushift=0.,
                       rebin_factor=0, 
                       smooth='Epanechnikov', smooth_window=21, qplot=0.97):
    """
    plot an echelle diagramme as an image from a power spectrum
    """

    binsize=nu[1]-nu[0]
    
    if rebin_factor is None:
        rebin=1
    elif rebin_factor < 1: #automatique: au plus 1000 point en x
        rebin=max(1,round(Dnu/binsize/1000))
    else:
        rebin=rebin_factor
        
    window=2*(round(max(1,smooth_window)+1)//2)-1
    nmax=round(numax/Dnu)
    nu0=max(nu.min(),(nmax-Norder[0])*Dnu+nushift)
    nu1=min(nu.max(),(nmax+Norder[1])*Dnu+nushift)
    window_nu=window*binsize

    
    if smooth == None or smooth == 'None' or smooth_window==1:
        spc=sp
        print("No smoothing")
    else:
        if smooth =='Epanechnikov':
            Kernel=1-(2*(np.arange(1,window+1))/(window+1)-1)**2
            print("Epanechnikov smoothing, window=",window,window_nu)
        elif smooth =='Hanning':
            Kernel=np.hanning(window)
            print("Hanning smoothing, window=",window,window_nu)
        else:
            Kernel=np.ones(window)
            print("Carbox smoothing, window=",window,window_nu)
        Kernel=Kernel/Kernel.sum()
        spc=np.convolve(sp,Kernel,mode='same')

    npt0=sp.size
    if(rebin > 1):
        nptr=npt0//rebin
        spr=spc[:rebin*nptr].reshape(nptr,rebin).mean(1)
        nur=nu[:rebin*nptr].reshape(nptr,rebin).mean(1)
        print("Rebinning factor:",rebin)
    else:
        nptr=npt0
        spr=spc
        nur=nu
        print("No rebinning")
        
    binsizer=nur[1]-nur[0]
    nptr_Dnu=round(Dnu/binsizer)
    Dnur=binsizer*nptr_Dnu

    i0=round((nu0-nur[0])/binsizer)
    nu0r=i0*binsizer
    norder=round((nu1-nu0r)/Dnur)
    i1=i0+norder*nptr_Dnu
    if (i1>nur.size):
        i1=i1-nptr_Dnu
        norder=norder-1

    imr=spr[i0:i1].reshape(norder,nptr_Dnu)

    x = np.arange(nptr_Dnu)*binsizer
    y = nur[i0:i1:nptr_Dnu]+0.5*Dnur

    vmax=np.quantile(imr,qplot)
    print("max, {q:.1f}% = {m:.3g}, {v:.3g}".format(q=qplot*100,m=imr.max(),v=vmax))
    plt.pcolormesh(x,y,imr,vmin=0,vmax=vmax)
    plt.xlabel(r'$\nu$ mod $\Delta\nu$ ({:.2f} $\mu$Hz)'.format(Dnur))
    plt.ylabel('frequency')
    
