#! /usr/bin/env python

import os
import sys
import subprocess
import numpy as np
from datetime import datetime
import ephem
from collections import OrderedDict
import numpy
import json
import Cat3FGL



###### Main Script

# Change to root folder

root_folder = os.environ.get('BAR_ROOT')

quiet=False

if root_folder is None:
    if not quiet:
        print("No $BAR_ROOT set, exiting....")
    sys.exit(1)
    
try:
    os.chdir(root_folder)
except FileNotFoundError:
    if not quiet:
        print("{} does not exist, exiting...".format(root_folder))
    sys.exit(1)
except NotADirectoryError:
    if not quiet:
        print("{} is not a directory, exiting...".format(root_folder))
    sys.exit(1)


###########################################################################

# make Swift web page

# default out file is: "Swift_LCs.html"
res=subprocess.call("makeSwiftLCHTML.py -c -l 14", shell=True)

###########################################################################


###########################################################################

# check the LAT page for date of last update

LATLC_DATE_FILE="LATLC_last_update.txt"

try:
    with open(LATLC_DATE_FILE,"r") as f:
        last_update=f.readline()
except:
    last_update="never"

res=subprocess.check_output("getFermiLCobjects.py -m -q ", shell=True).decode('UTF-8')

#print(res.strip(), last_update.strip())

if res.strip()==last_update.strip():
    pass
else:
    with open(LATLC_DATE_FILE,"w") as f:
        f.write(res+'\n')


    print("going to work...")

    res=subprocess.call("makeLATLCSite.py &> makeLATLCSite.log",shell=True)

#    res=subprocess.call("makeLATLCSiteData.py > makeLATLCSiteData.log",shell=True)
#    print("makeLATLCSiteData.py",res)

#    res=subprocess.call("makeLATLCSiteHTML.py> makeLATLCSiteHTML.log",shell=True)
#    print("makeLATLCSiteHTML.py",res)

###########################################################################



 
