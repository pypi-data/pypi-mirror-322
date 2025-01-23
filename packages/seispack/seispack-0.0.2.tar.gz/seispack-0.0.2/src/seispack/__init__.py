"""
package for asteroseismic analysis
"""
import importlib.metadata
__version__ = importlib.metadata.version(__package__)

from .plot_stretch import plot_stretch
from .plot_echelle import plot_echelle
from .plot_echelle_image import plot_echelle_image
from .eacf import eacf
from .psd import psd
#from .FreqSet import FreqSet
from .basic import *

plot_sed = plot_stretch
plot_ced = plot_echelle

