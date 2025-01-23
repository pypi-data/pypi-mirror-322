import numpy as _np
import copy as _copy
# En developpement....
class FreqSet:
    def __init__(self, nu, l=[], m=[], n=[], err=[], unit='muHz'):

        self.nu = _np.array(nu)
        nmode = self.nu.size
        self.nmode = nmode
        self.nu = self.nu.reshape(nmode)

        if _np.size(err) == 1:
            self.err = _np.full(nmode,err)
        elif _np.size(err) == nmode:
            self.err = _np.array(err).reshape(nmode)
        else:
            self.err = _np.array([])
        self.nu = self.nu.astype(float)

        if _np.size(l) == 1:
            self.l = _np.full(nmode,l)
        elif _np.size(l) == nmode:
            self.l = _np.array(l).reshape(nmode)
        else:
            self.l = _np.array([])
        self.l = self.l.astype(int)

        if _np.size(m) == 1:
            self.m = _np.full(nmode,m)
        elif _np.size(m) == nmode:
            self.m = _np.array(m).reshape(nmode)
        else:
            self.m = _np.array([])
        self.m = self.m.astype(int)

        if _np.size(n) == 1:
            self.n = _np.full(nmode,n)
        elif _np.size(n) == nmode:
            self.n = _np.array(n).reshape(nmode)
        else:
            self.n = _np.array([])
        self.n = self.n.astype(int)

        self.unit = unit

    def toUnit(self,newunit: str):
        if newunit == 'Hz':
            if self.unit == 'muHz':
                self.nu  *= 1.e-6
                self.err *= 1.e-6
            elif self.unit == 'rads':
                self.nu  *= 1./(2.*_np.pi)
                self.err *= 1./(2.*_np.pi)
            elif self.unit == 's':
                self.nu  = 1./self.nu
                self.err = self.err * self.nu**2 # nu is already the frequency in Hz
            else:
                if(self.unit != 'Hz'): print("unknown current unit (Hz, muHz, rads, s): "+self.unit)
            self.unit = newunit
        elif newunit == 'muHz':
            if self.unit == 'Hz':
                self.nu  *= 1.e+6
                self.err *= 1.e+6
            elif self.unit == 'rads':
                self.nu  *= 1.e+6 / (2*_np.pi)
                self.err *= 1.e+6 / (2*_np.pi)
            elif self.unit == 's':
                self.nu  = 1.e+6/self.nu
                self.err = 1.e-6 * self.err * self.nu**2 # nu is already the frequency in µHe
            else:
                if(self.unit != 'muHz'): print("unknown current unit (Hz, muHz, rads, s): "+self.unit)
            self.unit = newunit
        elif newunit == 'rads':
            if self.unit == 'Hz':
                self.nu  *= 2.*_np.pi
                self.err *= 2.*_np.pi
            elif self.unit == 'muHz':
                self.nu  *= 2.e-6*_np.pi
                self.err *= 2.e-6*_np.pi
            elif self.unit == 's':
                self.nu  = 2.*_np.pi / self.nu
                self.err = self.err * self.nu**2 / (2*_np.pi)# nu is already the pulsation
            else:
                if(self.unit != 'rads'): print("unknown current unit (Hz, muHz, rads, s): "+self.unit)
            self.unit = newunit
        elif newunit == 's':
            if self.unit == 'Hz':
                self.nu  = 1. / self.nu
                self.err = self.err * self.nu**2 # nu is already the period in s
            elif self.unit == 'muHz':
                self.nu  = 1.e+6 / self.nu
                self.err = 1.e-6 * self.err * self.nu**2 # nu is already the period in s
            elif self.unit == 'rads':
                self.nu  = 2.*_np.pi / self.nu
                self.err = self.err * self.nu**2 / (2*_np.pi)
            else:
                if(self.unit != 's'): print("unknown current unit (Hz, muHz, rads, s): "+self.unit)
            self.unit = newunit
        else:
            print("unknown  new unit (Hz, muHz, rads, s): "+newunit)
        
        return self

    def copy(self):
        return _copy.deepcopy(self)

"""     def append(self,newset): # to be completed
        if newset.nmode == 0: return
        tmp=_copy.deepcopy(newset)
        print(type(newset),type(tmp))
        tmp.toUnit(self.unit)
        self.nu=_np.concatenate((self.nu,tmp.nu))

       # self.err=_np.concatenate((self.nerr,tmp))

        return self
    
    def __getitem__(self, i): # to be completed if needed...
        nu=self.nu[i]
        if(len(self.l)>0):
            l=self.l[i]
        else:   
            l=None #to be improved

        return nu, l
    

    
def append(set,newset): # to be completed
    if newset.nmode == 0: return
    tmp=_copy.deepcopy(newset)
    print("typetmp",type(tmp),type(tmp.nu))
    tmp=tmp.toUnit(set.unit)
    print("typetmp",type(tmp),type(tmp.nu))
    
    out=_copy.deepcopy(set)
    out.nu=_np.concatenate((set.nu,tmp.nu))
    
    # self.err=_np.concatenate((self.nerr,tmp))

    return out """


            




