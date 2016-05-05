"""
Created May 4, 2016

Produce a plot which represents the path of a satellite through the local sky.

@author: EP-Guy
"""

import matplotlib.pyplot as plt
import numpy as np


class SkyPlot:
    """A matplotlib plot axes for plotting stars and satellites on."""

    def __init__(self):
        self.ax, self.fig = self._init_plot()

    def _mapr(self, r):
        """Convert polar plot radius axis so 90 is at center."""
        if isinstance(r, list):
            return [90-x for x in r]
        else:
            return 90-r

    def _d2r(self, theta):
        """Convert from degrees to radians."""
        if isinstance(theta, list):
            return [t*np.pi/180 for t in theta]
        else:
            return theta*np.pi/180

    def _init_plot(self):
        """Initialize matplotlib plot figure."""

        # Turn off interactive plotting
        plt.ioff()

        # Create new figure and close so it's not displayed
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], projection='polar')

        ax.set_ylim(90, 0)
        ax.set_yticks(range(0, 90, 10))
        ax.set_yticklabels(list(map(str, range(90, 0, -10))))
        ax.set_theta_zero_location("N")

        return (ax, fig)

    def show(self):
        """Show plot."""
        plt.show()

    def add_points(self, az, alt):
        """Add azimuth(theta) and alt(r) points to plot in degrees.

        This function automatically applies mapr so that 90 deg is at zenith.
        """

        az = self._d2r(az)
        alt = self._mapr(alt)
        self.ax.plot(az, alt, marker='.', linestyle='none')


# ax.plot(theta, mapr(r), marker='.')
# theta = 2
# r = 44

# j = SkyPlot()
# j.add_points((theta, r))
# k = j.show()
