"""
Created May 13, 2016

Star object for plotting in SkyPlot.

@author: EP-Guy
"""

import numpy as np
import pandas as pd
import struct

import skyfield.api
from skyfield.units import Angle
from astropy import units as u


class Star:
    """Star object for plotting in SkyPlot.

    observation must be an Observation object.

    Note: No conversion is made between B1950 BSC and ICRS SkyField coords.
    Star positions should not be used without proper conversion between systems.
    """

    def __init__(self, observation):
        self.obsv = observation
        self.catnum = []
        self.sstar = []
        self.mag = []
        
    @staticmethod
    def mid_obstime(obstimes):
    	"""Return obstime at middle of presorted obstimes array."""
    	
    	midpt = len(obstimes)//2
    	
    	return obstimes[midpt]

    def load_bsc(self, star_file):
        """Load Yale bright star catalog (binary)."""

        def _num_datagrams(data):
            """Number of 32 byte data instances in file."""
            assert len(data) % 32 == 0

            return int(len(data) / 32)

        with open(star_file, mode='rb') as file:
            file_header = file.read(28)
            file_content = file.read()

        header = struct.unpack('>iiii4?ii', file_header)
        print(header)

        catid = []
        skyfield_star = []
        vmag = []

        for index in range(_num_datagrams(file_content)):
            offset = index * 32
            dat = struct.unpack('>fdd2chff', file_content[offset:offset+32])

            # Create Skyfield Star instance
            ra_hms = Angle(radians=dat[1]).hms(warn=False)
            dec_dms = Angle(radians=dat[2]).dms()
            ra_mas_py = Angle(radians=dat[6]).to(u.mas).value
            dec_mas_py = Angle(radians=dat[7]).to(u.mas).value

            ss = skyfield.api.Star(ra_hours=ra_hms, dec_degrees=dec_dms,
                                   ra_mas_per_year=ra_mas_py,
                                   dec_mas_per_year=dec_mas_py)

            catid.append(dat[0])
            skyfield_star.append(ss)
            vmag.append(dat[5]/100.)

        self.catnum = catid
        self.sstar = skyfield_star
        self.mag = vmag

    def return_vis_stars(obstime, limiting_mag=4):
        """Return stars visible at time t from observation location down to
        limiting_mag."""
        
        # Check elevation at time t
        catid, skyfield_star, vmag = [c, s, v for c, s, v in
                                      zip(catid, skyfield_star, vmag) if
                                      self.obsv.obs.at(obstime).observe(s).altaz()[0] > 5]

		# Check limiting magnitude
        catid, skyfield_star, vmag = [c, s, v for c, s, v in
                                      zip(self.catnum, self.sstar, self.mag) if
                                      v <= limiting_mag]
                                      
        return (catid, skyfield_star, vmag)           
        
	def return_star_altaz(obstime, skyfield_stars):
		"""Return star (alt, az) at obstime."""
		
		alt = []
		az = []
		for s in skyfield_stars:
			a, z, d = self.obsv.obs.at(obstime).observe(s).apparent().altaz()
			alt.append(a)
			az.append(z)
		
		return (alt, az)
