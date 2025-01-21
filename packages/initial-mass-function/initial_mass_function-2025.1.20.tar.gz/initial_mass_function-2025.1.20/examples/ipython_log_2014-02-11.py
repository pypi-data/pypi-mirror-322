########################################################
# Started Logging At: 2014-02-11 11:33:22
########################################################

########################################################
# # Started Logging At: 2014-02-11 11:33:25
########################################################
import imf
get_ipython().magic(u'pinfo imf.imf')
get_ipython().magic(u'pinfo imf.imf.make_cluster')
imf.imf.make_cluster(800)
peaks = [imf.imf.make_cluster(800).max() for ii in range(1000)]
min(peaks)
max(peaks)
peaks = [imf.imf.make_cluster(800).max() for ii in range(10000)]
min(peaks)
sort(peaks)
(sort(peaks)-12).argmin()
abs(sort(peaks)-12).argmin()
40/1e5
abs(sort(peaks)-20).argmin()
816/1e5
