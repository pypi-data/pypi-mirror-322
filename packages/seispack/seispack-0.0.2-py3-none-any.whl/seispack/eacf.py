import numpy as np

def eacf(nu, sp, *, nurange=None, fac=1.2, over=10, nDnu=5):
    """
    look for the large separation of a spectrum by computing it envelope autocorrelation function.
    @param nu: array containing the frequencies (in µHz) where the spectrum is provided
    @param sp: array containing the power spectrum (or the spectral density)
    optional inputs
    @param nurange: 2-elements list containing the interval to scan for numax. 
                    The interval goes from nurange[0] to nu.max + nurange[1]
    @param fac: from one step to the next, tested numax is multiplied by fac (default 1.2) 
    @param over: oversampling used to compute the FFT (default: 10)
    @param nDu: controls the width of the envelop on which the ACF is performed.
                it is provided in unit of large separation (default: 5)
    @result Dnu_eacf, numax_eacf: large separation and numax found by the method
    No error estimate are performed.
    After:
     - I. W. Roxburgh & S. V. Vorontsov (2006), MNRAS 369, 1491
     - B. Mosser & T. Appourchaux (2009), A&A 508, 877
)
    """

    if nurange is None:
        if nu.max()>1000: #long cadence data
            nurange=[100.,-500.]
        else: # short cadence data
            nurange=[10.,-50.]
    if nurange[1]>0.:
        print("nurange[1] must be negative")
        return 0,0
    numax=nurange[0]
    nuend=nu.max()+nurange[1]
    nubin=nu[1]-nu[0]
    x=[]
    y=[]
    nuc=[]

    lawe=0.791 # exponent of the scaling relation between Dnu and numax
    lawc=0.233 # factor of the relation: Dnu ~ lawc*numax**lawe

    while (numax < nuend):
        Dnu=lawc*numax**lawe
        nuindex=(nu>numax-nDnu*Dnu)&(nu<numax+nDnu*Dnu)
        sp1=sp[nuindex]
        npt=sp1.size
        sp1=sp1*np.hanning(npt)
        sp1=np.pad(sp1,(0,(over-1)*npt))
        acf=np.abs(np.fft.fft(sp1, norm="forward"))
        tacf=np.fft.fftfreq(over*npt,d=nubin)
        y.append(acf[2*over:over//2*npt].max())
        x.append(tacf[2*over+np.argmax(acf[2*over:over//2*npt])])
        nuc.append(numax)
        numax = numax*fac

    x=np.array(x)
    y=np.array(y)
    nuc=np.array(nuc)

    i=np.argmax(y)
    Dnu_eacf=2./x[i]
    numax_eacf = nuc[i]
    if(i > 0 and i < nuc.max()-1):
        Dp=np.log(y[i+1]/y[i])
        Dm=np.log(y[i-1]/y[i])
        correction=0.5*(1.+fac)*(Dp/fac**2+Dm)/(Dp/fac+Dm)
        numax_eacf = numax_eacf*correction

    lnfac=(lawe*np.log(numax_eacf)+np.log(lawc))/np.log(Dnu_eacf)
    roundfac = int(np.round(lnfac/np.log(2.)))
    #verify if there is a possible factor of 2 in the value found for Dnu
    if roundfac == 0:
        pass
    elif roundfac == -1:
        Dnu_eacf /= 2
    elif roundfac == 1:
        Dnu_eacf *= 2
    else:
        print(f'Dnu is probably incorrect. Discrepancy from the scaling law by factor of {np.exp(lnfac)}')

    return Dnu_eacf, numax_eacf

