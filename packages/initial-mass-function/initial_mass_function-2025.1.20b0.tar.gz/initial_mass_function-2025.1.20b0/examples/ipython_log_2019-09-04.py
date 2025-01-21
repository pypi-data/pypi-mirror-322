########################################################
# Started Logging At: 2019-09-04 09:54:20
########################################################

########################################################
# # Started Logging At: 2019-09-04 09:54:21
########################################################
get_ipython().run_line_magic('run', 'mass_to_light.py')
get_ipython().run_line_magic('paste', '')
m_to_ls = []
for slope in np.linspace(2.0, 2.6, 10):
    imf = imf.Kroupa(p3=slope)
    cluster = imf.make_cluster(1e5, mmax=120, silent=True)
    lum = imf.lum_of_cluster(cluster)
    m_to_l = 1e5/lum
    m_to_ls.append(m_to_l)
import imf
get_ipython().run_line_magic('paste', '')
m_to_ls = []
for slope in np.linspace(2.0, 2.6, 10):
    Kroupa = imf.Kroupa(p3=slope)
    cluster = imf.make_cluster(1e5, Kroupa, mmax=120, silent=True)
    lum = imf.lum_of_cluster(cluster)
    m_to_l = 1e5/lum
    m_to_ls.append(m_to_l)
get_ipython().run_line_magic('paste', '')
m_to_ls = []
for slope in np.linspace(2.1, 2.6, 10):
    Kroupa = imf.Kroupa(p3=slope)
    cluster = imf.make_cluster(1e5, Kroupa, mmax=120, silent=True)
    lum = imf.lum_of_cluster(cluster)
    m_to_l = 1e5/lum
    m_to_ls.append(m_to_l)
get_ipython().run_line_magic('debug', '')
imf.expectedmass_cache
del imf.expectedmass_cache
get_ipython().run_line_magic('paste', '')
m_to_ls = []
for slope in np.linspace(2.1, 2.6, 10):
    Kroupa = imf.Kroupa(p3=slope)
    cluster = imf.make_cluster(1e5, Kroupa, mmax=120, silent=True)
    lum = imf.lum_of_cluster(cluster)
    m_to_l = 1e5/lum
    m_to_ls.append(m_to_l)
imf.expectedmass_cache
get_ipython().run_line_magic('debug', '')
get_ipython().run_line_magic('paste', '')
m_to_ls = []
for slope in np.linspace(2.1, 2.6, 10):
    Kroupa = imf.Kroupa(p3=slope)
    cluster = imf.make_cluster(1e5, Kroupa, mmax=120, silent=True)
    lum = imf.lum_of_cluster(cluster)
    m_to_l = 1e5/lum
    m_to_ls.append(m_to_l)
get_ipython().run_line_magic('debug', '')
get_ipython().run_line_magic('paste', '')
m_to_ls = []
for slope in np.linspace(2.1, 2.6, 10):
    Kroupa = imf.Kroupa(p3=slope)
    cluster = imf.make_cluster(1e5, Kroupa, mmax=120, silent=True)
    lum = imf.lum_of_cluster(cluster)
    m_to_l = 1e5/lum
    m_to_ls.append(m_to_l)
########################################################
# Started Logging At: 2019-09-04 09:58:42
########################################################

########################################################
# # Started Logging At: 2019-09-04 09:58:43
########################################################
import imf
get_ipython().run_line_magic('paste', '')
m_to_ls = []
for slope in np.linspace(2.1, 2.6, 10):
    Kroupa = imf.Kroupa(p3=slope)
    cluster = imf.make_cluster(1e5, Kroupa, mmax=120, silent=True)
    lum = imf.lum_of_cluster(cluster)
    m_to_l = 1e5/lum
    m_to_ls.append(m_to_l)
get_ipython().run_line_magic('paste', '')
m_to_ls = []
for slope in np.linspace(2.2, 2.6, 10):
    Kroupa = imf.Kroupa(p3=slope)
    cluster = imf.make_cluster(1e5, Kroupa, mmax=120, silent=True)
    lum = imf.lum_of_cluster(cluster)
    m_to_l = 1e5/lum
    m_to_ls.append(m_to_l)
get_ipython().run_line_magic('paste', '')
m_to_ls = []
for slope in np.linspace(2.5, 2.9, 10):
    Kroupa = imf.Kroupa(p3=slope)
    cluster = imf.make_cluster(1e5, Kroupa, mmax=120, silent=True)
    lum = imf.lum_of_cluster(cluster)
    m_to_l = 1e5/lum
    m_to_ls.append(m_to_l)
Kroupa
Kroupa.mmax
Kroupa.p3
Kroupa(np.linspace(0.03, 120)
)
cluster = imf.make_cluster(1e5, Kroupa, mmax=120, silent=True)
imf.inverse_imf(0.5, massfunc=Kroupa)
imf.inverse_imf(0.99, massfunc=Kroupa)
cluster = imf.make_cluster(1e5, Kroupa, mmax=120, silent=True)
get_ipython().run_line_magic('debug', '')
########################################################
# Started Logging At: 2019-09-04 10:01:26
########################################################

########################################################
# # Started Logging At: 2019-09-04 10:01:26
########################################################
import imf
get_ipython().run_line_magic('paste', '')
cluster = imf.make_cluster(1e5, Kroupa, mmax=120, silent=True)
get_ipython().run_line_magic('paste', '')
m_to_ls = []
for slope in np.linspace(2.1, 2.9, 10):
    Kroupa = imf.Kroupa(p3=slope)
    cluster = imf.make_cluster(1e5, Kroupa, mmax=120, silent=True)
    lum = imf.lum_of_cluster(cluster)
    m_to_l = 1e5/lum
    m_to_ls.append(m_to_l)
Kroupa.m_integrate(0.03, 120)
Kroupa.m_integrate(0.03, 120, numerical=True)
get_ipython().run_line_magic('paste', '')
m_to_ls = []
for slope in np.linspace(2.1, 2.9, 10):
    Kroupa = imf.Kroupa(p3=slope)
    cluster = imf.make_cluster(1e5, Kroupa, mmax=120, silent=True, numerical=True)
    lum = imf.lum_of_cluster(cluster)
    m_to_l = 1e5/lum
    m_to_ls.append(m_to_l)
########################################################
# Started Logging At: 2019-09-04 10:04:44
########################################################

########################################################
# # Started Logging At: 2019-09-04 10:04:44
########################################################
import imf
get_ipython().run_line_magic('paste', '')
m_to_ls = []
for slope in np.linspace(2.1, 2.9, 10):
    Kroupa = imf.Kroupa(p3=slope)
    cluster = imf.make_cluster(1e5, Kroupa, mmax=120, silent=True, numerical=True)
    lum = imf.lum_of_cluster(cluster)
    m_to_l = 1e5/lum
    m_to_ls.append(m_to_l)

#pl.loglog(clusters.keys(), np.array(list(mean_luminosities.values())) / np.array(list(mean_masses.values())), '.', alpha=0.1)

# compute mass-to-light ratio vs age
get_ipython().run_line_magic('paste', '')
m_to_ls = []
for slope in np.linspace(2.1, 2.9, 10):
    Kroupa = imf.Kroupa(p3=slope)
    cluster = imf.make_cluster(1e5, Kroupa, mmax=120, silent=True)
    lum = imf.lum_of_cluster(cluster)
    m_to_l = 1e5/lum
    m_to_ls.append(m_to_l)

#pl.loglog(clusters.keys(), np.array(list(mean_luminosities.values())) / np.array(list(mean_masses.values())), '.', alpha=0.1)

# compute mass-to-light ratio vs age
m_to_ls
pl.plot(np.linspace(2.1, 2.9, 10), m_to_ls)
import pylab as pl
pl.plot(np.linspace(2.1, 2.9, 10), m_to_ls)
get_ipython().run_line_magic('paste', '')
m_to_ls = []
slopes = np.linspace(1.7, 2.9, 20)
for slope in slopes:
    Kroupa = imf.Kroupa(p3=slope)
    cluster = imf.make_cluster(1e5, Kroupa, mmax=120, silent=True)
    lum = imf.lum_of_cluster(cluster)
    m_to_l = 1e5/lum
    m_to_ls.append(m_to_l)

pl.figure(4).clf()
pl.plot(np.linspace(2.1, 2.9, 10), m_to_ls)
get_ipython().run_line_magic('paste', '')
m_to_ls = []
slopes = np.linspace(1.7, 2.9, 20)
for slope in slopes:
    Kroupa = imf.Kroupa(p3=slope)
    cluster = imf.make_cluster(1e5, Kroupa, mmax=120, silent=True)
    lum = imf.lum_of_cluster(cluster)
    m_to_l = 1e5/lum
    m_to_ls.append(m_to_l)

pl.figure(4).clf()
pl.plot(slopes, m_to_ls)
pl.xlabel("Upper-end power-law slope $\\alpha$")
pl.ylabel("Mass-to-light ratio [M$_\odot$/L$_\odot$]")
pl.savefig("masstolight_vs_slope.pdf")
