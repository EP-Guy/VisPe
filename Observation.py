"""
Created May 13, 2016

Observation object for calculating satellite and star positions using SkyField.

@author: EP-Guy
"""

import numpy as np
import pandas as pd

from skyfield.api import load


class Observation:
    """Observation object for times and positions of an observer.

    Observer is a tuple of strings (lat, lon).
    Time may be a list of datetime objects.
    """

    def __init__(self, observer, time_list):
        self.earth = self._createearth()
        self.ts = load.timescale()
        self.time = self._createdatearray(time_list)
        self.obs = self._createobs(observer)

    @staticmethod
    def _createearth():
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
