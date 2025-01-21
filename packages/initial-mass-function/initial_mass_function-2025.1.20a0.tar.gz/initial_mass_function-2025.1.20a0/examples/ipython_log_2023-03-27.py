########################################################
# Started Logging At: 2023-03-27 11:07:16
########################################################

########################################################
# # Started Logging At: 2023-03-27 11:07:17
########################################################
pl.rcParams['font.size'] = 14
pl.rcParams['figure.dpi'] = 150
fig = pl.figure(figsize=(10,6))
ax1 = pl.subplot(1,2,1)
pl.semilogx(masses, kr)
pl.xlabel("Stellar Mass")
pl.ylabel("Cumulative Probability");
ax2 = pl.subplot(1,2,2)
#pl.scatter(10, 0.5, marker='o')
pl.xlim(0.03, 120)
pl.ylim(0,1)
pl.semilogx();
pl.xlabel("Mass")
pl.yticks([])
target_mass = 50
txt2 = ax2.text(10, 0.95, f"$M_{{tgt}}={target_mass}$")

txt = ax2.text(10, 0.9, "$M_{tot}=0$")
masslist = []

mfc = imf.Kroupa()
expected_mass = mfc.m_integrate(mfc.mmin, mfc.mmax)[0]
nstars = target_mass / expected_mass
#print(nstars)
pp = np.linspace(0, 1-1/int(nstars), int(nstars))[::-1]

def animate(n):

    mtot = np.sum(masslist)

    if mtot < target_mass:

        if len(ax1.lines) > 1:
            for line in ax1.lines[1:]:
                ax1.lines.remove(line)
        
        ppi = pp[n]
        mass = mfc.distr.ppf(ppi)
        #print(ppi, n, mass)
        
        masslist.append(mass)
        
        mtot = np.sum(masslist)

        ax1.axhline(ppi, color='k', linewidth=0.5)
        ax1.axvline(mass, color='k', linewidth=0.5)
        ax2.scatter(mass, np.random.rand())

        txt.set_text(f'$M_{{tot}}={mtot:0.1f}$')

    return fig,     

anim = animation.FuncAnimation(fig, animate, frames=int(nstars)+10, repeat_delay=5000,
                              interval=50)
anim.save('cluster_population_animation_odf.mp4')
get_ipython().run_line_magic('run', 'clustermf_figure.py')
colors
np.array(colors)
np.array(colors).max()
get_ipython().run_line_magic('run', 'clustermf_figure.py')
