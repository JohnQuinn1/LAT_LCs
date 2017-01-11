#!/usr/bin/env python

# needs packages:
# astroquery (built on astropy), requests, BeautifulSoup, lxml

############################################################################################

import argparse

desc="""Script to scrape Fermi-LAT LC web site to get list
of monitored sources and also query NED to see if 
extragalactic and to get their redshifts. NED query
is SLOW so it can be turned off.
If the redshift of an object is -1 then it was not found
in the NED database (probably galactic) and if the redshift is '0'
then it was found in NED but the redshift is unknown."""



parser = argparse.ArgumentParser(description=desc, 
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('-f', '--file', 
                    type=str, 
                    default="",  
                    help='save results in comma-separated format to given filename')

parser.add_argument('-d', '--DecInterval',
                    type=float, 
                    nargs=2, 
                    metavar=("Dec. low", "Dec. high"),
                    default=(-90,+90), 
                    help='Declination interval in degrees.')

parser.add_argument('-r', '--RAInterval',
                    type=float, 
                    nargs=2, 
                    metavar=("RA. low", "RA. high"),
                    default=(0,360), 
                    help='RA interval in degrees.')

parser.add_argument('-z','--zInterval',
                    type=float, 
                    nargs=2, 
                    metavar=("z low", "z high"),
                    default=(-1000,1000), 
                    help='redshift interval.')

parser.add_argument('-n','--no_ned', 
                    action='store_true', 
                    help='do not query NED')

parser.add_argument('-m','--mod_date', 
                    action='store_true', 
                    help='print date "Data last modified" and quit')

parser.add_argument('-q','--quiet', 
                    action='store_true', 
                    help='print out to screen')

cfg = parser.parse_args()

#if not cfg.verbose and not cfg.file and not cfg.mod_date:
#    parser.error("Please select options -v and/or -f or -m. Option -h for detailed help.")




############################################################################################

############################################################################################

def filter(RA, Dec, z, cfg):
    if (cfg.RAInterval[0] <= RA <= cfg.RAInterval[1]):
        if(cfg.DecInterval[0] <= Dec <= cfg.DecInterval[1]):
            if(cfg.zInterval[0] <= z <= cfg.zInterval[1]):
                return True

    return False

############################################################################################

import sys
from astroquery.ned import Ned
from astroquery.exceptions import RemoteServiceError


import requests
URL='http://fermi.gsfc.nasa.gov/ssc/data/access/lat/msl_lc/'
page=requests.get(URL)
if not cfg.quiet: print("Successfully downloaded:",URL)


from bs4 import BeautifulSoup
soup=BeautifulSoup(page.content,'lxml')



##### Get last modified date

if cfg.mod_date:
    if not quiet: print("Searching document for data modification date...")
    for p in soup.find_all("p"):
        ptxt=p.get_text()
        if ptxt.find('Data last modified:') >=0: 
            # find() returns index, which can be 0 but evaluates to false as a bool
            dlm=ptxt[ptxt.find(":")+2:]
            print(dlm)
            sys.exit()


##### Process the table....

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

        if not cfg.quiet: 
            print("Found LAT LC for:",name, end="")

            if not cfg.no_ned:
                print(". Now quering NED...", end="", flush=True)


        # Now query NED...
        if cfg.no_ned:
            z=0
        else:
            try:
                q=Ned.query_object(name)
                nedz=q['Redshift']
                if nedz.mask: # True if invalid/data missing (i.e. redshift missing)
                    z=0.0
                    if not cfg.quiet: print("found! no z!, assigning 0.0")
                else:
                    z=float(nedz)
                    if not cfg.quiet: print("found! z=",z)
            except RemoteServiceError: # i.e. object not found
                if not cfg.quiet: print("not found! assigning z=-1")
                z=-1
            
        if filter(ra,dec,z,cfg):
            names.append(name)
            ras.append(ra)
            decs.append(dec)
            zs.append(z)
            naccepted+=1
        else:
            pass



# find longest name length for printing
maxw=max([len(name) for name in names])


if not cfg.quiet:
    print()
    print("Accepted",naccepted,"of",nobjects,"objects:")
    for name, ra, dec, z in zip(names, ras, decs, zs):
        print("{name:{maxw}s} {ra:8.3f}  {dec:7.3f}  {z:7.4f}".format(name=name, maxw=maxw,ra=ra, dec=dec, z=z))

if cfg.file:
    if cfg.quiet: print("Saving to",cfg.File)
    with open(cfg.file,"w") as f:
        for name, ra, dec, z in zip(names, ras, decs, zs):
            f.write("{}, {},  {},  {}, \n".format(name, ra, dec, z))
        

    

