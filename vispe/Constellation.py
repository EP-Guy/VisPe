# -*- coding: utf-8 -*-
"""
Created on Mon May 30 15:51:22 2016

Constellation object.

@author: Forrest
"""

import numpy as np
import pandas as pd
import struct

import skyfield.api
from skyfield.units import Angle
from astropy import units as u
import csv

class Constellation:
    """Constellation object which holds constellation name, abbreviation, and
    RA/DEC for plotting."""

    def __init__(self, observation, obstime, file):
        self.obsv = observation
        self.obstime = obstime
        self.file = file
        self.abbrv = []
        self.name = []
        self.ra = []
        self.dec = []
        self.star = []

        self._read_csv()
        self._create_star_objs()

    def _read_csv(self):
        """Read csv file of constellation info into Constellation object."""

        with open(self.file) as f:
            reader = csv.reader(filter(lambda row: row[0] != '#', f))
            for row in reader:
                self.abbrv.append(row[0])
                self.name.append(row[1])
                self.ra.append(row[2])
                self.dec.append(row[3])

    def _create_star_objs(self):
        """Create star objs for each Constellation for calc of alt/az."""

        ra = [r.split() for r in self.ra]
        dec = [d.split() for d in self.dec]

        self.star = [skyfield.api.Star(ra_hours=(float(r[0]), float(r[1])),
                                       dec_degrees=(float(d[0]), float(d[1])))
                     for r, d in zip(ra, dec)]

    def return_vis_constellations(self):
        """Return constellations visible at obstime from obsv location."""

        obscon = self.obsv.obs.at(self.obstime)
        cons_dat = zip(self.abbrv, self.name, self.ra, self.dec, self.star)

        # Check elevation at time t
        new_cons_dat = [(ab, na, ra, de, st) for ab, na, ra, de, st in cons_dat
                        if obscon.observe(st).apparent().altaz()[0].degrees > 5]

        return zip(*new_cons_dat)

    def return_cons_altaz(self, skyfield_stars):
        """Return constellation (alt, az) at obstime."""

        alt = []
        az = []
        for s in skyfield_stars:
            a, z, d = self.obsv.obs.at(self.obstime).observe(s).apparent().altaz()
            alt.append(a.degrees)
            az.append(z.degrees)

        return (alt, az)
