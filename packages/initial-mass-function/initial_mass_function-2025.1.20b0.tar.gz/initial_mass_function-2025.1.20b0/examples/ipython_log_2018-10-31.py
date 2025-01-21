########################################################
# Started Logging At: 2018-10-31 11:13:28
########################################################

########################################################
# # Started Logging At: 2018-10-31 11:13:29
########################################################
from astroquery.vizier import Vizier
get_ipython().magic('pinfo Vizier.get_catalogs')
from astroquery.vizier import Vizier
Vizier.get_catalogs('J/A+A/537/A146/iso')
Vizier.row_limit=1e7
Vizier.get_catalogs('J/A+A/537/A146/iso')
get_ipython().magic('paste')
Vizier.ROW_LIMIT=1e7

Vizier.get_catalogs('J/A+A/537/A146/iso')
    # # FAILURE: table is inadequate
    # hr diagram
    # pl.figure(2).clf()

    # #tbl = Table.read('/Users/adam/repos/imf/imf/data/pecaut2013_table_with_lyclum.txt', format='ascii.fixed_width')
    # #tbl = Table.read('/Users/adam/repos/imf/imf/data/EEM_dwarf_UBVIJHK_colors_Teff_noheader.txt', format='ascii.commented_header')
    # tbl = Table.read('/Users/adam/repos/imf/imf/data/EEM_dwarf_UBVIJHK_colors_Teff_noheader.txt', format='ascii.commented_header')
    # ok = tbl['Msun'] < 500
    # colors = imf.color_of_cluster(tbl['Msun'][ok])
    # pl.gca().set_xscale('log')
    # pl.gca().set_yscale('log')
    # pl.scatter(tbl['Teff'][ok], tbl['Msun'][ok], c=colors,
    #            s=tbl['logL'][ok]*85)
tbl = Vizier.get_catalogs('J/A+A/537/A146/iso')[0]
tbl
tbl['logAge'].min()
get_ipython().magic('paste ')
from astroquery.vizier import Vizier

Vizier.ROW_LIMIT=1e7

tbl = Vizier.get_catalogs('J/A+A/537/A146/iso')[0]
    # hr diagram
pl.figure(2).clf()

ok = tbl['logAge'] == 6.5

colors = imf.color_of_cluster(tbl['Msun'][ok])
pl.gca().set_xscale('log')
pl.gca().set_yscale('log')
pl.scatter(tbl['Teff'][ok], tbl['Msun'][ok], c=colors,
           s=tbl['logL'][ok]*85)
get_ipython().magic('paste')
import pylab as pl
from astroquery.vizier import Vizier

Vizier.ROW_LIMIT=1e7

tbl = Vizier.get_catalogs('J/A+A/537/A146/iso')[0]
    # hr diagram
pl.figure(2).clf()

ok = tbl['logAge'] == 6.5

colors = imf.color_of_cluster(tbl['Msun'][ok])
pl.gca().set_xscale('log')
pl.gca().set_yscale('log')
pl.scatter(tbl['Teff'][ok], tbl['Msun'][ok], c=colors,
           s=tbl['logL'][ok]*85)
get_ipython().magic('paste')
import imf
import pylab as pl
from astroquery.vizier import Vizier

Vizier.ROW_LIMIT=1e7

tbl = Vizier.get_catalogs('J/A+A/537/A146/iso')[0]
    # hr diagram
pl.figure(2).clf()

ok = tbl['logAge'] == 6.5

colors = imf.color_of_cluster(tbl['Msun'][ok])
pl.gca().set_xscale('log')
pl.gca().set_yscale('log')
pl.scatter(tbl['Teff'][ok], tbl['Msun'][ok], c=colors,
           s=tbl['logL'][ok]*85)
tbl
get_ipython().magic('paste')
import imf
import pylab as pl
from astroquery.vizier import Vizier

Vizier.ROW_LIMIT=1e7

tbl = Vizier.get_catalogs('J/A+A/537/A146/iso')[0]
    # hr diagram
pl.figure(2).clf()

ok = tbl['logAge'] == 6.5

colors = imf.color_of_cluster(tbl['Mass'][ok])
pl.gca().set_xscale('log')
pl.gca().set_yscale('log')
pl.scatter(tbl['Teff'][ok], tbl['Mass'][ok], c=colors,
           s=tbl['logL'][ok]*85)
tbl
get_ipython().magic('run hr_diagram.py')
tbl['Mass'][ok]
get_ipython().magic('run hr_diagram.py')
colors
subtbl['Mass']
get_ipython().magic('run hr_diagram.py')
colors
imf.color_from_mass(0.1)
imf.color_from_mass(0.2)
imf.color_from_mass(0.5)
imf.color_from_mass(1)
imf.color_from_mass(10)
subtbl['Mass']
get_ipython().magic('run hr_diagram.py')
imf.color_from_mass(0.1)
subtbl
subtbl['Mass'].min()
tbl['Mass'].min()
imf.color_from_mass(0.8)
pl.scatter([1e4],[10],c=imf.color_from_mass(0.8),s=1000)
colors[:10]
10**subtbl['logTe']
subtbl['Mass']
subtbl['logL']*85
subtbl
get_ipython().magic('run hr_diagram.py')
get_ipython().magic('run hr_diagram.py')
tbl
[tbl['logAge'] == 10.1]['Mass'].max()
[tbl['logAge'] == 10.1]['Mass']
[tbl['logAge'] == 10.1]
tbl[tbl['logAge'] == 10.1]
tbl[tbl['logAge'] == 10.1]['Mass']
tbl[tbl['logAge'] == 10.1]['Mass'].max()
tbl
subtbl['Mass'] < 2
subtbl[subtbl['Mass'] < 2]
#np.polyfit(
lowmass = subtbl[subtbl['Mass'] < 2]
get_ipython().magic('pinfo np.polyfit')
np.polyfit(np.log10(lowmass['Mass']), lowmass['logL'], 1)
np.polyfit((lowmass['Mass']), 10**lowmass['logL'], 1)
pl.figure()
pl.plot(lowmass['mass'], 10**lowmass['logL'])
pl.plot(lowmass['Mass'], 10**lowmass['logL'], '.')
get_ipython().magic('pinfo np.poly1d')
fit = np.polyfit(np.log10(lowmass['Mass']), lowmass['logL'], 1)
masses = np.linspace(0.03, 0.8)
lums = np.poly1d(fit)(masses)
pl.plot(np.log10(lowmass['Mass']), lowmass['logL'], '.')
pl.clf()
pl.plot(np.log10(lowmass['Mass']), lowmass['logL'], '.')
fit = np.polyfit(np.log10(lowmass['Mass']), lowmass['logL'], 1)
masses = np.linspace(0.03, 0.8)
lums = np.poly1d(fit)(masses)
pl.plot(masses, lums)
pl.plot(np.log10(masses), lums)
masses = np.linspace(0.03, 0.8)
lums = np.poly1d(fit)(np.log10(masses))
pl.plot(np.log10(masses), lums)
pl.clf()
pl.plot(np.log10(lowmass['Mass']), lowmass['logTe'], '.')
lums
get_ipython().magic('run hr_diagram.py')
get_ipython().magic('run hr_diagram.py')
get_ipython().magic('run hr_diagram.py')
ages
get_ipython().magic('run hr_diagram.py')
get_ipython().magic('R')
get_ipython().magic('run hr_diagram.py')
agemass
get_ipython().magic('run hr_diagram.py')
get_ipython().magic('pinfo pl.hline')
pl.hlines
get_ipython().magic('pinfo pl.hlines')
get_ipython().magic('run hr_diagram.py')
for age in (6.5, 7, 8, 9):
        pl.hlines(agemass[age], [1e3,1e5], linestyle='--', color='k')
        
for age in (6.5, 7, 8, 9):
        pl.hlines(agemass[age], 1e3, 1e5, linestyle='--', color='k')
        
get_ipython().magic('run hr_diagram.py')
pl.gca().get_lines()
get_ipython().magic('paste')
lines = []
for age in (6.5, 7, 8, 9):
    L = pl.hlines(agemass[age], 1e3, 1e5, linestyle='--', color='k',
                  label="10^{0} yr".format(age))
    lines.append(L)
lines
get_ipython().magic('run hr_diagram.py')
L
get_ipython().magic('run hr_diagram.py')
get_ipython().magic('run hr_diagram.py')
subtbl
subtbl['logL']
10**subtbl['logL']
get_ipython().magic('run hr_diagram.py')
get_ipython().magic('run hr_diagram.py')
get_ipython().magic('R')
get_ipython().magic('run hr_diagram.py')
get_ipython().magic('run hr_diagram.py')
get_ipython().magic('run hr_diagram.py')
get_ipython().system('git commit -av')
git push
get_ipython().system('git push')
get_ipython().magic('run hr_diagram.py')
get_ipython().magic('run hr_diagram.py')
agemass
get_ipython().magic('run hr_diagram.py')
agell
agelum
get_ipython().magic('run hr_diagram.py')
get_ipython().magic('run hr_diagram.py')
Lfit
get_ipython().magic('run hr_diagram.py')
get_ipython().magic('r')
get_ipython().magic('run hr_diagram.py')
lums
lums[masses<np.log10(0.43)] = 0.23*(masses[masses<np.log10(0.43)])**2.3
lums
0.23*(masses[masses<np.log10(0.43)])**2.3
masses
get_ipython().magic('run hr_diagram.py')
get_ipython().magic('run hr_diagram.py')
get_ipython().magic('pwd ')
get_ipython().magic('run hr_diagram.py')
get_ipython().system('open *svg')
get_ipython().magic('run hr_diagram.py')
get_ipython().magic('run hr_diagram.py')
get_ipython().system('open *svg')
get_ipython().magic('run hr_diagram.py')
get_ipython().magic('run hr_diagram.py')
get_ipython().magic('run hr_diagram.py')
get_ipython().magic('run hr_diagram.py')
get_ipython().magic('run hr_diagram.py')
htems
10**htems
np.log10(highmass['Mass']), highmass['logTe']
np.log10(highmass['Mass']), highmass['logTe']
get_ipython().magic('run hr_diagram.py')
hmasses
htems
10**htems
hmasses
get_ipython().magic('run hr_diagram.py')
10**htems
Tfit
pl.figure()
pl.plot(np.log10(highmass['Mass']), highmass['logTe'])
pl.plot(np.log10(highmass['Mass']), highmass['logTe'], 's')
get_ipython().magic('run hr_diagram.py')
10**htems
get_ipython().magic('run hr_diagram.py')
get_ipython().magic('run hr_diagram.py')
get_ipython().magic('run hr_diagram.py')
get_ipython().magic('paste')
pl.figure(3).clf()

colors = [imf.color_from_mass(m) for m in subtbl['Mass']]
#pl.gca().set_xscale('log')
pl.gca().set_yscale('log')
pl.scatter(10**subtbl['logTe'],
           10**subtbl['logL'],
           c=colors,
           s=(subtbl['Mass'])*5)

colors = [imf.color_from_mass(m) for m in masses]
pl.scatter(10**tems,
           10**lums,
           c=colors,
           s=masses*5)

lines = []
for age in (6.5, 7, 8, 9):
    L, = pl.plot([10**tems.min(), (10**subtbl['logTe'].max())],
                 [10**agelum[age]]*2,
                 linestyle='--', color='k',
                 label="$10^{{{0}}}$ yr".format(age))
    lines.append(L)

labelLines(lines)
pl.xlabel("Temperature")
pl.ylabel("Luminosity")
pl.savefig("HR_diagram.svg", bbox_inches='tight')
get_ipython().magic('run hr_diagram.py')
get_ipython().magic('run hr_diagram.py')
get_ipython().magic('run hr_diagram.py')
get_ipython().magic('run hr_diagram.py')
get_ipython().magic('run hr_diagram.py')
get_ipython().magic('run hr_diagram.py')
get_ipython().magic('run hr_diagram.py')
pl.close('all')
get_ipython().magic('run hr_diagram.py')
get_ipython().magic('run hr_diagram.py')
get_ipython().magic('run hr_diagram.py')
get_ipython().magic('run hr_diagram.py')
get_ipython().magic('run hr_diagram.py')
get_ipython().magic('run hr_diagram.py')
get_ipython().magic('run hr_diagram.py')
get_ipython().magic('pinfo pl.savefig')
get_ipython().magic('run hr_diagram.py')
get_ipython().magic('pinfo pl.savefig')
pl.gca().bbox
get_ipython().magic('run hr_diagram.py')
get_ipython().magic('run hr_diagram.py')
get_ipython().magic('run hr_diagram.py')
get_ipython().magic('run hr_diagram.py')
