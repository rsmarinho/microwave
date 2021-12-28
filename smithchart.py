import matplotlib.pyplot as plt
import numpy as np

class smith:
    """
    Simple Smith Chart drawing.
    """

    def __init__(self, Z0=50, size=8.0):
        """
        Creates the figure and draws the grid.
        Z0: characteristic impedance
        """
        plt.ioff()
        self.Z0=Z0
        self.fig = plt.figure(figsize=(size, size))
        plt.axes().set_axis_off()
        self.drawGrid()

    def show(self):
        """
        Shows the plot. The plot can't be updated after it has been
        closed.
        """
        plt.figure(self.fig.number)
        plt.show()

    def save(self, filename):
        """
        Saves the plot to filename. The extension defines the filetype.
        """
        self.fig.savefig(filename)

    def markZ(self, z, text=None, c='b', ms=1):
        """
        Marks an impedance with a dot.
        """
        plt.figure(self.fig.number)
        g = self.z2gamma(z)
        plt.plot(g.real, g.imag, 'o'+c, ms=ms)
        if text:
            plt.text(g.real+0.02, g.imag+0.02, text, color=c, weight='demi')
        plt.draw()

    def drawGammaMark(self, l, text=None, c='b', ms=1):
        """
        RSM - mark gamma
        """
        plt.figure(self.fig.number)
        plt.plot(l.real, l.imag, 'o'+c, ms=ms)
        if text:
            plt.text(l.real+0.02, l.imag+0.02, text, color=c, weight='demi')
        plt.draw()

    def drawZList(self, l, c='b', lw=3):
        """
        Draws a list of impedances on the chart and connects them by lines. 
        To get a closed contour, the last impedance should be the same as the 
        first one. Use color c for the drawing.
        """
        plt.figure(self.fig.number)
        xlst = self.z2gamma(l).real
        ylst = self.z2gamma(l).imag
        plt.plot(xlst, ylst, c, lw=lw)
        plt.draw()

    def drawGammaList(self, l, c='b', lw=3):
        """
        RSM - draw gamma list
        """
        plt.figure(self.fig.number)
        xlst = l.real
        ylst = l.imag
        plt.plot(xlst, ylst, c, lw=lw)
        plt.draw()

    def drawXCircle(self, x, npts=200):
        """
        Draws a circle with constant real part.
        """
        zlst = np.hstack((np.array([x]), np.array([x+1j*z for z in np.logspace(-6, 6, npts)])))
        self.drawZList(zlst, 'k', lw=0.5)
        zlst = np.hstack((np.array([x]), np.array([x-1j*z for z in np.logspace(-6, 6, npts)])))
        self.drawZList(zlst, 'k', lw=0.5)

    def drawYCircle(self, y, npts=200):
        """
        Draws a circle with constant imaginary part.
        """
        zlst = np.hstack((np.array([0+1j*y]), np.array([z+1j*y for z in np.logspace(-6, 6, npts)])))
        self.drawZList(zlst, 'k', lw=0.5)

    def z2gamma(self, zl):
        """
        Converts an impedance to a reflection coefficient.
        """
        return ((zl-self.Z0)/(zl+self.Z0))

    def drawGrid(self):
        """
        Draws the Smith Chart grid.
        """
        self.drawXCircle(0)
        self.drawXCircle(self.Z0/5)
        self.drawXCircle(self.Z0/2)
        self.drawXCircle(self.Z0)
        self.drawXCircle(self.Z0*2)
        self.drawXCircle(self.Z0*5)
        
        self.drawYCircle(0)
        self.drawYCircle(self.Z0/5)
        self.drawYCircle(-self.Z0/5)
        self.drawYCircle(self.Z0/2)
        self.drawYCircle(-self.Z0/2)
        self.drawYCircle(self.Z0)
        self.drawYCircle(-self.Z0)
        self.drawYCircle(self.Z0*2)
        self.drawYCircle(-self.Z0*2)
        self.drawYCircle(self.Z0*5)
        self.drawYCircle(-self.Z0*5)