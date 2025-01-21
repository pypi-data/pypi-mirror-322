########################################################
# Started Logging At: 2019-11-18 19:35:10
########################################################
########################################################
# # Started Logging At: 2019-11-18 19:35:11
########################################################
get_ipython().run_line_magic('matplotlib', 'inline')
import pylab as pl
from astropy import convolution
g_rand = np.random.randn([100,100])
pl.subplot(1,3,1).imshow(g_rand)
pl.subplot(1,3,2).imshow(convolution.convolve(g_rand,
                                              convolution.TopHat2DKernel(3)))
pl.subplot(1,3,3).imshow(convolution.convolve(g_rand,
                                              convolution.TopHat2DKernel(9)))
get_ipython().run_line_magic('matplotlib', 'inline')
import pylab as pl
from astropy import convolution
g_rand = np.random.randn(100,100)
pl.subplot(1,3,1).imshow(g_rand)
pl.subplot(1,3,2).imshow(convolution.convolve(g_rand,
                                              convolution.TopHat2DKernel(3)))
pl.subplot(1,3,3).imshow(convolution.convolve(g_rand,
                                              convolution.TopHat2DKernel(9)))
get_ipython().run_line_magic('matplotlib', 'inline')
import pylab as pl
from astropy import convolution
g_rand = np.random.randn(100,100)
pl.subplot(1,3,1).imshow(g_rand)
pl.subplot(1,3,2).imshow(convolution.convolve(g_rand,
                                              convolution.Tophat2DKernel(3)))
pl.subplot(1,3,3).imshow(convolution.convolve(g_rand,
                                              convolution.Tophat2DKernel(9)))
#[Out]# <matplotlib.image.AxesImage at 0xb15a4e6d8>
get_ipython().run_line_magic('matplotlib', 'inline')
import pylab as pl

from astropy import convolution
with plt.style.context({'xtick.bottom': False, 'ytick.left': False}):
    g_rand = np.random.randn(100,100)
    pl.subplot(1,3,1).imshow(g_rand)
    pl.subplot(1,3,2).imshow(convolution.convolve(g_rand,
                                                  convolution.Tophat2DKernel(3)))
    pl.subplot(1,3,3).imshow(convolution.convolve(g_rand,
                                                  convolution.Tophat2DKernel(9)))
get_ipython().run_line_magic('matplotlib', 'inline')
import pylab as pl

from astropy import convolution
with pl.style.context({'xtick.bottom': False, 'ytick.left': False}):
    g_rand = np.random.randn(100,100)
    pl.subplot(1,3,1).imshow(g_rand)
    pl.subplot(1,3,2).imshow(convolution.convolve(g_rand,
                                                  convolution.Tophat2DKernel(3)))
    pl.subplot(1,3,3).imshow(convolution.convolve(g_rand,
                                                  convolution.Tophat2DKernel(9)))
get_ipython().run_line_magic('matplotlib', 'inline')
import pylab as pl

from astropy import convolution
with pl.style.context({'xtick.labelbottom': False,
                       'ytick.labelleft': False}):
    g_rand = np.random.randn(100,100)
    pl.subplot(1,3,1).imshow(g_rand)
    pl.subplot(1,3,2).imshow(convolution.convolve(g_rand,
                                                  convolution.Tophat2DKernel(3)))
    pl.subplot(1,3,3).imshow(convolution.convolve(g_rand,
                                                  convolution.Tophat2DKernel(9)))
get_ipython().run_line_magic('matplotlib', 'inline')
import pylab as pl

from astropy import convolution
with pl.style.context({'xtick.labelbottom': False,
                       'xtick.bottom': False,
                       'ytick.bottom': False,
                       'ytick.labelleft': False}):
    g_rand = np.random.randn(100,100)
    pl.subplot(1,3,1).imshow(g_rand)
    pl.subplot(1,3,2).imshow(convolution.convolve(g_rand,
                                                  convolution.Tophat2DKernel(3)))
    pl.subplot(1,3,3).imshow(convolution.convolve(g_rand,
                                                  convolution.Tophat2DKernel(9)))
get_ipython().run_line_magic('matplotlib', 'inline')
import pylab as pl

from astropy import convolution
with pl.style.context({'xtick.labelbottom': False,
                       'xtick.bottom': False,
                       'ytick.keft': False,
                       'ytick.labelleft': False}):
    g_rand = np.random.randn(100,100)
    pl.subplot(1,3,1).imshow(g_rand)
    pl.subplot(1,3,2).imshow(convolution.convolve(g_rand,
                                                  convolution.Tophat2DKernel(3)))
    pl.subplot(1,3,3).imshow(convolution.convolve(g_rand,
                                                  convolution.Tophat2DKernel(9)))
get_ipython().run_line_magic('matplotlib', 'inline')
import pylab as pl

from astropy import convolution
with pl.style.context({'xtick.labelbottom': False,
                       'xtick.bottom': False,
                       'ytick.left': False,
                       'ytick.labelleft': False}):
    g_rand = np.random.randn(100,100)
    pl.subplot(1,3,1).imshow(g_rand)
    pl.subplot(1,3,2).imshow(convolution.convolve(g_rand,
                                                  convolution.Tophat2DKernel(3)))
    pl.subplot(1,3,3).imshow(convolution.convolve(g_rand,
                                                  convolution.Tophat2DKernel(9)))
get_ipython().run_line_magic('matplotlib', 'inline')
import pylab as pl
from astropy.convolution import convolve, Tophat2DKernel
with pl.style.context({'xtick.labelbottom': False,
                       'xtick.bottom': False,
                       'ytick.left': False,
                       'ytick.labelleft': False}):
    g_rand = np.random.randn(100,100)
    pl.subplot(1,3,1).imshow(g_rand)
    pl.subplot(1,3,2).imshow(convolve(g_rand,
                                      Tophat2DKernel(3)))
    pl.subplot(1,3,3).imshow(convolve(g_rand,
                                      Tophat2DKernel(9)))
from scipy.special import erfc
pl.plot(0.5 * erfc(np.logspace(-2,2))
from scipy.special import erfc
pl.plot(0.5 * erfc(np.logspace(-2,2)))
#[Out]# [<matplotlib.lines.Line2D at 0xb15db2978>]
from scipy.special import erfc
pl.plot(0.5 * erfc(np.linspace(-2,2)))
#[Out]# [<matplotlib.lines.Line2D at 0xb15e06be0>]
from scipy.special import erfc
pl.plot(0.5 * erfc(np.logspace(-2,1)))
#[Out]# [<matplotlib.lines.Line2D at 0xb15c8dfd0>]
from scipy.special import erfc
pl.plot(np.logspace(-2, 1),
        0.5 * erfc(np.logspace(-2,1)))
#[Out]# [<matplotlib.lines.Line2D at 0xb159f73c8>]
from scipy.special import erfc
pl.loglog(np.logspace(-2, 1),
        0.5 * erfc(np.logspace(-2,1)))
#[Out]# [<matplotlib.lines.Line2D at 0xb15ca4c50>]
from scipy.special import erfc
pl.semilogx(np.logspace(-2, 1),
        0.5 * erfc(np.logspace(-2,1)))
#[Out]# [<matplotlib.lines.Line2D at 0x1076dc240>]
from scipy.special import erf
pl.semilogx(np.logspace(-2, 1),
        0.5 * erf(np.logspace(-2,1)))
#[Out]# [<matplotlib.lines.Line2D at 0xb1583c898>]
Plugging that in above, we get:
$$n(M) dM = 
\sqrt{\frac{2}{\pi}}
\frac{\rho_{M,0}}{M^2}
\frac{\delta_c}{\sigma(M)}
\left| \frac{d \ln \sigma}{d\ln M} \right|
\exp\left(\frac{\delta_c^2}{2\sigma^2{M}}\right)
dM$$
