########################################################
# Started Logging At: 2018-10-26 14:04:09
########################################################

########################################################
# # Started Logging At: 2018-10-26 14:04:10
########################################################
import imf
imf.kroupa
imf.kroupa.__class__.__name__
imf.chabrier
get_ipython().magic('run imf_figure.py')
imf.chabrier
imf.chabrier2005
imf.chabrier2005.mmin
get_ipython().magic('run imf_figure.py')
get_ipython().system('open *imf_figure*png')
get_ipython().magic('ls *imf_figure*png')
get_ipython().magic('ls *imf_figure*png')
get_ipython().magic('run imf_figure.py')
get_ipython().system('open *imf_figure*png')
get_ipython().magic('run imf_figure.py')
get_ipython().magic('run imf_figure.py')
pl.close('all')
get_ipython().magic('run imf_figure.py')
get_ipython().magic('run imf_figure.py')
get_ipython().magic('run imf_figure.py')
get_ipython().system('open *imf_figure*png')
get_ipython().magic('run imf_figure.py')
get_ipython().system('open *imf_figure_log.png')
imf.lum_of_star
get_ipython().magic('cd ..')
get_ipython().system('ag pecaut')
tbl = Table.read('/Users/adam/repos/imf/imf/data/pecaut2013_table_with_lyclum.txt')
from astropy import constants, units as u, table, stats, coordinates, wcs, log, coordinates as coord, convolution, modeling, visualization; from astropy.io import fits, ascii; from astropy.table import Table
tbl = Table.read('/Users/adam/repos/imf/imf/data/pecaut2013_table_with_lyclum.txt')
tbl = Table.read('/Users/adam/repos/imf/imf/data/pecaut2013_table_with_lyclum.txt', format='ascii.fixed_width')
tbl
pl.plot(tbl['Teff'], tbl['Msun'], 'o')
pl.clf()
pl.plot(tbl['Teff'], tbl['Msun'], 'o')
pl.loglog(tbl['Teff'], tbl['Msun'], 'o')
get_ipython().magic('history ')
tbl
get_ipython().magic('paste')
pl.figure(2).clf()

tbl = Table.read('/Users/adam/repos/imf/imf/data/pecaut2013_table_with_lyclum.txt', format='ascii.fixed_width')
ok = tbl['Msun'] < 500
colors = imf.color_from_mass(tbl['Msun'])
pl.gca().set_xscale('log')
pl.gca().set_yscale('log')
pl.scatter(tbl['Teff'][ok], tbl['Msun'][ok], c=colors[ok],
           s=tbl['logL'][ok]*85)
ok
colors
colors
get_ipython().magic('paste')
pl.figure(2).clf()

tbl = Table.read('/Users/adam/repos/imf/imf/data/pecaut2013_table_with_lyclum.txt', format='ascii.fixed_width')
ok = tbl['Msun'] < 500
colors = imf.color_from_mass(tbl['Msun'][ok])
pl.gca().set_xscale('log')
pl.gca().set_yscale('log')
pl.scatter(tbl['Teff'][ok], tbl['Msun'][ok], c=colors,
           s=tbl['logL'][ok]*85)
get_ipython().magic('paste')
pl.figure(2).clf()

tbl = Table.read('/Users/adam/repos/imf/imf/data/pecaut2013_table_with_lyclum.txt', format='ascii.fixed_width')
ok = tbl['Msun'] < 500
colors = imf.color_of_cluster(tbl['Msun'][ok])
pl.gca().set_xscale('log')
pl.gca().set_yscale('log')
pl.scatter(tbl['Teff'][ok], tbl['Msun'][ok], c=colors,
           s=tbl['logL'][ok]*85)
tbl
tbl = Table.read('/Users/adam/repos/imf/imf/data/EEM_dwarf_UBVIJHK_colors_Teff.txt', format='ascii.fixed_width')
tbl
tbl = Table.read('/Users/adam/repos/imf/imf/data/EEM_dwarf_UBVIJHK_colors_Teff.txt', format='ascii.fixed_width', comment='#')
tbl
get_ipython().magic('pinfo Table.read')
tbl = Table.read('/Users/adam/repos/imf/imf/data/EEM_dwarf_UBVIJHK_colors_Teff.txt', format='ascii.fixed_width', comment='#', enddata=148)
tbl = Table.read('/Users/adam/repos/imf/imf/data/EEM_dwarf_UBVIJHK_colors_Teff.txt', format='ascii.commented_header', comment='#', enddata=148)
tbl = Table.read('/Users/adam/repos/imf/imf/data/EEM_dwarf_UBVIJHK_colors_Teff.txt', format='ascii.commented_header', comment='#', end_line=148)
tbl = Table.read('/Users/adam/repos/imf/imf/data/EEM_dwarf_UBVIJHK_colors_Teff.txt', format='ascii.commented_header', comment='#', end_line=148, start_line=23)
tbl = Table.read('/Users/adam/repos/imf/imf/data/EEM_dwarf_UBVIJHK_colors_Teff.txt', format='ascii.fixed_width', comment='#', end_line=148, start_line=23)
get_ipython().magic('pinfo ascii.read')
tbl = Table.read('/Users/adam/repos/imf/imf/data/EEM_dwarf_UBVIJHK_colors_Teff_noheader.txt', format='ascii.fixed_width')
tbl
tbl = Table.read('/Users/adam/repos/imf/imf/data/EEM_dwarf_UBVIJHK_colors_Teff_noheader.txt', format='ascii.commented_header')
tbl
get_ipython().magic('paste')
pl.figure(2).clf()

#tbl = Table.read('/Users/adam/repos/imf/imf/data/pecaut2013_table_with_lyclum.txt', format='ascii.fixed_width')
#tbl = Table.read('/Users/adam/repos/imf/imf/data/EEM_dwarf_UBVIJHK_colors_Teff_noheader.txt', format='ascii.commented_header')
tbl = Table.read('/Users/adam/repos/imf/imf/data/EEM_dwarf_UBVIJHK_colors_Teff_noheader.txt', format='ascii.commented_header')
ok = tbl['Msun'] < 500
colors = imf.color_of_cluster(tbl['Msun'][ok])
pl.gca().set_xscale('log')
pl.gca().set_yscale('log')
pl.scatter(tbl['Teff'][ok], tbl['Msun'][ok], c=colors,
           s=tbl['logL'][ok]*85)
tbl
tbl['Msun']
tbl
get_ipython().magic('ls /Users/adam/repos/slug')
massfunc
get_ipython().magic('pinfo imf.Kroupa')
get_ipython().magic('paste')
massfunc = imf.Kroupa(p3=1.75)
name='KroupaTopHeavy'
pl.figure(1, figsize=(10,8))
pl.clf()
cluster,yax,colors = coolplot(1000, massfunc=massfunc)
pl.scatter(cluster, yax, c=colors, s=np.log10(cluster+3)*85)
pl.gca().set_xscale('log')

masses = np.logspace(np.log10(cluster.min()), np.log10(cluster.max()),10000)

pl.plot(masses,np.log10(massfunc(masses)),'r--',linewidth=2,alpha=0.5)
pl.xlabel("Stellar Mass")
pl.ylabel("log(dN(M)/dM)")
pl.gca().axis([min(cluster)/1.1,max(cluster)*1.1,min(yax)-0.2,max(yax)+0.5])
pl.savefig("{0}_imf_figure_log.png".format(name),bbox_inches='tight', dpi=150)
pl.savefig("{0}_imf_figure_log.pdf".format(name),bbox_inches='tight')
get_ipython().system('open KroupaTopHeavy_imf_figure_log.p*')
get_ipython().system('open Kroupa*png')
get_ipython().magic('ls ')
get_ipython().magic('mv KroupaTopHeavy_imf_figure_log.p* ex')
get_ipython().magic('mv KroupaTopHeavy_imf_figure_log.p* examples/')
get_ipython().magic('cd examples/')
get_ipython().system('open Kroupa*png')
get_ipython().system('open Kroupa*png')
get_ipython().system('open Kroupa*png')
x = np.array([135.17352 140.68657 218.63655 218.63655 299.34192 380.0462 460.75275 541.45703])
x = np.array(map(float, "135.17352 140.68657 218.63655 218.63655 299.34192 380.0462 460.75275 541.45703".split()))
x
x = np.array(list(map(float, "135.17352 140.68657 218.63655 218.63655 299.34192 380.0462 460.75275 541.45703".split())))
x
x/2
(x/2).tolist()
" ".join((x/2).tolist())
" ".join(map(str,(x/2).tolist()))
x = np.array(list(map(float, "122.81505 128.32809 206.27808 286.98346 367.68774 448.39429 529.09857".split())))
" ".join(map(str, np.array(list(map(float, "122.81505 128.32809 206.27808 286.98346 367.68774 448.39429 529.09857".split())))/1.5))
np.arange(5)
np.arange(5) / np.zeros(5)
get_ipython().magic('history ')
