########################################################
# Started Logging At: 2017-08-31 11:10:34
########################################################

########################################################
# # Started Logging At: 2017-08-31 11:10:35
########################################################
get_ipython().magic('run ~/repos/imf/examples/pmf_comparison.py')
get_ipython().magic('ls -lhrt')
get_ipython().system('open *mmax*png')
get_ipython().magic('run ~/repos/imf/examples/pmf_comparison.py')
get_ipython().magic('run ~/repos/imf/examples/pmf_comparison.py')
get_ipython().magic('run ~/repos/imf/examples/pmf_comparison.py')
from scipy.special import erf
kroupa.integrate(10,120)
kroupa.integrate()
kroupa.integrate(mmin,mmax)
kroupa.normalize(log=False, mmin=mmin, mmax=mmax)
kroupa.integrate(mmin,mmax)
kroupa.normfactor
kroupa.normalize(log=False, mmin=mmin, mmax=mmax)
kroupa.normfactor
kroupa.normalize(log=False, mmin=mmin, mmax=mmax)
kroupa.normfactor
kroupa.normalize(log=False, mmin=mmin, mmax=mmax)
kroupa.normfactor
kroupa.normalize(log=False, mmin=mmin, mmax=mmax)
kroupa.normfactor
########################################################
# Started Logging At: 2017-08-31 16:49:16
########################################################

########################################################
# # Started Logging At: 2017-08-31 16:49:17
########################################################
get_ipython().magic('run pmf_stats.py')
kroupa.normfactor
kroupa.integrate(mmin,mmax)
kroupa.normalize(log=False, mmin=mmin, mmax=mmax)
kroupa.normfactor
kroupa.normalize(log=False, mmin=mmin, mmax=mmax)
kroupa.normfactor
kroupa.m_integrate(mmin,mmax)
kroupa.m_integrate(3,mmax)
get_ipython().magic('paste')
mfs = {'ChabrierPMF_IS': ChabrierPMF_IS,
       'ChabrierPMF_TC': ChabrierPMF_TC,
       'ChabrierPMF_CA': ChabrierPMF_CA,
       'ChabrierPMF_2CTC': ChabrierPMF_2CTC,
       'ChabrierIMF': chabrier2005,
       'KroupaPMF_IS': KroupaPMF_IS,
       'KroupaPMF_TC': KroupaPMF_TC,
       'KroupaPMF_CA': KroupaPMF_CA,
       'KroupaPMF_2CTC': KroupaPMF_2CTC,
       'KroupaIMF': kroupa,
      }

for mf in mfs:
    total = mfs[mf].m_integrate(mmin, mmax)
    gt10 = mfs[mf].m_integrate(10, mmax)
    print("Mass fraction M>10 = {0:0.3f}".format(gt10/total))
get_ipython().magic('paste')
for mf in mfs:
    total = mfs[mf].m_integrate(mmin, mmax)[0]
    gt10 = mfs[mf].m_integrate(10, mmax)[0]
    print("Mass fraction M>10 = {0:0.3f}".format(gt10/total))
########################################################
# Started Logging At: 2017-08-31 16:58:34
########################################################

########################################################
# # Started Logging At: 2017-08-31 16:58:34
########################################################
get_ipython().magic('run pmf_stats.py')
get_ipython().magic('paste')
for mf in mfs:
    total = mfs[mf].m_integrate(mmin, mmax)[0]
    gt10 = mfs[mf].m_integrate(10, mmax)[0]
    print("Mass fraction for {1} M>10 = {0:0.3f}".format(gt10/total, mf))
gt10
total
get_ipython().magic('run pmf_stats.py')
kroupa.integrate(1,10)
kroupa(10, integral_form=True)-kroupa(1, integral_form=True)
