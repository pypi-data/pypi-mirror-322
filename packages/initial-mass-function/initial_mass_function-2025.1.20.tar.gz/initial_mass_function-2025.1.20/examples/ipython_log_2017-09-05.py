########################################################
# Started Logging At: 2017-09-05 16:01:44
########################################################

########################################################
# # Started Logging At: 2017-09-05 16:01:45
########################################################
get_ipython().magic('run pmf_evolution.py')
get_ipython().magic('run pmf_stats.py')
get_ipython().magic('run pmf_stats.py')
########################################################
# Started Logging At: 2017-09-05 16:42:55
########################################################

########################################################
# # Started Logging At: 2017-09-05 16:42:55
########################################################
get_ipython().magic('run pmf_stats.py')
########################################################
# Started Logging At: 2017-09-05 16:48:32
########################################################

########################################################
# # Started Logging At: 2017-09-05 16:48:33
########################################################
get_ipython().magic('run pmf_stats.py')
ChabrierPMF_AcceleratingSF_IS(np.linspace(0.03, 3)
)
self = ChabrierPMF_AcceleratingSF_IS
get_ipython().magic('paste')
def num_func(x, mass_):
    tm = self.tf1 * mass_**(1-self.j) / (x**(self.jf-self.j))
    return self.imf(x)*x**(self.j-self.jf-1) * np.exp(-tm / tau)

def integrate(lolim, mass_):
    integral = scipy.integrate.quad(num_func, lolim, self.mmax, args=(mass_), **kwargs)[0]
    return integral

numerator = np.vectorize(integrate)(np.where(self.mmin < mass, mass, self.mmin), mass)
mass = np.linspace(0.03, 3)
get_ipython().magic('paste')
def num_func(x, mass_):
    tm = self.tf1 * mass_**(1-self.j) / (x**(self.jf-self.j))
    return self.imf(x)*x**(self.j-self.jf-1) * np.exp(-tm / tau)

def integrate(lolim, mass_):
    integral = scipy.integrate.quad(num_func, lolim, self.mmax, args=(mass_), **kwargs)[0]
    return integral

numerator = np.vectorize(integrate)(np.where(self.mmin < mass, mass, self.mmin), mass)
import scipy.integrate
get_ipython().magic('paste')
def num_func(x, mass_):
    tm = self.tf1 * mass_**(1-self.j) / (x**(self.jf-self.j))
    return self.imf(x)*x**(self.j-self.jf-1) * np.exp(-tm / tau)

def integrate(lolim, mass_):
    integral = scipy.integrate.quad(num_func, lolim, self.mmax, args=(mass_), **kwargs)[0]
    return integral

numerator = np.vectorize(integrate)(np.where(self.mmin < mass, mass, self.mmin), mass)
kwargs={}
get_ipython().magic('paste')
def num_func(x, mass_):
    tm = self.tf1 * mass_**(1-self.j) / (x**(self.jf-self.j))
    return self.imf(x)*x**(self.j-self.jf-1) * np.exp(-tm / tau)

def integrate(lolim, mass_):
    integral = scipy.integrate.quad(num_func, lolim, self.mmax, args=(mass_), **kwargs)[0]
    return integral

numerator = np.vectorize(integrate)(np.where(self.mmin < mass, mass, self.mmin), mass)
tau = self.tau
tau
get_ipython().magic('paste')
def num_func(x, mass_):
    tm = self.tf1 * mass_**(1-self.j) / (x**(self.jf-self.j))
    return self.imf(x)*x**(self.j-self.jf-1) * np.exp(-tm / tau)

def integrate(lolim, mass_):
    integral = scipy.integrate.quad(num_func, lolim, self.mmax, args=(mass_), **kwargs)[0]
    return integral

numerator = np.vectorize(integrate)(np.where(self.mmin < mass, mass, self.mmin), mass)
numerator
result
result = self.tf1 * (1-self.j) * mass**(1-self.j) * numerator / self.denominator
result
self.denominator
########################################################
# Started Logging At: 2017-09-05 16:57:17
########################################################

########################################################
# # Started Logging At: 2017-09-05 16:57:18
########################################################
get_ipython().magic('run pmf_stats.py')
########################################################
# Started Logging At: 2017-09-05 17:01:03
########################################################

########################################################
# # Started Logging At: 2017-09-05 17:01:03
########################################################
get_ipython().magic('run pmf_stats.py')
self = ChabrierPMF_AcceleratingSF_IS
mass = np.linspace(0.03, 3)
import scipy.integrate
tau = self.tau
kwargs={}
get_ipython().magic('paste')
def num_func(x, mass_):
    tm = self.tf1 * mass_**(1-self.j) / (x**(self.jf-self.j))
    return self.imf(x)*x**(self.j-self.jf-1) * np.exp(-tm / tau)

def integrate(lolim, mass_):
    integral = scipy.integrate.quad(num_func, lolim, self.mmax, args=(mass_), **kwargs)[0]
    return integral

numerator = np.vectorize(integrate)(np.where(self.mmin < mass, mass, self.mmin), mass)
numerator
self.denominator
result = self.tf1 * (1-self.j) * mass**(1-self.j) * numerator / self.denominator
result
result * (result>0)
self.normfactor
McKeeOffner_AcceleratingSF_PMF(j=0, jf=0, tau=tau).m_integrate(0.03, 3)
McKeeOffner_AcceleratingSF_PMF(j=0, jf=0, tau=tau).m_integrate(0.03, 120)
McKeeOffner_AcceleratingSF_PMF(j=0, jf=0, tau=tau).m_integrate(10, 120)
McKeeOffner_AcceleratingSF_PMF(j=0.5, jf=0.75, tau=tau).m_integrate(10, 120)
McKeeOffner_AcceleratingSF_PMF(j=0.5, jf=0.75, tau=1.0)(10,50,120)
McKeeOffner_AcceleratingSF_PMF(j=0.5, jf=0.75, tau=1.0)([10,50,120])
np.asarray(5)
McKeeOffner_AcceleratingSF_PMF(j=0.5, jf=0.75, tau=1.0)(np.array([10,50,120]))
########################################################
# Started Logging At: 2017-09-05 17:12:53
########################################################

########################################################
# # Started Logging At: 2017-09-05 17:12:53
########################################################
get_ipython().magic('paste')
import imf.imf, imf.pmf, imp
from imf.pmf import ChabrierPMF_AcceleratingSF_IS, ChabrierPMF_AcceleratingSF_TC, ChabrierPMF_AcceleratingSF_CA#, ChabrierPMF_AcceleratingSF_2CTC
import pylab as pl
import numpy as np
imp.reload(imf.imf)
imp.reload(imf.pmf)
imp.reload(imf.imf)
imp.reload(imf.pmf)

mmin = 0.033
get_ipython().magic('paste')
import imf.imf, imf.pmf, imp
imp.reload(imf.imf)
imp.reload(imf.pmf)
imp.reload(imf.imf)
imp.reload(imf.pmf)
from imf.pmf import ChabrierPMF_IS, ChabrierPMF_TC, ChabrierPMF_CA, ChabrierPMF_2CTC
from imf.pmf import KroupaPMF_IS, KroupaPMF_TC, KroupaPMF_CA, KroupaPMF_2CTC
from imf.pmf import McKeeOffner_AcceleratingSF_PMF, ChabrierPMF_AcceleratingSF_IS, ChabrierPMF_AcceleratingSF_TC, ChabrierPMF_AcceleratingSF_CA#, ChabrierPMF_AcceleratingSF_2CTC
import pylab as pl
import numpy as np

mmin = 0.033
mmax = 120
McKeeOffner_AcceleratingSF_PMF(j=0.5, jf=0.75, tau=1.0)(np.array([10,50,120]))
get_ipython().magic('debug')
McKeeOffner_AcceleratingSF_PMF(j=0.5, jf=0.75, tau=1.0, mmax=120)(np.array([10,50,120]))
get_ipython().magic('debug')
########################################################
# Started Logging At: 2017-09-05 17:17:02
########################################################

########################################################
# # Started Logging At: 2017-09-05 17:17:02
########################################################
get_ipython().magic('run pmf_stats.py')
get_ipython().magic('run pmf_evolution.py')
