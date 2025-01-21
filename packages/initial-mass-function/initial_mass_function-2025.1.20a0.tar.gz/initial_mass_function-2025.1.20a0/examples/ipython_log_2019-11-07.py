########################################################
# Started Logging At: 2019-11-07 18:30:48
########################################################

########################################################
# # Started Logging At: 2019-11-07 18:30:49
########################################################
get_ipython().run_line_magic('run', 'pmf_comparison.py')
get_ipython().run_line_magic('pl.rc', "('line', width=2)")
pl.rc('line', width=2)
pl.rc('font', size=16)
pl.rc('font', size=16)
pl.rc('pl.rc('lines', linewidth=2)font', size=16)
pl.rc('lines', linewidth=2)
pl.draw(); pl.show()
pl.rc('lines', linewidth=3)
pl.draw(); pl.show()
pl.draw(); pl.show()
get_ipython().run_line_magic('paste', '')
fig3 = pl.figure(3)
fig3.clf()
ax3 = fig3.gca()
ax3.set_title("Steady State McKee/Offner + Kroupa PMF")
ax3.loglog(masses, kroupa.__getattribute__(fname)(masses), label="IMF", color='k')
ax3.loglog(masses, KroupaPMF_IS.__getattribute__(fname)(masses), label="IS", color='r', linestyle=':')
ax3.loglog(masses, KroupaPMF_TC.__getattribute__(fname)(masses), label="TC", color='g', linestyle='-.')
ax3.loglog(masses, KroupaPMF_CA.__getattribute__(fname)(masses), label="CA", color='y', linestyle='-.')
ax3.loglog(masses, KroupaPMF_2CTC.__getattribute__(fname)(masses), label="2CTC", color='b', linestyle='--')
ax3.set_xlabel("(Proto)Stellar Mass (M$_\odot$)")
ax3.set_ylabel("m P(m)" if mass_weighted else "Normalized P(M)")
ax3.axis([mmin, mmax, 1e-4, 1])

pl.legend(loc='best')
pl.savefig('steadystate_pmf_kroupa{0}_mmax{1}.png'.format("_integral" if mass_weighted else "",
                                                          int(mmax)), bbox_inches='tight')
get_ipython().run_line_magic('pinfo', 'ax3.set_title')
ax3.set_title("Steady State McKee/Offner + Kroupa PMF")
ax3.set_title("Steady State McKee/Offner + Kroupa PMF", pad=0.1)
ax3.set_title("Steady State McKee/Offner + Kroupa PMF", pad=0.5)
ax3.set_title("Steady State McKee/Offner + Kroupa PMF", pad=2)
ax3.set_title("Steady State McKee/Offner + Kroupa PMF", pad=20)
ax3.set_title("Steady State McKee/Offner + Kroupa PMF", pad=10)
get_ipython().run_line_magic('paste', '')
fig3 = pl.figure(3)
fig3.clf()
ax3 = fig3.gca()
ax3.set_title("Steady State McKee/Offner + Kroupa PMF", pad=12)
ax3.loglog(masses, kroupa.__getattribute__(fname)(masses), label="IMF", color='k')
ax3.loglog(masses, KroupaPMF_IS.__getattribute__(fname)(masses), label="IS", color='r', linestyle=':')
ax3.loglog(masses, KroupaPMF_TC.__getattribute__(fname)(masses), label="TC", color='g', linestyle='-.')
ax3.loglog(masses, KroupaPMF_CA.__getattribute__(fname)(masses), label="CA", color='y', linestyle='-.')
ax3.loglog(masses, KroupaPMF_2CTC.__getattribute__(fname)(masses), label="2CTC", color='b', linestyle='--')
ax3.set_xlabel("(Proto)Stellar Mass (M$_\odot$)")
ax3.set_ylabel("m P(m)" if mass_weighted else "Normalized P(M)")
ax3.axis([mmin, mmax, 1e-4, 1])

pl.legend(loc='best')
pl.savefig('steadystate_pmf_kroupa{0}_mmax{1}.png'.format("_integral" if mass_weighted else "",
                                                          int(mmax)), bbox_inches='tight')
pl.savefig('steadystate_pmf_kroupa{0}_mmax{1}.pdf'.format("_integral" if mass_weighted else "",
                                                          int(mmax)), bbox_inches='tight')
                                                  
get_ipython().run_line_magic('paste', '')
fig3 = pl.figure(3)
fig3.clf()
ax3 = fig3.gca()
ax3.set_title("Steady State McKee/Offner + Kroupa PMF", pad=15)
ax3.loglog(masses, kroupa.__getattribute__(fname)(masses), label="IMF", color='k')
ax3.loglog(masses, KroupaPMF_IS.__getattribute__(fname)(masses), label="IS", color='r', linestyle=':')
ax3.loglog(masses, KroupaPMF_TC.__getattribute__(fname)(masses), label="TC", color='g', linestyle='-.')
ax3.loglog(masses, KroupaPMF_CA.__getattribute__(fname)(masses), label="CA", color='y', linestyle='-.')
ax3.loglog(masses, KroupaPMF_2CTC.__getattribute__(fname)(masses), label="2CTC", color='b', linestyle='--')
ax3.set_xlabel("(Proto)Stellar Mass (M$_\odot$)")
ax3.set_ylabel("m P(m)" if mass_weighted else "Normalized P(M)")
ax3.axis([mmin, mmax, 1e-4, 1])

pl.legend(loc='best')
pl.savefig('steadystate_pmf_kroupa{0}_mmax{1}.png'.format("_integral" if mass_weighted else "",
                                                          int(mmax)), bbox_inches='tight')
pl.savefig('steadystate_pmf_kroupa{0}_mmax{1}.pdf'.format("_integral" if mass_weighted else "",
                                                          int(mmax)), bbox_inches='tight')
ax3.set_xlabel("(Proto)Stellar Mass $(\\textrm{M}_\odot)$")
ax3.set_xlabel("(Proto)Stellar Mass $(\\mathrm{M}_\odot)$")
ax3.set_xlabel("(Proto)Stellar Mass $\\left(\\mathrm{M}_\odot\\right)$")
ax3.set_xlabel("(Proto)Stellar Mass $\\left(\\mathrm{M}_\odot\\right)$")
pl.savefig('steadystate_pmf_kroupa{0}_mmax{1}.png'.format("_integral" if mass_weighted else "",
                                                          int(mmax)), bbox_inches='tight')
                                                          pl.savefig('steadystate_pmf_kroupa{0}_mmax{1}.pdf'.format("_integral" if mass_weighted else "",
                                                                                                                    int(mmax)), bbox_inches='tight')
                                                                                                                    
get_ipython().run_line_magic('padste', '')
get_ipython().run_line_magic('paste', '')
pl.savefig('steadystate_pmf_kroupa{0}_mmax{1}.png'.format("_integral" if mass_weighted else "",
                                                          int(mmax)), bbox_inches='tight')
pl.savefig('steadystate_pmf_kroupa{0}_mmax{1}.pdf'.format("_integral" if mass_weighted else "",
                                                          int(mmax)), bbox_inches='tight')
