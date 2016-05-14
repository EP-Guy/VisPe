"""
Created May 13, 2016

Star object for plotting in SkyPlot.

@author: EP-Guy
"""

import numpy as np
import pandas as pd
import struct


class Star:
    """Star object for plotting in SkyPlot.

    observation must be an Observation object.
    """

    def __init__(self, observation):
        self.obsv = observation

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
        ra = []
        dec = []
        spectype = []
        vmag = []
        rapm = []
        decpm = []

        for index in range(_num_datagrams(file_content)):
            offset = index * 32
            dat = struct.unpack('>fdd2chff', file_content[offset:offset+32])

        print(dat)
