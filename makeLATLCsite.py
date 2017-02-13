#! /usr/bin/env python

import os
import sys
import subprocess

# Steps:
#
# Change to root folder
#
# Swift:
# - make swift page
# 
# LAT LCs:
# - get list of objects
# - for each object:
# - - make folder for each object
# - - change to folder
# - - download LAT LC for object 
# - - download swift LC for each object
# - - generate 4 plots
# - - extract last flux point for daily point 
# - - get LAT flux value and extrapolated VHE in terms of Crab (store)
# - - generate object visibility for coming night and coming month?
# - - generate web page for object
# - make main web page with LAT LCs and some text..


###########################################################################

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

# make Swift web page

# default out file is: "Swift_LCs.html"
res=subprocess.call("makeSwiftLCHTML.py -c -l 7", shell=True)

###########################################################################

###########################################################################

# download LAT list

LC_File="LAT_LC_objects.txt"
DEC_min=32-50
DEC_max=32+50
RA_window=7
z_min=0
z_max=1.5
command="getFermiLCobjects.py -f {} -d {} {} -w {} -z {} {} -q".format(LC_File, 
                                                                       DEC_min, 
                                                                       DEC_max, 
                                                                       RA_window, 
                                                                       z_min, 
                                                                       z_max)

#print(command)
#res=subprocess.call(command, shell=True)
#print(res)

###########################################################################

# load txt file and extract names etc...

LC_File="test.txt"

objects={}

with open(LC_File,"r") as f:
    for line in f:
        fields=line.split(",")
        object=fields[0].replace(" ","")
        objects[object]=(fields[1], fields[2], fields[3], fields[4]) # URL, RA, Dec, Redshift
        

#print(objects)
        

###########################################################################

# Loop over each object...

import map_name
import glob

import SwiftLC
SLC=SwiftLC.SwiftLC(quiet=True)

for name in objects:
    print()
    print(name)
    print()

    # if directpry does not exist make it
    if not os.path.isdir(name):
        if os.path.isfile(name):
            os.remove(name)
        os.mkdir(name)

    os.chdir(name)

    for lc_file in glob.glob("*.lc"):
        os.remove(lc_file)

    for png_file in glob.glob("*.png"):
        os.remove(png_file)


    Swift_LC_file=SLC.download(name)

    # Daily 100 MeV to 300 GeV
    command="plotFermiLC.py -A -a -n {} -e {} -q -N".format(name, "FLUX_100_300000")
    if Swift_LC_file: command+=" -S {}".format(Swift_LC_file)
    res=subprocess.check_output(command, shell=True).decode('utf-8')

    # Daily 1 GeV to 300 GeV
    command="plotFermiLC.py -A -a -n {} -e {} -q -N".format(name, "FLUX_1000_300000")   
    if Swift_LC_file: command+=" -S {}".format(Swift_LC_file)
    res=subprocess.check_output(command, shell=True).decode('utf-8')

    os.chdir("..")





     


            



  
