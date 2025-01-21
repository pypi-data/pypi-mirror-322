########################################################
# Started Logging At: 2017-09-01 12:54:59
########################################################

########################################################
# # Started Logging At: 2017-09-01 12:55:00
########################################################
from imf.imf import Kroupa
Kroupa()
Kroupa().integrate(1,10, numerical=False)
Kroupa().integrate(1,10, numerical=True)
Kroupa().integrate(0.1,10, numerical=True)
Kroupa().integrate(0.1,10, numerical=False)
########################################################
# Started Logging At: 2017-09-01 12:58:17
########################################################

########################################################
# # Started Logging At: 2017-09-01 12:58:18
########################################################
from imf.imf import Kroupa
Kroupa().integrate(0.1,10, numerical=False)
Kroupa().integrate(0.1,10, numerical=True)
Kroupa().integrate(0.1,0.5, numerical=True)
Kroupa().integrate(0.1,0.5, numerical=False)
########################################################
# Started Logging At: 2017-09-01 13:00:32
########################################################

########################################################
# # Started Logging At: 2017-09-01 13:00:32
########################################################
from imf.imf import Kroupa
Kroupa().integrate(0.1,0.5, numerical=False)
Kroupa().integrate(0.1,0.5, numerical=True)
Kroupa().normfactor
Kroupa().integrate(0.1,0.4, numerical=True)
Kroupa().integrate(0.1,0.4, numerical=True)
Kroupa().integrate(0.03,0.07, numerical=True)
Kroupa().integrate(0.03,0.07, numerical=False)
Kroupa().integrate(0.1,0.4, numerical=True)
Kroupa().integrate(0.1,0.4, numerical=False)
Kroupa().integrate(0.1,0.5, numerical=True)
Kroupa().integrate(0.1,0.5, numerical=False)
Kroupa().integrate(0.1,0.49999, numerical=False)
Kroupa().integrate(0.1,0.49999, numerical=True)
np.finfo
np.finfo()
np.finfo(np.float)
np.finfo(np.float).eps
########################################################
# Started Logging At: 2017-09-01 13:08:25
########################################################

########################################################
# # Started Logging At: 2017-09-01 13:08:26
########################################################
from imf.imf import Kroupa, kroupa, test_kroupa_integral
test_kroupa_integral()
########################################################
# Started Logging At: 2017-09-01 13:08:48
########################################################

########################################################
# # Started Logging At: 2017-09-01 13:08:48
########################################################
from imf.imf import Kroupa, kroupa, test_kroupa_integral
test_kroupa_integral()
get_ipython().magic('debug')
get_ipython().magic('debug')
########################################################
# Started Logging At: 2017-09-01 13:10:54
########################################################

########################################################
# # Started Logging At: 2017-09-01 13:10:54
########################################################
from imf.imf import Kroupa, kroupa, test_kroupa_integral
test_kroupa_integral()
get_ipython().magic('debug')
get_ipython().magic('debug')
########################################################
# Started Logging At: 2017-09-01 13:11:23
########################################################

########################################################
# # Started Logging At: 2017-09-01 13:11:23
########################################################
from imf.imf import Kroupa, kroupa, test_kroupa_integral
test_kroupa_integral()
get_ipython().magic('debug')
########################################################
# Started Logging At: 2017-09-01 13:13:11
########################################################

########################################################
# # Started Logging At: 2017-09-01 13:13:12
########################################################
from imf.imf import Kroupa, kroupa, test_kroupa_integral
test_kroupa_integral()
x = [1,2,3]
np.diff(x)
break1=0.08
break2=0.5
mlow=0.01
mhigh = 10
m = [mlow, break1, break2, mhigh]
for elt1, elt2 in zip(m, m[1:]):
        if elt2 < elt1:
                m.remove(elt2)
        
m
mhigh = 0.2
m = [mlow, break1, break2, mhigh]
for elt1, elt2 in zip(m, m[1:]):
        if elt2 < elt1:
                m.remove(elt2)
        
m
mhigh = 10
mlow = 0.1
for elt1, elt2 in zip(m, m[1:]):
        if elt2 < elt1:
                m.remove(elt2)
        
m
m = [mlow, break1, break2, mhigh]
for elt1, elt2 in zip(m, m[1:]):
        if elt2 < elt1:
                m.remove(elt2)
        
m
m = [mlow,
     break1 if mhigh > break1 and mlow < break1 else None,
     break2 if mhigh > break2 and mlow < break2 else None,
     mhigh]
m = [x for x in m if x is not None]
m
mlow
mlow = 0.01
m = [mlow,
     break1 if mhigh > break1 and mlow < break1 else None,
     break2 if mhigh > break2 and mlow < break2 else None,
     mhigh]
m = [x for x in m if x is not None]
m
mhigh = 0.2
m = [mlow,
     break1 if mhigh > break1 and mlow < break1 else None,
     break2 if mhigh > break2 and mlow < break2 else None,
     mhigh]
m = [x for x in m if x is not None]
m
########################################################
# Started Logging At: 2017-09-01 13:33:25
########################################################

########################################################
# # Started Logging At: 2017-09-01 13:33:26
########################################################
from imf.imf import Kroupa, kroupa, test_kroupa_integral
test_kroupa_integral()
get_ipython().magic('debug')
########################################################
# Started Logging At: 2017-09-01 13:35:23
########################################################

########################################################
# # Started Logging At: 2017-09-01 13:35:23
########################################################
from imf.imf import Kroupa, kroupa, test_kroupa_integral
test_kroupa_integral()
########################################################
# Started Logging At: 2017-09-01 13:35:45
########################################################

########################################################
# # Started Logging At: 2017-09-01 13:35:45
########################################################
from imf.imf import Kroupa, kroupa, test_kroupa_integral
test_kroupa_integral()
########################################################
# Started Logging At: 2017-09-01 13:36:06
########################################################

########################################################
# # Started Logging At: 2017-09-01 13:36:07
########################################################
from imf.imf import Kroupa, kroupa, test_kroupa_integral
test_kroupa_integral()
Kroupa().normfactor
def f(x):
    return x**-2

scipy.quad.integrate
import scipy.quad.integrate
def y(x):
    return f(x) * x

from scipy.integrate import quad
quad(y, 1, 3)
np.log(3)-np.log(1)
def f(x):
    return x**-2.5

quad(y, 1, 3)
(3**-0.5/-0.5) - (1**-0.5 / -0.5)
Kroupa().p1
p1 = Kroupa().p1
break1 - Kroupa().break1
kroupa.break1
break1 = Kroupa().break1
break2 = Kroupa().break2
p2 = kroupa.p2
p3 = kroupa.p3
binv = ((break1**(-(p1-1)) - mmin**(-(p1-1)))/(1-p1) +
        (break2**(-(p2-1)) - break1**(-(p2-1))) * (break1**(p2-p1))/(1-p2) +
        (- break2**(-(p3-1))) * (break1**(p2-p1)) * (break2**(p3-p2))/(1-p3))
b = 1./binv
c = b * break1**(p2-p1)
d = c * break2**(p3-p2)
mmin=kroupa.mmin
get_ipython().magic('paste')
binv = ((break1**(-(p1-1)) - mmin**(-(p1-1)))/(1-p1) +
        (break2**(-(p2-1)) - break1**(-(p2-1))) * (break1**(p2-p1))/(1-p2) +
        (- break2**(-(p3-1))) * (break1**(p2-p1)) * (break2**(p3-p2))/(1-p3))
b = 1./binv
c = b * break1**(p2-p1)
d = c * break2**(p3-p2)
b
c
d
def zeta(m):
        return (b*(m**(2-p1))/(2-p1) * (m<break1) +
                c*(m**(2-p2))/(2-p2) * (m>=break1) * (m<break2) +
                d*(m**(2-p3))/(2-p3) * (m>=break2))

zeta
zeta(0.02)
zeta(0.02)-zeta(0.01)
kroupa.m_integrate(0.01, 0.02, numerical=False)
kroupa.m_integrate(0.01, 0.02, numerical=True)
def f(x):
    return x**-2.5

def y(x):
    return f(x) * x

quad(y, 1.5, 3)
(3**-0.5/-0.5) - (1.5**-0.5 / -0.5)
def int_f(x):
    return x**-0.5 / -0.5

int_f(3)-int_f(1.5)
def zeta(m):
        return (b*(m**(2-p1))/(2-p1) * (m<break1) +
                c*(m**(2-p2))/(2-p2) * (m>=break1) * (m<break2) +
                d*(m**(2-p3))/(2-p3) * (m>=break2))

zeta
def int_zeta_m(m):
        return (b*(m**(2-p1))/(2-p1) * (m<break1) +
                c*(m**(2-p2))/(2-p2) * (m>=break1) * (m<break2) +
                d*(m**(2-p3))/(2-p3) * (m>=break2))

def zeta(m):
    return (b*(m**(-(p1))) * (m<break1) +
                        c*(m**(-(p2))) * (m>=break1) * (m<break2) +
                        d*(m**(-(p3))) * (m>=break2))

quad(zeta, 0.01, 0.02)
int_zeta_m(0.02)-int_zeta_m(0.01)
def zetam(m):
    return zeta(m) * m

quad(zeta, 0.01, 0.02)
quad(zeta_m, 0.01, 0.02)
quad(zetam, 0.01, 0.02)
########################################################
# Started Logging At: 2017-09-01 13:51:11
########################################################

########################################################
# # Started Logging At: 2017-09-01 13:51:12
########################################################
from scipy.integrate import quad
from imf.imf import Kroupa, kroupa, test_kroupa_integral
test_kroupa_integral()
########################################################
# Started Logging At: 2017-09-01 13:51:24
########################################################

########################################################
# # Started Logging At: 2017-09-01 13:51:24
########################################################
from imf.imf import Kroupa, kroupa, test_kroupa_integral
test_kroupa_integral()
########################################################
# Started Logging At: 2017-09-01 13:54:33
########################################################

########################################################
# # Started Logging At: 2017-09-01 13:54:34
########################################################
from imf.imf import Kroupa, kroupa, test_kroupa_integral
test_kroupa_integral()
########################################################
# Started Logging At: 2017-09-01 13:55:35
########################################################

########################################################
# # Started Logging At: 2017-09-01 13:55:36
########################################################
get_ipython().magic('run pmf_stats.py')
np.finfo(np.float)
########################################################
# Started Logging At: 2017-09-01 14:00:32
########################################################

########################################################
# # Started Logging At: 2017-09-01 14:00:33
########################################################
get_ipython().magic('run pmf_stats.py')
get_ipython().magic('ls *png')
get_ipython().system('open *integral.png')
get_ipython().system('open *integral*120.png')
get_ipython().system('open *integral*120.png')
get_ipython().system('open *integral*120.png')
mmax
kroupa(10)
kroupa(10, integral_form=True)
########################################################
# Started Logging At: 2017-09-01 14:36:54
########################################################

########################################################
# # Started Logging At: 2017-09-01 14:36:55
########################################################
from imf.imf import Kroupa, kroupa, test_kroupa_integral, Chabrier2005, chabrier2005, test_chabrier_integral
test_chabrier_integral()
########################################################
# Started Logging At: 2017-09-01 14:37:23
########################################################

########################################################
# # Started Logging At: 2017-09-01 14:37:24
########################################################
from imf.imf import Kroupa, kroupa, test_kroupa_integral, Chabrier2005, chabrier2005, test_chabrier_integral
test_chabrier_integral()
########################################################
# Started Logging At: 2017-09-01 14:37:45
########################################################

########################################################
# # Started Logging At: 2017-09-01 14:37:45
########################################################
from imf.imf import Kroupa, kroupa, test_kroupa_integral, Chabrier2005, chabrier2005, test_chabrier_integral
test_chabrier_integral()
########################################################
# Started Logging At: 2017-09-01 14:39:11
########################################################

########################################################
# # Started Logging At: 2017-09-01 14:39:12
########################################################
from imf.imf import Kroupa, kroupa, test_kroupa_integral, Chabrier2005, chabrier2005, test_chabrier_integral
test_chabrier_integral()
########################################################
# Started Logging At: 2017-09-01 14:39:58
########################################################

########################################################
# # Started Logging At: 2017-09-01 14:39:59
########################################################
from imf.imf import Kroupa, kroupa, test_kroupa_integral, Chabrier2005, chabrier2005, test_chabrier_integral
test_chabrier_integral()
chabrier2005(3)
chabrier2005(1)
chabrier2005(1.00001)
get_ipython().system('open *integral*3.png')
chabrier2005(0.05)
chabrier2005(0.033, integral_form=True)
chabrier2005(0.05, integral_form=True)
masses = np.logspace(np.log10(0.033), np.log10(3))
pl.figure()
import pylab as pl
pl.plot(masses, chabrier2005(masses, integral_form=True))
pl.figure()
pl.plot(masses, chabrier2005(masses, integral_form=False))
########################################################
# Started Logging At: 2017-09-01 14:48:20
########################################################

########################################################
# # Started Logging At: 2017-09-01 14:48:21
########################################################
from imf.imf import Kroupa, kroupa, test_kroupa_integral, Chabrier2005, chabrier2005, test_chabrier_integral
test_chabrier_integral()
import pylab as pl
masses = np.logspace(np.log10(0.033), np.log10(3))
pl.plot(masses, chabrier2005(masses, integral_form=True))
########################################################
# Started Logging At: 2017-09-01 15:04:26
########################################################

########################################################
# # Started Logging At: 2017-09-01 15:04:26
########################################################
from imf.imf import Kroupa, kroupa, test_kroupa_integral, Chabrier2005, chabrier2005, test_chabrier_integral
test_chabrier_integral()
########################################################
# Started Logging At: 2017-09-01 15:13:31
########################################################

########################################################
# # Started Logging At: 2017-09-01 15:13:31
########################################################
from imf.imf import Kroupa, kroupa, test_kroupa_integral, Chabrier2005, chabrier2005, test_chabrier_integral
test_chabrier_integral()
########################################################
# Started Logging At: 2017-09-01 15:14:00
########################################################

########################################################
# # Started Logging At: 2017-09-01 15:14:00
########################################################
get_ipython().magic('run ~/repos/imf/examples/pmf_comparison.py')
########################################################
# Started Logging At: 2017-09-01 15:14:16
########################################################

########################################################
# # Started Logging At: 2017-09-01 15:14:16
########################################################
get_ipython().magic('run pmf_stats.py')
########################################################
# Started Logging At: 2017-09-01 15:31:31
########################################################

########################################################
# # Started Logging At: 2017-09-01 15:31:32
########################################################
########################################################
# Started Logging At: 2017-09-01 15:31:32
########################################################

########################################################
# # Started Logging At: 2017-09-01 15:31:33
########################################################
get_ipython().magic('run pmf_stats.py')
get_ipython().magic('run ~/repos/imf/examples/pmf_comparison.py')
