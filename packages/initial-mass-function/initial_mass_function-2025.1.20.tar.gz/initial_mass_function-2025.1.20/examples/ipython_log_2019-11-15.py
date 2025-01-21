########################################################
# Started Logging At: 2019-11-15 15:42:26
########################################################

########################################################
# # Started Logging At: 2019-11-15 15:42:27
########################################################
imf.vgslogL
imf.vgslogLe
imf.lum_of_star(np.linspace(0.033, 200))
get_ipython().run_line_magic('paste', '')
from astroquery.vizier import Vizier
Vizier.ROW_LIMIT = 1e7 # effectively infinite

# this query should cache
tbl = Vizier.get_catalogs('J/A+A/537/A146/iso')[0]

match = tbl['logAge'] == 6.5
masses = tbl['Mass'][match]
lums = tbl['logL'][match]
mass_0 = 0.033
lum_0 = np.log10((mass_0/masses[0])**3.5 * 10**lums[0])
mass_f = 200 # extrapolate to 200 Msun...
lum_f = np.log10(lums[-1] * (mass_f/masses[-1])**1.35)

masses = np.array([mass_0] + masses.tolist() + [mass_f])
lums = np.array([lum_0] + lums.tolist() + [lum_f])
list(zip(masses, lums))
list(zip(masses, lums))[0]
list(zip(masses, lums))[-1]
list(zip(masses, lums))[-10]
list(zip(masses, lums))[-5]
masses[-1]
lum_f = np.log10(lums[-1] * (mass_f/masses[-1])**1.35)
mass_f[-1]
lum_f = np.log10(10**lums[-1] * (mass_f/masses[-1])**1.35)
lum_f
lums[-1]
mass_f
masses[-1]
get_ipython().run_line_magic('paste', '')
match = tbl['logAge'] == 6.5
masses = tbl['Mass'][match]
lums = tbl['logL'][match]
mass_0 = 0.033
lum_0 = np.log10((mass_0/masses[0])**3.5 * 10**lums[0])
mass_f = 200 # extrapolate to 200 Msun...
lum_f = np.log10(10**lums[-1] * (mass_f/masses[-1])**1.35)

masses = np.array([mass_0] + masses.tolist() + [mass_f])
lums = np.array([lum_0] + lums.tolist() + [lum_f])
list(zip(masses, lums))[-1]
imf.lum_of_star(np.linspace(0.033, 200))
get_ipython().run_line_magic('pinfo', 'np.interp')
np.interp(np.linspace(0.033, 200), masses, lums)
########################################################
# Started Logging At: 2019-11-15 16:00:42
########################################################

########################################################
# # Started Logging At: 2019-11-15 16:00:43
########################################################
import imf
imf.lum_of_star(np.linspace(0.033, 200))
get_ipython().run_line_magic('paste', '')
from astroquery.vizier import Vizier
Vizier.ROW_LIMIT = 1e7 # effectively infinite

# this query should cache
tbl = Vizier.get_catalogs('J/A+A/537/A146/iso')[0]

match = tbl['logAge'] == 6.5
masses = tbl['Mass'][match]
lums = tbl['logL'][match]
mass_0 = 0.033
lum_0 = np.log10((mass_0/masses[0])**3.5 * 10**lums[0])
mass_f = 200 # extrapolate to 200 Msun...
lum_f = np.log10(10**lums[-1] * (mass_f/masses[-1])**1.35)

masses = np.array([mass_0] + masses.tolist() + [mass_f])
lums = np.array([lum_0] + lums.tolist() + [lum_f])
lums[0:2]
get_ipython().run_line_magic('run', 'mass_to_light.py')
imf.lum_of_cluster(cluster)
imf.lum_of_star(cluster)
#imf.lum_of_star(cluster)
cluster
imf.lum_of_star(cluster).max()
get_ipython().run_line_magic('run', 'mass_to_light.py')
get_ipython().run_line_magic('paste', '')
from astroquery.vizier import Vizier
Vizier.ROW_LIMIT = 1e7 # effectively infinite

# this query should cache
tbl = Vizier.get_catalogs('J/A+A/537/A146/iso')[0]

match = tbl['logAge'] == 6.5
masses = tbl['Mass'][match]
lums = tbl['logL'][match]
mass_0 = 0.033
lum_0 = np.log10((mass_0/masses[0])**3.5 * 10**lums[0])
mass_f = 200 # extrapolate to 200 Msun...
lum_f = np.log10(10**lums[-1] * (mass_f/masses[-1])**1.35)

masses = np.array([mass_0] + masses.tolist() + [mass_f])
lums = np.array([lum_0] + lums.tolist() + [lum_f])
tbl
########################################################
# Started Logging At: 2019-11-15 16:26:34
########################################################

########################################################
# # Started Logging At: 2019-11-15 16:26:34
########################################################
get_ipython().run_line_magic('run', 'mass_to_light.py')
########################################################
# Started Logging At: 2019-11-15 16:28:02
########################################################

########################################################
# # Started Logging At: 2019-11-15 16:28:02
########################################################
get_ipython().run_line_magic('run', '-i mass_to_light.py')
0.3**10
10**0.3
