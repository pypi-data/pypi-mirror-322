########################################################
# Started Logging At: 2018-06-12 15:33:04
########################################################
########################################################
# # Started Logging At: 2018-06-12 15:33:04
########################################################
########################################################
# Started Logging At: 2018-06-12 15:45:09
########################################################

########################################################
# # Started Logging At: 2018-06-12 15:45:09
########################################################
get_ipython().magic('run mass_to_light.py')
get_ipython().magic('run mass_to_light.py')
get_ipython().magic('run mass_to_light.py')
get_ipython().magic('run mass_to_light.py')
pl.loglog()
get_ipython().magic('paste')
pl.figure(1).clf()
pl.plot(clusters.keys(), np.array(list(mean_luminosities.values()))/np.array(list(mean_masses.values())), ',')

mass_to_light = [mean_masses[k]/10**mean_luminosities[k] for k in sorted(clusters.keys())]

pl.figure(2).clf()
pl.plot(sorted(clusters.keys()), mass_to_light, ',')
get_ipython().magic('paste')
pl.figure(1).clf()
pl.loglog(clusters.keys(), np.array(list(mean_luminosities.values()))/np.array(list(mean_masses.values())), ',')

mass_to_light = [mean_masses[k]/10**mean_luminosities[k] for k in sorted(clusters.keys())]

pl.figure(2).clf()
pl.loglog(sorted(clusters.keys()), mass_to_light, ',')
get_ipython().system('ag --python max')
max_masses = {}
for clmass in clusters:
    max_masses[clmass] = np.max(clusters[clmass])
    
pl.figure(3).clf()
pl.loglog(max_masses.keys(), max_masses.values(), ',')
get_ipython().magic('paste')
pl.figure(1).clf()
pl.loglog(clusters.keys(), np.array(list(mean_luminosities.values()))/np.array(list(mean_masses.values())), '.', alpha=0.5)

mass_to_light = [mean_masses[k]/10**mean_luminosities[k] for k in sorted(clusters.keys())]

pl.figure(2).clf()
pl.loglog(sorted(clusters.keys()), mass_to_light, '.', alpha=0.5)


pl.figure(3).clf()
pl.loglog(max_masses.keys(), max_masses.values(), '.', alpha=0.5)
get_ipython().magic('paste')
pl.figure(1).clf()
pl.loglog(clusters.keys(), np.array(list(mean_luminosities.values()))/np.array(list(mean_masses.values())), '.', alpha=0.1)

mass_to_light = [mean_masses[k]/10**mean_luminosities[k] for k in sorted(clusters.keys())]

pl.figure(2).clf()
pl.loglog(sorted(clusters.keys()), mass_to_light, '.', alpha=0.1)


pl.figure(3).clf()
pl.loglog(max_masses.keys(), max_masses.values(), '.', alpha=0.1)
get_ipython().magic('paste')
mass_to_light = [mean_masses[k]/10**mean_luminosities[k] for k in sorted(clusters.keys())]

pl.figure(2).clf()
pl.loglog(sorted(clusters.keys()), mass_to_light, '.', alpha=0.1)
pl.xlabel("Cluster Mass")
pl.ylabel("Mass to Light Ratio")


pl.figure(3).clf()
pl.loglog(max_masses.keys(), max_masses.values(), '.', alpha=0.1)
pl.xlabel("Cluster Mass")
pl.ylabel("Maximum stellar mass")
mean_luminosities
get_ipython().magic('paste')
mass_to_light = np.array([mean_masses[k]/mean_luminosities[k] for k in sorted(clusters.keys())])

pl.figure(2).clf()
pl.loglog(sorted(clusters.keys()), mass_to_light**-1, '.', alpha=0.1)
pl.xlabel("Cluster Mass")
pl.ylabel("Light to Mass $L_\odot / M_\odot$")
pl.savefig("light_to_mass_vs_mass.pdf")


pl.figure(3).clf()
pl.loglog(max_masses.keys(), max_masses.values(), '.', alpha=0.1)
pl.xlabel("Cluster Mass")
pl.ylabel("Maximum stellar mass")
pl.savefig("maxmass_vs_clustermass.pdf")

#pl.loglog(clusters.keys(), np.array(list(mean_luminosities.values())) / np.array(list(mean_masses.values())), '.', alpha=0.1)
get_ipython().magic('paste')
mass_to_light = np.array([mean_masses[k]/mean_luminosities[k] for k in sorted(clusters.keys())])

pl.figure(2).clf()
pl.loglog(sorted(clusters.keys()), mass_to_light**-1, '.', alpha=0.1)
pl.xlabel("Cluster Mass")
pl.ylabel("Light to Mass $L_\odot / M_\odot$")
pl.ylim(6,25)
pl.savefig("light_to_mass_vs_mass.pdf")


pl.figure(3).clf()
pl.loglog(max_masses.keys(), max_masses.values(), '.', alpha=0.1)
pl.xlabel("Cluster Mass")
pl.ylabel("Maximum stellar mass")
pl.savefig("maxmass_vs_clustermass.pdf")

#pl.loglog(clusters.keys(), np.array(list(mean_luminosities.values())) / np.array(list(mean_masses.values())), '.', alpha=0.1)
get_ipython().magic('paste')
pl.figure(2).clf()
pl.loglog(sorted(clusters.keys()), mass_to_light**-1, '.', alpha=0.1)
pl.xlabel("Cluster Mass")
pl.ylabel("Light to Mass $L_\odot / M_\odot$")
pl.ylim(6,21)
pl.savefig("light_to_mass_vs_mass.pdf")


pl.figure(3).clf()
pl.loglog(max_masses.keys(), max_masses.values(), '.', alpha=0.1)
pl.xlabel("Cluster Mass")
pl.ylabel("Maximum stellar mass")
pl.savefig("maxmass_vs_clustermass.pdf")

#pl.loglog(clusters.keys(), np.array(list(mean_luminosities.values())) / np.array(list(mean_masses.values())), '.', alpha=0.1)
get_ipython().magic('paste')
pl.figure(2).clf()
pl.semilogx(sorted(clusters.keys()), mass_to_light**-1, '.', alpha=0.1)
pl.xlabel("Cluster Mass")
pl.ylabel("Light to Mass $L_\odot / M_\odot$")
pl.ylim(6,21)
pl.savefig("light_to_mass_vs_mass.pdf")
get_ipython().magic('run mass_to_light.py')
get_ipython().magic('run mass_to_light.py')
