########################################################
# Started Logging At: 2019-11-14 11:41:43
########################################################
########################################################
# # Started Logging At: 2019-11-14 11:41:45
########################################################
$$\alpha = 2.35$$
120**-1.35
#[Out]# 0.0015599307452825832
120**1.35
#[Out]# 641.0541000131701
120**-1.35
#[Out]# 0.0015599307452825832
120**1.35 *2.35
#[Out]# 1506.4771350309497
########################################################
# Started Logging At: 2019-11-14 15:50:15
########################################################

########################################################
# # Started Logging At: 2019-11-14 15:50:16
########################################################
get_ipython().run_line_magic('run', 'imf_figure.py')
get_ipython().run_line_magic('pinfo', 'imf.salpeter')
get_ipython().run_line_magic('pinfo2', 'imf.salpeter')
get_ipython().run_line_magic('run', 'imf_figure.py')
get_ipython().run_line_magic('run', 'imf_figure.py')
########################################################
# Started Logging At: 2019-11-14 15:56:10
########################################################

########################################################
# # Started Logging At: 2019-11-14 15:56:10
########################################################
get_ipython().run_line_magic('run', 'imf_figure.py')
get_ipython().run_line_magic('debug', '')
########################################################
# Started Logging At: 2019-11-14 16:03:46
########################################################

########################################################
# # Started Logging At: 2019-11-14 16:03:47
########################################################
get_ipython().run_line_magic('R', '')
get_ipython().run_line_magic('run', 'imf_figure.py')
get_ipython().run_line_magic('debug', '')
########################################################
# Started Logging At: 2019-11-14 16:10:25
########################################################

########################################################
# # Started Logging At: 2019-11-14 16:10:26
########################################################
get_ipython().run_line_magic('run', 'imf_figure.py')
########################################################
# Started Logging At: 2019-11-14 16:11:22
########################################################

########################################################
# # Started Logging At: 2019-11-14 16:11:23
########################################################
get_ipython().run_line_magic('run', 'imf_figure.py')
########################################################
# Started Logging At: 2019-11-14 16:12:24
########################################################

########################################################
# # Started Logging At: 2019-11-14 16:12:25
########################################################
get_ipython().run_line_magic('run', 'imf_figure.py')
get_ipython().run_line_magic('debug', '')
########################################################
# Started Logging At: 2019-11-14 16:17:12
########################################################

########################################################
# # Started Logging At: 2019-11-14 16:17:13
########################################################
get_ipython().run_line_magic('debug', '')
get_ipython().run_line_magic('run', 'imf_figure.py')
get_ipython().run_line_magic('debug', '')
########################################################
# Started Logging At: 2019-11-14 16:20:22
########################################################

########################################################
# # Started Logging At: 2019-11-14 16:20:23
########################################################
get_ipython().run_line_magic('debug', '')
get_ipython().run_line_magic('run', 'imf_figure.py')
########################################################
# Started Logging At: 2019-11-14 16:20:52
########################################################

########################################################
# # Started Logging At: 2019-11-14 16:20:52
########################################################
get_ipython().run_line_magic('run', 'imf_figure.py')
get_ipython().run_line_magic('debug', '')
########################################################
# Started Logging At: 2019-11-14 16:22:04
########################################################

########################################################
# # Started Logging At: 2019-11-14 16:22:05
########################################################
get_ipython().run_line_magic('run', 'imf_figure.py')
get_ipython().system('open *Alpha*png')
open *Salp*png
get_ipython().run_line_magic('ls', '-rt')
open(Salpeter_imf_figure_l*png)
get_ipython().system('open Salpeter_imf_figure_l*png')
get_ipython().system('open Salpeter_imf_figure_log.png Alpha*log.png')
get_ipython().system('open Salpeter_imf_figure_log.png Alpha*log.png')
get_ipython().system('open Salpeter_imf_figure_log.png Alpha*log.png')
get_ipython().system('open Salpeter_imf_figure_log.png Alpha*log.png')
$$ \frac{dN}{dm} = N_0 m^{-\alpha}$$
########################################################
# Started Logging At: 2019-11-14 17:31:20
########################################################

########################################################
# # Started Logging At: 2019-11-14 17:31:21
########################################################
get_ipython().run_line_magic('run', 'hr_diagram.py')
get_ipython().run_line_magic('run', 'mass_to_light.py')
########################################################
# Started Logging At: 2019-11-14 17:49:40
########################################################

########################################################
# # Started Logging At: 2019-11-14 17:49:41
########################################################
get_ipython().run_line_magic('ls', '*alpha*png')
get_ipython().run_line_magic('ls', '*alpha*pdf')
get_ipython().run_line_magic('ls', '')
get_ipython().system('ag masstolight')
pl.savefig("masstolight_vs_slope.pdf")
lum
get_ipython().run_line_magic('run', 'mass_to_light.py')
get_ipython().system('open masstolight_vs_slope.pdf')
sloeps
slopes
slopes[10]
ax=pl.gca()
ax.twiny()
ax.twinx()
tw = ax.twinx()
tw.set_ylim(m_to_ls[0]/m_to_ls[10], m_to_ls[-1]/m_to_ls[10])
get_ipython().run_line_magic('paste', '')
pl.figure(4).clf()
pl.plot(slopes, m_to_ls)
pl.xlabel("Upper-end power-law slope $\\alpha$")
pl.ylabel("Mass-to-light ratio [M$_\odot$/L$_\odot$]")
ax = pl.gca()
tw = ax.twinx()
tw.set_ylim(m_to_ls[0]/m_to_ls[10], m_to_ls[-1]/m_to_ls[10])
tw.set_ylabel("M/L / M/L($\\alpha=2.3$)")

pl.savefig("masstolight_vs_slope.pdf")

#pl.loglog(clusters.keys(), np.array(list(mean_luminosities.values())) / np.array(list(mean_masses.values())), '.', alpha=0.1)

# compute mass-to-light ratio vs age
get_ipython().run_line_magic('paste', '')
pl.rc('font', size=16)
pl.figure(4).clf()
pl.plot(slopes, m_to_ls)
pl.xlabel("Upper-end power-law slope $\\alpha$")
pl.ylabel("Mass-to-light ratio [M$_\odot$/L$_\odot$]")
ax = pl.gca()
tw = ax.twinx()
tw.set_ylim(m_to_ls[0]/m_to_ls[10], m_to_ls[-1]/m_to_ls[10])
tw.set_ylabel("M/L / M/L($\\alpha=2.3$)")

pl.savefig("masstolight_vs_slope.pdf")

#pl.loglog(clusters.keys(), np.array(list(mean_luminosities.values())) / np.array(list(mean_masses.values())), '.', alpha=0.1)

# compute mass-to-light ratio vs age
pl.savefig("masstolight_vs_slope.pdf", bbox_inches='tight')
get_ipython().run_line_magic('run', 'mass_to_light.py')
get_ipython().system('open masstolight_vs_slope*')
tw.semilogy()
.get_xaxis().get_major_formatter().labelOnlyBase = False
tw.get_xaxis().get_major_formatter().labelOnlyBase = False
pl.draw(); pl.show()
tw.get_yaxis().get_major_formatter().labelOnlyBase = False
pl.draw(); pl.show()
tw.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
tw.set_yticks([0.5,1,2,5])
pl.draw(); pl.show()
get_ipython().run_line_magic('paste', '')
pl.rc('font', size=16)
pl.figure(4).clf()
pl.semilogy(slopes, m_to_ls)
pl.xlabel("Upper-end power-law slope $\\alpha$")
pl.ylabel("Mass-to-light ratio [M$_\odot$/L$_\odot$]")
ax = pl.gca()
tw = ax.twinx()
tw.semilogy()
tw.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
tw.set_yticks([0.5,1,2,5])
tw.set_ylim(m_to_ls[0]/m_to_ls[10], m_to_ls[-1]/m_to_ls[10])
tw.set_ylabel("M/L / M/L($\\alpha=2.3$)")

pl.savefig("masstolight_vs_slope_log.pdf", bbox_inches='tight')

#pl.loglog(clusters.keys(), np.array(list(mean_luminosities.values())) / np.array(list(mean_masses.values())), '.', alpha=0.1)

# compute mass-to-light ratio vs age
get_ipython().run_line_magic('oaste', '')
get_ipython().run_line_magic('paste', '')
pl.rc('font', size=16)
pl.figure(4).clf()
pl.semilogy(slopes, m_to_ls)
pl.xlabel("Upper-end power-law slope $\\alpha$")
pl.ylabel("Mass-to-light ratio [M$_\odot$/L$_\odot$]")
ax = pl.gca()
tw = ax.twinx()
tw.semilogy()
tw.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
tw.set_yticks([0.5,1,2,5])
tw.set_ylim(m_to_ls[0]/m_to_ls[10], m_to_ls[-1]/m_to_ls[10])
tw.set_ylabel("M/L / M/L($\\alpha=2.3$)")

pl.savefig("masstolight_vs_slope_log.pdf", bbox_inches='tight')

#pl.loglog(clusters.keys(), np.array(list(mean_luminosities.values())) / np.array(list(mean_masses.values())), '.', alpha=0.1)

# compute mass-to-light ratio vs age
import matplotlib
get_ipython().run_line_magic('paste', '')
pl.rc('font', size=16)
pl.figure(4).clf()
pl.semilogy(slopes, m_to_ls)
pl.xlabel("Upper-end power-law slope $\\alpha$")
pl.ylabel("Mass-to-light ratio [M$_\odot$/L$_\odot$]")
ax = pl.gca()
tw = ax.twinx()
tw.semilogy()
tw.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
tw.set_yticks([0.5,1,2,5])
tw.set_ylim(m_to_ls[0]/m_to_ls[10], m_to_ls[-1]/m_to_ls[10])
tw.set_ylabel("M/L / M/L($\\alpha=2.3$)")

pl.savefig("masstolight_vs_slope_log.pdf", bbox_inches='tight')

#pl.loglog(clusters.keys(), np.array(list(mean_luminosities.values())) / np.array(list(mean_masses.values())), '.', alpha=0.1)

# compute mass-to-light ratio vs age
pl.grid()
get_ipython().run_line_magic('paste', '')
pl.rc('font', size=16)
pl.figure(4).clf()
pl.semilogy(slopes, m_to_ls)
pl.xlabel("Upper-end power-law slope $\\alpha$")
pl.ylabel("Mass-to-light ratio [M$_\odot$/L$_\odot$]")
ax = pl.gca()
tw = ax.twinx()
tw.semilogy()
tw.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
tw.set_yticks([0.5,1,2,5])
tw.set_ylim(m_to_ls[0]/m_to_ls[10], m_to_ls[-1]/m_to_ls[10])
tw.set_xlim(ax.get_xlim())
pl.grid()
tw.set_ylabel("M/L / M/L($\\alpha=2.3$)")

pl.savefig("masstolight_vs_slope_log.pdf", bbox_inches='tight')

#pl.loglog(clusters.keys(), np.array(list(mean_luminosities.values())) / np.array(list(mean_masses.values())), '.', alpha=0.1)

# compute mass-to-light ratio vs age
pl.grid(linestyle='--')
#tw.get_xaxis().set_ticks(ax.
ax.get_xticks()
tw.get_xaxis().set_ticks(ax.get_xticks())
pl.draw(); pl.show()
ax.grid(which='major')
tw.gr%paste
get_ipython().run_line_magic('paste', '')
pl.rc('font', size=16)
pl.figure(4).clf()
pl.semilogy(slopes, m_to_ls)
pl.xlabel("Upper-end power-law slope $\\alpha$")
pl.ylabel("Mass-to-light ratio [M$_\odot$/L$_\odot$]")
ax = pl.gca()
tw = ax.twinx()
tw.semilogy()
tw.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
tw.set_yticks([0.5,1,2,5])
tw.set_ylim(m_to_ls[0]/m_to_ls[10], m_to_ls[-1]/m_to_ls[10])
tw.set_xlim(ax.get_xlim())
tw.grid(which='major', linestyle='--')
tw.set_ylabel("M/L / M/L($\\alpha=2.3$)")

pl.savefig("masstolight_vs_slope_log.pdf", bbox_inches='tight')

#pl.loglog(clusters.keys(), np.array(list(mean_luminosities.values())) / np.array(list(mean_masses.values())), '.', alpha=0.1)

# compute mass-to-light ratio vs age
tw.get_xlim()
tw.get_xticks()
tw.grid(which='minor')
get_ipython().run_line_magic('paste', '')
pl.rc('font', size=16)
pl.figure(4).clf()
pl.semilogy(slopes, m_to_ls)
ax = pl.gca()
ylim = ax.get_ylim()
ax.vlines(2.3, 1e-5, 1, 'k--', alpha=0.5, zorder=-10)
ax.set_ylim(ylim)
pl.xlabel("Upper-end power-law slope $\\alpha$")
pl.ylabel("Mass-to-light ratio [M$_\odot$/L$_\odot$]")
tw = ax.twinx()
tw.semilogy()
tw.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
tw.set_yticks([0.5,1,2,5])
tw.set_ylim(m_to_ls[0]/m_to_ls[10], m_to_ls[-1]/m_to_ls[10])
tw.set_xlim(ax.get_xlim())
tw.hlines(1, 1, 5, linestyle='--', color='k', alpha=0.5, zorder=-20)
#tw.grid(which='major', linestyle='--')
tw.set_ylabel("M/L / M/L($\\alpha=2.3$)")

pl.savefig("masstolight_vs_slope_log.pdf", bbox_inches='tight')

#pl.loglog(clusters.keys(), np.array(list(mean_luminosities.values())) / np.array(list(mean_masses.values())), '.', alpha=0.1)

# compute mass-to-light ratio vs age
get_ipython().run_line_magic('paste', '')
pl.rc('font', size=16)
pl.figure(4).clf()
pl.semilogy(slopes, m_to_ls)
ax = pl.gca()
ylim = ax.get_ylim()
ax.vlines(2.3, 1e-5, 1, linestyle='--', color='k', alpha=0.5, zorder=-10)
ax.set_ylim(ylim)
pl.xlabel("Upper-end power-law slope $\\alpha$")
pl.ylabel("Mass-to-light ratio [M$_\odot$/L$_\odot$]")
tw = ax.twinx()
tw.semilogy()
tw.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
tw.set_yticks([0.5,1,2,5])
tw.set_ylim(m_to_ls[0]/m_to_ls[10], m_to_ls[-1]/m_to_ls[10])
tw.set_xlim(ax.get_xlim())
tw.hlines(1, 1, 5, linestyle='--', color='k', alpha=0.5, zorder=-20)
#tw.grid(which='major', linestyle='--')
tw.set_ylabel("M/L / M/L($\\alpha=2.3$)")

pl.savefig("masstolight_vs_slope_log.pdf", bbox_inches='tight')

#pl.loglog(clusters.keys(), np.array(list(mean_luminosities.values())) / np.array(list(mean_masses.values())), '.', alpha=0.1)

# compute mass-to-light ratio vs age
get_ipython().run_line_magic('paste', '')
pl.rc('font', size=16)
pl.figure(4).clf()
pl.semilogy(slopes, m_to_ls)
ax = pl.gca()
ylim = ax.get_ylim()
ax.vlines(2.3, 1e-5, 1, linestyle='--', color='k', alpha=0.2, zorder=-10)
ax.set_ylim(ylim)
pl.xlabel("Upper-end power-law slope $\\alpha$")
pl.ylabel("Mass-to-light ratio [M$_\odot$/L$_\odot$]")
tw = ax.twinx()
tw.semilogy()
tw.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
tw.set_yticks([0.5,1,2,5])
tw.set_ylim(m_to_ls[0]/m_to_ls[10], m_to_ls[-1]/m_to_ls[10])
tw.set_xlim(ax.get_xlim())
tw.hlines(1, 1, 5, linestyle='--', color='k', alpha=0.2, zorder=-20)
#tw.grid(which='major', linestyle='--')
tw.set_ylabel("M/L / M/L($\\alpha=2.3$)")

pl.savefig("masstolight_vs_slope_log.pdf", bbox_inches='tight')

#pl.loglog(clusters.keys(), np.array(list(mean_luminosities.values())) / np.array(list(mean_masses.values())), '.', alpha=0.1)

# compute mass-to-light ratio vs age
get_ipython().system('open masstolight_vs_slope_log.pdf')
get_ipython().system('open maxmass_vs_clustermass.pdf')
get_ipython().run_line_magic('pinfo', 'imf.make_cluster')
clusters
luminosities
clusters
luminosities
masses
mean_luminosities
mean_masses
max_masses
import h5py
stop_crit='nearest'
synth_data = {}
synth_data[stop_crit] = {'clusters': clusters,
                         'luminosities': luminosities,
                         'masses': masses,
                         'mean_luminosities': mean_luminosities,
                         'mean_masses': mean_masses,
                         'max_masses': max_masses}
                     
h5py.Dataset(synth_data)
h5 = h5py.Dataset(synth_data)
clusters
clusters[0]
clusters.keys()
get_ipython().run_line_magic('pinfo', 'json.dump')
json.dump
import json
get_ipython().run_line_magic('pinfo', 'json.dump')
get_ipython().run_line_magic('paste', '')
with open('synth_data_m_to_l.json', 'w') as fh:
    for crit in synth_data:
        for cl in synth_data['clusters']:
            synth_data[crit]['clusters'][cl] = synth_data[crit]['clusters'][cl].tolist()

    json.dump(synth_data, fh)
get_ipython().run_line_magic('paste', '')
with open('synth_data_m_to_l.json', 'w') as fh:
    for crit in synth_data:
        for cl in synth_data[crit]['clusters']:
            synth_data[crit]['clusters'][cl] = synth_data[crit]['clusters'][cl].tolist()

    json.dump(synth_data, fh)
get_ipython().run_line_magic('ls', '-lh *json')
len(clusters)
for cl in clusters:
    number[clmass] = len(clusters[clmass])
    
number = {}
for cl in clusters:
    number[clmass] = len(clusters[clmass])
    
number
clusters
number[cl] = len(clusters[cl])
for cl in clusters:
    number[cl] = len(clusters[cl])
    
number
synth_data[stop_crit] = {#'clusters': clusters,
                         'number': number,
                         'luminosities': luminosities,
                         'masses': masses,
                         'mean_luminosities': mean_luminosities,
                         'mean_masses': mean_masses,
                         'max_masses': max_masses}
                     
get_ipython().run_line_magic('paste', '')
with open('synth_data_m_to_l.json', 'w') as fh:
    # TOO BIG
    #for crit in synth_data:
    #    for cl in synth_data[crit]['clusters']:
    #        synth_data[crit]['clusters'][cl] = synth_data[crit]['clusters'][cl].tolist()

    json.dump(synth_data, fh)
get_ipython().run_line_magic('run', 'mass_to_light.py')
get_ipython().run_line_magic('run', 'mass_to_light.py')
get_ipython().run_line_magic('run', 'mass_to_light.py')
get_ipython().run_line_magic('run', 'mass_to_light.py')
get_ipython().system('open maxmass_vs_clustermass*')
luminosities
get_ipython().run_line_magic('run', 'mass_to_light.py')
get_ipython().run_line_magic('run', 'mass_to_light.py')
pl.close('all')
get_ipython().run_line_magic('run', 'mass_to_light.py')
clmasses
mass_to_light
clmasses
clmasses = sorted(map(float, masses))
clmasses
max_masses
get_ipython().run_line_magic('run', 'mass_to_light.py')
mean_masses
get_ipython().run_line_magic('run', 'mass_to_light.py')
get_ipython().run_line_magic('run', 'mass_to_light.py')
get_ipython().system('open maxmass_vs_clustermass*')
get_ipython().system('open maxmass_vs_clustermass*png')
get_ipython().run_line_magic('run', 'mass_to_light.py')
get_ipython().run_line_magic('run', 'mass_to_light.py')
luminosities
mean_luminosities
mean_masses
mass_to_light = np.array([mean_masses[str(k)]/10**mean_luminosities[str(k)] for k in clmasses])
pl.figure(2).clf()
pl.semilogx(clmasses, mass_to_light**-1, '.', alpha=0.1)
pl.xlabel("Cluster Mass")
pl.ylabel("Light to Mass $L_\odot / M_\odot$")
luminosities
mean_luminosities
k
clmasses
mass_to_light = np.array([k/10**luminosities[str(k)] for k in clmasses])
mass_to_light
pl.figure(2).clf()
pl.semilogx(clmasses, mass_to_light**-1, '.', alpha=0.1)
pl.loglog(clmasses, mass_to_light**-1, '.', alpha=0.1)
pl.close(2)
get_ipython().run_line_magic('paste', '')
pl.figure(2).clf()
pl.loglog(clmasses, mass_to_light**-1, '.', alpha=0.1)
pl.xlabel("Cluster Mass")
pl.ylabel("Light to Mass $L_\odot / M_\odot$")
pl.ylim(1,5e4)
pl.savefig(f"light_to_mass_vs_mass_{stop_crit}.png", bbox_inches='tight', dpi=200)
pl.savefig(f"light_to_mass_vs_mass_{stop_crit}.pdf", bbox_inches='tight')
clusters = [imf.make_cluster(100, 'kroupa', mmax=150, silent=True) for ii in range(1000)]
pl.figure()
pl.hist([cl.mean() for cl in clusters], bins=25)
get_ipython().run_line_magic('pinfo', 'imf.lum_of_cluster')
get_ipython().run_line_magic('pinfo2', 'imf.lum_of_cluster')
pl.figure()
pl.plot(np.logspace(-1,2), imf.lum_of_star(np.logspace(-1,2))
)
tbl = Vizier.get_catalogs('J/A+A/537/A146/iso')[0]
from astroquery.vizier import Vizier
tbl = Vizier.get_catalogs('J/A+A/537/A146/iso')[0]
tbl
Vizier.ROW_LIMIT=1e7
tbl = Vizier.get_catalogs('J/A+A/537/A146/iso')[0]
tbl
tbl['Mass']
tbl['Mass'].max()
tbl['Mass'].min()
tbl
match = tbl['logAge'] == 6.5
masses = tbl['Mass'][match]
lums = tbl['logL'][match]
masses[-2:]
lums[-2:]
np.log10(masses[-1]/masses[-2]) / (lums[-1]-lums[-2])
(np.log10(masses[-1]) - np.log10(masses[-2])) / (lums[-1]-lums[-2])
1/((np.log10(masses[-1]) - np.log10(masses[-2])) / (lums[-1]-lums[-2]))
get_ipython().run_line_magic('run', 'mass_to_light.py')
$$L_{pop} = \int L_*(m) N(m) dm$$
1/2.35 * (100**-1.35 - 8**-1.35)
#[Out]# -0.02484074818843998
-1/2.35 * (100**-1.35 - 8**-1.35) / (-1/1.35 * (100**-0.35 - 0.1**-0.35))
#[Out]# 0.01644522058097654
-1/2.35 * (100**-1.35 - 8**-1.35) / (-1/1.35 * (100**-0.35 - 0.1**-0.35)) /2
#[Out]# 0.00822261029048827
-1/2.35 * (100**-1.35 - 8**-1.35) / (-1/1.35 * (100**-0.35 - 0.1**-0.35)) 
#[Out]# 0.01644522058097654
(100**-1.35 - 8**-1.35) / ( (100**-0.35 - 0.1**-0.35)) 
#[Out]# 0.028626865455773975
-1/2.35 * (100**-1.35 - 8**-1.35)
#[Out]# 0.02484074818843998
(-1/1.35 * (100**-0.35 - 0.1**-0.35)) 
#[Out]# 1.5105147459788528
from scipy.integrate import quad
quad(f(x):x**-2.35, 8, 100)
from scipy.integrate import quad
quad(lambda (x):x**-2.35, 8, 100)
from scipy.integrate import quad
quad(lambda x:x**-2.35, 8, 100)
#[Out]# (0.04324130240209924, 1.664224581884688e-10)
-1/1.35 * (100**-1.35 - 8**-1.35)
#[Out]# 0.043241302402099224
(-1/0.35 * (100**-0.35 - 0.1**-0.35)) 
#[Out]# 5.82627116306129
-1/1.35 * (100**-1.35 - 8**-1.35) / (-1/0.35 * (100**-0.35 - 0.1**-0.35)) 
#[Out]# 0.0074217799329784374
-1/1.35 * (120**-1.35 - 8**-1.35) / (-1/0.35 * (120**-0.35 - 0.1**-0.35)) 
#[Out]# 0.007432171927854529
def wtfunc(mmax=100):
    return -1/1.35 * (mmax**-1.35 - 8**-1.35) / (-1/0.35 * (mmax**-0.35 - 0.1**-0.35)) 
pl.plot(np.linspace(20,300), wtfunc(np.linspace(20,300)))
get_ipython().run_line_magic('matplotlib', 'inline')
import pylab as pl
pl.plot(np.linspace(20,300), wtfunc(np.linspace(20,300)))
#[Out]# [<matplotlib.lines.Line2D at 0x1523758940>]
def wtfunc(mmax=100, alpha=2.35):
    return -1/(alpha-1) * (mmax**-(alpha-1) - 8**-(alpha-1)) / (-1/(alpha-2) * (mmax**-(alpha-2) - 0.1**-(alpha-2))) 
get_ipython().run_line_magic('matplotlib', 'inline')
import pylab as pl
pl.plot(np.linspace(20,300), wtfunc(np.linspace(20,300)))
#[Out]# [<matplotlib.lines.Line2D at 0x15238b4e80>]
pl.plot(np.linspace(1.5,3), wtfunc(alpha=np.linspace(1.5,3)))
#[Out]# [<matplotlib.lines.Line2D at 0x152398aba8>]
pl.plot(np.linspace(1.5,3), wtfunc(alpha=np.linspace(1.5,3)) / wtfunc())
#[Out]# [<matplotlib.lines.Line2D at 0x15239f06d8>]
pl.semilogy(np.linspace(1.5,3), wtfunc(alpha=np.linspace(1.5,3)) / wtfunc())
#[Out]# [<matplotlib.lines.Line2D at 0x1523a9eeb8>]
pl.rc('font', size=16)
pl.semilogy(np.linspace(1.5,3), wtfunc(alpha=np.linspace(1.5,3)) / wtfunc())
pl.xlabel("$\alpha$")
pl.ylabel("SNe/M$_\odot$ relative to $\alpha=2.35$")
#[Out]# Text(0,0.5,'SNe/M$_\\odot$ relative to $\x07lpha=2.35$')
pl.rc('font', size=16)
pl.semilogy(np.linspace(1.5,3), wtfunc(alpha=np.linspace(1.5,3)) / wtfunc())
pl.xlabel(r"$\alpha$")
pl.ylabel(r"SNe/M$_\odot$ relative to $\alpha=2.35$")
#[Out]# Text(0,0.5,'SNe/M$_\\odot$ relative to $\\alpha=2.35$')
pl.rc('font', size=16)
pl.rc('figure', dpi=300)
pl.semilogy(np.linspace(1.5,3), wtfunc(alpha=np.linspace(1.5,3)) / wtfunc())
pl.xlabel(r"$\alpha$")
pl.ylabel(r"SNe/M$_\odot$ relative to $\alpha=2.35$")
#[Out]# Text(0,0.5,'SNe/M$_\\odot$ relative to $\\alpha=2.35$')
get_ipython().run_line_magic('matplotlib', 'inline')
import pylab as pl
pl.plot(np.linspace(20,300), wtfunc(np.linspace(20,300)))
pl.xlabel(r"M$_{max}$ [M$_\odot$]")
pl.ylabel("SNe/M$_\odot$")
#[Out]# Text(0,0.5,'SNe/M$_\\odot$')
get_ipython().run_line_magic('matplotlib', 'inline')
import pylab as pl
pl.rc('font', size=16)
pl.rc('figure', dpi=300)
pl.plot(np.linspace(20,300), wtfunc(np.linspace(20,300)))
pl.xlabel(r"M$_{max}$ [M$_\odot$]")
pl.ylabel("SNe/M$_\odot$")
#[Out]# Text(0,0.5,'SNe/M$_\\odot$')
pl.rc('font', size=16)
pl.rc('figure', dpi=300)
pl.semilogy(np.linspace(1.5,3), wtfunc(alpha=np.linspace(1.5,3)) / wtfunc())
ylim = pl.ylim()
pl.vlines(2.35, 0.01, 100, color='k', linestyle='--', alpha=0.5)
pl.hlines(1.0, 1, 4, color='k', linestyle='--', alpha=0.5)
pl.ylim(ylim)
pl.xlabel(r"$\alpha$")
pl.ylabel(r"SNe/M$_\odot$ relative to $\alpha=2.35$")
#[Out]# Text(0,0.5,'SNe/M$_\\odot$ relative to $\\alpha=2.35$')
pl.rc('font', size=16)
pl.rc('figure', dpi=300)
pl.semilogy(np.linspace(1.5,3), wtfunc(alpha=np.linspace(1.5,3)) / wtfunc())
axis = pl.axis()
pl.vlines(2.35, 0.01, 100, color='k', linestyle='--', alpha=0.5)
pl.hlines(1.0, 1, 4, color='k', linestyle='--', alpha=0.5)
pl.axis(*axis)
pl.xlabel(r"$\alpha$")
pl.ylabel(r"SNe/M$_\odot$ relative to $\alpha=2.35$")
pl.rc('font', size=16)
pl.rc('figure', dpi=300)
pl.semilogy(np.linspace(1.5,3), wtfunc(alpha=np.linspace(1.5,3)) / wtfunc())
axislims = pl.axis()
pl.vlines(2.35, 0.01, 100, color='k', linestyle='--', alpha=0.5)
pl.hlines(1.0, 1, 4, color='k', linestyle='--', alpha=0.5)
pl.axis(axlims)
pl.xlabel(r"$\alpha$")
pl.ylabel(r"SNe/M$_\odot$ relative to $\alpha=2.35$")
pl.rc('font', size=16)
pl.rc('figure', dpi=300)
pl.semilogy(np.linspace(1.5,3), wtfunc(alpha=np.linspace(1.5,3)) / wtfunc())
axlims = pl.axis()
pl.vlines(2.35, 0.01, 100, color='k', linestyle='--', alpha=0.5)
pl.hlines(1.0, 1, 4, color='k', linestyle='--', alpha=0.5)
pl.axis(axlims)
pl.xlabel(r"$\alpha$")
pl.ylabel(r"SNe/M$_\odot$ relative to $\alpha=2.35$")
#[Out]# Text(0,0.5,'SNe/M$_\\odot$ relative to $\\alpha=2.35$')
def wtfunc(mmax=100, alpha=2.35, mmin=0.1):
    return (-1/(alpha-1) * (mmax**-(alpha-1) - 8**-(alpha-1))
            / (-1/(alpha-2) * (mmax**-(alpha-2) - mmin**-(alpha-2))))
pl.loglog(np.logspace(-2,0), wtfunc(mmin=np.linspace(-2, 0)))
pl.xlabel(r"M$_{min}$ [M$_\odot$]")
pl.ylabel("SNe/M$_\odot$")
#[Out]# Text(0,0.5,'SNe/M$_\\odot$')
wtfunc(mmin=np.linspace(-2, 0))
#[Out]# array([nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan,
#[Out]#        nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan,
#[Out]#        nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan,
#[Out]#        nan, nan, nan, nan, nan, nan, nan, nan, nan, nan,  0.])
pl.loglog(np.logspace(-2,0), wtfunc(mmin=np.logspace(-2, 0)))
pl.xlabel(r"M$_{min}$ [M$_\odot$]")
pl.ylabel("SNe/M$_\odot$")
#[Out]# Text(0,0.5,'SNe/M$_\\odot$')
wtfunc(mmin=np.logspace(-2, 0))
#[Out]# array([0.00314492, 0.0032546 , 0.00336828, 0.00348609, 0.00360821,
#[Out]#        0.00373482, 0.00386608, 0.00400219, 0.00414334, 0.00428973,
#[Out]#        0.00444158, 0.00459912, 0.00476258, 0.0049322 , 0.00510824,
#[Out]#        0.00529098, 0.00548071, 0.0056777 , 0.0058823 , 0.00609481,
#[Out]#        0.0063156 , 0.00654503, 0.00678347, 0.00703135, 0.00728908,
#[Out]#        0.00755712, 0.00783594, 0.00812606, 0.008428  , 0.00874232,
#[Out]#        0.00906963, 0.00941056, 0.00976577, 0.01013599, 0.01052197,
#[Out]#        0.01092451, 0.01134448, 0.01178278, 0.01224039, 0.01271836,
#[Out]#        0.01321779, 0.01373987, 0.01428589, 0.0148572 , 0.01545527,
#[Out]#        0.01608169, 0.01673815, 0.01742649, 0.01814868, 0.01890687])
pl.loglog(np.logspace(-2,0), wtfunc(mmin=np.logspace(-2, 0))/wtfunc())
pl.xlabel(r"M$_{min}$ [M$_\odot$]")
pl.ylabel("SNe/M$_\odot$")
#[Out]# Text(0,0.5,'SNe/M$_\\odot$')
pl.loglog(np.logspace(-2,0), wtfunc(mmin=np.logspace(-2, 0))/wtfunc())
pl.xlabel(r"M$_{min}$ [M$_\odot$]")
pl.ylabel(r"SNe/M$_\odot$ relative to M$_{min}=0.01$ M$_\odot$")
#[Out]# Text(0,0.5,'SNe/M$_\\odot$ relative to M$_{min}=0.01$ M$_\\odot$')
$${\displaystyle N=R_{*}\cdot f_{\mathrm {p} }\cdot n_{\mathrm {e} }\cdot f_{\mathrm {l} }\cdot f_{\mathrm {i} }\cdot f_{\mathrm {c} }\cdot L}$$
