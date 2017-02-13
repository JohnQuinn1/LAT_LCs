#! /usr/bin/env python

# needs packages:
# matplotlib, astropy, wget 

from __future__ import print_function
from __future__ import division

import matplotlib.pyplot as plt
from astropy.io import fits
import numpy as np


import map_name

import sys
#if len(sys.argv) = 2:
#    print("Usage: {} 'object name'".format(sys.argv[0]))
#    sys.exit(0)
          

import argparse
desc="""Download and plot Fermi-LAT light curves. 
Only data points are plotted - upper limits are ignored.
Note: the Fermi lightcurve names have all spaces removed, 
thus giving names like "CTA 102" will automatically be 
translated to "CTA102". The filenames are case sensitive and must
match what is on the LAT web site. Also, the y-axis scaling
is set by the range of fluxes in the entire file.

Note: LAT Crab flux > 100 MeV is: ~2.75e-6 ph cm^-2 s^-1""" 

parser = argparse.ArgumentParser(description=desc, 
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('-d','--days', 
                    type=int, 
                    default=100, 
                    help="recent number of days to plot, a value of 0 plots all")

parser.add_argument('-r','--remove_FITS', 
                    action='store_true', 
                    help='remove FITS file after processing')

parser.add_argument('-a','--already_downloaded', 
                    action='store_true', 
                    help="use already-downloaded FITS file - don't redownload")

parser.add_argument('-w','--weekly', 
                    action='store_true', 
                    help='download and plot weekly light curve instead of daily')

parser.add_argument('-c','--column_info', 
                    action='store_true', 
                    help='print column info from FITS file')

parser.add_argument('-s','--stdout', 
                    action='store_true', 
                    help='print data to std out')

parser.add_argument('-p','--plot_window', 
                    action='store_true', 
                    help='open plot window (otherwise plot produced just on disk')


parser.add_argument('-N','--no_png', 
                    action='store_true', 
                    help="don't save png file")

parser.add_argument('-e','--energy_range', 
                    type=str, 
                    choices=['FLUX_1000_300000', 'FLUX_300_1000', 'FLUX_100_300000'],
                    default='FLUX_100_300000', 
                    help='choose energy range')

parser.add_argument('-l','--load_mjds', 
                    type=str, 
                    default="", 
                    help="load 2-column ascii file of MJDs for plotting.")

#parser.add_argument('-S','--Swift', 
#                    type=str, 
#                    default="", 
#                    help="load Swift data in lightcurve.txt ('overall') format for plotting")

parser.add_argument('-S','--Swift', 
                    nargs="?",
                    const="get", 
                    default="", 
                    help=("give filename for  Swift data in lightcurve.txt ('overall') format "
                          "to be plotted. If no filename is given the lightcurve txt file will "
                          "be downloaded and renamed from the Switf site"))

parser.add_argument('-n','--name',
                    type=str,
                    required=True,
                    help='name of object to be downloaded')


parser.add_argument('-q', '--quiet', 
                    action='store_true', 
                    help='no printing of what is going on')


parser.add_argument('-C', '--Crab_flux',
                    action='store_true',
                    help='plot a horizontal line indicating the mean Crab Nebula flux')


parser.add_argument('-A', '--Average',
                    action='store_true',
                    help=("plot a horizontal line indicating the object's 3FGL average flux"
                          " (calculated by numericaly integrating 3FGL spectral model)"))


cfg = parser.parse_args()

print(cfg)

Crab_fluxes={'FLUX_1000_300000':1.8e-7, 'FLUX_300_1000':5.74e-7, 'FLUX_100_300000':2.75e-6}


# remove spaces in object names to match LAT LC filenames.
#object=cfg.name.replace(" ","")

object=map_name.map_name(cfg.name,"LAT_LC")

if cfg.weekly: 
    FITS=object+'_604800.lc'
else:
    FITS=object+'_86400.lc'


##############################################################
# download or use already-existing file...

import os

if cfg.already_downloaded:
    if not cfg.quiet: print("Using downloaded",FITS)
    
else:
    import wget

    if not cfg.quiet:
        bar_style=wget.bar_adaptive
    else:
        bar_style=None


    # Daily
    if os.path.isfile(FITS):
        if not cfg.quiet: print("Removing old file:",FITS)
        os.remove(FITS)

    if not cfg.quiet: print("Downloading latest daily file:",FITS)

    remote_file='http://fermi.gsfc.nasa.gov/FTP/glast/data/lat/catalogs/asp/current/lightcurves/'+FITS

    if not cfg.quiet: print("wget:",remote_file)

    try:
        from urllib.error import HTTPError # just so I can catch and handle this exception
        x=wget.download(remote_file, bar=bar_style)
    except HTTPError as e:
        print(e)
        print("Exiting...")
        sys.exit(1)
    except:
        print("Some error occurred...")
        raise
        

    if not cfg.quiet: print()


##############################################################

try:
    hdulist = fits.open(FITS)
except:
    print("Error opening file:",FITS)
    print("Exiting...")
    sys.exit(1)

tbdata=hdulist[1].data

if cfg.column_info:
    cols = hdulist[1].columns
    print(cols.info())

F=cfg.energy_range
if F=='FLUX_100_300000':
    FERR='ERROR_100_300000'
    UL='UL_100_300000'
elif F=='FLUX_300_1000':
    FERR='ERROR_300_1000'
    UL='UL_300_1000'
elif F=='FLUX_1000_300000':
    FERR='ERROR_1000_300000'
    UL='UL_1000_300000'


f=np.array(tbdata[F])
fe=np.array(tbdata[FERR])
x=(np.array(tbdata['START']) + np.array(tbdata['STOP']))/2
dx=(x-np.array(tbdata['START']))/(60*60*24) 
TS=np.array(tbdata['TEST_STATISTIC'])
ulf=np.array(tbdata[UL])

t=51910+x/(60*60*24)  # convert mission secs to MJD                                                                    

# which points are ULs?
i=np.where(ulf==False)


if cfg.stdout:
    if not cfg.quiet:
        print("Printing data to stdout:")
        print("{:8s}  {:4s}  {:8s}  {:8s}".format("MJD_mid", "dMJD", "Flux", "Flux_err"))
    for j in i[0]: # where returns a tuple of arrays so the first element is the array!
        print("{:8.2f}  {:4.2f}  {:3.2e}  {:3.2e}".format(t[j], dx[j], f[j], fe[j]))


plt.clf()
plt.errorbar(t[i],f[i],fe[i],xerr=dx[i],fmt='o')


timescale= "weekly" if cfg.weekly else "daily"
plt.title('{} Fermi-LAT {} light curve'.format(object,timescale))
plt.xlabel('MJD')
plt.ylabel('{} '.format(F)+'($ph\,cm^{-2}\,s^{-1}$)')
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
ax=plt.gca()
ax.yaxis.major.formatter._useMathText=True

if cfg.days>0:
    tmin=int(max(t)-cfg.days)
else:
    tmin=min(t)

tmax=int(max(t)+dx[-1]-tmin)*1.05+tmin
plt.axis(xmin=tmin)
plt.axis(xmax=tmax)
plt.axis(ymin=0)
#plt.axis(ymax=0.8e-5)
plt.grid()



# prevent axes from being displayed as, for example,  5.773e4 + offset
plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)


# Plot the upper limits
ii=np.where(ulf==True)
ymin,ymax=plt.ylim()
ulsize=(ymax-ymin)/40
plt.errorbar(t[ii],f[ii],yerr=ulsize, uplims=True, xerr=dx[ii],fmt='r.', alpha=0.1)




if cfg.Crab_flux:
    cf=Crab_fluxes[F]  # F previously defined as selection of flux energy range
    if not cfg.quiet:
        print("Plotting Crab flux {}: {} ph cm-2 s-1".format(F,cf))
    plt.plot([tmin,tmax], [cf,cf],'g-')


if cfg.Average:
    import Cat3FGL
    cat=Cat3FGL.Cat3FGL(quiet=cfg.quiet)
    cat.select_object(map_name.map_name(cfg.name,"3FGL_ASSOC1"))

    if F=='FLUX_100_300000':
        flux3FGL=cat.calc_int_flux(100,300000)
    elif F=='FLUX_300_1000':
        flux3FGL=cat.calc_int_flux(300,1000)
    elif F=='FLUX_1000_300000':
        flux3FGL=cat.calc_int_flux(1000,300000)
    

    if not cfg.quiet:
        print("Plotting object average flux {}: {:.2e} ph cm-2 s-1".format(F,flux3FGL))

    plt.plot([tmin,tmax], [flux3FGL,flux3FGL],'b-')




if cfg.load_mjds:    
    ymjd=np.mean(plt.gca().get_ylim())  # get axes y limits and mid point
    if not cfg.quiet: print("Loading MJDs from",cfg.load_mjds)
    mjds_start,mjds_end=np.loadtxt(cfg.load_mjds,unpack=True)
    mjd_mid=(mjds_start+mjds_end)/2

    for start,end in zip(mjds_start, mjds_end):
        plt.plot([start, end],[ymjd, ymjd],'r-')
        plt.plot(mjd_mid,np.ones(len(mjd_mid))*ymjd,'r.')


if cfg.Swift:
    swift_file=cfg.Swift
    if swift_file=="get": # "-S given w/o file so must download
        import SwiftLC
        SLC=SwiftLC.SwiftLC(quiet=cfg.quiet)
        swift_file=SLC.download(object)

    if swift_file is None:
        if not cfg.quiet: print("Could not download Swift lightcurve for", object)            
    else:  # "-S given w file so use
        if not cfg.quiet: print("Loading Swift data from",swift_file)
        swift_data=np.loadtxt(swift_file, skiprows=23)
        swift_mjd=swift_data[:,0]
        swift_dmjd=swift_data[:,1]
        swift_rate=swift_data[:,2]
        swift_raterr=swift_data[:,3]
        ax2=plt.gca().twinx()
        ax2.errorbar(swift_mjd, swift_rate, xerr=swift_dmjd, yerr=swift_raterr,fmt='go')
        ax2.set_ylabel('Swift XRT cts/s.', color='g')
        ax2.tick_params('y', colors='g')
        if swift_mjd[-1]+swift_dmjd[-1] > t[-1] + dx[-1]: # i.e. if Swift has more recent data than LAT
            tmax=int(max(swift_mjd)+swift_dmjd[-1]-tmin)*1.05+tmin

plt.axis(xmin=tmin)
plt.axis(xmax=tmax)




if not cfg.no_png:
    pngfile=object+"_"+timescale+"_"+F+".png"
    if not cfg.quiet: print("Saving",pngfile)
    plt.savefig(pngfile)


if cfg.plot_window:
    print("Please manualy close figure window for program to continue!")
    plt.show()


if cfg.remove_FITS:
    if not cfg.quiet: print("Removing",FITS)
    os.remove(FITS)

