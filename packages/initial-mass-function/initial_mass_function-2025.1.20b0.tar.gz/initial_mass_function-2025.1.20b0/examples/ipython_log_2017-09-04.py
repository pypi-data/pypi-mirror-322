########################################################
# Started Logging At: 2017-09-04 16:05:06
########################################################

########################################################
# # Started Logging At: 2017-09-04 16:05:06
########################################################
get_ipython().magic('run pmf_evolution.py')
########################################################
# Started Logging At: 2017-09-04 16:05:40
########################################################

########################################################
# # Started Logging At: 2017-09-04 16:05:40
########################################################
get_ipython().magic('run pmf_evolution.py')
get_ipython().magic('run pmf_evolution.py')
get_ipython().magic('run pmf_evolution.py')
self = Chabrier2005()
self = ChabrierPMF_AcceleratingSF_TC
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
numerator
self.mmin
mass[0]
integrate(self.mmin, mass[0])
integrate(mass[5], mass[5])
numerator[5]
get_ipython().magic('run pmf_evolution.py')
