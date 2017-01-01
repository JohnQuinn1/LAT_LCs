#!/usr/bin/env python

# needs packages:
# astroquery (built on astropy), requests, BeautifulSoup, lxml

############################################################################################

import argparse

desc="""Script to scrape Fermi-LAT LC web site to get list
of monitored sources and also query NED to see if 
extragalactic and to get their redshifts.
If the redshift of an object is -1 then it was not found
in the NED database (probably galactic) and if the redshift is '0'
then it was found in NED but the redshift is unknown."""



parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('-F', '--File', type=str, default="",  help='save results in comma-separated format to given filename')

parser.add_argument('-D', '--DecInterval',type=float, nargs=2, metavar=("Dec. low", "Dec. high"),
                    default=(-90,+90), help='Declination interval in degrees.')

parser.add_argument('-R', '--RAInterval',type=float, nargs=2, metavar=("RA. low", "RA. high"),
                    default=(0,360), help='RA interval in degrees.')

parser.add_argument('-z','--zInterval',type=float, nargs=2, metavar=("z low", "z high"),
                    default=(-1000,1000), help='redshift interval.')

parser.add_argument('-v','--verbose', action='store_true', help='print out to screen')

cfg = parser.parse_args()


############################################################################################

############################################################################################

def filter(RA, Dec, z, cfg):
    if (cfg.RAInterval[0] <= RA <= cfg.RAInterval[1]):
        if(cfg.DecInterval[0] <= Dec <= cfg.DecInterval[1]):
            if(cfg.zInterval[0] <= z <= cfg.zInterval[1]):
                return True

    return False

############################################################################################


from astroquery.ned import Ned
from astroquery.exceptions import RemoteServiceError


import requests
URL='http://fermi.gsfc.nasa.gov/ssc/data/access/lat/msl_lc/'
page=requests.get(URL)
if cfg.verbose: print("Successfully downloaded:",URL)


from bs4 import BeautifulSoup
soup=BeautifulSoup(page.content,'lxml')

table=soup.find("table")

names=[]
ras=[]
decs=[]
zs=[]

nobjects=0
naccepted=0

for row in table.findAll("tr"):
    cells=row.findAll("td")
    # Every first row has 3 cells while every second row only has two cells
    # The first cell of the first row (i.e cell[0]) contains the source details at 
    # the start. 

    if(len(cells)==3):
        nobjects+=1

        t=cells[0].getText()

        # The format is along the lines of:
        # '\n1ES 2344+514(RA = 356.770, Dec = 51.7050)\n\t\t\nDaily Light Curve\nDaily Light Curve (1yr)\nDaily Light Curve Fits File\nWeekly Light Curve\nWeekly Light Curve (1yr)\nWeekly Light Curve Fits File\n\n'

        name=t[1:t.find("(")]
        
        ra=float(t[t.find('(RA')+5:t.find(',')])
        dec=float(t[t.find(', Dec')+7:t.find(')')])

        if cfg.verbose: print("Found LAT LC for:",name,"now quering NED...", end="")


        # Now query NED...

        try:
            q=Ned.query_object(name)
            nedz=q['Redshift']
            if nedz.mask: # True if invalid/data missing (i.e. redshift missing)
                z=0.0
                if cfg.verbose: print("found! no z!, assigning 0.0")
            else:
                z=float(nedz)
                if cfg.verbose: print("found! z=",z)
        except RemoteServiceError: # i.e. object not found
            if cfg.verbose: print("not found! assigning z=-1")
            z=-1
            
        if filter(ra,dec,z,cfg):
#            if cfg.verbose: print(name,"accepted by filter")
            names.append(name)
            ras.append(ra)
            decs.append(dec)
            zs.append(z)
            naccepted+=1
        else:
 #           if cfg.verbose:print(name,"rejected by filter")
            pass



# find longest name length for printing
maxw=max([len(name) for name in names])


if cfg.verbose:
    print()
    print("Accepted",naccepted,"of",nobjects,"objects:")
    for name, ra, dec, z in zip(names, ras, decs, zs):
        print("{name:{maxw}s} {ra:8.3f}  {dec:7.3f}  {z:7.4f}".format(name=name, maxw=maxw,ra=ra, dec=dec, z=z))

if cfg.File:
    if cfg.verbose: print("Saving to",cfg.File)
    with open(cfg.File,"w") as f:
        for name, ra, dec, z in zip(names, ras, decs, zs):
            f.write("{}, {},  {},  {}, \n".format(name, ra, dec, z))
        

    

