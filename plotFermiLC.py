#! /usr/bin/env python

# needs packages:
# matplotlib, astropy, wget 

from __future__ import print_function
from __future__ import division

import matplotlib.pyplot as plt
from astropy.io import fits
import numpy as np

import LATLC

import map_name

import sys
          

import argparse
desc="""Download and plot Fermi-LAT light curves. 
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
                    help="recent number of days to plot, a value of 0 plots all, -1 ro include Swift taken before LAT")

parser.add_argument('-r','--remove_FITS', 
                    action='store_true', 
                    help='remove FITS file after processing')

parser.add_argument('-a','--already_downloaded', 
                    action='store_true', 
                    help="use already-downloaded FITS file if it exists- otherwise redownload")

parser.add_argument('-w','--weekly', 
                    action='store_true', 
                    help='download and plot weekly light curve instead of daily')

parser.add_argument('-c','--column_info', 
                    action='store_true', 
                    help='print column info from FITS file')

parser.add_argument('-s','--stdout', 
                    action='store_true', 
                    help='print lightcurve data to std out')


parser.add_argument('-p','--plot_window', 
                    action='store_true', 
                    help='open plot window')


parser.add_argument('-N','--png', 
                    action='store_true', 
                    help="save PNG file")



parser.add_argument('-P','--pdf', 
                    action='store_true', 
                    help="save PDF image")


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
                          "be downloaded and renamed from the Swift site"))

parser.add_argument('-n','--name',
                    type=str,
                    required=True,
                    help='name of object to be downloaded')

parser.add_argument('-F','--file',
                    action='store_true',
                    help='save lightcurve data to text file - name same as image but .txt')


parser.add_argument('-q', '--quiet', 
                    action='store_true', 
                    help='no printing of what is going on')


parser.add_argument('-C', '--Crab_flux',
                    action='store_true',
                    help='plot a horizontal line indicating the mean Crab Nebula flux')

parser.add_argument('-R', '--Root_filename',
                    action='store_true',
                    help='Print the root filename (i.e. w/o extension) for plots and text out/')


parser.add_argument('-A', '--Average',
                    action='store_true',
                    help=("plot a horizontal line indicating the object's 3FGL average flux"
                          " (calculated by numericaly integrating 3FGL spectral model)"))

parser.add_argument('-m', '--MJD_interval',
                    nargs=2,
                    type=float,
                    metavar=("Begin","End"),
                    help=("MJD interval to be plotted"))

parser.add_argument('-ymw', '--y_max_window',
                    action='store_true',
                    help=("y max on graph (Swift and LAT) based on MJD window rather than entire lightcurve"))

parser.add_argument('-ymp', '--y_max_points_only',
                    action='store_true',
                    help=("y max on graph (LAT) based on points only - ULs not used in calculation"))

parser.add_argument('-yml','--y_max_LAT', 
                    type=float, 
                    default=-1, 
                    help="set ymax on Fermi light curve - negative value ignored.")


cfg = parser.parse_args()

################################################################


Crab_fluxes={'FLUX_1000_300000':1.8e-7, 'FLUX_300_1000':5.74e-7, 'FLUX_100_300000':2.75e-6}


object=map_name.map_name(cfg.name,"LAT_LC")

LC=LATLC.LATLC(quiet=cfg.quiet)

FITS=LC.download(object,cfg.weekly,cfg.already_downloaded)

if FITS is None:
    sys.exit(1)

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
i_pt=np.where(ulf==False)
i_ul=np.where(ulf==True)

#############################################################

try:
    import Cat3FGL
    cat=Cat3FGL.Cat3FGL(quiet=cfg.quiet)
    in_3FGL=cat.select_object(map_name.map_name(cfg.name,"3FGL_ASSOC1"))
except:
    in_3FGL = False

    
if in_3FGL:

    if F=='FLUX_100_300000':
        flux_3FGL=cat.calc_int_flux(100,300000)
    elif F=='FLUX_300_1000':
        flux_3FGL=cat.calc_int_flux(300,1000)
    elif F=='FLUX_1000_300000':
        flux_3FGL=cat.calc_int_flux(1000,300000)

    flux_3FGL_gt_200GeV=cat.calc_int_flux(200000,50000000)


flux_crab_gt_200GeV=2.36e-10

#############################################################


plt.figure(figsize=[8,4])
plt.clf()
plt.errorbar(t[i_pt],f[i_pt],fe[i_pt],xerr=dx[i_pt],fmt='ob',markeredgecolor='k',markersize=5)


timescale= "weekly" if cfg.weekly else "daily"
plt.title('{} Fermi-LAT {} light curve'.format(object,timescale))
plt.xlabel('MJD')
plt.ylabel('{} '.format(F)+'($ph\,cm^{-2}\,s^{-1}$)')
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
ax=plt.gca()
ax.yaxis.major.formatter._useMathText=True


if cfg.MJD_interval:
    tmin=cfg.MJD_interval[0]
    tmax=cfg.MJD_interval[1]
else:
    if cfg.days>0:
        tmin=int(max(t)-cfg.days)
    else:
        tmin=min(t)-(max(t)-min(t))*0.02

    tmax=int(max(t)+dx[-1]-tmin)*1.02+tmin


plt.axis(xmin=tmin)
plt.axis(xmax=tmax)
plt.axis(ymin=0)
#plt.axis(ymax=0.8e-5)
plt.grid()


# Set ymax if necessary

if cfg.y_max_points_only:
    LAT_fluxes_for_lims=f[i_pt]+fe[i_pt]
    LAT_fluxes_for_lims_t=t[i_pt]
else:
    LAT_fluxes_for_lims=f+fe
    LAT_fluxes_for_lims_t=t

if cfg.y_max_window:
    LAT_window_fluxes=1.05*LAT_fluxes_for_lims[(LAT_fluxes_for_lims_t>=tmin) & (LAT_fluxes_for_lims_t<=tmax)]
    if len(LAT_window_fluxes)>0:
        y_max_LAT=np.max(LAT_window_fluxes)
        plt.axis(ymax=y_max_LAT)
else:
    y_max_LAT=np.max(1.05*LAT_fluxes_for_lims)
    plt.axis(ymax=y_max_LAT)

if cfg.y_max_LAT > 0:
    plt.axis(ymax=cfg.y_max_LAT)
                    




# prevent axes from being displayed as, for example,  5.773e4 + offset
plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)


# Plot the upper limits
#ii=np.where(ulf==True)
ymin,ymax=plt.ylim()
ulsize=(ymax-ymin)/40
plt.errorbar(t[i_ul], f[i_ul], yerr=ulsize,
             uplims=True, xerr=dx[i_ul],
             fmt='b.', alpha=0.1)


if cfg.Crab_flux:
    cf=Crab_fluxes[F]  # F previously defined as selection of flux energy range
    if not cfg.quiet:
        print("Plotting Crab flux {}: {} ph cm-2 s-1".format(F,cf))
    plt.plot([tmin,tmax], [cf,cf],'m-')



if cfg.Average:
    if in_3FGL:
        if not cfg.quiet:
            print("Plotting object average flux {}: {:.2e} ph cm-2 s-1".format(F,flux_3FGL))

        plt.plot([tmin,tmax], [flux_3FGL,flux_3FGL],'b-')



if cfg.load_mjds:    
    ymjd=np.mean(plt.gca().get_ylim())  # get axes y limits and mid point
    if not cfg.quiet: print("Loading MJDs from",cfg.load_mjds)
    mjds_start,mjds_end=np.loadtxt(cfg.load_mjds,unpack=True)
    mjd_mid=(mjds_start+mjds_end)/2

    ylims=plt.gca().get_ylim()
    for start,end in zip(mjds_start, mjds_end):
#        plt.plot([start, end],[ymjd, ymjd],'r-')
#        plt.plot(mjd_mid,np.ones(len(mjd_mid))*ymjd,'r.')
        plt.fill_between([start, end], ylims[1], facecolor='red', alpha=0.5,edgecolor='red')




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
        swift_data=np.loadtxt(swift_file, skiprows=23, ndmin=2)  # ndmin needed for when only 1 row

        swift_mjd=swift_data[:,0]
        swift_dmjd=swift_data[:,1]
        swift_rate=swift_data[:,2]
        swift_raterr=swift_data[:,3]

        swift_ptsi=np.where(swift_raterr >=0.0)
        swift_ulsi=np.where(swift_raterr <0.0)   # ULs have -1 for error bar

        ax2=plt.gca().twinx()

        #### plot error bars
        ax2.errorbar(swift_mjd[swift_ptsi], swift_rate[swift_ptsi], 
                     xerr=swift_dmjd[swift_ptsi], yerr=swift_raterr[swift_ptsi],
                     fmt='go', markeredgecolor='k', markersize=5.0)

        #### plot upper limits

        ymin,ymax=plt.ylim()
        ulsize=(ymax-ymin)/40

        ax2.errorbar(swift_mjd[swift_ulsi], swift_rate[swift_ulsi], 
                     xerr=swift_dmjd[swift_ulsi], yerr=ulsize, 
                     uplims=True,fmt='g.', alpha=1)


        ax2.set_ylabel('Swift XRT cts/s.', color='g')
        ax2.tick_params('y', colors='g')

        if not cfg.MJD_interval:
            if swift_mjd[-1]+swift_dmjd[-1] > t[-1] + dx[-1]: # i.e. if Swift has more recent data than LAT
                tmax=int(max(swift_mjd)+swift_dmjd[-1]-tmin)*1.02+tmin

            if cfg.days==-1:
                if swift_mjd[0]<tmin: # i.e. Swift obs before the first Fermi one
                    tmin=swift_mjd[0]-(tmax-swift_mjd[0])*0.02


        if cfg.y_max_window:
            XRT_window_counts=1.05*(swift_rate+swift_raterr)[(swift_mjd>=tmin) & (swift_mjd<=tmax)]
            if len(XRT_window_counts) >0:
                y_max_XRT=np.max(XRT_window_counts)
                ax2.axis(ymax=y_max_XRT)


                    
                    
plt.axis(xmin=tmin)
plt.axis(xmax=tmax)


plt.tight_layout()


# for naming of plots....
if cfg.days<=0:
    dur="_all"
else:
    dur="_last{:d}days".format(cfg.days)

if cfg.MJD_interval:
    dur="_{:.2f}_to_{:.2f}".format(*cfg.MJD_interval)


root_filename=object+"_"+timescale+"_"+F+dur

##################################################################################

if cfg.png:
    png_file=root_filename+".png"
    if not cfg.quiet: print("Saving",png_file)
    plt.savefig(png_file)


if cfg.pdf:
    pdf_file=root_filename+".pdf"
    if not cfg.quiet: print("Saving",pdf_file)
    plt.savefig(pdf_file)


##################################################################################

if cfg.remove_FITS:
    if not cfg.quiet: print("Removing",FITS)
    os.remove(FITS)


##################################################################################
#
# save data to stdout or file.

if cfg.stdout or cfg.file:
    outstr=""
    divisor = 7 if cfg.weekly else 1

    index_max=len(t)

    if cfg.days==0 or cfg.MJD_interval:
        index_from_end=index_max
    else:
        index_from_end=cfg.days//divisor


    index_from_end=min(index_from_end,index_max)


    for i in range(index_max-index_from_end, index_max):
        if ulf[i] or not in_3FGL:
            ferr=0.0
            flux_ratio_3FGL=0.0
            flux_gt_200GeV=0.0
            flux_frac_crab_gt_200GeV = 0.0
        else:
            ferr=fe[i]
            flux_ratio_3FGL=f[i]/flux_3FGL
            flux_gt_200GeV=f[i]/flux_3FGL * flux_3FGL_gt_200GeV
            flux_frac_crab_gt_200GeV = flux_gt_200GeV/flux_crab_gt_200GeV



        outstr+="{:8.2f}  {:4.2f}  {:3.2e}  {:3.2e}    {:4.2f}    {:4.2f}\n".format(t[i], 
                                                                                    dx[i], 
                                                                                    f[i], 
                                                                                    ferr, 
                                                                                    flux_ratio_3FGL, 
                                                                                    flux_frac_crab_gt_200GeV)


if cfg.stdout:
    if not cfg.quiet:
        print("{:8s}  {:4s}  {:8s}  {:8s}  {:4s}  {:4s}".format("MJD_mid", 
                                                                "dMJD", 
                                                                "Flux", 
                                                                "Flux_err", 
                                                                "Frac3FGL", 
                                                                "FracCrabGt200GeV"))
    print(outstr)


if cfg.file:
    filename=root_filename+".txt"
    with open(filename,"w") as f:
        f.write(outstr)

##################################################################################

if cfg.Root_filename:
    print(root_filename)

##################################################################################

if cfg.plot_window:
    print("Please manually close figure window for program to continue!")
    plt.show()
