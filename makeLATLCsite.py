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


def write_main_html(objects):
    
    str="""
    <!DOCTYPE html>        
    <html>   
    <head> 
    <style>

    table, th, td {
       border: 1px solid black;
       border-collapse: collapse;
       margin-left: auto;
       margin-right: auto;
    }

    th, td {
       padding: 5px;
       text-align: left;
    }

    div {
        width:100%;
        height:30px;
    }
    </style>
    </head>      
                               
    <h1 align="center"> Fermi-LAT and Swift Lightcurves </h1> 
    <p align="center"> Time of last update of this page:  UT: {3:%Y-%m-%d %H:%M}  (MJD: {4:.3f})</p>     
    <body>
    """.format(datetime.utcnow(), ephem.julian_date(datetime.utcnow())-2400000.5 )


    # Make table

    str+="""
         <center>
         <table  style="width:90%">    
         """

    for object in objects:
        objdict=objects[object]
        name=objdict['name'].replace(" ","")

        d100png=name+"/"+objdict['filename_100_daily']+'.png'
        w100png=name+"/"+objdict['filename_100_weekly']+'.png'
        d1000png=name+"/"+objdict['filename_1000_daily']+'.png'
        w1000png=name+"/"+objdict['filename_1000_weekly']+'.png'

        d100png=name+"/"+objdict['filename_100_daily']+'.png'
        w100png=name+"/"+objdict['filename_100_weekly']+'.png'

        d100="""<img src="{}" alt="Daily >100 MeV" width="400">""".format(d100png)
        d1000="""<img src="{}" alt="Daily >1000 MeV" width="400">""".format(d1000png)
        w100="""<img src="{}" alt="Weekly >100 MeV" width="400">""".format(w100png)
        w1000="""<img src="{}" alt="Weekly >1000 MeV" width="400">""".format(w1000png)


        infostr=""" <a href="{0}/index.html">{0}</a> <br><br>
                    z={1}<br><br> 
                    <b>Last Points: Extrapolated >200 GeV (Crab):<b> <br><br>
                    <u> Flux_100_300000</u>:<br>
                    Daily:  {2:.2f} <br>
                    Weekly: {3:.2f} <br><br>
                    <u> Flux_1000_300000</u>:<br>
                    Daily:  {4:.2f} <br>
                    Weekly: {5:.2f} 
                    """.format(name,
                               objdict['z'],
                               objdict['last_100_daily'][5],
                               objdict['last_100_weekly'][5],
                               objdict['last_1000_daily'][5],
                               objdict['last_1000_weekly'][5])

        str+="""
        <tr>
            <td rowspan="4"> {} </td>
            <th> Daily 100 MeV to 300 GeV  </th> 
            <th> Weekly 100 MeV to 300 GeV </th>
        </tr>
        <tr>
            <td> {}  </td> 
            <td> {}  </td>
        </tr>
        <tr>
            <th> Daily 1 GeV to 300 GeV   </th> 
            <th> Weekly 1 GeV to 300 GeV </th>
        </tr>
        <tr> 
            <td> {} </td>
            <td> {} </td>
        </tr>
        <tr><td/><td/><td/></tr>
        """.format(infostr,d100,w100, d1000, w1000)

    str+="""</table> </center>"""     

    str+="""
         </body>
         </html>
         """
    
    return str





###########################################################################



def make_LAT_flux_table(f):
    data=np.loadtxt(f)
    
    from_end=min(5,len(data[:,0]))  # some sources have very few points, even ULs!
    last=data[-from_end:,:]

#         <table style="width:50%">    
    str=""

    str+="""
         <center>
         <table  style="width:50%">    
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
                
    str+="""</table> </center>"""     
        
    return str



def make_individual_HTML(object_dict):
    """Write web page for individual object passed a dictionary of object properties"""

    object=object_dict

    str="""                                                                     
    <!DOCTYPE html>        
    <html>   
    <head> 
    <style>
    table, th, td {{
       border: 1px solid black;
       border-collapse: collapse;
       margin-left: auto;
       margin-right: auto;                                                                                                  }}                                                                                                                               
    th, td {{                                                                                                                        
        padding: 5px;                                                                                                               
        text-align: left;                                                                                                           
    }}

    div {{
        width:100%;
        height:30px;
    }}
    </style>                                                                                                                            
    </head>      
                               
    <h1 align="center"> {0} </h1>                        
    <body>
    """.format(object['name'])                 



    str+="""
    <p align="center"> LAT Lightcurve site: <a href="{0}">{0}</a></p>                 
    <p align="center"> Swift site: <a href="{1}">{1}</a></p>                 
    <p align="center"> NED: <a href="http://nedwww.ipac.caltech.edu/cgi-bin/nph-objsearch?extend=no&of=html&objname={2:}">Query</a></p>
    <p align="center"> Time of last update of this page:  UT: {3:%Y-%m-%d %H:%M}  (MJD: {4:.3f})</p>     
    """.format(object['LAT_URL'],object['Swift_URL'],object['name'],datetime.utcnow(), ephem.julian_date(datetime.utcnow())-2400000.5 )




    #############################################################
    str+="""
         <div></div>
         <center>
         <table style="width:50%">    
         <caption> Object Properties </caption>

         <tr>                                                                                                                                
            <th align="left"> Property </th> 
            <th align="left"> Value </th>  
         </tr>"""

    RA=ephem.hours(float(object['RA'])*ephem.pi/180.0)
    Dec=ephem.degrees(float(object['Dec'])*ephem.pi/180.0)

    str+="""
         <tr>
             <td> R.A. </td>
             <td> {} </td>
         </tr>
         <tr>
             <td> Dec. </td>
             <td> {} </td>
         </tr>
         <tr>
             <td> z </td>
             <td> {} </td>
         </tr>
         <tr>
             <td> 3FGL SpectrumType </td>
             <td> {} </td>
         </tr>
         <tr>
             <td> 3FGL PL Index </td>
             <td> {} </td>
         </tr>
         <tr>
             <td> 3FGL Flux_100_300000 </td>
             <td> {:.2e} </td>
         </tr>
         <tr>
             <td> 3FGL Flux_1000_300000 </td>
             <td> {:.2e} </td>
         </tr>
         <tr>
             <td> 3FGL Extrap. Crab >200 GeV </td>
             <td> {:.2f} </td>
         </tr>
         """.format(RA, 
                    Dec, 
                    object['z'],
                    object['3FGL_spec_type'],
                    object['3FGL_PL_index'],
                    object['3FGL_flux_100'],
                    object['3FGL_flux_1000'],
                    object['3FGL_frac_gt200GeV'])

    str+="""
         </table>
         </center>
         <div></div>
         """
    
    #############################################################
    ### 100 MeV to 300 GeV 
    ### Daily:
    str+="<hr>"
    str+="<center> <h3> LAT light curves: 100 MeV to 300 GeV </h3></center>"
    
    str+="""<center><img src="{0}"> </center>""".format(object['filename_100_daily']+'.png')
    str+="""<div></div>"""
    str+=make_LAT_flux_table(object['filename_100_daily']+'.txt')
    str+="""<div></div>"""

    ### Weekly:
    
    str+="""<center><img src="{0}"> </center>""".format(object['filename_100_weekly']+'.png')
    str+="""<div></div>"""
    str+=make_LAT_flux_table(object['filename_100_weekly']+'.txt')
    str+="""<div></div>"""
    #############################################################


    #############################################################
    ### 1000 MeV to 300 GeV 
    ### Daily:
    str+="<hr>"
    str+="<center> <h3> LAT light curves: 1000 MeV to 300 GeV </h3></center>"
    
    str+="""<center><img src="{0}"> </center>""".format(object['filename_1000_daily']+'.png')
    str+="""<div></div>"""
    str+=make_LAT_flux_table(object['filename_1000_daily']+'.txt')
    str+="""<div></div>"""


    ### Weekly:
    
    str+="""<center><img src="{0}"> </center>""".format(object['filename_1000_weekly']+'.png')
    str+="""<div></div>"""
    str+=make_LAT_flux_table(object['filename_1000_weekly']+'.txt')
    str+="""<div></div>"""

    #############################################################

    str+="""<hr>"""

    str+="""<div></div>"""

    str+="""<center><h3> VERITAS {} visibility tonight </h3></center>""".format(object['name'])
    
    command="obs_tool.py -c {} {} 2000".format(object['RA'],object['Dec'])
    res=subprocess.check_output(command, shell=True).decode('utf-8').strip()                        
    str+="""
         <div style="margin:auto; height:auto; width:50%;">
         <pre style="text-align: left;">{}</pre>
         </div>
         """.format(res)

    str+="""
    </body>
    </html>
    """

    return str

##################################################################


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

LC_File="all_extragalactic.txt"

objects=OrderedDict()

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

#    for lc_file in glob.glob("*.lc"):
#        os.remove(lc_file)

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
    

    ##### Swift:

    Swift_LC_file=SLC.download(object)
    if Swift_LC_file is not None:
        swift_name=map_name.map_name(object,"Swift_LC")
        objects[object]['Swift_URL']='http://www.swift.psu.edu/monitoring/source.php?source={}'.format(swift_name)
        print(object,'http://www.swift.psu.edu/monitoring/source.php?source={}'.format(swift_name))
    else:
        print(object, "Swift LC not found!")
        objects[object]['Swift_URL']=''


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


    str=make_individual_HTML(objects[object])

    with open ("index.html","w") as f:
        f.write(str)


    os.chdir("..")


str=write_main_html(objects)
with open ("index.html","w") as f:
    f.write(str)



print(json.dumps(objects, sort_keys=True, indent=4, separators=(',', ': ')))
