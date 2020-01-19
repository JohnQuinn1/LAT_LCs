#! /usr/bin/env python

import os
import sys
import subprocess
import numpy as np
from collections import OrderedDict
import json

###########################################################################

from datetime import datetime
import ephem


###########################################################################


def make_main_html(objects,updating=False, LATLC_last_site_update=""):

# turn off broswer caching, see:  http://www.tech-faq.com/prevent-caching.html

    if LATLC_last_site_update:
        LAT_site_update_str="(last updated: {})".format(LATLC_last_site_update)
    else:
        LAT_site_update_str=""



    str="""
    <!DOCTYPE html>        
    <html>   
    <head> 

    <meta http-equiv=”Pragma” content=”no-cache”>
    <meta http-equiv=”Expires” content=”-1″>
    <meta http-equiv=”CACHE-CONTROL” content=”NO-CACHE”>

    <meta http-equiv="cache-control" content="max-age=0">
    <meta http-equiv="cache-control" content="no-cache">
    <meta http-equiv="expires" content="-1">
    <meta http-equiv="expires" content="Tue, 01 Jan 1980 11:00:00 GMT">
    <meta http-equiv="pragma" content="no-cache">

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

    <body>
    """ 

    str+="""                              
    <h1 align="center"> Fermi-LAT and Swift Lightcurves </h1> 
    <center> <a href="https://fermi.gsfc.nasa.gov/ssc/data/access/lat/msl_lc/"> Original LAT site</a> {0:}</center> <br>
    <center> <a href="https://www.swift.psu.edu/monitoring/"> Original Swift site </a> and 
             <a href="Swift_LCs.html"> Recent Updates </a> </center><br>
    <p align="center"> Time of last update of this page:  UT: {1:%Y-%m-%d %H:%M}  (MJD: {2:.3f})</p>     
    """.format(LAT_site_update_str, datetime.utcnow(), ephem.julian_date(datetime.utcnow())-2400000.5)


    if updating:
        str+="""<center><font color="red"> The data and plots on this site are currently updating - please check back soon!</font></center><br>"""


    # Make table

    str+="""
         <center>
         <table  style="width:90%">    
         """

    for object in objects:
        objdict=objects[object]
        name=objdict['name']

        
        #######################################################################################
        if not objdict['valid']:
            infostr="""{} <font color="red"> An Error Occurred!</font>""".format(objdict['name_ws'])

            str+="""
            <tr>
                 <td rowspan="4"> {} </td>
                 <th> Daily 100 MeV to 300 GeV  </th> 
                 <th> Weekly 100 MeV to 300 GeV </th>
            </tr>
            <tr>
                <td>   </td> 
                <td>  </td>
            </tr>
            <tr>
                <th> Daily 1 GeV to 300 GeV   </th> 
                <th> Weekly 1 GeV to 300 GeV </th>
            </tr>
            <tr> 
                <td>  </td>
                <td>  </td>
            </tr>
            <tr><td/><td/><td/></tr>
            """.format(infostr)
                                                                          
            continue
        ########################################################################################

        # valid so ok to write table

        d100png=name+"/"+objdict['filename_100_daily']+'.png'
        w100png=name+"/"+objdict['filename_100_weekly']+'.png'
        d1000png=name+"/"+objdict['filename_1000_daily']+'.png'
        w1000png=name+"/"+objdict['filename_1000_weekly']+'.png'

#        d100png=name+"/"+objdict['filename_100_daily']+'.png'
#        w100png=name+"/"+objdict['filename_100_weekly']+'.png'

        d100="""<img src="{}" alt="Daily >100 MeV" width="400">""".format(d100png)
        d1000="""<img src="{}" alt="Daily >1000 MeV" width="400">""".format(d1000png)
        w100="""<img src="{}" alt="Weekly >100 MeV" width="400">""".format(w100png)
        w1000="""<img src="{}" alt="Weekly >1000 MeV" width="400">""".format(w1000png)

    
        infostr=""" 
                <a href="{0}/index.html">{1}</a> <br><br>
                z={2}<br><br> 
                <b>Last Points: Extrapolated >200 GeV (Crab):</b> <br><br>
                <u> Flux_100_300000</u>:<br>
                Daily:  {3:.2f} <br>
                Weekly: {4:.2f} <br><br>
                <u> Flux_1000_300000</u>:<br>
                Daily:  {5:.2f} <br>
                Weekly: {6:.2f} 
                """.format(objdict['name'],
                           objdict['name_ws'],
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
    data=np.loadtxt(f,ndmin=2)
    
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

    if not object['valid']:
        return ""


    str="""                                                                     
    <!DOCTYPE html>        
    <html>   
    <head> 

    <meta http-equiv=”Pragma” content=”no-cache”>                               
    <meta http-equiv=”Expires” content=”-1″>                                    
    <meta http-equiv=”CACHE-CONTROL” content=”NO-CACHE”>                        
                                                                                
    <meta http-equiv="cache-control" content="max-age=0">                       
    <meta http-equiv="cache-control" content="no-cache">                        
    <meta http-equiv="expires" content="-1">                                    
    <meta http-equiv="expires" content="Tue, 01 Jan 1980 11:00:00 GMT">         
    <meta http-equiv="pragma" content="no-cache"> 


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
    """.format(object['name_ws'])                 



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

    try:
        res=subprocess.check_output(command, shell=True).decode('utf-8').strip()                        
    except:
        res=""


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


###########################################################################


if __name__ == "__main__":

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

#json_file=os.environ.get('BAR_JSON_FILENAME')
#
#if json_file is None:
#    if not quiet:
#        print("No $BAR_JSON_FILENAME set, exiting....")
#    sys.exit(1)

    json_file="LATLC_data.json"

    try:
        tmpdict = json.load(open(json_file))
    except FileNotFoundError:
        print("Error, cannot open:",json_file,"exiting...")
        sys.exit(1)

    # sort dictionary into new ordered dictionary by RA
    objects=OrderedDict(sorted(tmpdict.items(), key = lambda x: float(x[1]['RA'])))

   # print(objects.keys())

###########################################################################

    for name in objects:
        print(name)

        # if directpry does not exist make it
        if not os.path.isdir(name):
            if not quiet:
                print("Directory",name,"does not exist, skipping...")
            continue

        os.chdir(name)

        str=make_individual_HTML(objects[name])

        with open ("index.html","w") as f:
            f.write(str)

        os.chmod("index.html",0o644)
        
        os.chdir("..")




    str=make_main_html(objects)
    with open("index.html","w") as f:
        f.write(str)

    os.chmod("index.html",0o644)
     


            



  
