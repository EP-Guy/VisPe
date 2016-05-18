"""
Created May 4, 2016

Calculate satellite az/el in sky above observer using SkyField.

@author: EP-Guy
"""

import numpy as np
import pandas as pd

from skyfield.api import load

import matplotlib.pyplot as plt

import SkyPlot
from Observation import Observation
from Star import Star


class SatellitePass:
    """An object which contains the path of a satellite in an observer's sky.

    observation must be an Observation object.
    """

    def __init__(self, observation):
        self.sat = None
        self.obsv = observation
        self.pos = []

    def load_tle(self, tle_file):
        """Load a 3 line tle file of satellite orbit."""
        with open(tle_file, 'r') as fid:
            tle_str = fid.read()

        self.sat = self.obsv.earth.satellite(tle_str)

    def calc_pos(self):
        """Return apparent (alt, az, dist) of satellite above observer at time."""
        position = self.obsv.obs.at(self.obsv.time).observe(self.sat)
        self.pos = position.altaz()


path = r"E:\images\Satellites\Astro-H\2016-04-28\Astro-H_main\2016-04-28_T_05-21-35-0602_L_FITS\calibrated\cropped"
df = pd.read_csv(path+'/instrumental.csv', index_col=0, parse_dates=True)
dtimes = df.index.tz_localize('utc')
obs = Observation(('29.1879 N', '81.0483 W'), dtimes)
sat = SatellitePass(obs)
sat.load_tle(r"E:\images\Satellites\Astro-H\2016-04-28\Astro-H_main\sat.tle")
sat.calc_pos()
alt, az, _ = sat.pos

s = Star(obs)
s.load_bsc(r'C:\Users\Forrest\Downloads\BSC5ra')
midtime = Star.midobstime(dtimes)
catid, stars, mag = s.return_vis_stars(midtime)
alt, az = s.return_star_altaz(midtime, stars)

p = SkyPlot.SkyPlot()
p.add_sat(az.degrees, alt.degrees)
p.add_stars(az, alt, mag)
p.show()
