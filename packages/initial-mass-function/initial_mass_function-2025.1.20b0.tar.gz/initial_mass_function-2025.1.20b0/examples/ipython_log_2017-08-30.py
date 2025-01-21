########################################################
# Started Logging At: 2017-08-30 16:44:38
########################################################

########################################################
# # Started Logging At: 2017-08-30 16:44:38
########################################################
get_ipython().magic('run ~/repos/imf/examples/pmf_comparison.py')
imf.chabrier
imf.chabrier(masses)
pl.figure(1).gca().plot(masses, imf.chabrier(masses))
pl.figure(1).gca().plot(masses, imf.kroupa(masses))
pl.figure()
pl.loglog(masses, imf.kroupa(masses)/masses)
pl.loglog(masses, imf.chabrier(masses)/masses)
masses
dm = np.diff(masses)
dm
pl.loglog(masses, imf.kroupa(masses)/dm)
dm = np.concatenate(np.diff(masses), [masses[-1]-masses[-2]])
dm = np.concatenate([np.diff(masses), [masses[-1]-masses[-2]]])
dm
pl.loglog(masses, imf.kroupa(masses)/dm)
pl.loglog(masses, imf.chabrier(masses)/dm)
pl.loglog(masses, imf.kroupa(masses)*np.log(masses))
pl.clf()
pl.loglog(masses, imf.kroupa(masses)*np.log(masses))
pl.loglog(masses, imf.chabrier(masses)*np.log(masses))
np.log(masses)
dlogm = np.concatenate([np.diff(np.log10(masses)), [np.log10(masses[-1])-np.log10(masses[-2])]])
pl.loglog(masses, imf.chabrier(masses)*dlogm)
pl.clf()
pl.loglog(masses, imf.chabrier(masses)*dlogm)
pl.loglog(masses, imf.kroupa(masses)*dlogm)
pl.loglog(masses, imf.kroupa(masses)/dlogm)
pl.loglog(masses, imf.kroupa(masses, integral_form=True))
get_ipython().magic('run ~/repos/imf/examples/pmf_comparison.py')
get_ipython().magic('run ~/repos/imf/examples/pmf_comparison.py')
get_ipython().system('open *png')
get_ipython().magic('run ~/repos/imf/examples/pmf_comparison.py')
get_ipython().system('open *png')
10**-0.2
get_ipython().magic('run ~/repos/imf/examples/pmf_comparison.py')
get_ipython().magic('run ~/repos/imf/examples/pmf_comparison.py')
get_ipython().system('open *png')
