"""
Created May 4, 2016

Calculate satellite az/el in sky above observer using SkyField.

@author: EP-Guy
"""

import numpy as np
import pandas as pd

from skyfield.api import load

import SkyPlot

import matplotlib.pyplot as plt


class SatellitePass:
    """An object which contains the path of a satellite in an observer's sky.

    Observer is a tuple of strings (lat, lon).
    Time may be a list of datetime objects.
    """

    def __init__(self, observer, time_list):
        self.sat = None
        self.pos = []
        self.earth = self._createearth()
        self.ts = load.timescale()
        self.time = self._createdatearray(time_list)
        self.obs = self._createobs(observer)

    def _createearth(self):
        """Create SkyField earth object for efficiency."""
        eph = load('de421.bsp')
        return eph['earth']

    def _createdatearray(self, time_list):
        """Create SkyField date array from list of datetimes.

        Note: this does not properly handle leap seconds
        """
        return self.ts.utc(time_list)

    def _createobs(self, observer):
        """Create Earth topos object"""
        return self.earth.topos(observer[0], observer[1])

    def load_tle(self, tle_file):
        """Load a 3 line tle file of satellite orbit."""
        with open(tle_file, 'r') as fid:
            tle_str = fid.read()

        self.sat = self.earth.satellite(tle_str)

    def calc_pos(self):
        """Return apparent (alt, az, dist) of satellite above observer at time."""
        position = self.obs.at(self.time).observe(self.sat)
        self.pos = position.altaz()


path = r"E:\images\Satellites\Astro-H\2016-04-28\Astro-H_main\2016-04-28_T_05-21-35-0602_L_FITS\calibrated\cropped"
df = pd.read_csv(path+'/instrumental.csv', index_col=0, parse_dates=True)
sat = SatellitePass(('29.1879 N', '81.0483 W'), df.index.tz_localize('utc'))
sat.load_tle(r"E:\images\Satellites\Astro-H\2016-04-28\Astro-H_main\sat.tle")
sat.calc_pos()
alt, az, _ = sat.pos

p = SkyPlot.SkyPlot()
p.add_points(az.degrees, alt.degrees)
p.show()
