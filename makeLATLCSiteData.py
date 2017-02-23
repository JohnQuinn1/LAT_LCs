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


###########################################################################

# download LAT list

LC_File="LATLC_objects.txt"
DEC_min=32-40
DEC_max=32+40
RA_window=9
z_min=0
z_max=1.5
command="getFermiLCobjects.py -f {} -d {} {} -w {} -z {} {} -q".format(LC_File, 
                                                                       DEC_min, 
                                                                       DEC_max, 
                                                                       RA_window, 
                                                                       z_min, 
                                                                       z_max)

#print(command)
res=subprocess.call(command, shell=True)
#print(res)

###########################################################################

# load txt file and extract names etc...

#LC_File="all_extragalactic.txt"

#objects=OrderedDict()

objects={}

with open(LC_File,"r") as f:
    for line in f:
        fields=line.split(",")
        object=fields[0].replace(" ","")
        objects[object]={'name':fields[0],
                         'LAT_URL':fields[1],
                         'RA':fields[2], 
                         'Dec':fields[3], 
                         'z':fields[4]} 
        
#print(objects)
        

###########################################################################

# Loop over each object...

import map_name
import glob

import SwiftLC
SLC=SwiftLC.SwiftLC(quiet=True)


for object in objects:
    print("*"*40)
    print(object)

    # if directory does not exist make it
    if not os.path.isdir(object):
        if os.path.isfile(object):
            os.remove(object)
        os.mkdir(object)

    os.chdir(object)

    for lc_file in glob.glob("*.lc"):
        os.remove(lc_file)

    for png_file in glob.glob("*.png"):
        os.remove(png_file)


    #### 3FGL:

    LAT3FGL=Cat3FGL.Cat3FGL()

    if not LAT3FGL.select_object(object):
        objects[object]['3FGL_spec_type']=""
        objects[object]['3FGL_PL_index']="{:.2f}".format(-1)
        objects[object]['3FGL_flux_100']=-1
        objects[object]['3FGL_flux_1000']=-1
        objects[object]['3FGL_flux_gt200GeV']=-1
        objects[object]['3FGL_frac_gt200GeV']=-1
    else:
        objects[object]['3FGL_spec_type']=LAT3FGL.get_SpectrumType()
        if objects[object]['3FGL_spec_type']=="PowerLaw":
            objects[object]['3FGL_PL_index']="{:.2f}".format(LAT3FGL.get_field('Spectral_Index'))
            objects[object]['3FGL_flux_100']=LAT3FGL.calc_PL_int_flux(100,300000)
            objects[object]['3FGL_flux_1000']=LAT3FGL.calc_PL_int_flux(1000,300000)
            objects[object]['3FGL_flux_gt200GeV']=LAT3FGL.calc_PL_int_flux(2e5,2e7)
            objects[object]['3FGL_frac_gt200GeV']=LAT3FGL.calc_PL_int_flux(2e5,2e7)/2.36e-10
        else:
            objects[object]['3FGL_PL_index']=""
            objects[object]['3FGL_flux_100']=LAT3FGL.calc_int_flux(100,300000)
            objects[object]['3FGL_flux_1000']=LAT3FGL.calc_int_flux(1000,300000)
            objects[object]['3FGL_flux_gt200GeV']=LAT3FGL.calc_int_flux(2e5,2e7)
            objects[object]['3FGL_frac_gt200GeV']=LAT3FGL.calc_int_flux(2e5,2e7)/2.36e-10
    

#    print(objects[object])

    ##### Swift:

    Swift_LC_file=SLC.download(object)
    if Swift_LC_file is not None:
        swift_name=map_name.map_name(object,"Swift_LC")
        objects[object]['Swift_URL']='http://www.swift.psu.edu/monitoring/source.php?source={}'.format(swift_name)
        print(object,'http://www.swift.psu.edu/monitoring/source.php?source={}'.format(swift_name))
    else:
        print(object, "Swift LC not found!")
        objects[object]['Swift_URL']=''


    ## Needs to either turn off check_output throwin exception with a non=zer return code 
    ## or else catch and handle

    # Daily 100 MeV to 300 GeV
    command="plotFermiLC.py -A -a -n {} -e {} -q -N -F -R".format(object, "FLUX_100_300000")
    if Swift_LC_file: command+=" -S {}".format(Swift_LC_file)
    root_filename=subprocess.check_output(command, shell=True).decode('utf-8').strip()
    objects[object]['filename_100_daily']=root_filename
    data=np.loadtxt(root_filename+".txt")[-1,:]
    objects[object]['last_100_daily']=data.tolist()


    # Daily 1 GeV to 300 GeV
    command="plotFermiLC.py -A -a -n {} -e {} -q -N -F -R".format(object, "FLUX_1000_300000")   
    if Swift_LC_file: command+=" -S {}".format(Swift_LC_file)
    root_filename=subprocess.check_output(command, shell=True).decode('utf-8').strip()
    objects[object]['filename_1000_daily']=root_filename
    data=np.loadtxt(root_filename+".txt")[-1,:]
    objects[object]['last_1000_daily']=data.tolist()


    # Weekly 100 MeV to 300 GeV
    command="plotFermiLC.py -A -a -n {} -e {} -q -N -w -F -R".format(object, "FLUX_100_300000")
    if Swift_LC_file: command+=" -S {}".format(Swift_LC_file)
    root_filename=subprocess.check_output(command, shell=True).decode('utf-8').strip()
    objects[object]['filename_100_weekly']=root_filename
    data=np.loadtxt(root_filename+".txt")[-1,:]
    objects[object]['last_100_weekly']=data.tolist()


    # Weekly 1 GeV to 300 GeV
    command="plotFermiLC.py -A -a -n {} -e {} -q -N -w -F -R".format(object, "FLUX_1000_300000")   
    if Swift_LC_file: command+=" -S {}".format(Swift_LC_file)
    root_filename=subprocess.check_output(command, shell=True).decode('utf-8').strip()
    objects[object]['filename_1000_weekly']=root_filename    
    data=np.loadtxt(root_filename+".txt")[-1,:]
    objects[object]['last_1000_weekly']=data.tolist()


    os.chdir("..")



print(json.dumps(objects, sort_keys=True, indent=4, separators=(',', ': ')))
with open("LATLC_data.json","w") as f:
    f.write(json.dumps(objects))
