########################################################
# Started Logging At: 2022-03-17 08:58:14
########################################################

########################################################
# # Started Logging At: 2022-03-17 08:58:15
########################################################
get_ipython().run_line_magic('run', 'imf_schematic.py')
get_ipython().run_line_magic('run', 'imf_schematic.py')
get_ipython().run_line_magic('run', 'imf_schematic.py')
########################################################
# Started Logging At: 2022-03-17 08:58:55
########################################################

########################################################
# # Started Logging At: 2022-03-17 08:58:55
########################################################
get_ipython().run_line_magic('run', 'imf_schematic.py')
########################################################
# Started Logging At: 2022-03-17 08:59:36
########################################################

########################################################
# # Started Logging At: 2022-03-17 08:59:37
########################################################
get_ipython().run_line_magic('run', 'imf_schematic.py')
get_ipython().run_line_magic('run', 'imf_schematic.py')
########################################################
# Started Logging At: 2022-03-17 09:05:12
########################################################

########################################################
# # Started Logging At: 2022-03-17 09:05:12
########################################################
get_ipython().run_line_magic('run', 'imf_schematic.py')
########################################################
# Started Logging At: 2022-03-17 09:05:27
########################################################

########################################################
# # Started Logging At: 2022-03-17 09:05:27
########################################################
get_ipython().run_line_magic('run', 'imf_schematic.py')
get_ipython().run_line_magic('run', 'imf_schematic.py')
get_ipython().run_line_magic('run', 'imf_schematic.py')
get_ipython().run_line_magic('run', 'imf_schematic.py')
get_ipython().run_line_magic('run', 'imf_schematic.py')
get_ipython().run_line_magic('run', 'IMF_MoverL.ipynb')
########################################################
# Started Logging At: 2022-03-17 09:08:35
########################################################
########################################################
# Started Logging At: 2022-03-17 09:08:35
########################################################
########################################################
########################################################
# # Started Logging At: 2022-03-17 09:08:36
########################################################
# # Started Logging At: 2022-03-17 09:08:36
########################################################
########################################################
# Started Logging At: 2022-03-17 09:09:14
########################################################
########################################################
# # Started Logging At: 2022-03-17 09:09:14
########################################################
get_ipython().run_line_magic('matplotlib', 'inline')
import pylab as pl
import numpy as np
from imf import imf
clusters, luminosities, masses, mean_luminosities, mean_masses = {},{},{},{},{}
for p in (2.0, 2.1, 2.2, 2.3, 2.4, 2.5):
    # make 100 clusters of 10^4 msun each (very good sampling of total mass range)
    clusters[p] = [imf.make_cluster(10000, 'kroupa', p3=p, silent=True, mmax=150) for x in range(100)]
    # cluster luminosities
    luminosities[p] = [imf.lum_of_cluster(cl) for cl in clusters[p]]
    masses[p] = [cl.sum() for cl in clusters[p]]
    mean_luminosities[p] = np.mean(luminosities[p])
    mean_masses[p] = np.mean(masses[p])
mass_to_light = [mean_masses[k]/10**mean_luminosities[k] for k in sorted(clusters.keys())]
pl.plot(sorted(clusters.keys()), mass_to_light)
pl.xlabel("Powerlaw alpha")
pl.ylabel("Mass / Light (Msun/Lsun)")
#[Out]# Text(0, 0.5, 'Mass / Light (Msun/Lsun)')
clusters, luminosities, masses, mean_luminosities, mean_masses = {},{},{},{},{}
for mmax in (50,100,150,200,250,300,500,1000):
    # make 100 clusters of 10^4 msun each (very good sampling of total mass range)
    clusters[mmax] = [imf.make_cluster(10000, 'kroupa', silent=True, mmax=mmax) for x in range(100)]
    # cluster luminosities
    luminosities[mmax] = [imf.lum_of_cluster(cl) for cl in clusters[mmax]]
    masses[mmax] = [cl.sum() for cl in clusters[mmax]]
    mean_luminosities[mmax] = np.mean(luminosities[mmax])
    mean_masses[mmax] = np.mean(masses[mmax])
mass_to_light = [mean_masses[k]/10**mean_luminosities[k] for k in sorted(clusters.keys())]
pl.plot(sorted(clusters.keys()), mass_to_light)
pl.vlines([100,300],0.0001,0.0007,color='k', linestyle='--')
pl.xlabel("Maximum Stellar Mass")
pl.ylabel("Mass / Light (Msun/Lsun)")
#[Out]# Text(0, 0.5, 'Mass / Light (Msun/Lsun)')
########################################################
# Started Logging At: 2022-03-17 09:11:59
########################################################
########################################################
# # Started Logging At: 2022-03-17 09:11:59
########################################################
get_ipython().run_line_magic('matplotlib', 'inline')
import pylab as pl
import numpy as np
pl.rcParams['figure.facecolor'] = 'w'
from imf import imf
clusters, luminosities, masses, mean_luminosities, mean_masses = {},{},{},{},{}
for p in (2.0, 2.1, 2.2, 2.3, 2.4, 2.5):
    # make 100 clusters of 10^4 msun each (very good sampling of total mass range)
    clusters[p] = [imf.make_cluster(10000, 'kroupa', p3=p, silent=True, mmax=150) for x in range(100)]
    # cluster luminosities
    luminosities[p] = [imf.lum_of_cluster(cl) for cl in clusters[p]]
    masses[p] = [cl.sum() for cl in clusters[p]]
    mean_luminosities[p] = np.mean(luminosities[p])
    mean_masses[p] = np.mean(masses[p])
mass_to_light = [mean_masses[k]/10**mean_luminosities[k] for k in sorted(clusters.keys())]
pl.plot(sorted(clusters.keys()), mass_to_light)
pl.xlabel("Powerlaw alpha")
pl.ylabel("Mass / Light (Msun/Lsun)")
#[Out]# Text(0, 0.5, 'Mass / Light (Msun/Lsun)')
clusters, luminosities, masses, mean_luminosities, mean_masses = {},{},{},{},{}
for mmax in (50,100,150,200,250,300,500,1000):
    # make 100 clusters of 10^4 msun each (very good sampling of total mass range)
    clusters[mmax] = [imf.make_cluster(10000, 'kroupa', silent=True, mmax=mmax) for x in range(100)]
    # cluster luminosities
    luminosities[mmax] = [imf.lum_of_cluster(cl) for cl in clusters[mmax]]
    masses[mmax] = [cl.sum() for cl in clusters[mmax]]
    mean_luminosities[mmax] = np.mean(luminosities[mmax])
    mean_masses[mmax] = np.mean(masses[mmax])
mass_to_light = [mean_masses[k]/10**mean_luminosities[k] for k in sorted(clusters.keys())]
pl.plot(sorted(clusters.keys()), mass_to_light)
pl.vlines([100,300],0.0001,0.0007,color='k', linestyle='--')
pl.xlabel("Maximum Stellar Mass")
pl.ylabel("Mass / Light (Msun/Lsun)")
#[Out]# Text(0, 0.5, 'Mass / Light (Msun/Lsun)')
########################################################
# Started Logging At: 2022-03-17 09:12:15
########################################################
########################################################
# # Started Logging At: 2022-03-17 09:12:16
########################################################
120**1.35 *2.35
#[Out]# 1506.4771350309497
120**-1.35
#[Out]# 0.0015599307452825832
-1/1.35 * (120**-1.35 - 8**-1.35) / (-1/0.35 * (120**-0.35 - 0.1**-0.35)) 
#[Out]# 0.007432171927854529
from scipy.integrate import quad
quad(lambda x:x**-2.35, 8, 100)
#[Out]# (0.04324130240209924, 1.664224581884688e-10)
-1/1.35 * (100**-1.35 - 8**-1.35)
#[Out]# 0.043241302402099224
(-1/0.35 * (100**-0.35 - 0.1**-0.35)) 
#[Out]# 5.82627116306129
(100**-1.35 - 8**-1.35) / ( (100**-0.35 - 0.1**-0.35)) 
#[Out]# 0.028626865455773975
def wtfunc(mmax=100, alpha=2.35, mmin=0.1):
    return (-1/(alpha-1) * (mmax**-(alpha-1) - 8**-(alpha-1))
            / (-1/(alpha-2) * (mmax**-(alpha-2) - mmin**-(alpha-2))))
get_ipython().run_line_magic('matplotlib', 'inline')
import pylab as pl
pl.rcParams['figure.facecolor'] = 'w'
pl.rc('font', size=16)
pl.rc('figure', dpi=300)
pl.plot(np.linspace(20,300), wtfunc(np.linspace(20,300)))
pl.xlabel(r"M$_{max}$ [M$_\odot$]")
pl.ylabel("SNe/M$_\odot$")
#[Out]# Text(0, 0.5, 'SNe/M$_\\odot$')
pl.loglog(np.logspace(-2,0), wtfunc(mmin=np.logspace(-2, 0))/wtfunc())
pl.xlabel(r"M$_{min}$ [M$_\odot$]")
pl.ylabel(r"SNe/M$_\odot$ relative to M$_{min}=0.01$ M$_\odot$")
#[Out]# Text(0, 0.5, 'SNe/M$_\\odot$ relative to M$_{min}=0.01$ M$_\\odot$')
pl.rc('font', size=16)
pl.rc('figure', dpi=300)
pl.semilogy(np.linspace(1.5,3), wtfunc(alpha=np.linspace(1.5,3)) / wtfunc())
axlims = pl.axis()
pl.vlines(2.35, 0.01, 100, color='k', linestyle='--', alpha=0.5)
pl.hlines(1.0, 1, 4, color='k', linestyle='--', alpha=0.5)
pl.axis(axlims)
pl.xlabel(r"$\alpha$")
pl.ylabel(r"SNe/M$_\odot$ relative to $\alpha=2.35$")
#[Out]# Text(0, 0.5, 'SNe/M$_\\odot$ relative to $\\alpha=2.35$')
########################################################
# Started Logging At: 2022-03-17 09:25:44
########################################################
########################################################
# # Started Logging At: 2022-03-17 09:25:45
########################################################
import imf
get_ipython().run_line_magic('pinfo', 'imf.kroupa.m_integrate')
kroupa_mass_integral = imf.kroupa.m_integrate(imf.kroupa.mmin, imf.kroupa.mmax)
kroupa_num_integral = imf.kroupa.integrate(imf.kroupa.mmin, imf.kroupa.mmax)
kroupa_mass_integral, kroupa_num_integral
#[Out]# ((0.4339293611895671, 0), (1.0, 0))
mean_mass = kroupa_mass_integral / kroupa_num_integral
mean_mass = kroupa_mass_integral[0] / kroupa_num_integral[0]
chabrier_mass_integral = imf.chabrier.m_integrate(imf.chabrier.mmin, imf.chabrier.mmax)
chabrier_num_integral = imf.chabrier.integrate(imf.chabrier.mmin, imf.chabrier.mmax)
chabrier_mass_integral, chabrier_num_integral
mean_mass_chabrier = chabrier_mass_integral[0] / chabrier_num_integral[0]
print(f'Chabrier mean mass: {mean_mass_chabrier}')
kroupa_mass_integral = imf.kroupa.m_integrate(imf.kroupa.mmin, imf.kroupa.mmax)
kroupa_num_integral = imf.kroupa.integrate(imf.kroupa.mmin, imf.kroupa.mmax)
kroupa_mass_integral, kroupa_num_integral
mean_mass_kroupa = kroupa_mass_integral[0] / kroupa_num_integral[0]
print(f'Kroupa mean mass: {mean_mass_kroupa}')
salpeter_mass_integral = imf.salpeter.m_integrate(imf.salpeter.mmin, imf.salpeter.mmax)
salpeter_num_integral = imf.salpeter.integrate(imf.salpeter.mmin, imf.salpeter.mmax)
salpeter_mass_integral, salpeter_num_integral
mean_mass_salpeter = salpeter_mass_integral[0] / salpeter_num_integral[0]
print(f'Salpeter mean mass: {mean_mass_salpeter}')
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    ratio_highmass = distr.integrate(8, distr.mmax)[0]
    ratio_highmasslowmass = distr.integrate(8, distr.mmax)[0] / distr.integrate(distr.mmin, 8)[0]
    print(f'{distribution} N(M>8) / N(tot) = {ratio_highmass}, N(M>8) / N(low) = {ratio_highmasslowmass}
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    ratio_highmass = distr.integrate(8, distr.mmax)[0]
    ratio_highmasslowmass = distr.integrate(8, distr.mmax)[0] / distr.integrate(distr.mmin, 8)[0]
    print(f'{distribution} N(M>8) / N(tot) = {ratio_highmass}, N(M>8) / N(low) = {ratio_highmasslowmass}')
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    ratio_highmass = distr.integrate(8, distr.mmax)[0]
    ratio_highmasslowmass = distr.integrate(8, distr.mmax)[0] / distr.integrate(distr.mmin, 8)[0]
    print(f'{distribution} N(M>8) / N(tot) = {ratio_highmass:0.2f}, N(M>8) / N(low) = {ratio_highmasslowmass:0.2f}')
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    ratio_highmass = distr.integrate(8, distr.mmax)[0]
    ratio_highmasslowmass = distr.integrate(8, distr.mmax)[0] / distr.integrate(distr.mmin, 8)[0]
    print(f'{distribution} N(M>8) / N(tot) = {ratio_highmass:0.4f}, N(M>8) / N(low) = {ratio_highmasslowmass:0.4f}')
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    ratio_highmass = distr.m_integrate(8, distr.mmax)[0] / distr.m_integrate(distr.mmin, distr.mmax)[0]
    ratio_highmasslowmass = distr.m_integrate(8, distr.mmax)[0] / distr.m_integrate(distr.mmin, 8)[0]
    print(f'{distribution} N(M>8) / N(tot) = {ratio_highmass:0.4f}, N(M>8) / N(low) = {ratio_highmasslowmass:0.4f}')
imf.salpeter.mmin, imf.salpeter.mmax
#[Out]# (0.3, 120)
import imf
imf.salpeter.mmin, imf.salpeter.mmax
#[Out]# (0.3, 120)
imf.kroupa.mmin, imf.chabrier.mmax
#[Out]# (0.03, inf)
imf.chabrier.mmin, imf.chabrier.mmax
#[Out]# (0, inf)
mmin=0.03
mmax=120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    print(f'{distribution} mean mass: {mass_integral/n_integral:0.2f}')
mmax = 100
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    print(f'{distribution} mean mass: {mass_integral/n_integral:0.2f}')
    
    ratio_highmass = distr.m_integrate(8, distr.mmax)[0] / distr.m_integrate(distr.mmin, distr.mmax)[0]
    ratio_highmasslowmass = distr.m_integrate(8, distr.mmax)[0] / distr.m_integrate(distr.mmin, 8)[0]
    print(f'{distribution} M(M>8) / M(tot) = {ratio_highmass:0.4f}, M(M>8) / M(low) = {ratio_highmasslowmass:0.4f}')

    ratio_highmass = distr.integrate(8, distr.mmax)[0]
    ratio_highmasslowmass = distr.integrate(8, distr.mmax)[0] / distr.integrate(distr.mmin, 8)[0]
    print(f'{distribution} N(M>8) / N(tot) = {ratio_highmass:0.4f}, N(M>8) / N(low) = {ratio_highmasslowmass:0.4f}')
for mmax in (100, 1000):
    print(f'\nM_max = {mmax}')
    for distribution in ('salpeter', 'chabrier', 'kroupa'):
        distr = getattr(imf, distribution)
        mass_integral = distr.m_integrate(mmin, mmax)[0]
        n_integral = distr.integrate(mmin, mmax)[0]
        print(f'{distribution} mean mass: {mass_integral/n_integral:0.2f}')

        ratio_highmass = distr.m_integrate(8, distr.mmax)[0] / distr.m_integrate(distr.mmin, distr.mmax)[0]
        ratio_highmasslowmass = distr.m_integrate(8, distr.mmax)[0] / distr.m_integrate(distr.mmin, 8)[0]
        print(f'{distribution} M(M>8) / M(tot) = {ratio_highmass:0.4f}, M(M>8) / M(low) = {ratio_highmasslowmass:0.4f}')

        ratio_highmass = distr.integrate(8, distr.mmax)[0]
        ratio_highmasslowmass = distr.integrate(8, distr.mmax)[0] / distr.integrate(distr.mmin, 8)[0]
        print(f'{distribution} N(M>8) / N(tot) = {ratio_highmass:0.4f}, N(M>8) / N(low) = {ratio_highmasslowmass:0.4f}')
for mmax in (100, 1000):
    print(f'\nM_max = {mmax}')
    for distribution in ('salpeter', 'chabrier', 'kroupa'):
        distr = getattr(imf, distribution)
        mass_integral = distr.m_integrate(mmin, mmax)[0]
        n_integral = distr.integrate(mmin, mmax)[0]
        print(f'{distribution} mean mass: {mass_integral/n_integral:0.2f}')

        ratio_highmass = distr.m_integrate(8, mmax)[0] / distr.m_integrate(distr.mmin, mmax)[0]
        ratio_highmasslowmass = distr.m_integrate(8, distr.mmax)[0] / distr.m_integrate(distr.mmin, 8)[0]
        print(f'{distribution} M(M>8) / M(tot) = {ratio_highmass:0.4f}, M(M>8) / M(low) = {ratio_highmasslowmass:0.4f}')

        ratio_highmass = distr.integrate(8, mmax)[0]
        ratio_highmasslowmass = distr.integrate(8, distr.mmax)[0] / distr.integrate(distr.mmin, 8)[0]
        print(f'{distribution} N(M>8) / N(tot) = {ratio_highmass:0.4f}, N(M>8) / N(low) = {ratio_highmasslowmass:0.4f}')
########################################################
# Started Logging At: 2022-03-17 09:45:11
########################################################
########################################################
# # Started Logging At: 2022-03-17 09:45:12
########################################################
import imf
imf.salpeter.mmin, imf.salpeter.mmax
#[Out]# (0.3, 120)
imf.kroupa.mmin, imf.kroupa.mmax
#[Out]# (0.03, 120)
imf.chabrier.mmin, imf.chabrier.mmax
#[Out]# (0, inf)
mmin=0.03
mmax=120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    print(f'{distribution} mean mass: {mass_integral/n_integral:0.2f}')
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    ratio_highmass = distr.integrate(8, mmax)[0]
    ratio_highmasslowmass = distr.integrate(8, mmax)[0] / distr.integrate(mmin, 8)[0]
    print(f'{distribution} N(M>8) / N(tot) = {ratio_highmass:0.4f}, N(M>8) / N(low) = {ratio_highmasslowmass:0.4f}')
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    ratio_highmass = distr.m_integrate(8, mmax)[0] / distr.m_integrate(mmin, mmax)[0]
    ratio_highmasslowmass = distr.m_integrate(8, mmax)[0] / distr.m_integrate(mmin, 8)[0]
    print(f'{distribution} M(M>8) / M(tot) = {ratio_highmass:0.4f}, M(M>8) / M(low) = {ratio_highmasslowmass:0.4f}')
for mmax in (100, 1000):
    print(f'\nM_max = {mmax}')
    for distribution in ('salpeter', 'chabrier', 'kroupa'):
        distr = getattr(imf, distribution)
        mass_integral = distr.m_integrate(mmin, mmax)[0]
        n_integral = distr.integrate(mmin, mmax)[0]
        print(f'{distribution} mean mass: {mass_integral/n_integral:0.2f}')

        ratio_highmass = distr.m_integrate(8, mmax)[0] / distr.m_integrate(distr.mmin, mmax)[0]
        ratio_highmasslowmass = distr.m_integrate(8, distr.mmax)[0] / distr.m_integrate(distr.mmin, 8)[0]
        print(f'{distribution} M(M>8) / M(tot) = {ratio_highmass:0.4f}, M(M>8) / M(low) = {ratio_highmasslowmass:0.4f}')

        ratio_highmass = distr.integrate(8, mmax)[0]
        ratio_highmasslowmass = distr.integrate(8, distr.mmax)[0] / distr.integrate(distr.mmin, 8)[0]
        print(f'{distribution} N(M>8) / N(tot) = {ratio_highmass:0.4f}, N(M>8) / N(low) = {ratio_highmasslowmass:0.4f}')
for mmax in (100, 1000):
    print(f'\nM_max = {mmax}')
    for distribution in ('salpeter', 'chabrier', 'kroupa'):
        distr = getattr(imf, distribution)
        mass_integral = distr.m_integrate(mmin, mmax)[0]
        n_integral = distr.integrate(mmin, mmax)[0]
        print(f'{distribution} mean mass: {mass_integral/n_integral:0.2f}')

        ratio_highmass = distr.m_integrate(8, mmax)[0] / distr.m_integrate(mmin, mmax)[0]
        ratio_highmasslowmass = distr.m_integrate(8, mmax)[0] / distr.m_integrate(mmin, 8)[0]
        print(f'{distribution} M(M>8) / M(tot) = {ratio_highmass:0.4f}, M(M>8) / M(low) = {ratio_highmasslowmass:0.4f}')

        ratio_highmass = distr.integrate(8, mmax)[0]
        ratio_highmasslowmass = distr.integrate(8, mmax)[0] / distr.integrate(mmin, 8)[0]
        print(f'{distribution} N(M>8) / N(tot) = {ratio_highmass:0.4f}, N(M>8) / N(low) = {ratio_highmasslowmass:0.4f}')
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    frac_highmass = distr.integrate(8, mmax)[0]

    print(f'{distribution} N(M>8) = {frac_highmass*1000}')
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    mean_highmass = distr.m_integrate(8, mmax)[0] / distr.integrate(8, mmax)[0]

    print(f'{distribution} Mean M(M>8) = {meanhighmass}')
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    mean_highmass = distr.m_integrate(8, mmax)[0] / distr.integrate(8, mmax)[0]

    print(f'{distribution} Mean M(M>8) = {mean_highmass}')
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    frac_highmass = distr.m_integrate(8, mmax)[0] / distr.m_integrate(mmin, mmax)[0]
    mean_highmass = distr.m_integrate(8, mmax)[0] / distr.integrate(8, mmax)[0]

    print(f'{distribution} N(M>8) = {frac_highmass*1000 / mean_highmass}')
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    massrange = np.linspace(8, 100)
    frac_highmass = distr.n_integrate(massrange)
    print(frac_highmass)
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    massrange = np.linspace(8, 100)
    frac_highmass = distr.integrate(massrange)
    print(frac_highmass)
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    massrange = np.linspace(8, 100)
    frac_highmass = distr.integrate(massrange, mmax)
    print(frac_highmass)
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    massrange = np.linspace(8, 100)
    frac_highmass = [distr.integrate(mr, mmax) for mr in massrange]
    pl.plot(massrange, 1/frac_highmass)
get_ipython().run_line_magic('matplotlib', 'inline')
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    massrange = np.linspace(8, 100)
    frac_highmass = [distr.integrate(mr, mmax) for mr in massrange]
    pl.plot(massrange, 1/frac_highmass)
get_ipython().run_line_magic('matplotlib', 'inline')
import pylab as pl
pl.rcParams['figure.facecolor'] = 'w'
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    massrange = np.linspace(8, 100)
    frac_highmass = [distr.integrate(mr, mmax) for mr in massrange]
    pl.plot(massrange, 1/frac_highmass)
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    massrange = np.linspace(8, 100)
    frac_highmass = np.array([distr.integrate(mr, mmax) for mr in massrange])
    pl.plot(massrange, 1/frac_highmass)
imf.salpeter.mmin, imf.salpeter.mmax
#[Out]# (0.3, 120)
imf.kroupa.mmin, imf.kroupa.mmax
#[Out]# (0.03, 120)
imf.chabrier.mmin, imf.chabrier.mmax
#[Out]# (0, inf)
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    massrange = np.linspace(8, 100)
    frac_highmass = np.array([distr.integrate(mr, mmax) for mr in massrange])
    pl.plot(massrange, 1/frac_highmass, label=distribution)
pl.legend(loc='best')
#[Out]# <matplotlib.legend.Legend at 0x12740a910>
mmax = 120
pl.clf()
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    massrange = np.linspace(8, 100)
    frac_highmass = np.array([distr.integrate(mr, mmax) for mr in massrange])
    pl.plot(massrange, 1/frac_highmass, label=distribution)
pl.legend(loc='best')
#[Out]# <matplotlib.legend.Legend at 0x1272eb280>
mmax = 120
pl.clf()
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    massrange = np.linspace(8, 100)
    frac_highmass = np.array([distr.integrate(mr, mmax)[0] for mr in massrange])
    pl.plot(massrange, 1/frac_highmass, label=distribution)
pl.legend(loc='best')
#[Out]# <matplotlib.legend.Legend at 0x10d436c10>
mmax = 120
pl.clf()
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    massrange = np.linspace(8, 100)
    frac_highmass = np.array([distr.integrate(mr, mmax)[0] for mr in massrange])
    pl.loglog(massrange, 1/frac_highmass, label=distribution)
pl.legend(loc='best')
#[Out]# <matplotlib.legend.Legend at 0x127337af0>
mmax = 120
pl.clf()
for mstar in (10,100):
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    massrange = np.linspace(8, 100)
    frac_highmass = distr.integrate(mstar, mmax)[0]
    print(f"{distribution}: nstars to make {mstar} = {int(1/frac_highmass)}")
mmax = 120
pl.clf()
for mstar in (10,100):
    for distribution in ('salpeter', 'chabrier', 'kroupa'):
        distr = getattr(imf, distribution)
        massrange = np.linspace(8, 100)
        frac_highmass = distr.integrate(mstar, mmax)[0]
        print(f"{distribution}: nstars to make {mstar} = {int(1/frac_highmass)}")
mmax = 120
pl.clf()
for mstar in (10,100):
    print()
    for distribution in ('salpeter', 'chabrier', 'kroupa'):
        distr = getattr(imf, distribution)
        massrange = np.linspace(8, 100)
        frac_highmass = distr.integrate(mstar, mmax)[0]
        print(f"{distribution}: nstars to make {mstar} = {int(1/frac_highmass)}")
mmax = 120
for mstar in (10,100):
    print()
    for distribution in ('salpeter', 'chabrier', 'kroupa'):
        distr = getattr(imf, distribution)
        massrange = np.linspace(8, 100)
        frac_highmass = distr.integrate(mstar, mmax)[0]
        print(f"{distribution}: nstars to make {mstar} = {int(1/frac_highmass)}")
mmax = 120
pl.clf()
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    massrange = np.linspace(8, 100)
    frac_highmass = np.array([distr.integrate(mr, mmax)[0] for mr in massrange])
    
    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    meanmass = mass_integral/n_integral
    
    pl.loglog(massrange, meanmass * 1/frac_highmass, label=distribution)
pl.legend(loc='best')
pl.xlabel("$M_{max,cl}$")
pl.ylabel("$M_{*,cl}$")
#[Out]# Text(0, 0.5, '$M_{*,cl}$')
mmax = 120
pl.clf()
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    massrange = np.linspace(8, 100)
    frac_highmass = np.array([distr.integrate(mr, mmax)[0] for mr in massrange])
    pl.loglog(massrange, 1/frac_highmass, label=distribution)
pl.legend(loc='best')
pl.xlabel("$M_{max,cl}$")
pl.ylabel("$N_{*,cl}$")
#[Out]# Text(0, 0.5, '$N_{*,cl}$')
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    
    n_integral_100 = distr.integrate(100, mmax)[0]

    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]    
    meanmass = mass_integral/n_integral
    
    minmass_cluster = 0.95 / n_integral_100 * meanmass
    
    print(f"{distribution}: Min mass for >1 100 Msun star at 95%: {minmass_cluster}")
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    
    n_integral_100 = distr.integrate(100, mmax)[0]

    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]    
    meanmass = mass_integral/n_integral
    
    nstar = np.log(1-0.95) / np.log(n_integral_100)
    
    minmass_cluster = meanmass*nstar
    
    print(f"{distribution}: Min mass for >1 100 Msun star at 95%: {minmass_cluster} nstars={nstar}")
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    
    n_integral_100 = 1-distr.integrate(100, mmax)[0]

    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]    
    meanmass = mass_integral/n_integral
    
    nstar = np.log(1-0.95) / np.log(n_integral_100)
    
    minmass_cluster = meanmass*nstar
    
    print(f"{distribution}: Min mass for >1 100 Msun star at 95%: {minmass_cluster} nstars={nstar}")
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    
    n_integral_100 = 1-distr.integrate(100, mmax)[0]

    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]    
    meanmass = mass_integral/n_integral
    
    nstar = np.log(1-0.95) / np.log(n_integral_100)
    
    minmass_cluster = meanmass*nstar
    
    print(f"{distribution}: Min mass for >1 100 Msun star at 95%: {minmass_cluster:0.2g} nstars={int(nstar)}")
1/6 * (5/6)**99
#[Out]# 2.4149346944827437e-09
1/6
#[Out]# 0.16666666666666666
1/6 * 5/6
#[Out]# 0.13888888888888887
1/6 * 5/6 * 2
#[Out]# 0.27777777777777773
1/6 * 5/6**2 * 3
#[Out]# 0.06944444444444445
1/6 * 5/6**3 * 4
#[Out]# 0.015432098765432098
1/6 * 5/6 
#[Out]# 0.13888888888888887
1/6 * 5/6  + 1/6*5/6
#[Out]# 0.27777777777777773
(1-(1/6)**2 - (5/6)**2)
#[Out]# 0.2777777777777777
(1-(1/6)**3 - (1/6)**2*5/6*3 - 5/6**3)
#[Out]# 0.9027777777777778
1- ((1/6)**3 - (1/6)**2*5/6*3 - 5/6**3)
#[Out]# 1.087962962962963
1- ((1/6)**3 +(1/6)**2*5/6*3 + 5/6**3)
#[Out]# 0.9027777777777778
1- ((1/6)**3 +(1/6)**2*5/6*3 + (5/6)**3)
#[Out]# 0.3472222222222221
1- ((1/6)**3 +(1/6)**2*(5/6)*3 + (5/6)**3)
#[Out]# 0.3472222222222221
((1/6)**3 + (1/6)**2*(5/6)*3 + (5/6)**3) + (1/6)*(5/6)**2*3
#[Out]# 1.0000000000000002
1/6 * (5/6)**2 * 3
#[Out]# 0.34722222222222227
1/6 * (5/6)**3 * 4
#[Out]# 0.3858024691358025
nrolls = np.arange(1,100)
pl.plot(nrolls, (1/6) * (5/6)**(nrolls-1) * (nrolls-1))
#[Out]# [<matplotlib.lines.Line2D at 0x127f15850>]
nrolls = np.arange(1,30)
pl.plot(nrolls, (1/6) * (5/6)**(nrolls-1) * (nrolls-1))
pl.ylabel("P(N(six) = 1)")
pl.xlabel("Number of rolls")
#[Out]# Text(0.5, 0, 'Number of rolls')
nrolls = np.arange(1,20)
pl.plot(nrolls, (1/6) * (5/6)**(nrolls-1) * (nrolls-1))
pl.ylabel("P(N(six) = 1)")
pl.xlabel("Number of rolls")
#[Out]# Text(0.5, 0, 'Number of rolls')
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    
    n_integral_100 = 1-distr.integrate(100, mmax)[0]
    print(f"{distribution} P(>100) = {n_integral_100}")


    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    meanmass = mass_integral/n_integral
    
    nstar = np.log(1-0.95) / np.log(n_integral_100)
    
    minmass_cluster = meanmass*nstar
    
    print(f"{distribution}: Min mass for >1 100 Msun star at 95%: {minmass_cluster:0.2g} nstars={int(nstar)}")
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    
    n_integral_100 = 1-distr.integrate(100, mmax)[0]
    print(f"{distribution} P(>100) = {n_integral_100}, 1/(1-P(>100)={1/(1-n_integral_100)}")


    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    meanmass = mass_integral/n_integral
    
    nstar = np.log(1-0.95) / np.log(n_integral_100)
    
    minmass_cluster = meanmass*nstar
    
    print(f"{distribution}: Min mass for >1 100 Msun star at 95%: {minmass_cluster:0.2g} nstars={int(nstar)}")
Probability of one successful roll out of two attempts
########################################################
# Started Logging At: 2022-03-17 11:16:13
########################################################
########################################################
# # Started Logging At: 2022-03-17 11:16:14
########################################################
import imf
imf.salpeter.mmin, imf.salpeter.mmax
#[Out]# (0.3, 120)
imf.kroupa.mmin, imf.kroupa.mmax
#[Out]# (0.03, 120)
imf.chabrier.mmin, imf.chabrier.mmax
#[Out]# (0, inf)
mmin=0.03
mmax=120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    print(f'{distribution} mean mass: {mass_integral/n_integral:0.2f}')
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    mean_highmass = distr.m_integrate(8, mmax)[0] / distr.integrate(8, mmax)[0]

    print(f'{distribution} Mean M(M>8) = {mean_highmass}')
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    ratio_highmass = distr.integrate(8, mmax)[0]
    ratio_highmasslowmass = distr.integrate(8, mmax)[0] / distr.integrate(mmin, 8)[0]
    print(f'{distribution} N(M>8) / N(tot) = {ratio_highmass:0.4f}, N(M>8) / N(low) = {ratio_highmasslowmass:0.4f}')
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    ratio_highmass = distr.m_integrate(8, mmax)[0] / distr.m_integrate(mmin, mmax)[0]
    ratio_highmasslowmass = distr.m_integrate(8, mmax)[0] / distr.m_integrate(mmin, 8)[0]
    print(f'{distribution} M(M>8) / M(tot) = {ratio_highmass:0.4f}, M(M>8) / M(low) = {ratio_highmasslowmass:0.4f}')
for mmax in (100, 1000):
    print(f'\nM_max = {mmax}')
    for distribution in ('salpeter', 'chabrier', 'kroupa'):
        distr = getattr(imf, distribution)
        mass_integral = distr.m_integrate(mmin, mmax)[0]
        n_integral = distr.integrate(mmin, mmax)[0]
        print(f'{distribution} mean mass: {mass_integral/n_integral:0.2f}')

        ratio_highmass = distr.m_integrate(8, mmax)[0] / distr.m_integrate(mmin, mmax)[0]
        ratio_highmasslowmass = distr.m_integrate(8, mmax)[0] / distr.m_integrate(mmin, 8)[0]
        print(f'{distribution} M(M>8) / M(tot) = {ratio_highmass:0.4f}, M(M>8) / M(low) = {ratio_highmasslowmass:0.4f}')

        ratio_highmass = distr.integrate(8, mmax)[0]
        ratio_highmasslowmass = distr.integrate(8, mmax)[0] / distr.integrate(mmin, 8)[0]
        print(f'{distribution} N(M>8) / N(tot) = {ratio_highmass:0.4f}, N(M>8) / N(low) = {ratio_highmasslowmass:0.4f}')
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    frac_highmass = distr.integrate(8, mmax)[0]

    print(f'{distribution} N(M>8) = {frac_highmass*1000}')
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    frac_highmass = distr.m_integrate(8, mmax)[0] / distr.m_integrate(mmin, mmax)[0]
    mean_highmass = distr.m_integrate(8, mmax)[0] / distr.integrate(8, mmax)[0]

    print(f'{distribution} N(M>8) = {frac_highmass*1000 / mean_highmass}')
get_ipython().run_line_magic('matplotlib', 'inline')
import pylab as pl
pl.rcParams['figure.facecolor'] = 'w'
mmax = 120
for mstar in (10,100):
    print()
    for distribution in ('salpeter', 'chabrier', 'kroupa'):
        distr = getattr(imf, distribution)
        massrange = np.linspace(8, 100)
        frac_highmass = distr.integrate(mstar, mmax)[0]
        print(f"{distribution}: nstars to make {mstar} = {int(1/frac_highmass)}")
mmax = 120
pl.clf()
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    massrange = np.linspace(8, 100)
    frac_highmass = np.array([distr.integrate(mr, mmax)[0] for mr in massrange])
    pl.loglog(massrange, 1/frac_highmass, label=distribution)
pl.legend(loc='best')
pl.xlabel("$M_{max,cl}$")
pl.ylabel("$N_{*,cl}$")
#[Out]# Text(0, 0.5, '$N_{*,cl}$')
mmax = 120
pl.clf()
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    massrange = np.linspace(8, 100)
    frac_highmass = np.array([distr.integrate(mr, mmax)[0] for mr in massrange])
    
    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    meanmass = mass_integral/n_integral
    
    pl.loglog(massrange, meanmass * 1/frac_highmass, label=distribution)
pl.legend(loc='best')
pl.xlabel("$M_{max,cl}$")
pl.ylabel("$M_{*,cl}$")
#[Out]# Text(0, 0.5, '$M_{*,cl}$')
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    
    n_integral_100 = 1-distr.integrate(100, mmax)[0]
    print(f"{distribution} P(>100) = {n_integral_100}, 1/(1-P(>100)={1/(1-n_integral_100)}")


    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    meanmass = mass_integral/n_integral
    
    nstar = np.log(1-0.95) / np.log(n_integral_100)
    
    minmass_cluster = meanmass*nstar
    
    print(f"{distribution}: Min mass for >1 100 Msun star at 95%: {minmass_cluster:0.2g} nstars={int(nstar)}")
1/6
#[Out]# 0.16666666666666666
1/6 * 5/6  + 1/6*5/6
#[Out]# 0.27777777777777773
(1-(1/6)**2 - (5/6)**2)
#[Out]# 0.2777777777777777
1/6 * (5/6)**2 * 3
#[Out]# 0.34722222222222227
1- ((1/6)**3 + (1/6)**2*(5/6)*3 + (5/6)**3)
#[Out]# 0.3472222222222221
((1/6)**3 + (1/6)**2*(5/6)*3 + (5/6)**3) + (1/6)*(5/6)**2*3
#[Out]# 1.0000000000000002
nrolls = np.arange(1,20)
pl.plot(nrolls, (1/6) * (5/6)**(nrolls-1) * (nrolls-1))
pl.ylabel("P(N(six) = 1)")
pl.xlabel("Number of rolls")
#[Out]# Text(0.5, 0, 'Number of rolls')
mmax = 120
pl.clf()
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    massrange = np.linspace(8, 100)
    frac_highmass = np.array([distr.integrate(mr, mmax)[0] for mr in massrange])
    
    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    meanmass = mass_integral/n_integral
    
    pl.loglog(massrange, meanmass * 1/frac_highmass, label=distribution)
    print(f"{distribution}: mass(100Msun) = {meanmass / frac_highmass[-1]}, N(100msun) = {int(1/frac_highmass[-1])}")
pl.legend(loc='best')
pl.xlabel("$M_{max,cl}$")
pl.ylabel("$M_{*,cl}$")
#[Out]# Text(0, 0.5, '$M_{*,cl}$')
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    
    n_integral_100 = 1-distr.integrate(100, mmax)[0]
    print(f"{distribution} P(>100) = {n_integral_100}, 1/(1-P(>100)={1/(1-n_integral_100)}")


    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    meanmass = mass_integral/n_integral
    
    nstar = np.log(1-0.95) / np.log(n_integral_100)
    nstar50 = np.log(1-0.5) / np.log(n_integral_100)

    
    minmass_cluster = meanmass*nstar
    
    print(f"{distribution}: Min mass for >1 100 Msun star at 95%: {minmass_cluster:0.2g} nstars={int(nstar)}")
    print(f"{distribution}: Min mass for >1 100 Msun star at 50%: {meanmass*nstar50:0.2g} nstars={int(nstar50)}")
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    
    n_integral_100 = 1-distr.integrate(100, mmax)[0]
    print(f"{distribution} P(>100) = {n_integral_100}, 1/(1-P(>100)={1/(1-n_integral_100)}")


    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    meanmass = mass_integral/n_integral
    
    nstar = np.log(1-0.95) / np.log(n_integral_100)
    nstar50 = np.log(1-0.68) / np.log(n_integral_100)

    
    minmass_cluster = meanmass*nstar
    
    print(f"{distribution}: Min mass for >1 100 Msun star at 95%: {minmass_cluster:0.2g} nstars={int(nstar)}")
    print(f"{distribution}: Min mass for >1 100 Msun star at 50%: {meanmass*nstar50:0.2g} nstars={int(nstar50)}")
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    
    n_integral_100 = 1-distr.integrate(100, mmax)[0]
    print(f"{distribution} P(>100) = {n_integral_100}, 1/(1-P(>100)={int(1/(1-n_integral_100))}")


    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    meanmass = mass_integral/n_integral
    
    nstar = np.log(1-0.95) / np.log(n_integral_100)
    nstar50 = np.log(1-0.68) / np.log(n_integral_100)

    
    minmass_cluster = meanmass*nstar
    
    print(f"{distribution}: Min mass for >1 100 Msun star at 95%: {minmass_cluster:0.2g} nstars={int(nstar)}")
    print(f"{distribution}: Min mass for >1 100 Msun star at 50%: {meanmass*nstar50:0.2g} nstars={int(nstar50)}")
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    
    n_integral_100 = 1-distr.integrate(100, mmax)[0]
    print(f"{distribution} P(>100) = {n_integral_100}, 1/(1-P(>100)={int(1/(1-n_integral_100))}")


    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    meanmass = mass_integral/n_integral
    
    nstar = np.log(1-0.95) / np.log(n_integral_100)
    nstar50 = np.log(1-0.65) / np.log(n_integral_100)

    
    minmass_cluster = meanmass*nstar
    
    print(f"{distribution}: Min mass for >1 100 Msun star at 95%: {minmass_cluster:0.2g} nstars={int(nstar)}")
    print(f"{distribution}: Min mass for >1 100 Msun star at 50%: {meanmass*nstar50:0.2g} nstars={int(nstar50)}")
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    
    n_integral_100 = 1-distr.integrate(100, mmax)[0]
    print(f"{distribution} P(>100) = {n_integral_100}, 1/(1-P(>100)={int(1/(1-n_integral_100))}")


    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    meanmass = mass_integral/n_integral
    
    nstar = np.log(1-0.95) / np.log(n_integral_100)
    nstar50 = np.log(1-0.63) / np.log(n_integral_100)

    
    minmass_cluster = meanmass*nstar
    
    print(f"{distribution}: Min mass for >1 100 Msun star at 95%: {minmass_cluster:0.2g} nstars={int(nstar)}")
    print(f"{distribution}: Min mass for >1 100 Msun star at 50%: {meanmass*nstar50:0.2g} nstars={int(nstar50)}")
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    
    n_integral_100 = 1-distr.integrate(100, mmax)[0]
    print(f"{distribution} P(>100) = {n_integral_100}, 1/(1-P(>100)={int(1/(1-n_integral_100))}")


    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    meanmass = mass_integral/n_integral
    
    nstar = np.log(1-0.95) / np.log(n_integral_100)
    nstar50 = np.log(1-0.62) / np.log(n_integral_100)

    
    minmass_cluster = meanmass*nstar
    
    print(f"{distribution}: Min mass for >1 100 Msun star at 95%: {minmass_cluster:0.2g} nstars={int(nstar)}")
    print(f"{distribution}: Min mass for >1 100 Msun star at 50%: {meanmass*nstar50:0.2g} nstars={int(nstar50)}")
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    
    n_integral_100 = 1-distr.integrate(100, mmax)[0]
    print(f"{distribution} P(>100) = {n_integral_100}, 1/(1-P(>100)={int(1/(1-n_integral_100))}")


    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    meanmass = mass_integral/n_integral
    
    nstar = np.log(1-0.95) / np.log(n_integral_100)
    nstar50 = np.log(1-0.62.5) / np.log(n_integral_100)

    
    minmass_cluster = meanmass*nstar
    
    print(f"{distribution}: Min mass for >1 100 Msun star at 95%: {minmass_cluster:0.2g} nstars={int(nstar)}")
    print(f"{distribution}: Min mass for >1 100 Msun star at 50%: {meanmass*nstar50:0.2g} nstars={int(nstar50)}")
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    
    n_integral_100 = 1-distr.integrate(100, mmax)[0]
    print(f"{distribution} P(>100) = {n_integral_100}, 1/(1-P(>100)={int(1/(1-n_integral_100))}")


    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    meanmass = mass_integral/n_integral
    
    nstar = np.log(1-0.95) / np.log(n_integral_100)
    nstar50 = np.log(1-0.625) / np.log(n_integral_100)

    
    minmass_cluster = meanmass*nstar
    
    print(f"{distribution}: Min mass for >1 100 Msun star at 95%: {minmass_cluster:0.2g} nstars={int(nstar)}")
    print(f"{distribution}: Min mass for >1 100 Msun star at 50%: {meanmass*nstar50:0.2g} nstars={int(nstar50)}")
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    
    n_integral_100 = 1-distr.integrate(100, mmax)[0]
    print(f"{distribution} P(>100) = {n_integral_100}, 1/(1-P(>100)={int(1/(1-n_integral_100))}")


    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    meanmass = mass_integral/n_integral
    
    nstar = np.log(1-0.95) / np.log(n_integral_100)
    nstar50 = np.log(1-0.628) / np.log(n_integral_100)

    
    minmass_cluster = meanmass*nstar
    
    print(f"{distribution}: Min mass for >1 100 Msun star at 95%: {minmass_cluster:0.2g} nstars={int(nstar)}")
    print(f"{distribution}: Min mass for >1 100 Msun star at 50%: {meanmass*nstar50:0.2g} nstars={int(nstar50)}")
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    
    n_integral_100 = 1-distr.integrate(100, mmax)[0]
    print(f"{distribution} P(>100) = {n_integral_100}, 1/(1-P(>100)={int(1/(1-n_integral_100))}")


    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    meanmass = mass_integral/n_integral
    
    nstar = np.log(1-0.95) / np.log(n_integral_100)
    nstar50 = np.log(1-0.63) / np.log(n_integral_100)

    
    minmass_cluster = meanmass*nstar
    
    print(f"{distribution}: Min mass for >1 100 Msun star at 95%: {minmass_cluster:0.2g} nstars={int(nstar)}")
    print(f"{distribution}: Min mass for >1 100 Msun star at 50%: {meanmass*nstar50:0.2g} nstars={int(nstar50)}")
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    
    n_integral_100 = 1-distr.integrate(100, mmax)[0]
    print(f"{distribution} P(>100) = {n_integral_100}, 1/(1-P(>100)={int(1/(1-n_integral_100))}")


    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    meanmass = mass_integral/n_integral
    
    nstar = np.log(1-0.95) / np.log(n_integral_100)
    nstar50 = np.log(1-0.64) / np.log(n_integral_100)

    
    minmass_cluster = meanmass*nstar
    
    print(f"{distribution}: Min mass for >1 100 Msun star at 95%: {minmass_cluster:0.2g} nstars={int(nstar)}")
    print(f"{distribution}: Min mass for >1 100 Msun star at 50%: {meanmass*nstar50:0.2g} nstars={int(nstar50)}")
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    
    n_integral_100 = 1-distr.integrate(100, mmax)[0]
    print(f"{distribution} P(>100) = {n_integral_100}, 1/(1-P(>100)={int(1/(1-n_integral_100))}")


    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    meanmass = mass_integral/n_integral
    
    nstar = np.log(1-0.95) / np.log(n_integral_100)
    nstar50 = np.log(1-0.635) / np.log(n_integral_100)

    
    minmass_cluster = meanmass*nstar
    
    print(f"{distribution}: Min mass for >1 100 Msun star at 95%: {minmass_cluster:0.2g} nstars={int(nstar)}")
    print(f"{distribution}: Min mass for >1 100 Msun star at 50%: {meanmass*nstar50:0.2g} nstars={int(nstar50)}")
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    
    n_integral_100 = 1-distr.integrate(100, mmax)[0]
    print(f"{distribution} P(>100) = {n_integral_100}, 1/(1-P(>100)={int(1/(1-n_integral_100))}")


    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    meanmass = mass_integral/n_integral
    
    nstar = np.log(1-0.95) / np.log(n_integral_100)
    nstar50 = np.log(1-0.632) / np.log(n_integral_100)

    
    minmass_cluster = meanmass*nstar
    
    print(f"{distribution}: Min mass for >1 100 Msun star at 95%: {minmass_cluster:0.2g} nstars={int(nstar)}")
    print(f"{distribution}: Min mass for >1 100 Msun star at 50%: {meanmass*nstar50:0.2g} nstars={int(nstar50)}")
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    
    n_integral_100 = 1-distr.integrate(100, mmax)[0]
    print(f"{distribution} P(>100) = {n_integral_100}, 1/(1-P(>100)={int(1/(1-n_integral_100))}")


    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    meanmass = mass_integral/n_integral
    
    nstar = np.log(1-0.95) / np.log(n_integral_100)
    nstar50 = np.log(1-0.6321) / np.log(n_integral_100)

    
    minmass_cluster = meanmass*nstar
    
    print(f"{distribution}: Min mass for >1 100 Msun star at 95%: {minmass_cluster:0.2g} nstars={int(nstar)}")
    print(f"{distribution}: Min mass for >1 100 Msun star at 50%: {meanmass*nstar50:0.2g} nstars={int(nstar50)}")
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    def lum(x):
        return m**3 * imf(x)
    lum_int = scipy.integrate.quad(lum, mmin, mmax)
    mass_int = imf.m_integrate(mmin,mmax)
    
    print(f"{distribution}: L/M = {lum_int/mass_int:0.1f}")
import scipy.integrate
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    def lum(x):
        return m**3 * imf(x)
    lum_int = scipy.integrate.quad(lum, mmin, mmax)
    mass_int = imf.m_integrate(mmin,mmax)
    
    print(f"{distribution}: L/M = {lum_int/mass_int:0.1f}")
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    def lum(x):
        return m**3 * imf(x)
    lum_int = scipy.integrate.quad(lum, mmin, mmax)[0]
    mass_int = imf.m_integrate(mmin,mmax)
    
    print(f"{distribution}: L/M = {lum_int/mass_int:0.1f}")
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    def lum(x):
        return x**3 * imf(x)
    lum_int = scipy.integrate.quad(lum, mmin, mmax)[0]
    mass_int = imf.m_integrate(mmin,mmax)
    
    print(f"{distribution}: L/M = {lum_int/mass_int:0.1f}")
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    def lum(x):
        return x**3 * distr(x)
    lum_int = scipy.integrate.quad(lum, mmin, mmax)[0]
    mass_int = imf.m_integrate(mmin,mmax)
    
    print(f"{distribution}: L/M = {lum_int/mass_int:0.1f}")
mmax = 120
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=mmin, mmax=mmax)
    def lum(x):
        return x**3 * distr(x)
    lum_int = scipy.integrate.quad(lum, mmin, mmax)[0]
    mass_int = imf.m_integrate(mmin,mmax)[0]
    
    print(f"{distribution}: L/M = {lum_int/mass_int:0.1f}")
mmax = 120
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=mmin, mmax=mmax)
    def lum(x):
        return x**3 * distr(x)
    lum_int = scipy.integrate.quad(lum, mmin, mmax)[0]
    mass_int = imf.m_integrate(mmin,mmax)
    
    print(f"{distribution}: L/M = {lum_int/mass_int:0.1f}")
mmax = 120
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=mmin, mmax=mmax)
    def lum(x):
        return x**3 * distr(x)
    lum_int = scipy.integrate.quad(lum, mmin, mmax)[0]
    mass_int = distr.m_integrate(mmin,mmax)
    
    print(f"{distribution}: L/M = {lum_int/mass_int:0.1f}")
mmax = 120
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=mmin, mmax=mmax)
    def lum(x):
        return x**3 * distr(x)
    lum_int = scipy.integrate.quad(lum, mmin, mmax)[0]
    mass_int = distr.m_integrate(mmin,mmax)[0]
    
    print(f"{distribution}: L/M = {lum_int/mass_int:0.1f}")
mmax = 120
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=mmin, mmax=mmax)
    def lum(x):
        return 2*(x/2)**3 * distr(x)
    lum_int = scipy.integrate.quad(lum, mmin, mmax)[0]
    mass_int = distr.m_integrate(mmin,mmax)[0]
    
    print(f"{distribution}: L/M = {lum_int/mass_int:0.1f}")
mmin = 0.03
mmax = 120
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=mmin, mmax=mmax)
    def lum(x):
        return 2*(x/2)**3 * distr(x)
    lum_int = scipy.integrate.quad(lum, mmin, mmax)[0]
    mass_int = distr.m_integrate(mmin,mmax)[0]
    
    print(f"{distribution}: L/M = {lum_int/mass_int:0.1f}")
mmin = 0.3
mmax = 120
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=mmin, mmax=mmax)
    def lum(x):
        return 2*(x/2)**3 * distr(x)
    lum_int = scipy.integrate.quad(lum, mmin, mmax)[0]
    mass_int = distr.m_integrate(mmin,mmax)[0]
    
    print(f"{distribution}: L/M = {lum_int/mass_int:0.1f}")
mmin = 0.25
mmax = 120
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=mmin, mmax=mmax)
    def lum(x):
        return 2*(x/2)**3 * distr(x)
    lum_int = scipy.integrate.quad(lum, mmin, mmax)[0]
    mass_int = distr.m_integrate(mmin,mmax)[0]
    
    print(f"{distribution}: L/M = {lum_int/mass_int:0.1f}")
mmin = 0.25
mmax = 120
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=0.01, mmax=120)
    def lum(x):
        return 2*(x/2)**3 * distr(x)
    lum_int = scipy.integrate.quad(lum, mmin, mmax)[0]
    mass_int = distr.m_integrate(mmin,mmax)[0]
    
    print(f"{distribution}: L/M = {lum_int/mass_int:0.1f}")
mmin = 0.3
mmax = 120
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=0.01, mmax=120)
    def lum(x):
        return 2*(x/2)**3 * distr(x)
    lum_int = scipy.integrate.quad(lum, mmin, mmax)[0]
    mass_int = distr.m_integrate(mmin,mmax)[0]
    
    print(f"{distribution}: L/M = {lum_int/mass_int:0.1f}")
masses = np.geomspace(0.03, 120, 1000)
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    pl.loglog(masses, distr(masses), label=distribution)
pl.legend(loc='best')
#[Out]# <matplotlib.legend.Legend at 0x1279f8af0>
get_ipython().run_line_magic('matplotlib', 'inline')
import pylab as pl
pl.rcParams['figure.facecolor'] = 'w'
masses = np.geomspace(0.03, 120, 1000)
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    pl.loglog(masses, distr(masses), label=distribution)
pl.legend(loc='best')
#[Out]# <matplotlib.legend.Legend at 0x127b87e20>
########################################################
# Started Logging At: 2022-03-17 11:52:15
########################################################
########################################################
# # Started Logging At: 2022-03-17 11:52:17
########################################################
import imf
imf.salpeter.mmin, imf.salpeter.mmax
#[Out]# (0.3, 120)
imf.kroupa.mmin, imf.kroupa.mmax
#[Out]# (0.03, 120)
imf.chabrier.mmin, imf.chabrier.mmax
#[Out]# (0, inf)
mmin=0.03
mmax=120
get_ipython().run_line_magic('matplotlib', 'inline')
import pylab as pl
pl.rcParams['figure.facecolor'] = 'w'
masses = np.geomspace(0.03, 120, 1000)
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    pl.loglog(masses, distr(masses), label=distribution)
pl.legend(loc='best')
#[Out]# <matplotlib.legend.Legend at 0x1280a34c0>
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    print(f'{distribution} mean mass: {mass_integral/n_integral:0.2f}')
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    mean_highmass = distr.m_integrate(8, mmax)[0] / distr.integrate(8, mmax)[0]

    print(f'{distribution} Mean M(M>8) = {mean_highmass}')
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    ratio_highmass = distr.integrate(8, mmax)[0]
    ratio_highmasslowmass = distr.integrate(8, mmax)[0] / distr.integrate(mmin, 8)[0]
    print(f'{distribution} N(M>8) / N(tot) = {ratio_highmass:0.4f}, N(M>8) / N(low) = {ratio_highmasslowmass:0.4f}')
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    ratio_highmass = distr.m_integrate(8, mmax)[0] / distr.m_integrate(mmin, mmax)[0]
    ratio_highmasslowmass = distr.m_integrate(8, mmax)[0] / distr.m_integrate(mmin, 8)[0]
    print(f'{distribution} M(M>8) / M(tot) = {ratio_highmass:0.4f}, M(M>8) / M(low) = {ratio_highmasslowmass:0.4f}')
for mmax in (100, 1000):
    print(f'\nM_max = {mmax}')
    for distribution in ('salpeter', 'chabrier', 'kroupa'):
        distr = getattr(imf, distribution)
        mass_integral = distr.m_integrate(mmin, mmax)[0]
        n_integral = distr.integrate(mmin, mmax)[0]
        print(f'{distribution} mean mass: {mass_integral/n_integral:0.2f}')

        ratio_highmass = distr.m_integrate(8, mmax)[0] / distr.m_integrate(mmin, mmax)[0]
        ratio_highmasslowmass = distr.m_integrate(8, mmax)[0] / distr.m_integrate(mmin, 8)[0]
        print(f'{distribution} M(M>8) / M(tot) = {ratio_highmass:0.4f}, M(M>8) / M(low) = {ratio_highmasslowmass:0.4f}')

        ratio_highmass = distr.integrate(8, mmax)[0]
        ratio_highmasslowmass = distr.integrate(8, mmax)[0] / distr.integrate(mmin, 8)[0]
        print(f'{distribution} N(M>8) / N(tot) = {ratio_highmass:0.4f}, N(M>8) / N(low) = {ratio_highmasslowmass:0.4f}')
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    frac_highmass = distr.integrate(8, mmax)[0]

    print(f'{distribution} N(M>8) = {frac_highmass*1000}')
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    frac_highmass = distr.m_integrate(8, mmax)[0] / distr.m_integrate(mmin, mmax)[0]
    mean_highmass = distr.m_integrate(8, mmax)[0] / distr.integrate(8, mmax)[0]

    print(f'{distribution} N(M>8) = {frac_highmass*1000 / mean_highmass}')
mmax = 120
for mstar in (10,100):
    print()
    for distribution in ('salpeter', 'chabrier', 'kroupa'):
        distr = getattr(imf, distribution)
        massrange = np.linspace(8, 100)
        frac_highmass = distr.integrate(mstar, mmax)[0]
        print(f"{distribution}: nstars to make {mstar} = {int(1/frac_highmass)}")
mmax = 120
pl.clf()
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    massrange = np.linspace(8, 100)
    frac_highmass = np.array([distr.integrate(mr, mmax)[0] for mr in massrange])
    pl.loglog(massrange, 1/frac_highmass, label=distribution)
pl.legend(loc='best')
pl.xlabel("$M_{max,cl}$")
pl.ylabel("$N_{*,cl}$")
#[Out]# Text(0, 0.5, '$N_{*,cl}$')
mmax = 120
pl.clf()
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    massrange = np.linspace(8, 100)
    frac_highmass = np.array([distr.integrate(mr, mmax)[0] for mr in massrange])
    
    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    meanmass = mass_integral/n_integral
    
    pl.loglog(massrange, meanmass * 1/frac_highmass, label=distribution)
    print(f"{distribution}: mass(100Msun) = {meanmass / frac_highmass[-1]}, N(100msun) = {int(1/frac_highmass[-1])}")
pl.legend(loc='best')
pl.xlabel("$M_{max,cl}$")
pl.ylabel("$M_{*,cl}$")
#[Out]# Text(0, 0.5, '$M_{*,cl}$')
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    
    n_integral_100 = 1-distr.integrate(100, mmax)[0]
    print(f"{distribution} P(>100) = {n_integral_100}, 1/(1-P(>100)={int(1/(1-n_integral_100))}")


    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    meanmass = mass_integral/n_integral
    
    nstar = np.log(1-0.95) / np.log(n_integral_100)
    nstar50 = np.log(1-0.6321) / np.log(n_integral_100)

    
    minmass_cluster = meanmass*nstar
    
    print(f"{distribution}: Min mass for >1 100 Msun star at 95%: {minmass_cluster:0.2g} nstars={int(nstar)}")
    print(f"{distribution}: Min mass for >1 100 Msun star at 50%: {meanmass*nstar50:0.2g} nstars={int(nstar50)}")
import scipy.integrate
mmax = 120
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=mmin, mmax=mmax)
    def lum(x):
        return x**3 * distr(x)
    lum_int = scipy.integrate.quad(lum, mmin, mmax)[0]
    mass_int = distr.m_integrate(mmin,mmax)[0]
    
    print(f"{distribution}: L/M = {lum_int/mass_int:0.1f}")
mmax = 120
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=mmin, mmax=mmax)
    def lum(x):
        return 2*(x/2)**3 * distr(x)
    lum_int = scipy.integrate.quad(lum, mmin, mmax)[0]
    mass_int = distr.m_integrate(mmin,mmax)[0]
    
    print(f"{distribution}: L/M = {lum_int/mass_int:0.1f}")
mmin = 0.3
mmax = 120
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=0.01, mmax=120)
    def lum(x):
        return 2*(x/2)**3 * distr(x)
    lum_int = scipy.integrate.quad(lum, mmin, mmax)[0]
    mass_int = distr.m_integrate(mmin,mmax)[0]
    
    print(f"{distribution}: L/M = {lum_int/mass_int:0.1f}")
1/6
#[Out]# 0.16666666666666666
1/6 * 5/6  + 1/6*5/6
#[Out]# 0.27777777777777773
(1-(1/6)**2 - (5/6)**2)
#[Out]# 0.2777777777777777
1/6 * (5/6)**2 * 3
#[Out]# 0.34722222222222227
1- ((1/6)**3 + (1/6)**2*(5/6)*3 + (5/6)**3)
#[Out]# 0.3472222222222221
((1/6)**3 + (1/6)**2*(5/6)*3 + (5/6)**3) + (1/6)*(5/6)**2*3
#[Out]# 1.0000000000000002
nrolls = np.arange(1,20)
pl.plot(nrolls, (1/6) * (5/6)**(nrolls-1) * (nrolls-1))
pl.ylabel("P(N(six) = 1)")
pl.xlabel("Number of rolls")
#[Out]# Text(0.5, 0, 'Number of rolls')
########################################################
# Started Logging At: 2022-03-17 11:53:15
########################################################
########################################################
# # Started Logging At: 2022-03-17 11:53:18
########################################################
import imf
imf.salpeter.mmin, imf.salpeter.mmax
#[Out]# (0.3, 120)
imf.kroupa.mmin, imf.kroupa.mmax
#[Out]# (0.03, 120)
imf.chabrier.mmin, imf.chabrier.mmax
#[Out]# (0, inf)
mmin=0.03
mmax=120
get_ipython().run_line_magic('matplotlib', 'inline')
import pylab as pl
pl.rcParams['figure.facecolor'] = 'w'
masses = np.geomspace(0.03, 120, 1000)
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    pl.loglog(masses, distr(masses), label=distribution)
pl.legend(loc='best')
#[Out]# <matplotlib.legend.Legend at 0x12711c580>
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    print(f'{distribution} mean mass: {mass_integral/n_integral:0.2f}')
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    mean_highmass = distr.m_integrate(8, mmax)[0] / distr.integrate(8, mmax)[0]

    print(f'{distribution} Mean M(M>8) = {mean_highmass}')
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    ratio_highmass = distr.integrate(8, mmax)[0]
    ratio_highmasslowmass = distr.integrate(8, mmax)[0] / distr.integrate(mmin, 8)[0]
    print(f'{distribution} N(M>8) / N(tot) = {ratio_highmass:0.4f}, N(M>8) / N(low) = {ratio_highmasslowmass:0.4f}')
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    ratio_highmass = distr.m_integrate(8, mmax)[0] / distr.m_integrate(mmin, mmax)[0]
    ratio_highmasslowmass = distr.m_integrate(8, mmax)[0] / distr.m_integrate(mmin, 8)[0]
    print(f'{distribution} M(M>8) / M(tot) = {ratio_highmass:0.4f}, M(M>8) / M(low) = {ratio_highmasslowmass:0.4f}')
for mmax in (100, 1000):
    print(f'\nM_max = {mmax}')
    for distribution in ('salpeter', 'chabrier', 'kroupa'):
        distr = getattr(imf, distribution)
        mass_integral = distr.m_integrate(mmin, mmax)[0]
        n_integral = distr.integrate(mmin, mmax)[0]
        print(f'{distribution} mean mass: {mass_integral/n_integral:0.2f}')

        ratio_highmass = distr.m_integrate(8, mmax)[0] / distr.m_integrate(mmin, mmax)[0]
        ratio_highmasslowmass = distr.m_integrate(8, mmax)[0] / distr.m_integrate(mmin, 8)[0]
        print(f'{distribution} M(M>8) / M(tot) = {ratio_highmass:0.4f}, M(M>8) / M(low) = {ratio_highmasslowmass:0.4f}')

        ratio_highmass = distr.integrate(8, mmax)[0]
        ratio_highmasslowmass = distr.integrate(8, mmax)[0] / distr.integrate(mmin, 8)[0]
        print(f'{distribution} N(M>8) / N(tot) = {ratio_highmass:0.4f}, N(M>8) / N(low) = {ratio_highmasslowmass:0.4f}')
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    frac_highmass = distr.integrate(8, mmax)[0]

    print(f'{distribution} N(M>8) = {frac_highmass*1000}')
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    frac_highmass = distr.m_integrate(8, mmax)[0] / distr.m_integrate(mmin, mmax)[0]
    mean_highmass = distr.m_integrate(8, mmax)[0] / distr.integrate(8, mmax)[0]

    print(f'{distribution} N(M>8) = {frac_highmass*1000 / mean_highmass}')
mmax = 120
for mstar in (10,100):
    print()
    for distribution in ('salpeter', 'chabrier', 'kroupa'):
        distr = getattr(imf, distribution)
        massrange = np.linspace(8, 100)
        frac_highmass = distr.integrate(mstar, mmax)[0]
        print(f"{distribution}: nstars to make {mstar} = {int(1/frac_highmass)}")
mmax = 120
pl.clf()
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    massrange = np.linspace(8, 100)
    frac_highmass = np.array([distr.integrate(mr, mmax)[0] for mr in massrange])
    pl.loglog(massrange, 1/frac_highmass, label=distribution)
pl.legend(loc='best')
pl.xlabel("$M_{max,cl}$")
pl.ylabel("$N_{*,cl}$")
#[Out]# Text(0, 0.5, '$N_{*,cl}$')
mmax = 120
pl.clf()
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    massrange = np.linspace(8, 100)
    frac_highmass = np.array([distr.integrate(mr, mmax)[0] for mr in massrange])
    
    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    meanmass = mass_integral/n_integral
    
    pl.loglog(massrange, meanmass * 1/frac_highmass, label=distribution)
    print(f"{distribution}: mass(100Msun) = {meanmass / frac_highmass[-1]}, N(100msun) = {int(1/frac_highmass[-1])}")
pl.legend(loc='best')
pl.xlabel("$M_{max,cl}$")
pl.ylabel("$M_{*,cl}$")
#[Out]# Text(0, 0.5, '$M_{*,cl}$')
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    
    n_integral_100 = 1-distr.integrate(100, mmax)[0]
    print(f"{distribution} P(>100) = {n_integral_100}, 1/(1-P(>100)={int(1/(1-n_integral_100))}")


    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    meanmass = mass_integral/n_integral
    
    nstar = np.log(1-0.95) / np.log(n_integral_100)
    nstar50 = np.log(1-0.6321) / np.log(n_integral_100)

    
    minmass_cluster = meanmass*nstar
    
    print(f"{distribution}: Min mass for >1 100 Msun star at 95%: {minmass_cluster:0.2g} nstars={int(nstar)}")
    print(f"{distribution}: Min mass for >1 100 Msun star at 50%: {meanmass*nstar50:0.2g} nstars={int(nstar50)}")
import scipy.integrate
mmax = 120
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=mmin, mmax=mmax)
    def lum(x):
        return x**3 * distr(x)
    lum_int = scipy.integrate.quad(lum, mmin, mmax)[0]
    mass_int = distr.m_integrate(mmin,mmax)[0]
    
    print(f"{distribution}: L/M = {lum_int/mass_int:0.1f}")
mmax = 120
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=mmin, mmax=mmax)
    def lum(x):
        return 2*(x/2)**3 * distr(x)
    lum_int = scipy.integrate.quad(lum, mmin, mmax)[0]
    mass_int = distr.m_integrate(mmin,mmax)[0]
    
    print(f"{distribution}: L/M = {lum_int/mass_int:0.1f}")
mmin = 0.3
mmax = 120
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=0.01, mmax=120)
    def lum(x):
        return 2*(x/2)**3 * distr(x)
    lum_int = scipy.integrate.quad(lum, mmin, mmax)[0]
    mass_int = distr.m_integrate(mmin,mmax)[0]
    
    print(f"{distribution}: L/M = {lum_int/mass_int:0.1f}")
1/6
#[Out]# 0.16666666666666666
1/6 * 5/6  + 1/6*5/6
#[Out]# 0.27777777777777773
(1-(1/6)**2 - (5/6)**2)
#[Out]# 0.2777777777777777
1/6 * (5/6)**2 * 3
#[Out]# 0.34722222222222227
1- ((1/6)**3 + (1/6)**2*(5/6)*3 + (5/6)**3)
#[Out]# 0.3472222222222221
((1/6)**3 + (1/6)**2*(5/6)*3 + (5/6)**3) + (1/6)*(5/6)**2*3
#[Out]# 1.0000000000000002
nrolls = np.arange(1,20)
pl.plot(nrolls, (1/6) * (5/6)**(nrolls-1) * (nrolls-1))
pl.ylabel("P(N(six) = 1)")
pl.xlabel("Number of rolls")
#[Out]# Text(0.5, 0, 'Number of rolls')
########################################################
# Started Logging At: 2022-03-17 11:58:03
########################################################
########################################################
# # Started Logging At: 2022-03-17 11:58:04
########################################################
import imf
imf.salpeter.mmin, imf.salpeter.mmax
#[Out]# (0.3, 120)
imf.kroupa.mmin, imf.kroupa.mmax
#[Out]# (0.03, 120)
imf.chabrier.mmin, imf.chabrier.mmax
#[Out]# (0, inf)
mmin=0.03
mmax=120
get_ipython().run_line_magic('matplotlib', 'inline')
import pylab as pl
pl.rcParams['figure.facecolor'] = 'w'
masses = np.geomspace(0.03, 120, 1000)
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    pl.loglog(masses, distr(masses), label=distribution)
pl.legend(loc='best')
#[Out]# <matplotlib.legend.Legend at 0x122f99190>
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    print(f'{distribution} mean mass: {mass_integral/n_integral:0.2f}')
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    mean_highmass = distr.m_integrate(8, mmax)[0] / distr.integrate(8, mmax)[0]

    print(f'{distribution} Mean M(M>8) = {mean_highmass}')
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    ratio_highmass = distr.integrate(8, mmax)[0]
    ratio_highmasslowmass = distr.integrate(8, mmax)[0] / distr.integrate(mmin, 8)[0]
    print(f'{distribution} N(M>8) / N(tot) = {ratio_highmass:0.4f}, N(M>8) / N(low) = {ratio_highmasslowmass:0.4f}')
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    ratio_highmass = distr.m_integrate(8, mmax)[0] / distr.m_integrate(mmin, mmax)[0]
    ratio_highmasslowmass = distr.m_integrate(8, mmax)[0] / distr.m_integrate(mmin, 8)[0]
    print(f'{distribution} M(M>8) / M(tot) = {ratio_highmass:0.4f}, M(M>8) / M(low) = {ratio_highmasslowmass:0.4f}')
for mmax in (100, 1000):
    print(f'\nM_max = {mmax}')
    for distribution in ('salpeter', 'chabrier', 'kroupa'):
        distr = getattr(imf, distribution)
        mass_integral = distr.m_integrate(mmin, mmax)[0]
        n_integral = distr.integrate(mmin, mmax)[0]
        print(f'{distribution} mean mass: {mass_integral/n_integral:0.2f}')

        ratio_highmass = distr.m_integrate(8, mmax)[0] / distr.m_integrate(mmin, mmax)[0]
        ratio_highmasslowmass = distr.m_integrate(8, mmax)[0] / distr.m_integrate(mmin, 8)[0]
        print(f'{distribution} M(M>8) / M(tot) = {ratio_highmass:0.4f}, M(M>8) / M(low) = {ratio_highmasslowmass:0.4f}')

        ratio_highmass = distr.integrate(8, mmax)[0]
        ratio_highmasslowmass = distr.integrate(8, mmax)[0] / distr.integrate(mmin, 8)[0]
        print(f'{distribution} N(M>8) / N(tot) = {ratio_highmass:0.4f}, N(M>8) / N(low) = {ratio_highmasslowmass:0.4f}')
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    frac_highmass = distr.integrate(8, mmax)[0]

    print(f'{distribution} N(M>8) = {frac_highmass*1000}')
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    frac_highmass = distr.m_integrate(8, mmax)[0] / distr.m_integrate(mmin, mmax)[0]
    mean_highmass = distr.m_integrate(8, mmax)[0] / distr.integrate(8, mmax)[0]

    print(f'{distribution} N(M>8) = {frac_highmass*1000 / mean_highmass}')
mmax = 120
for mstar in (10,100):
    print()
    for distribution in ('salpeter', 'chabrier', 'kroupa'):
        distr = getattr(imf, distribution)
        massrange = np.linspace(8, 100)
        frac_highmass = distr.integrate(mstar, mmax)[0]
        print(f"{distribution}: nstars to make {mstar} = {int(1/frac_highmass)}")
mmax = 120
pl.clf()
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    massrange = np.linspace(8, 100)
    frac_highmass = np.array([distr.integrate(mr, mmax)[0] for mr in massrange])
    pl.loglog(massrange, 1/frac_highmass, label=distribution)
pl.legend(loc='best')
pl.xlabel("$M_{max,cl}$")
pl.ylabel("$N_{*,cl}$")
#[Out]# Text(0, 0.5, '$N_{*,cl}$')
mmax = 120
pl.clf()
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    massrange = np.linspace(8, 100)
    frac_highmass = np.array([distr.integrate(mr, mmax)[0] for mr in massrange])
    
    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    meanmass = mass_integral/n_integral
    
    pl.loglog(massrange, meanmass * 1/frac_highmass, label=distribution)
    print(f"{distribution}: mass(100Msun) = {meanmass / frac_highmass[-1]}, N(100msun) = {int(1/frac_highmass[-1])}")
pl.legend(loc='best')
pl.xlabel("$M_{max,cl}$")
pl.ylabel("$M_{*,cl}$")
#[Out]# Text(0, 0.5, '$M_{*,cl}$')
mmax = 120
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    
    n_integral_100 = 1-distr.integrate(100, mmax)[0]
    print(f"{distribution} P(>100) = {n_integral_100}, 1/(1-P(>100)={int(1/(1-n_integral_100))}")


    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    meanmass = mass_integral/n_integral
    
    nstar = np.log(1-0.95) / np.log(n_integral_100)
    nstar50 = np.log(1-0.6321) / np.log(n_integral_100)

    
    minmass_cluster = meanmass*nstar
    
    print(f"{distribution}: Min mass for >1 100 Msun star at 95%: {minmass_cluster:0.2g} nstars={int(nstar)}")
    print(f"{distribution}: Min mass for >1 100 Msun star at 50%: {meanmass*nstar50:0.2g} nstars={int(nstar50)}")
import scipy.integrate
mmax = 120
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=mmin, mmax=mmax)
    def lum(x):
        return x**3 * distr(x)
    lum_int = scipy.integrate.quad(lum, mmin, mmax)[0]
    mass_int = distr.m_integrate(mmin,mmax)[0]
    
    print(f"{distribution}: L/M = {lum_int/mass_int:0.1f}")
mmax = 120
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=mmin, mmax=mmax)
    def lum(x):
        return 2*(x/2)**3 * distr(x)
    lum_int = scipy.integrate.quad(lum, mmin, mmax)[0]
    mass_int = distr.m_integrate(mmin,mmax)[0]
    
    print(f"{distribution}: L/M = {lum_int/mass_int:0.1f}")
mmin = 0.3
mmax = 120
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=0.01, mmax=120)
    def lum(x):
        return 2*(x/2)**3 * distr(x)
    lum_int = scipy.integrate.quad(lum, mmin, mmax)[0]
    mass_int = distr.m_integrate(mmin,mmax)[0]
    
    print(f"{distribution}: L/M = {lum_int/mass_int:0.1f}")
1/6
#[Out]# 0.16666666666666666
1/6 * 5/6  + 1/6*5/6
#[Out]# 0.27777777777777773
(1-(1/6)**2 - (5/6)**2)
#[Out]# 0.2777777777777777
1/6 * (5/6)**2 * 3
#[Out]# 0.34722222222222227
1- ((1/6)**3 + (1/6)**2*(5/6)*3 + (5/6)**3)
#[Out]# 0.3472222222222221
((1/6)**3 + (1/6)**2*(5/6)*3 + (5/6)**3) + (1/6)*(5/6)**2*3
#[Out]# 1.0000000000000002
nrolls = np.arange(1,20)
pl.plot(nrolls, (1/6) * (5/6)**(nrolls-1) * (nrolls-1))
pl.ylabel("P(N(six) = 1)")
pl.xlabel("Number of rolls")
#[Out]# Text(0.5, 0, 'Number of rolls')
mmin = 0.3
mmax = 120
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=0.01, mmax=120)
    def lum(x):
        return 2*(x/2)**3 * distr(x)
    lum_int = scipy.integrate.quad(lum, mmin, mmax)[0]
    mass_int = distr.m_integrate(mmin,mmax)[0]
    
    print(f"{distribution}: L/M = {lum_int/mass_int:0.1f}")
mmin = 0.3
mmax = 120
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=0.01, mmax=120)
    def lum(x):
        return 2*(x/2)**3 * distr(x)
    lum_int = scipy.integrate.quad(lum, mmin, mmax)[0]
    mass_int = distr.m_integrate(mmin,mmax)[0]
    
    print(f"{distribution}: L/M = {lum_int/mass_int:0.1f}")
mmin = 0.3
mmax = 120
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=0.01, mmax=120)
    def lum(x):
        return x**3 * distr(x)
    lum_int = scipy.integrate.quad(lum, mmin, mmax)[0]
    mass_int = distr.m_integrate(mmin,mmax)[0]
    
    print(f"{distribution}: L/M = {lum_int/mass_int:0.1f}")
get_ipython().run_line_magic('pinfo', 'np.interpolate')
get_ipython().run_line_magic('pinfo', 'np.interp')
mmax = 120
mtaurus = 100
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    
    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    meanmass = mass_integral/n_integral
    
    massrange = np.linspace(1,mtaurus)
    frac_highmass = np.array([distr.integrate(mr, mmax)[0] for mr in massrange])
    mcluster = meanmass * (1/frac_highmass)
    maxmass = np.interpolate(mtaurus, mcluster, massrange)
    
    def lum(x):
        return x**3 * distr(x)
    lum_int = scipy.integrate.quad(lum, mmin, maxmass)[0]
    mass_int = distr.m_integrate(mmin, maxmass)[0]
    
    print(f"{distribution}: Mmax = {maxmass} L/M = {lum_int/mass_int:0.1f}")
mmax = 120
mtaurus = 100
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    
    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    meanmass = mass_integral/n_integral
    
    massrange = np.linspace(1,mtaurus)
    frac_highmass = np.array([distr.integrate(mr, mmax)[0] for mr in massrange])
    mcluster = meanmass * (1/frac_highmass)
    maxmass = np.interp(mtaurus, mcluster, massrange)
    
    def lum(x):
        return x**3 * distr(x)
    lum_int = scipy.integrate.quad(lum, mmin, maxmass)[0]
    mass_int = distr.m_integrate(mmin, maxmass)[0]
    
    print(f"{distribution}: Mmax = {maxmass} L/M = {lum_int/mass_int:0.1f}")
mmax = 120
mtaurus = 100
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    
    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    meanmass = mass_integral/n_integral
    
    massrange = np.linspace(1,mtaurus)
    frac_highmass = np.array([distr.integrate(mr, mmax)[0] for mr in massrange])
    mcluster = meanmass * (1/frac_highmass)
    maxmass = np.interp(mtaurus, mcluster, massrange)
    
    def lum(x):
        return x**3 * distr(x)
    lum_int = scipy.integrate.quad(lum, mmin, maxmass)[0]
    mass_int = distr.m_integrate(mmin, maxmass)[0]
    
    print(f"{distribution}: Mmax = {maxmass:0.1f} L/M = {lum_int/mass_int:0.1f}")
mmax = 120
mmin = 0.03
mtaurus = 100
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=0.01, mmax=120)
    
    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    meanmass = mass_integral/n_integral
    
    massrange = np.linspace(1,mtaurus)
    frac_highmass = np.array([distr.integrate(mr, mmax)[0] for mr in massrange])
    mcluster = meanmass * (1/frac_highmass)
    maxmass = np.interp(mtaurus, mcluster, massrange)
    
    def lum(x):
        return x**3 * distr(x)
    lum_int = scipy.integrate.quad(lum, mmin, maxmass)[0]
    mass_int = distr.m_integrate(mmin, maxmass)[0]
    
    print(f"{distribution}: Mmax = {maxmass:0.1f} L/M = {lum_int/mass_int:0.1f}")
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=0.01, mmax=120)
    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    print(f'{distribution} mean mass: {mass_integral/n_integral:0.2f}')
########################################################
# Started Logging At: 2022-03-17 12:12:49
########################################################
########################################################
# # Started Logging At: 2022-03-17 12:12:51
########################################################
import imf
imf.salpeter.mmin, imf.salpeter.mmax
#[Out]# (0.3, 120)
imf.kroupa.mmin, imf.kroupa.mmax
#[Out]# (0.03, 120)
imf.chabrier.mmin, imf.chabrier.mmax
#[Out]# (0, inf)
mmin=0.03
mmax=120
get_ipython().run_line_magic('matplotlib', 'inline')
import pylab as pl
pl.rcParams['figure.facecolor'] = 'w'
masses = np.geomspace(0.03, 120, 1000)
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    pl.loglog(masses, distr(masses), label=distribution)
pl.legend(loc='best')
#[Out]# <matplotlib.legend.Legend at 0x1291967f0>
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=0.01, mmax=120)
    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    print(f'{distribution} mean mass: {mass_integral/n_integral:0.2f}')
mmax = 120
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=0.01, mmax=120)
    mean_highmass = distr.m_integrate(8, mmax)[0] / distr.integrate(8, mmax)[0]

    print(f'{distribution} Mean M(M>8) = {mean_highmass}')
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=0.01, mmax=120)
    ratio_highmass = distr.integrate(8, mmax)[0]
    ratio_highmasslowmass = distr.integrate(8, mmax)[0] / distr.integrate(mmin, 8)[0]
    print(f'{distribution} N(M>8) / N(tot) = {ratio_highmass:0.4f}, N(M>8) / N(low) = {ratio_highmasslowmass:0.4f}')
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=0.01, mmax=120)
    ratio_highmass = distr.m_integrate(8, mmax)[0] / distr.m_integrate(mmin, mmax)[0]
    ratio_highmasslowmass = distr.m_integrate(8, mmax)[0] / distr.m_integrate(mmin, 8)[0]
    print(f'{distribution} M(M>8) / M(tot) = {ratio_highmass:0.4f}, M(M>8) / M(low) = {ratio_highmasslowmass:0.4f}')
for mmax in (100, 1000):
    print(f'\nM_max = {mmax}')
    for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
        distr = getattr(imf, distribution)(mmin=0.01, mmax=mmax)
        mass_integral = distr.m_integrate(mmin, mmax)[0]
        n_integral = distr.integrate(mmin, mmax)[0]
        print(f'{distribution} mean mass: {mass_integral/n_integral:0.2f}')

        ratio_highmass = distr.m_integrate(8, mmax)[0] / distr.m_integrate(mmin, mmax)[0]
        ratio_highmasslowmass = distr.m_integrate(8, mmax)[0] / distr.m_integrate(mmin, 8)[0]
        print(f'{distribution} M(M>8) / M(tot) = {ratio_highmass:0.4f}, M(M>8) / M(low) = {ratio_highmasslowmass:0.4f}')

        ratio_highmass = distr.integrate(8, mmax)[0]
        ratio_highmasslowmass = distr.integrate(8, mmax)[0] / distr.integrate(mmin, 8)[0]
        print(f'{distribution} N(M>8) / N(tot) = {ratio_highmass:0.4f}, N(M>8) / N(low) = {ratio_highmasslowmass:0.4f}')
mmax = 120
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=0.01, mmax=120)
    frac_highmass = distr.integrate(8, mmax)[0]

    print(f'{distribution} N(M>8) = {frac_highmass*1000}')
mmax = 120
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=0.01, mmax=120)
    frac_highmass = distr.m_integrate(8, mmax)[0] / distr.m_integrate(mmin, mmax)[0]
    mean_highmass = distr.m_integrate(8, mmax)[0] / distr.integrate(8, mmax)[0]

    print(f'{distribution} N(M>8) = {frac_highmass*1000 / mean_highmass}')
mmax = 120
for mstar in (10,100):
    print()
    for distribution in ('salpeter', 'chabrier', 'kroupa'):
        distr = getattr(imf, distribution)
        massrange = np.linspace(8, 100)
        frac_highmass = distr.integrate(mstar, mmax)[0]
        print(f"{distribution}: nstars to make {mstar} = {int(1/frac_highmass)}")
mmax = 120
pl.clf()
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=0.01, mmax=120)
    massrange = np.linspace(8, 100)
    frac_highmass = np.array([distr.integrate(mr, mmax)[0] for mr in massrange])
    pl.loglog(massrange, 1/frac_highmass, label=distribution)
pl.legend(loc='best')
pl.xlabel("$M_{max,cl}$")
pl.ylabel("$N_{*,cl}$")
#[Out]# Text(0, 0.5, '$N_{*,cl}$')
mmax = 120
pl.clf()
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=0.01, mmax=120)
    massrange = np.linspace(8, 100)
    frac_highmass = np.array([distr.integrate(mr, mmax)[0] for mr in massrange])
    
    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    meanmass = mass_integral/n_integral
    
    pl.loglog(massrange, meanmass * 1/frac_highmass, label=distribution)
    print(f"{distribution}: mass(100Msun) = {meanmass / frac_highmass[-1]}, N(100msun) = {int(1/frac_highmass[-1])}")
pl.legend(loc='best')
pl.xlabel("$M_{max,cl}$")
pl.ylabel("$M_{*,cl}$")
#[Out]# Text(0, 0.5, '$M_{*,cl}$')
mmax = 120
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=0.01, mmax=120)
    
    n_integral_100 = 1-distr.integrate(100, mmax)[0]
    print(f"{distribution} P(>100) = {n_integral_100}, 1/(1-P(>100)={int(1/(1-n_integral_100))}")


    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    meanmass = mass_integral/n_integral
    
    nstar = np.log(1-0.95) / np.log(n_integral_100)
    nstar50 = np.log(1-0.6321) / np.log(n_integral_100)

    
    minmass_cluster = meanmass*nstar
    
    print(f"{distribution}: Min mass for >1 100 Msun star at 95%: {minmass_cluster:0.2g} nstars={int(nstar)}")
    print(f"{distribution}: Min mass for >1 100 Msun star at 50%: {meanmass*nstar50:0.2g} nstars={int(nstar50)}")
import scipy.integrate
mmin = 0.3
mmax = 120
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=0.01, mmax=120)
    def lum(x):
        return x**3 * distr(x)
    lum_int = scipy.integrate.quad(lum, mmin, mmax)[0]
    mass_int = distr.m_integrate(mmin,mmax)[0]
    
    print(f"{distribution}: L/M = {lum_int/mass_int:0.1f}")
mmin = 0.3
mmax = 120
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=0.01, mmax=120)
    def lum(x):
        return 2*(x/2)**3 * distr(x)
    lum_int = scipy.integrate.quad(lum, mmin, mmax)[0]
    mass_int = distr.m_integrate(mmin,mmax)[0]
    
    print(f"{distribution}: L/M = {lum_int/mass_int:0.1f}")
mmax = 120
mtaurus = 100
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=0.01, mmax=120)
    
    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    meanmass = mass_integral/n_integral
    
    massrange = np.linspace(1,mtaurus)
    frac_highmass = np.array([distr.integrate(mr, mmax)[0] for mr in massrange])
    mcluster = meanmass * (1/frac_highmass)
    maxmass = np.interp(mtaurus, mcluster, massrange)
    
    def lum(x):
        return x**3 * distr(x)
    lum_int = scipy.integrate.quad(lum, mmin, maxmass)[0]
    mass_int = distr.m_integrate(mmin, maxmass)[0]
    
    print(f"{distribution}: Mmax = {maxmass:0.1f} L/M = {lum_int/mass_int:0.1f}")
1/6
#[Out]# 0.16666666666666666
1/6 * 5/6  + 1/6*5/6
#[Out]# 0.27777777777777773
(1-(1/6)**2 - (5/6)**2)
#[Out]# 0.2777777777777777
1/6 * (5/6)**2 * 3
#[Out]# 0.34722222222222227
1- ((1/6)**3 + (1/6)**2*(5/6)*3 + (5/6)**3)
#[Out]# 0.3472222222222221
((1/6)**3 + (1/6)**2*(5/6)*3 + (5/6)**3) + (1/6)*(5/6)**2*3
#[Out]# 1.0000000000000002
nrolls = np.arange(1,20)
pl.plot(nrolls, (1/6) * (5/6)**(nrolls-1) * (nrolls-1))
pl.ylabel("P(N(six) = 1)")
pl.xlabel("Number of rolls")
#[Out]# Text(0.5, 0, 'Number of rolls')
96/8
#[Out]# 12.0
8/96
#[Out]# 0.08333333333333333
imf.Kroupa.m_integrate(8,120) / imf.Kroupa.m_integrate(0.01,120)
imf.kroupa.m_integrate(8,120) / imf.kroupa.m_integrate(0.01,120)
imf.kroupa.m_integrate(8,120)[0] / imf.kroupa.m_integrate(0.01,120)[0]
#[Out]# 0.20938564866220746
imf.kroupa.m_integrate(20,120)[0] / imf.kroupa.m_integrate(0.01,120)[0]
#[Out]# 0.11890946726068764
imf.kroupa.m_integrate(20,120)[0] / imf.kroupa.m_integrate(0.03,120)[0]
#[Out]# 0.11890946726068764
########################################################
# Started Logging At: 2022-03-17 12:59:11
########################################################
########################################################
# # Started Logging At: 2022-03-17 12:59:12
########################################################
import imf
imf.salpeter.mmin, imf.salpeter.mmax
#[Out]# (0.3, 120)
imf.kroupa.mmin, imf.kroupa.mmax
#[Out]# (0.03, 120)
imf.chabrier.mmin, imf.chabrier.mmax
#[Out]# (0, inf)
mmin=0.03
mmax=120
get_ipython().run_line_magic('matplotlib', 'inline')
import pylab as pl
pl.rcParams['figure.facecolor'] = 'w'
masses = np.geomspace(0.03, 120, 1000)
for distribution in ('salpeter', 'chabrier', 'kroupa'):
    distr = getattr(imf, distribution)
    pl.loglog(masses, distr(masses), label=distribution)
pl.legend(loc='best')
#[Out]# <matplotlib.legend.Legend at 0x12bd966d0>
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=0.01, mmax=120)
    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    print(f'{distribution} mean mass: {mass_integral/n_integral:0.2f}')
mmax = 120
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=0.01, mmax=120)
    mean_highmass = distr.m_integrate(8, mmax)[0] / distr.integrate(8, mmax)[0]

    print(f'{distribution} Mean M(M>8) = {mean_highmass}')
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=0.01, mmax=120)
    ratio_highmass = distr.integrate(8, mmax)[0]
    ratio_highmasslowmass = distr.integrate(8, mmax)[0] / distr.integrate(mmin, 8)[0]
    print(f'{distribution} N(M>8) / N(tot) = {ratio_highmass:0.4f}, N(M>8) / N(low) = {ratio_highmasslowmass:0.4f}')
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=0.01, mmax=120)
    ratio_highmass = distr.m_integrate(8, mmax)[0] / distr.m_integrate(mmin, mmax)[0]
    ratio_highmasslowmass = distr.m_integrate(8, mmax)[0] / distr.m_integrate(mmin, 8)[0]
    print(f'{distribution} M(M>8) / M(tot) = {ratio_highmass:0.4f}, M(M>8) / M(low) = {ratio_highmasslowmass:0.4f}')
for mmax in (100, 1000):
    print(f'\nM_max = {mmax}')
    for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
        distr = getattr(imf, distribution)(mmin=0.01, mmax=mmax)
        mass_integral = distr.m_integrate(mmin, mmax)[0]
        n_integral = distr.integrate(mmin, mmax)[0]
        print(f'{distribution} mean mass: {mass_integral/n_integral:0.2f}')

        ratio_highmass = distr.m_integrate(8, mmax)[0] / distr.m_integrate(mmin, mmax)[0]
        ratio_highmasslowmass = distr.m_integrate(8, mmax)[0] / distr.m_integrate(mmin, 8)[0]
        print(f'{distribution} M(M>8) / M(tot) = {ratio_highmass:0.4f}, M(M>8) / M(low) = {ratio_highmasslowmass:0.4f}')

        ratio_highmass = distr.integrate(8, mmax)[0]
        ratio_highmasslowmass = distr.integrate(8, mmax)[0] / distr.integrate(mmin, 8)[0]
        print(f'{distribution} N(M>8) / N(tot) = {ratio_highmass:0.4f}, N(M>8) / N(low) = {ratio_highmasslowmass:0.4f}')
mmax = 120
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=0.01, mmax=120)
    frac_highmass = distr.integrate(8, mmax)[0]

    print(f'{distribution} N(M>8) = {frac_highmass*1000}')
mmax = 120
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=0.01, mmax=120)
    frac_highmass = distr.m_integrate(8, mmax)[0] / distr.m_integrate(mmin, mmax)[0]
    mean_highmass = distr.m_integrate(8, mmax)[0] / distr.integrate(8, mmax)[0]

    print(f'{distribution} N(M>8) = {frac_highmass*1000 / mean_highmass}')
mmax = 120
for mstar in (10,100):
    print()
    for distribution in ('salpeter', 'chabrier', 'kroupa'):
        distr = getattr(imf, distribution)
        massrange = np.linspace(8, 100)
        frac_highmass = distr.integrate(mstar, mmax)[0]
        print(f"{distribution}: nstars to make {mstar} = {int(1/frac_highmass)}")
mmax = 120
pl.clf()
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=0.01, mmax=120)
    massrange = np.linspace(8, 100)
    frac_highmass = np.array([distr.integrate(mr, mmax)[0] for mr in massrange])
    pl.loglog(massrange, 1/frac_highmass, label=distribution)
pl.legend(loc='best')
pl.xlabel("$M_{max,cl}$")
pl.ylabel("$N_{*,cl}$")
#[Out]# Text(0, 0.5, '$N_{*,cl}$')
mmax = 120
pl.clf()
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=0.01, mmax=120)
    massrange = np.linspace(8, 100)
    frac_highmass = np.array([distr.integrate(mr, mmax)[0] for mr in massrange])
    
    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    meanmass = mass_integral/n_integral
    
    pl.loglog(massrange, meanmass * 1/frac_highmass, label=distribution)
    print(f"{distribution}: mass(100Msun) = {meanmass / frac_highmass[-1]}, N(100msun) = {int(1/frac_highmass[-1])}")
pl.legend(loc='best')
pl.xlabel("$M_{max,cl}$")
pl.ylabel("$M_{*,cl}$")
#[Out]# Text(0, 0.5, '$M_{*,cl}$')
mmax = 120
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=0.01, mmax=120)
    
    n_integral_100 = 1-distr.integrate(100, mmax)[0]
    print(f"{distribution} P(>100) = {n_integral_100}, 1/(1-P(>100)={int(1/(1-n_integral_100))}")


    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    meanmass = mass_integral/n_integral
    
    nstar = np.log(1-0.95) / np.log(n_integral_100)
    nstar50 = np.log(1-0.6321) / np.log(n_integral_100)

    
    minmass_cluster = meanmass*nstar
    
    print(f"{distribution}: Min mass for >1 100 Msun star at 95%: {minmass_cluster:0.2g} nstars={int(nstar)}")
    print(f"{distribution}: Min mass for >1 100 Msun star at 50%: {meanmass*nstar50:0.2g} nstars={int(nstar50)}")
import scipy.integrate
mmin = 0.3
mmax = 120
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=0.01, mmax=120)
    def lum(x):
        return x**3 * distr(x)
    lum_int = scipy.integrate.quad(lum, mmin, mmax)[0]
    mass_int = distr.m_integrate(mmin,mmax)[0]
    
    print(f"{distribution}: L/M = {lum_int/mass_int:0.1f}")
mmin = 0.3
mmax = 120
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=0.01, mmax=120)
    def lum(x):
        return 2*(x/2)**3 * distr(x)
    lum_int = scipy.integrate.quad(lum, mmin, mmax)[0]
    mass_int = distr.m_integrate(mmin,mmax)[0]
    
    print(f"{distribution}: L/M = {lum_int/mass_int:0.1f}")
mmax = 120
mtaurus = 100
for distribution in ('Salpeter', 'ChabrierPowerLaw', 'Kroupa'):
    distr = getattr(imf, distribution)(mmin=0.01, mmax=120)
    
    mass_integral = distr.m_integrate(mmin, mmax)[0]
    n_integral = distr.integrate(mmin, mmax)[0]
    meanmass = mass_integral/n_integral
    
    massrange = np.linspace(1,mtaurus)
    frac_highmass = np.array([distr.integrate(mr, mmax)[0] for mr in massrange])
    mcluster = meanmass * (1/frac_highmass)
    maxmass = np.interp(mtaurus, mcluster, massrange)
    
    def lum(x):
        return x**3 * distr(x)
    lum_int = scipy.integrate.quad(lum, mmin, maxmass)[0]
    mass_int = distr.m_integrate(mmin, maxmass)[0]
    
    print(f"{distribution}: Mmax = {maxmass:0.1f} L/M = {lum_int/mass_int:0.1f}")
1/6
#[Out]# 0.16666666666666666
1/6 * 5/6  + 1/6*5/6
#[Out]# 0.27777777777777773
(1-(1/6)**2 - (5/6)**2)
#[Out]# 0.2777777777777777
1/6 * (5/6)**2 * 3
#[Out]# 0.34722222222222227
1- ((1/6)**3 + (1/6)**2*(5/6)*3 + (5/6)**3)
#[Out]# 0.3472222222222221
((1/6)**3 + (1/6)**2*(5/6)*3 + (5/6)**3) + (1/6)*(5/6)**2*3
#[Out]# 1.0000000000000002
nrolls = np.arange(1,20)
pl.plot(nrolls, (1/6) * (5/6)**(nrolls-1) * (nrolls-1))
pl.ylabel("P(N(six) = 1)")
pl.xlabel("Number of rolls")
#[Out]# Text(0.5, 0, 'Number of rolls')
########################################################
# Started Logging At: 2022-03-17 14:55:35
########################################################

########################################################
# # Started Logging At: 2022-03-17 14:55:36
########################################################
########################################################
# Started Logging At: 2022-03-17 14:56:21
########################################################

########################################################
# # Started Logging At: 2022-03-17 14:56:21
########################################################
get_ipython().run_line_magic('run', 'chabrier_comparisons.py')
get_ipython().run_line_magic('run', 'chabrier_comparisons.py')
pl.ion(); pl.draw(); pl.show()
get_ipython().run_line_magic('run', 'chabrier_comparisons.py')
get_ipython().run_line_magic('run', 'chabrier_comparisons.py')
get_ipython().run_line_magic('run', 'chabrier_comparisons.py')
########################################################
# Started Logging At: 2022-03-17 15:03:31
########################################################

########################################################
# # Started Logging At: 2022-03-17 15:03:32
########################################################
########################################################
# Started Logging At: 2022-03-17 15:03:35
########################################################

########################################################
# # Started Logging At: 2022-03-17 15:03:36
########################################################
########################################################
# Started Logging At: 2022-03-17 16:13:57
########################################################

########################################################
# # Started Logging At: 2022-03-17 16:13:59
########################################################
np.log10(0.055)
10**0.22
np.exp(0.22)
0.055*np.log(10)
0.076*np.log(10)
0.079*np.log(10)
get_ipython().run_line_magic('run', 'chabrier_comparisons.py')
########################################################
# Started Logging At: 2022-03-17 16:36:14
########################################################

########################################################
# # Started Logging At: 2022-03-17 16:36:17
########################################################
########################################################
# Started Logging At: 2022-03-17 16:36:33
########################################################

########################################################
# # Started Logging At: 2022-03-17 16:36:36
########################################################
import pylab as pl
########################################################
# Started Logging At: 2022-03-17 16:36:41
########################################################

########################################################
# # Started Logging At: 2022-03-17 16:36:44
########################################################
imf.distributions.TruncatedOneOverXLogNormal(mu=0.22, sig=0.57*np.log(10), m1=0, m2=1)
########################################################
# Started Logging At: 2022-03-17 16:40:18
########################################################

########################################################
# Started Logging At: 2022-03-17 16:40:22
########################################################

########################################################
# # Started Logging At: 2022-03-17 16:40:22
########################################################
import imf
imf.distributions.TruncatedOneOverXLogNormal(mu=0.22, sig=0.57*np.log(10), m1=0, m2=1)
xx = imf.distributions.TruncatedOneOverXLogNormal(mu=0.22, sig=0.57*np.log(10), m1=0, m2=1)
get_ipython().run_line_magic('run', 'chabrier_comparisons.py')
pl.figure(1)
pl.plot(masses, xx(masses)
)
pl.plot(masses, xx.cdf(masses))
pl.ion()
pl.draw()
xx.cdf(masses))
xx.cdf(masses)
xx = imf.distributions.TruncatedOneOverXLogNormal(mu=0.22, sig=0.57*np.log(10), m1=0.01, m2=1)
xx.cdf(masses)
get_ipython().run_line_magic('run', 'chabrier_comparisons.py')
########################################################
# Started Logging At: 2022-03-17 17:40:44
########################################################

########################################################
# # Started Logging At: 2022-03-17 17:40:44
########################################################
xx = imf.distributions.TruncatedOneOverXLogNormal(mu=0.22, sig=0.57*np.log(10), m1=0.01, m2=1)
import imf
xx = imf.distributions.TruncatedOneOverXLogNormal(mu=0.22, sig=0.57*np.log(10), m1=0.01, m2=1)
xx = imf.distributions.TruncatedOneOverXLogNormal(mu=0.22, sig=0.57*np.log(10), m1=0.01, m2=1)
########################################################
# Started Logging At: 2022-03-17 17:42:01
########################################################

########################################################
# # Started Logging At: 2022-03-17 17:42:02
########################################################
import imf
imf.distributions.TruncatedOneOverXLogNormal(mu=0.22, sig=0.57*np.log(10), m1=0, m2=1)
imf.distributions.OneOverXLogNormal_gen
imf.distributions.OneOverXLogNormal_gen(a=1)
imf.distributions.OneOverXLogNormal_gen(a=0)
imf.distributions.OneOverXLogNormal_gen(a=0)._pdf(np.linspace(0,1), 0.5)
imf.distributions.OneOverXLogNormal_gen(a=0)._ppf(np.linspace(0,1), 0.5)
########################################################
# Started Logging At: 2022-03-17 17:46:01
########################################################

########################################################
# # Started Logging At: 2022-03-17 17:46:01
########################################################
import imf
xx = imf.distributions.TruncatedOneOverXLogNormal(mu=0.22, sig=0.57*np.log(10), m1=0.01, m2=1)
pl.plot(masses, xx.cdf(masses))
import pylab as pl
pl.plot(masses, xx.cdf(masses))
masses = np.geomspace(0.03, 120, 1000)
pl.plot(masses, xx.cdf(masses))
pl.loglog()
masses = np.geomspace(0.03, 1, 1000)
pl.clf()
pl.loglog(masses, xx.cdf(masses))
xx = imf.distributions.TruncatedOneOverXLogNormal(mu=np.log(0.22), sig=0.57*np.log(10), m1=0.01, m2=1)
pl.loglog(masses, xx.cdf(masses))
xx.d
xx.d.sacle
xx.d.scale
xx.d.a
########################################################
# Started Logging At: 2022-03-17 17:49:06
########################################################

########################################################
# # Started Logging At: 2022-03-17 17:49:07
########################################################
import imf
get_ipython().run_line_magic('ls', '-lhrt *py')
get_ipython().run_line_magic('cat', 'ipython_log_2022-03-17.py')
get_ipython().run_line_magic('run', 'chabrier_comparisons.py')
np.exp(0.55)
0.55*np.log(10)
get_ipython().run_line_magic('run', 'chabrier_comparisons.py')
get_ipython().run_line_magic('run', 'chabrier_comparisons.py')
np.exp(0.2)
np.exp(0.2)
get_ipython().run_line_magic('run', 'chabrier_comparisons.py')
get_ipython().run_line_magic('run', 'chabrier_comparisons.py')
get_ipython().run_line_magic('run', 'chabrier_comparisons.py')
get_ipython().run_line_magic('run', 'chabrier_comparisons.py')
get_ipython().run_line_magic('run', 'chabrier_comparisons.py')
get_ipython().run_line_magic('run', 'chabrier_comparisons.py')
