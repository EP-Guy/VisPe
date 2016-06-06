"""
Created May 4, 2016

Calculate satellite az/el in sky above observer using SkyField.

@author: EP-Guy
"""

import numpy as np
import pandas as pd

from skyfield.api import load

import matplotlib.pyplot as plt

from . import SkyPlot
from . import Observation
from . import Star
from . import Constellation


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
