#! /usr/bin/env python

import os
import sys
import subprocess
import numpy as np

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

from datetime import datetime
import ephem

#    <head>
#    <style>"""
#    p {{
#      margin-left:50px;
#    }}
#    </style>
#    <head>


def make_flux_table(f):
    data=np.loadtxt(f)
    last=data[-5:,:]

    str=""

    str+="""
         <center>
         <table style="width:50%">    
         <caption> Recent LAT flux values ... </caption>
         <tr>                                                                                                                                
            <th align="left"> MJD </th> 
            <th align="left"> dMJD </th>  
            <th align="left"> Flux </th>
            <th align="left"> dFlux </th>
            <th align="left"> Frac3FGL </th>
            <th align="left"> FracCrab>200GeV </th>
         </tr>"""

    for i in range(last.shape[0]):
        mjd_s="{:.2f}".format(last[i,0])
        dmjd_s="{:.2f}".format(last[i,1])
        flux_s="{:4.2e}".format(last[i,2])
        dflux_s="{:4.2e}".format(last[i,3])
        f3FGL_s="{:4.2f}".format(last[i,4])
        fCr200_s="{:4.2f}".format(last[i,5])
                
        str+="""
             <tr> 
                  <td> {} </td>
                  <td> {} </td>
                  <td> {} </td>
                  <td> {} </td>
                  <td> {} </td>
                  <td> {} </td>
             </tr>""".format(mjd_s,dmjd_s,flux_s,dflux_s,f3FGL_s,fCr200_s)
                
    str+="""</table> <center>"""     
        
    return str



def make_individual_HTML(name, object, files):
    """Write web page for individual object"""

    str="""                                                                     
    <!DOCTYPE html>        
    <html>                      
    <head>                                                                                                                              
        <style>                                                                                                                         
        table, th, td {{                                                                                                                 
            border: 1px solid black;                                                                                                    
            border-collapse: collapse;                                                                                                  
            margin-left: auto;                                                                                                          
            margin-right: auto;                                                                                                         
        }}                                                                                                                               
        th, td {{                                                                                                                        
            padding: 5px;                                                                                                               
            text-align: left;                                                                                                           
        }}                                                                                                                               
    </style>                                                                                                                            
    </head>      
                               
    <h1 align="center"> {0} </h1>                        
    <body>
    """.format(name)                 


    RA=ephem.hours(float(object['RA'])*ephem.pi/180.0)
    Dec=ephem.degrees(float(object['Dec'])*ephem.pi/180.0)

    str+="""
    <p align="center"> RA:   {} deg. = {} </p>
    <p align="center"> Dec.: {} deg. = {} </p>
    <p align="center"> z={} </p>
    """.format(object['RA'], RA, object['Dec'],Dec, object['z'])

    str+="""
    <p align="center"> Original site: <a href="{0}">{0}</a></p>                 
    <p align="center"> Time of last update of this page: UT {1:%Y-%m-%d %H:%M} </p>    
    """.format(object['URL'],datetime.utcnow())


    
   #### 100 MeV to 300 GeV:
    str+="<hr/>"
    str+="<center> <h3> LAT light curves: 100 MeV to 300 GeV </h3></center>"
    for f in files:
        if "100_300000" in f:
            str+="""
                 <center><img src="{0}"> </center>
                 """.format(f)

            str+=make_flux_table(f.replace(".png",".txt")) 

    str+="<hr/>"
    str+="<center> <h3> LAT light curves: 1 GeV to 300 GeV </h3></center>"

    for f in files:
        if "1000_300000" in f:
            str+="""
                 <center><img src="{0}"> </center>
                 """.format(f)
            str+=make_flux_table(f.replace(".png",".txt")) 

    str+="<hr/>"

    str+="""                                                                                      
    </body>                                                                                       
    </html>                                                                                       
    """

    return str


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
        objects[object]={'URL':fields[1],
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
    command="plotFermiLC.py -A -a -n {} -e {} -q -N -F -a".format(name, "FLUX_100_300000")
    if Swift_LC_file: command+=" -S {}".format(Swift_LC_file)
    res=subprocess.check_output(command, shell=True).decode('utf-8').strip()

    # Daily 1 GeV to 300 GeV
    command="plotFermiLC.py -A -a -n {} -e {} -q -N -F -a".format(name, "FLUX_1000_300000")   
    if Swift_LC_file: command+=" -S {}".format(Swift_LC_file)
    res=subprocess.check_output(command, shell=True).decode('utf-8').strip()


    # Weekly 100 MeV to 300 GeV
    command="plotFermiLC.py -A -a -n {} -e {} -q -N -w -F -a".format(name, "FLUX_100_300000")
    if Swift_LC_file: command+=" -S {}".format(Swift_LC_file)
    res=subprocess.check_output(command, shell=True).decode('utf-8')

    # Weekly 1 GeV to 300 GeV
    command="plotFermiLC.py -A -a -n {} -e {} -q -N -w -F -a".format(name, "FLUX_1000_300000")   
    if Swift_LC_file: command+=" -S {}".format(Swift_LC_file)
    res=subprocess.check_output(command, shell=True).decode('utf-8')
    
    files=glob.glob("*.png")
    
    s=make_individual_HTML(object,objects[object],files)

    with open("index.html","w") as f:
        f.write(s)

    os.chdir("..")





     


            



  
