"""
Created May 4, 2016

Produce a plot which represents the path of a satellite through the local sky.

@author: EP-Guy
"""

import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import numpy as np
import collections


class SkyPlot:
    """A matplotlib plot axes for plotting stars and satellites on."""

    def __init__(self, plot_name):
        self.name = plot_name
        self.ax, self.fig = self._init_plot()

    @staticmethod
    def _mapr(r):
        """Convert polar plot radius axis so 90 is at center."""
        if isinstance(r, collections.Iterable):
            return [90-x for x in r]
        else:
            return 90-r

    @staticmethod
    def _d2r(theta):
        """Convert from degrees to radians."""
        if isinstance(theta, collections.Iterable):
            return [t*np.pi/180 for t in theta]
        else:
            return theta*np.pi/180

    @staticmethod
    def _mag2size(mag):
        """Return plot size for star of magnitude mag."""

        star_mag = [-1, 0, 1, 2, 3, 4]
        star_size = [128, 64, 32, 16, 8, 4]

        # interp returns 640 and 20 for < -1 and > 4
        markersize = np.interp(mag, star_mag, star_size)
        markersize = [ms for ms in markersize]

        return markersize

    def _init_plot(self):
        """Initialize matplotlib plot figure."""

        # Turn off interactive plotting
        plt.ioff()

        # Create new figure and close so it's not displayed
        fig = plt.figure(self.name, figsize=(10, 10))
        ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], projection='polar')

        ax.set_ylim(90, 0)
        # ax.set_yticks(range(0, 90, 10))
        # ax.set_yticklabels(list(map(str, np.arange(90, 0, -10))))
        # ax.set_yticklabels(['', '80', '', '60', '', '40', '', '20', ''])
        ax.tick_params(axis='y', which='major', labelsize=10)
        ax.set_rgrids(np.arange(0.00000001, 90, 10),
                      labels=list(map(str, np.arange(90, 0, -10))),
                      horizontalalignment='center')
        ax.set_rlabel_position(0)

        ax.set_theta_zero_location("N")
        theta_ticks = np.arange(0, 360, 10)
        theta_labels = list(map(str, np.arange(0, 360, 10)))
        theta_labels[0] = ''
        theta_labels[9] = ''
        theta_labels[18] = ''
        theta_labels[27] = ''
        ax.set_thetagrids(theta_ticks, theta_labels, fontsize=10, frac=1.05,
                          horizontalalignment='center')
        ax.xaxis.grid(False)
        ax.text(0, 95, 'N', fontsize=15, horizontalalignment='center',
                verticalalignment='center')
        ax.text(np.pi/2, 95, 'E', fontsize=15, horizontalalignment='center',
                verticalalignment='center')
        ax.text(np.pi, 95, 'S', fontsize=15, horizontalalignment='center',
                verticalalignment='center')
        ax.text(np.pi*3/2, 95, 'W', fontsize=15, horizontalalignment='center',
                verticalalignment='center')

        # ax.set_xticks(np.arange(0, 2*np.pi, np.pi/18))
        # theta_ticks = np.arange(0, 2*np.pi, np.pi/18)
        
        # ax.tick_params(axis='x', which='major', labelsize=10,
        #                tickdir='out')

        return (ax, fig)

    def show(self):
        """Show plot."""
        plt.figure(self.name)
        plt.show()

    def add_sat(self, az, alt, color='r'):
        """Add satellite location in az(theta)/alt(r) in degrees."""

        az = self._d2r(az)
        alt = self._mapr(alt)

        self.ax.plot(az, alt, color=color, ls='-', zorder=10)

    def add_sathighlight(self, az, alt, color='r'):
        """Add satellite location in az(theta)/alt(r) in degrees."""

        az = self._d2r(az)
        alt = self._mapr(alt)

        self.ax.plot(az, alt, color=color, ls='-', linewidth=6, zorder=10)

    def add_stars(self, az, alt, mag):
        """Add star location in az(theta)/alt(r) in degrees.

        Star size corresponds to magnitude.
        """

        az = self._d2r(az)
        alt = self._mapr(alt)

        size = self._mag2size(mag)
        size = [ss for ss in size]
        self.ax.scatter(az, alt, s=size, color='darkgray')

    def add_cons(self, az, alt, text):
        """Add constellation text at location az(theta)/alt(r) in degrees."""

        az = self._d2r(az)
        alt = self._mapr(alt)

        for z, a, t in zip(az, alt, text):
            self.ax.text(z, a, t, fontsize=10, color='gray', va='bottom',
                         path_effects=[pe.withStroke(linewidth=10,
                                                     foreground='w')])

    def save_fig(self, filename):
        """Save plot to file based on `filename` extension."""

        self.fig.savefig(filename)

    def close_fig(self):
        """Close open figure."""

        plt.close(self.fig)
