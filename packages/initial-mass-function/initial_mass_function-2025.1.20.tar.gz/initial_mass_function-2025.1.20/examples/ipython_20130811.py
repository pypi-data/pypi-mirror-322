
########################################################
# # Started Logging At: 2013-08-11 17:34:51
########################################################
from pylab import *;import numpy,scipy,matplotlib,pyfits;
import imf
cluster = imf.make_cluster(100)
from imf import color_from_mass,lum_of_star
colors = [color_from_mass(m) for m in cluster]
luminosities = [lum_of_star(m) for m in cluster]
mean_color = (np.array(colors)*np.array(luminosities)).mean(axis=1)
mean_color = (np.array(colors)*np.array(luminosities)[:,None]).mean(axis=1)
mean_color
mean_color = (np.array(colors)*np.array(luminosities)).mean(axis=0)
mean_color = (np.array(colors)*np.array(luminosities)[:,None]).mean(axis=0)
mean_color
colors       = np.array([color_from_mass(m) for m in cluster])
luminosities = np.array([lum_of_star(m) for m in cluster])
mean_color = (colors*luminosities[:,None]).sum(axis=0)/luminosities.sum()
mean_color
luminosities
get_ipython().magic(u'pwd ')
get_ipython().magic(u'run clustermf_figure.py')

########################################################
# # Started Logging At: 2013-08-11 17:45:17
########################################################
from pylab import *;import numpy,scipy,matplotlib,pyfits;
get_ipython().magic(u'run clustermf_figure.py')
yax
len(yax)
yax = [np.random.rand()*(np.log10(pr(m))-np.log10(pr(m0))) + np.log10(pr(m0)) for m in cluster_masses]
yax
pl.scatter(cluster_masses, yax, c=colors, s=luminosities)
luminosities
import imf
figure()
plot(imf.vgsMe,imf.vgslogLe)
m = logspace(-2,1)
plot(m,m**2)
plot(m,log10(m**2)0
plot(m,log10(m**2))
clf()
plot(imf.vgsMe,imf.vgslogLe)
plot(m,log10(m**2))
plot(m,log10(m**2.5))
plot(m,log10(m**3))

########################################################
# # Started Logging At: 2013-08-11 17:51:42
########################################################
from pylab import *;import numpy,scipy,matplotlib,pyfits;
get_ipython().magic(u'run clustermf_figure.py')
import imf
plot(imf.vgsMe,imf.vgslogLe)
plot(imf.vgsM,imf.vgslogL)
plot(linspace(2,20),1.5**linspace(2,20)**3.5)
clf()
plot(imf.vgsM,imf.vgslogL)
plot(linspace(2,20),np.log10(1.5*linspace(2,20)**3.5))
get_ipython().magic(u'run clustermf_figure.py')

########################################################
# # Started Logging At: 2013-08-11 17:55:29
########################################################
from pylab import *;import numpy,scipy,matplotlib,pyfits;
get_ipython().magic(u'run clustermf_figure.py')
get_ipython().magic(u'run clustermf_figure.py')

########################################################
# # Started Logging At: 2013-08-11 17:56:09
########################################################
from pylab import *;import numpy,scipy,matplotlib,pyfits;
get_ipython().magic(u'run clustermf_figure.py')
luminosities
clusters
clusters[-1]
lum_of_cluster(clusters[-1])

########################################################
# # Started Logging At: 2013-08-11 17:57:32
########################################################
from pylab import *;import numpy,scipy,matplotlib,pyfits;
get_ipython().magic(u'run clustermf_figure.py')
luminosities
pl.scatter(cluster_masses, yax, c=colors, s=10**luminosities)
luminosities = np.array([lum_of_cluster(c) for c in clusters])
pl.scatter(cluster_masses, yax, c=colors, s=10**luminosities)
pl.scatter(cluster_masses, yax, c=colors, s=10**luminosities/1e3)
clf()
pl.scatter(cluster_masses, yax, c=colors, s=10**luminosities/1e3)

########################################################
# # Started Logging At: 2013-08-11 17:58:54
########################################################
from pylab import *;import numpy,scipy,matplotlib,pyfits;
get_ipython().magic(u'run clustermf_figure.py')
pl.scatter(cluster_masses, yax, c=colors, s=10*luminosities)
pl.scatter(cluster_masses, yax, c=colors, s=30*luminosities)
pr(m0)
pr(m)
yax
yax = [np.random.rand()*(np.log10(pr(m))-np.log10(pr(mmax))) + np.log10(pr(mmax)) for m in cluster_masses]
pl.scatter(cluster_masses, yax, c=colors, s=30*luminosities)
clf()
pl.scatter(cluster_masses, yax, c=colors, s=30*luminosities)
gca().set_xscale('log')
draw()
get_ipython().magic(u'run clustermf_figure.py')
get_ipython().magic(u'run clustermf_figure.py')
cluster_masses
yax
colors
len(colors[0])
np.where([len(c)==0 for c in colors])
clusters[47]
get_ipython().magic(u'run clustermf_figure.py')
get_ipython().magic(u'run clustermf_figure.py')
pl.cm.RdBu(0.1)
pl.cm.RdBu(0.9)
pl.cm.RdBu(1.1)
pl.cm.RdBu(100)
pl.cm.RdBu(1000)
get_ipython().magic(u'pinfo pl.cm.RdBu')
mmin=0.08
mmax=120
cr = np.log10(mmax)-np.log10(mmin)
lm = np.log10(mass)-np.log10(mmin)
mass=0.1
lm = np.log10(mass)-np.log10(mmin)
lm/cr
mass=119
lm/cr
lm = np.log10(mass)-np.log10(mmin)
lm/cr

########################################################
# # Started Logging At: 2013-08-11 18:12:03
########################################################
from pylab import *;import numpy,scipy,matplotlib,pyfits;
get_ipython().magic(u'run clustermf_figure.py')
ctable(100)
ctable(120)
ctable(10)
stars = np.logspace(np.log10(0.08),np.log10(120))
scatter(stars,stars,c=ctable(stars))
clf()
scatter(stars,stars,c=ctable(stars))
get_ipython().magic(u'paste')
def ctable(mass, mmin=0.08, mmax=120):
    return (mass-mmin)/(mmax-mmin)
    cr = np.log10(mmax)-np.log10(mmin)
    lm = np.log10(mass)-np.log10(mmin)
    return pl.cm.RdBu(lm/cr)
scatter(stars,stars,c=ctable(stars))
get_ipython().magic(u'paste')
def ctable(mass, mmin=0.08, mmax=120):
    return pl.cm.RdBu((mass-mmin)/(mmax-mmin))
scatter(stars,stars,c=ctable(stars))
get_ipython().magic(u'run clustermf_figure.py')

########################################################
# # Started Logging At: 2013-08-11 18:15:27
########################################################
from pylab import *;import numpy,scipy,matplotlib,pyfits;
get_ipython().magic(u'run clustermf_figure.py')

########################################################
# # Started Logging At: 2013-08-11 18:15:42
########################################################
from pylab import *;import numpy,scipy,matplotlib,pyfits;
get_ipython().magic(u'run clustermf_figure.py')
get_ipython().magic(u'run clustermf_figure.py')
get_ipython().magic(u'run clustermf_figure.py')
cb = pl.colorbar()
get_ipython().set_next_input(u'cb = pl.colorbar');get_ipython().magic(u'pinfo pl.colorbar')
S = pl.scatter(cluster_masses, yax, c=colors, s=30*luminosities)
S
cb = pl.colorbar(S)
cb = pl.colorbar(vmin=0.08,vmax=120)
cb = pl.colorbar(linspace(0.08,120),vmin=0.08,vmax=120)
sm = pl.cm.ScalarMappable(cmap=pl.cm.RdBu, norm=plt.normalize(min=0.08, max=120))
cb = pl.colorbar(sm)
get_ipython().magic(u'pinfo pl.normalize')
get_ipython().magic(u'pinfo pl.Normalize')
sm = pl.cm.ScalarMappable(cmap=pl.cm.RdBu, norm=pl.Normalize(vmin=0.08, vmax=120))
cb = pl.colorbar(sm)
sm
sm = pl.cm.ScalarMappable(cmap=pl.cm.RdBu, norm=pl.Normalize(vmin=0.08, vmax=120))
sm._A = []
cb = pl.colorbar(sm)
clf()
get_ipython().magic(u'paste')
pl.figure(1)
pl.clf()
pl.gca().set_xscale('log')

S = pl.scatter(cluster_masses, yax, c=colors, s=30*luminosities)
sm = pl.cm.ScalarMappable(cmap=pl.cm.RdBu, norm=pl.Normalize(vmin=0.08, vmax=120))
sm._A = []
cb = pl.colorbar(sm)

pl.show()
get_ipython().magic(u'paste')
pl.figure(1)
pl.clf()
pl.gca().set_xscale('log')

S = pl.scatter(cluster_masses, yax, c=colors, s=30*luminosities)
sm = pl.cm.ScalarMappable(cmap=pl.cm.RdBu, norm=pl.Normalize(vmin=0.08, vmax=120))
sm._A = []
cb = pl.colorbar(sm)

pl.show()
get_ipython().magic(u'run clustermf_figure.py')
S = pl.scatter(cluster_masses, yax, c=colors, s=luminosities**2)
S = pl.scatter(cluster_masses, yax, c=colors, s=luminosities**3)
luminosities
luminosities**3
S = pl.scatter(cluster_masses, yax, c=colors, s=luminosities**3, alpha=0.5)
clf()
S = pl.scatter(cluster_masses, yax, c=colors, s=luminosities**3, alpha=0.5)
get_ipython().magic(u'run clustermf_figure.py')
pl.gca().axis([min(cluster_masses)/1.1,max(cluster_masses)*1.1,min(yax)-0.2,max(yax)+0.5])
pl.gca().axis([min(cluster_masses)/1.05,max(cluster_masses)*1.1,min(yax)-0.2,max(yax)+0.5])
draw()
pl.gca().axis([min(cluster_masses)/1.1,max(cluster_masses)*1.1,min(yax)-0.2,max(yax)+0.5])
draw()
sizes = 10**luminosities/1e3
sizes
sizes.min()
sizes.max()
sizes = 10**luminosities/1e5
sizes.max()
get_ipython().magic(u'paste')
sizes = 10**luminosities/1e5
sizes[sizes < 10] = 10
S = pl.scatter(cluster_masses, yax, c=colors, s=sizes, alpha=0.5)
sm = pl.cm.ScalarMappable(cmap=pl.cm.RdBu, norm=pl.Normalize(vmin=0.08, vmax=120))
sm._A = []
cb = pl.colorbar(sm)
pl.gca().axis([min(cluster_masses)/1.1,max(cluster_masses)*1.1,min(yax)-0.2,max(yax)+0.5])

pl.show()
clf()
get_ipython().magic(u'paste')
sizes = 10**luminosities/1e5
sizes[sizes < 10] = 10
S = pl.scatter(cluster_masses, yax, c=colors, s=sizes, alpha=0.5)
sm = pl.cm.ScalarMappable(cmap=pl.cm.RdBu, norm=pl.Normalize(vmin=0.08, vmax=120))
sm._A = []
cb = pl.colorbar(sm)
pl.gca().axis([min(cluster_masses)/1.1,max(cluster_masses)*1.1,min(yax)-0.2,max(yax)+0.5])

pl.show()
get_ipython().magic(u'paste')
pl.rc('font',size=30)
pl.figure(1)
pl.clf()
pl.gca().set_xscale('log')

sizes = 10**luminosities/1e5
sizes[sizes < 10] = 10
S = pl.scatter(cluster_masses, yax, c=colors, s=sizes, alpha=0.5)
sm = pl.cm.ScalarMappable(cmap=pl.cm.RdBu, norm=pl.Normalize(vmin=0.08, vmax=120))
sm._A = []
cb = pl.colorbar(sm)
pl.gca().axis([min(cluster_masses)/1.1,max(cluster_masses)*1.1,min(yax)-0.2,max(yax)+0.5])

pl.show()
get_ipython().magic(u'paste')
pl.rc('font',size=30)
pl.figure(1)
pl.clf()
pl.gca().set_xscale('log')

sizes = 10**luminosities/1e5
sizes[sizes < 10] = 10
S = pl.scatter(cluster_masses, yax, c=colors, s=sizes, alpha=0.8)
sm = pl.cm.ScalarMappable(cmap=pl.cm.RdBu, norm=pl.Normalize(vmin=0.08, vmax=120))
sm._A = []
cb = pl.colorbar(sm)
pl.gca().axis([min(cluster_masses)/1.1,max(cluster_masses)*1.1,min(yax)-0.2,max(yax)+0.5])

pl.show()
get_ipython().magic(u'paste')
pl.figure(2)
pl.clf()
pl.gca().set_xscale('log')

sizes = cluster_masses / 1e3
sizes[sizes < 10] = 10
S = pl.scatter(cluster_masses, yax, c=pl.cm.BrBG((cluster_masses-m0)/(mmax-m0)), s=sizes, alpha=0.8)
sm = pl.cm.ScalarMappable(cmap=pl.cm.RdBu, norm=pl.Normalize(vmin=0.08, vmax=120))
sm._A = []
cb = pl.colorbar(sm)
pl.gca().axis([min(cluster_masses)/1.1,max(cluster_masses)*1.1,min(yax)-0.2,max(yax)+0.5])
cluster_masses=np.array(cluster_masses)
get_ipython().magic(u'paste')
pl.figure(2)
pl.clf()
pl.gca().set_xscale('log')

sizes = cluster_masses / 1e3
sizes[sizes < 10] = 10
S = pl.scatter(cluster_masses, yax, c=pl.cm.BrBG((cluster_masses-m0)/(mmax-m0)), s=sizes, alpha=0.8)
sm = pl.cm.ScalarMappable(cmap=pl.cm.RdBu, norm=pl.Normalize(vmin=0.08, vmax=120))
sm._A = []
cb = pl.colorbar(sm)
pl.gca().axis([min(cluster_masses)/1.1,max(cluster_masses)*1.1,min(yax)-0.2,max(yax)+0.5])

pl.show()
get_ipython().magic(u'paste')
pl.figure(2)
pl.clf()
pl.gca().set_xscale('log')

sizes = cluster_masses / 1e2
sizes[sizes < 10] = 10
S = pl.scatter(cluster_masses, yax, c=pl.cm.BrBG((cluster_masses-m0)/(mmax-m0)), s=sizes, alpha=0.8)
sm = pl.cm.ScalarMappable(cmap=pl.cm.RdBu, norm=pl.Normalize(vmin=0.08, vmax=120))
sm._A = []
cb = pl.colorbar(sm)
pl.gca().axis([min(cluster_masses)/1.1,max(cluster_masses)*1.1,min(yax)-0.2,max(yax)+0.5])

pl.show()
get_ipython().magic(u'paste')
pl.figure(2)
pl.clf()
pl.gca().set_xscale('log')

sizes = cluster_masses / 1e1
sizes[sizes < 10] = 10
S = pl.scatter(cluster_masses, yax, c=pl.cm.BrBG((cluster_masses-m0)/(mmax-m0)), s=sizes, alpha=0.8)
sm = pl.cm.ScalarMappable(cmap=pl.cm.RdBu, norm=pl.Normalize(vmin=0.08, vmax=120))
sm._A = []
cb = pl.colorbar(sm)
pl.gca().axis([min(cluster_masses)/1.1,max(cluster_masses)*1.1,min(yax)-0.2,max(yax)+0.5])

pl.show()
cluster_masses
m0
mmax
get_ipython().magic(u'Paste')
get_ipython().magic(u'paste')
pl.figure(2)
pl.clf()
pl.gca().set_xscale('log')

sizes = cluster_masses / 1e1
sizes[sizes < 10] = 10
S = pl.scatter(cluster_masses, yax, c=pl.cm.BrBG((cluster_masses-m0)/(cluster_masses.max()-m0)), s=sizes, alpha=0.8)
sm = pl.cm.ScalarMappable(cmap=pl.cm.RdBu, norm=pl.Normalize(vmin=0.08, vmax=120))
sm._A = []
cb = pl.colorbar(sm)
pl.gca().axis([min(cluster_masses)/1.1,max(cluster_masses)*1.1,min(yax)-0.2,max(yax)+0.5])
get_ipython().magic(u'paste')
pl.figure(2)
pl.clf()
pl.gca().set_xscale('log')

sizes = cluster_masses / 50
sizes[sizes < 10] = 10
S = pl.scatter(cluster_masses, yax, c=colors, s=sizes, alpha=0.8)
sm = pl.cm.ScalarMappable(cmap=pl.cm.RdBu, norm=pl.Normalize(vmin=0.08, vmax=120))
sm._A = []
cb = pl.colorbar(sm)
pl.gca().axis([min(cluster_masses)/1.1,max(cluster_masses)*1.1,min(yax)-0.2,max(yax)+0.5])

pl.show()
cb.set_label("Hi")
draw()
cb.set_label("Mass of Star producing average photon")
draw()
cb.set_label("Luminosity-weighted Mean Stellar Mass")
draw()
cb.set_label("Luminosity-weighted\nMean Stellar Mass")
draw()
get_ipython().magic(u'run clustermf_figure.py')
get_ipython().magic(u'paste')
TITLE: How do massive clusters form?  Clues from a complete Galactic sample

Massive stars form rarely and far away.  The biggest stars are most often
observed in the most massive, densest clusters.  Despite their rarity, these
most massive clusters dominate the total light production in other galaxies.
Within our own Galaxy, however, they are well-hidden behind the dust that fills
the Galactic Plane.  I will discuss the physical properties of these clusters
in their earliest state.  By searching for dusty and therefore extremely young
clusters, we are able to obtain a complete sample of very massive clusters in
our own Galaxy, and from this sample infer important features of their
population.  I will present results from a search for massive protoclusters
using 1.1 mm dust emission from the Bolocam Galactic Plane Survey.  The
resulting population census gives us important clues about how massive clusters
must form, suggesting that they have no quiescent predecessors.
get_ipython().magic(u'paste')
pl.rc('font',size=30)
pl.figure(1)
pl.clf()
pl.gca().set_xscale('log')

sizes = 10**luminosities/1e5
sizes[sizes < 10] = 10
S = pl.scatter(cluster_masses, yax, c=colors, s=sizes, alpha=0.8)
sm = pl.cm.ScalarMappable(cmap=pl.cm.RdBu, norm=pl.Normalize(vmin=0.08, vmax=120))
sm._A = []
cb = pl.colorbar(sm)
cb.set_label("Luminosity-weighted\nMean Stellar Mass")
pl.gca().axis([min(cluster_masses)/1.1,max(cluster_masses)*1.1,min(yax)-0.2,max(yax)+0.5])
pl.xlabel("Cluster Mass ($M_\odot$)")
pl.ylabel("Log(dN(M)/dM)")
pl.savefig("plots/clusterMF_lumcolor_lumsize.png",bbox_inches='tight')

pl.figure(2)
pl.clf()
pl.gca().set_xscale('log')

sizes = cluster_masses / 50
sizes[sizes < 10] = 10
S = pl.scatter(cluster_masses, yax, c=colors, s=sizes, alpha=0.8)
sm = pl.cm.ScalarMappable(cmap=pl.cm.RdBu, norm=pl.Normalize(vmin=0.08, vmax=120))
sm._A = []
cb = pl.colorbar(sm)
cb.set_label("Luminosity-weighted\nMean Stellar Mass")
pl.gca().axis([min(cluster_masses)/1.1,max(cluster_masses)*1.1,min(yax)-0.2,max(yax)+0.5])
pl.xlabel("Cluster Mass ($M_\odot$)")
pl.ylabel("Log(dN(M)/dM)")
pl.savefig("plots/clusterMF_lumcolor_massize.png",bbox_inches='tight')

pl.show()
get_ipython().system(u'open plots/*png')
luminosities / cluster_masses
(luminosities / cluster_masses).max()
(luminosities / cluster_masses).min()
(10**luminosities / cluster_masses).min()
(10**luminosities / cluster_masses).max()
(10**luminosities / cluster_masses).max()5*np.log(10**luminosities / cluster_masses)
5*np.log(10**luminosities / cluster_masses)
get_ipython().magic(u'paste')
pl.figure(3)
pl.clf()
pl.gca().set_xscale('log')

sizes = 5*np.log(10**luminosities / cluster_masses)
sizes[sizes < 10] = 10
S = pl.scatter(cluster_masses, yax, c=colors, s=sizes, alpha=0.8)
sm = pl.cm.ScalarMappable(cmap=pl.cm.RdBu, norm=pl.Normalize(vmin=0.08, vmax=120))
sm._A = []
cb = pl.colorbar(sm)
cb.set_label("Luminosity-weighted\nMean Stellar Mass")
pl.gca().axis([min(cluster_masses)/1.1,max(cluster_masses)*1.1,min(yax)-0.2,max(yax)+0.5])
pl.xlabel("Cluster Mass ($M_\odot$)")
pl.ylabel("Log(dN(M)/dM)")
pl.savefig("plots/clusterMF_lumcolor_mtolsize.png",bbox_inches='tight')
(5*np.log(10**luminosities / cluster_masses)).min()
(5*np.log(10**luminosities / cluster_masses)).max()
get_ipython().magic(u'paste')
sizes = 20*np.log(10**luminosities / cluster_masses)
sizes[sizes < 10] = 10
S = pl.scatter(cluster_masses, yax, c=colors, s=sizes, alpha=0.8)
sm = pl.cm.ScalarMappable(cmap=pl.cm.RdBu, norm=pl.Normalize(vmin=0.08, vmax=120))
sm._A = []
cb = pl.colorbar(sm)
cb.set_label("Luminosity-weighted\nMean Stellar Mass")
pl.gca().axis([min(cluster_masses)/1.1,max(cluster_masses)*1.1,min(yax)-0.2,max(yax)+0.5])
pl.xlabel("Cluster Mass ($M_\odot$)")
pl.ylabel("Log(dN(M)/dM)")
pl.savefig("plots/clusterMF_lumcolor_mtolsize.png",bbox_inches='tight')
get_ipython().magic(u'paste')
pl.figure(3)
pl.clf()
pl.gca().set_xscale('log')

sizes = 20*np.log(10**luminosities / cluster_masses)
sizes[sizes < 10] = 10
S = pl.scatter(cluster_masses, yax, c=colors, s=sizes, alpha=0.8)
sm = pl.cm.ScalarMappable(cmap=pl.cm.RdBu, norm=pl.Normalize(vmin=0.08, vmax=120))
sm._A = []
cb = pl.colorbar(sm)
cb.set_label("Luminosity-weighted\nMean Stellar Mass")
pl.gca().axis([min(cluster_masses)/1.1,max(cluster_masses)*1.1,min(yax)-0.2,max(yax)+0.5])
pl.xlabel("Cluster Mass ($M_\odot$)")
pl.ylabel("Log(dN(M)/dM)")
pl.savefig("plots/clusterMF_lumcolor_mtolsize.png",bbox_inches='tight')
sizes
figure()
hist(sizes)
get_ipython().magic(u'history ')
git@github.com:BGPS/distance_omnibus2.git
from scipy.ndimage.morphology import binary_dilation
get_ipython().magic(u'pinfo binary_dilation')
x = np.zeros([5,5])
x[2,2] = 1
x
binary_dilation(x)
binary_dilation(x,2)
get_ipython().magic(u'pinfo binary_dilation')
binary_dilation(x,iterations=2)
x = np.random.rand(5,5)
x
binary_dilation(x,iterations=2)
binary_dilation(x,iterations=1)
x
x.astype('bool')
get_ipython().magic(u'history ')
import itertools
itertools.repeat('x')
x = {1:2,3:4,5:6}
zip(x,itertools.repeat('i'))
list(set(x.values())
)
import pytest
pytest.mark.parametrize
pytest.mark.parametrize(('a',),list(set(x.values)))
pytest.mark.parametrize(('a',),list(set(x.values())))
pytest.mark.parametrize(('abc',),list(set(x.values())))
pytest.mark.parametrize('abc',list(set(x.values())))
import urlparse
urlparse.parse_qsl
figure()
semilogy(rand(100),rand(100))
semilogy(rand(100),rand(100),'.')
clf()
semilogy(rand(100),rand(100),'.')
from agpy import blackbody
figure()
nu = np.linspace(5,1.5e3,1000)
wav = np.linspace(20,50000,5000)
plot(wav,blackbody.blackbody_wavelength(wav,100))
loglog(wav,blackbody.blackbody_wavelength(wav,100))
get_ipython().magic(u'pinfo blackbody.blackbody_wavelength')
loglog(wav,blackbody.blackbody_wavelength(wav,100),wavelength_units='microns')
loglog(wav,blackbody.blackbody_wavelength(wav,100,wavelength_units='microns'))
clf()
loglog(wav,blackbody.blackbody_wavelength(wav,100,wavelength_units='microns'))
wav = np.logspace(1,4,1000)
loglog(wav,blackbody.blackbody_wavelength(wav,100,wavelength_units='microns'))
loglog(wav/1000,blackbody.blackbody_wavelength(wav,100,wavelength_units='microns'))
clf()
loglog(wav/1000,blackbody.blackbody_wavelength(wav,100,wavelength_units='microns'))
get_ipython().magic(u'history ')
get_ipython().magic(u'pinfo blackbody.modified_blackbody_wavelength')
get_ipython().magic(u'run ~/agpy/agpy/survey_plot.py')
show()
clf()
get_ipython().magic(u'run ~/agpy/agpy/survey_plot.py')
show()
get_ipython().magic(u'paste')
ff = (wav_cm/1e-3)**-0.1

pl.loglog(wav_cm/10,bb+ff)
pl.loglog(wav_cm/10,gb+ff)
get_ipython().magic(u'paste')
ff = (wav_cm/1e-3)**-0.1 * 1e-4

pl.loglog(wav_cm/10,bb+ff)
pl.loglog(wav_cm/10,gb+ff)
get_ipython().magic(u'run ~/agpy/agpy/survey_plot.py')
show()
get_ipython().magic(u'run ~/agpy/agpy/survey_plot.py')
show()
freq
get_ipython().magic(u'run ~/agpy/agpy/survey_plot.py')
show()
get_ipython().magic(u'run ~/agpy/agpy/survey_plot.py')
show()
reload(blackbody)
get_ipython().magic(u'run ~/agpy/agpy/survey_plot.py')
reload(agpy)
import agpy
reload(agpy)
from agpy import blackbody
reload(agpy)
reload(blackbody)
reload(blackbody)
reload(blackbody)
get_ipython().system(u'rm -i /Users/adam/agpy/agpy/blackbody.pyc')
reload(blackbody)
reload(blackbody)
get_ipython().magic(u'run ~/agpy/agpy/survey_plot.py')
deepreload blackbody
deepreload(blackbody)
reload(blackbody)
reload(blackbody)
reload(blackbody)
reload(blackbody)
get_ipython().magic(u'run -i ~/agpy/agpy/survey_plot.py')
show()
