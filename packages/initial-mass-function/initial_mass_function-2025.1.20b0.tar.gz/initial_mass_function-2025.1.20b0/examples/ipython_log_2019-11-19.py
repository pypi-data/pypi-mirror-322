########################################################
# Started Logging At: 2019-11-19 10:24:15
########################################################

########################################################
# # Started Logging At: 2019-11-19 10:24:15
########################################################
import imf
masses = np.logspace(-2, 2, 500)
salp = imf.Salpeter(masses)
pl.loglog(masses, salp
)
import pylab as pl
pl.ion()
pl.loglog(masses, salp)
salp
salp = imf.Salpeter()(masses)
salp
pl.loglog(masses, salp)
kr = imf.Kroupa()(masses)
pl.loglog(masses, kr)
get_ipython().run_line_magic('pinfo', 'imf.Salpeter')
chab = imf.Chabrier2005()(masses)
pl.loglog(masses, chab)
pl.figure()
pl.loglog(masses, salp*masses, label='Salpeter')
pl.loglog(masses, kr*masses, label='Kroupa')
pl.loglog(masses, chab*masses, label='Chabrier')
pl.xlabel("Stellar Mass (M$_\odot$)")
pl.ylabel("m dN / dM")
pl.rc('font', size=16)
pl.draw(); pl.show()
pl.rc('font', size=20)
pl.draw(); pl.show()
pl.xlabel("Stellar Mass (M$_\odot$)")
pl.ylabel("m dN / dM")
pl.draw(); pl.show()
pl.legend(loc='best')
get_ipython().run_line_magic('history', '')
pl.clf()
pl.loglog(masses, salp*masses, label='Salpeter')
pl.loglog(masses, kr*masses, label='Kroupa')
pl.loglog(masses, chab*masses, label='Chabrier')
pl.xlabel("Stellar Mass (M$_\odot$)")
pl.xlabel("Stellar Mass (M$_\odot$)")
pl.ylabel("m dN / dM")
pl.legend(loc='best')
pl.savefig('func_form_comparison.png', bbox_inches='tight')
get_ipython().system('open func_form_comparison.png')
np.log(5) - np.log(1)
np.log(9) - np.log(5)
get_ipython().run_line_magic('ls', '-1 *py')
get_ipython().run_line_magic('run', 'imf_figure.py')
get_ipython().run_line_magic('run', 'imf_figure.py')
get_ipython().run_line_magic('run', 'imf_figure.py')
get_ipython().system('open Alpha2p0_imf_figure_log.p*')
get_ipython().run_line_magic('paste', '')
for massfunc, name in [(imf.Salpeter(alpha=1.5), 'Alpha1p5'),
                       (imf.Salpeter(alpha=2), 'Alpha2p0'),
                       (imf.Salpeter(alpha=1), 'Alpha1p0'),
                       (imf.Salpeter(alpha=3), 'Alpha3p0')]:
    pl.figure(1, figsize=(10,8))
    pl.clf()
    cluster,yax,colors = coolplot(1000, massfunc=massfunc)
    pl.scatter(cluster, yax, c=colors, s=np.log10(cluster+3)*85,
               linewidths=0.5, edgecolors=(0,0,0,0.25), alpha=0.95)
    pl.gca().set_xscale('log')

    masses = np.logspace(np.log10(cluster.min()), np.log10(cluster.max()),10000)

    pl.plot(masses,np.log10(massfunc(masses)),'r--',linewidth=2,alpha=0.5)
    pl.xlabel("Stellar Mass")
    pl.ylabel("log(dN(M)/dM)")
    pl.gca().axis([min(cluster)/1.1,max(cluster)*1.1,min(yax)-0.2,max(yax)+0.5])
    pl.savefig("{0}_imf_figure_log.png".format(name),bbox_inches='tight', dpi=150)
    pl.savefig("{0}_imf_figure_log.pdf".format(name),bbox_inches='tight')
get_ipython().system('open  Alpha1*')
get_ipython().run_line_magic('run', 'imf_figure.py')
get_ipython().system('open  Alpha1*')
imf.Salpeter(alpha=1)(masses)
imf.Salpeter(alpha=1)
imf.Salpeter(alpha=1)(masses)
########################################################
# Started Logging At: 2019-11-19 10:52:27
########################################################

########################################################
# # Started Logging At: 2019-11-19 10:52:27
########################################################
get_ipython().run_line_magic('run', 'imf_figure.py')
imf.Salpeter(alpha=1)(masses)
imf.Salpeter(alpha=1)(np.array([0.5, 1, 5])
)
########################################################
# Started Logging At: 2019-11-19 10:53:41
########################################################

########################################################
# # Started Logging At: 2019-11-19 10:53:42
########################################################
get_ipython().run_line_magic('run', 'imf_figure.py')
imf.Salpeter(alpha=1)(np.array([0.5, 1, 5])

)
imf.Salpeter(alpha=1)(np.array([0.5, 1, 5]))
imf.Salpeter(alpha=1).slope
imf.Salpeter(alpha=1).distr
imf.Salpeter(alpha=1).distr.slope
########################################################
# Started Logging At: 2019-11-19 10:54:48
########################################################

########################################################
# # Started Logging At: 2019-11-19 10:54:49
########################################################
imf.Salpeter(alpha=1).distr.slope
import imf
imf.Salpeter(alpha=1).distr.slope
get_ipython().run_line_magic('run', 'imf_figure.py')
########################################################
# Started Logging At: 2019-11-19 11:08:27
########################################################

########################################################
# # Started Logging At: 2019-11-19 11:08:28
########################################################
import imf
imf.Salpeter(alpha=1).rvs(np.linspace(0,1), 5)
imf.Salpeter(alpha=1).distr.rvs(100)
imf.Salpeter(alpha=1).distr.rvs(100).max()
imf.Salpeter(alpha=1).distr.rvs(1e5).max()
imf.Salpeter(alpha=1).distr.rvs(10000).max()
#imf.Salpeter(alpha=1).distr.rvs(10000).max()
imf.Salpeter(alpha=1)
imf.Salpeter(alpha=1).mmin
imf.Salpeter(alpha=1).mmax
np.exp(0) * 0.3
np.exp(1/(np.log(120/0.3))) * 0.3
np.exp(1/(np.log(0.3/120))) * 0.3
np.exp((np.log(120/0.3))) * 0.3
########################################################
# Started Logging At: 2019-11-19 11:10:28
########################################################

########################################################
# # Started Logging At: 2019-11-19 11:10:28
########################################################
import imf
imf.Salpeter(alpha=1).distr.rvs(10000).max()
imf.Salpeter(alpha=1).distr.rvs(10000).min()
get_ipython().run_line_magic('run', 'imf_figure.py')
get_ipython().system('open  Alpha1*')
pl.clf()
pl.hist(imf.Salpeter(alpha=1).distr.rvs(10000))
pl.clf()
pl.close('all')
pl.hist(imf.Salpeter(alpha=1).distr.rvs(10000))
pl.hist(imf.Salpeter(alpha=1).distr.rvs(10000), bins=np.logspace(-2,2.5))
pl.clf()
pl.hist(imf.Salpeter(alpha=1).distr.rvs(10000), bins=np.logspace(-2,2.5))
pl.semilogx(); pl.hist(imf.Salpeter(alpha=1).distr.rvs(10000), bins=np.logspace(-2,2.5))
pl.semilogx(); pl.hist(imf.Salpeter(alpha=1).distr.rvs(10000), bins=np.logspace(-1,2.5))
pl.clf()
pl.semilogx(); pl.hist(imf.Salpeter(alpha=1).distr.rvs(10000), bins=np.logspace(-1,2.5))
