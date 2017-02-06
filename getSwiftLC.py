#! /usr/bin/env python

import sys

###############################################################################

import argparse

desc="""
Download Swift lightcurve and rename it for a given source.
Any existing file called ligtcurve.txt will be removed in the process.
"""

parser = argparse.ArgumentParser(description=desc, 
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('-n','--name',type=str, default="", required=True, 
                    help="Name of object to be downloaded")

cfg = parser.parse_args()

###############################################################################


import SwiftLC

sd=SwiftLC.SwiftLC()

sd.download(cfg.name)



