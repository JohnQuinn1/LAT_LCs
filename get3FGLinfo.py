#! /usr/bin/env python

import sys
import os
import wget


###############################################################################

import argparse

desc="""
Get information from 3FGL catalogue. It uses environment variable $CAT3FGL to
point to the 3FGL FITS file location (including name) - if not found the program
will look in the current (or user specified) directory for the cataloge with default name.

The catalogue can be dowloaded from: https://fermi.gsfc.nasa.gov/ssc/data/access/lat/4yr_catalog/
Direct link: https://fermi.gsfc.nasa.gov/ssc/data/access/lat/4yr_catalog/gll_psc_v16.fit
Note: some of the field names in the FITS file do not match the descriptions on the
web site: for example: web site: 'Flux_0p3_1_GeV' is 'Flux300_1000' in the FITS file. What is
FLUX1000 in the FITS file?? 
"""

parser = argparse.ArgumentParser(description=desc, 
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('-d','--download', action='store_true',
                    help="Download the catalogue to the current directory and exit")

parser.add_argument('-N','--Name_field', type=str, default="ASSOC1",
                    help="Specify name field to use: 'Source_Name', 'ASSOC1', etc.")

parser.add_argument('-n','--name',type=str, default="", 
                    help="""Select object by name. Name field selected with option -N. 
Need another option as well to print some field""")


parser.add_argument('-a','--all_fields', action='store_true',
                    help="print all fields from catalogue for object")

parser.add_argument("-f","--field", type=str,
                   help="Print selected field (e.g. 'Powerlaw_Index'] from cataloge for object")


parser.add_argument("-F","--Field_names", action='store_true',
                   help="Print names of all available fields and exit")


parser.add_argument('-p', '--powerlaw', action='store_true',
                    help="print the powerlaw spectral index, flux constant and decorrelation energy")


parser.add_argument('-t','--type', action='store_true',
                    help="prints the spectral type: either PowerLaw, LogParabola, or PLExpCutoff.")


parser.add_argument('-I','--integral_flux', 
                    type=float, 
                    nargs=2, 
                    metavar=("E_lower_MeV","E_upper_MeV"),
                    help=("print the best-model numerically integrated flux (ph cm^-2 s^-1) in energy range"))

parser.add_argument('-P','--PL_integral_flux', 
                    type=float, 
                    nargs=2, 
                    metavar=("E_lower_MeV","E_upper_MeV"),
                    help=("print the PL-calculated integrated flux (ph cm^-2 s^-1) in energy range"))


cfg = parser.parse_args()


###############################################################################



if cfg.download:
    remote_loc="https://fermi.gsfc.nasa.gov/ssc/data/access/lat/4yr_catalog/"
    file="gll_psc_v16.fit"
    if os.path.isfile(file):
        print(file, "exists, please remove first!")
        sys.exit(1)
    remote_file=remote_loc+file
    print("Downloading:",remote_file)
    
    try:
        from urllib.error import HTTPError # just so I can catch and handle this exception
        x=wget.download(remote_file, bar=wget.bar_adaptive)
    except HTTPError as e:
        print(e)
    except:
        print("Some error occurred...")
        #raise
    print("Exiting...")
    sys.exit(1)


import Cat3FGL
cat=Cat3FGL.Cat3FGL()


if cfg.Field_names:
    field_names=cat.get_field_names()
    for i in range(len(field_names)):
        print(field_names[i])
    sys.exit(1)


if not cfg.name:
    print("Please re-run with an object name or -F or -d options")
    print()
    parser.print_help()
    sys.exit(1)

cat.select_object(cfg.name, field=cfg.Name_field)

if cfg.all_fields:
    field_names=cat.get_field_names()
    fields=cat.get_all_fields()
    
    for i in range(len(fields)):
        print("{:20s}: {}".format(field_names[i],fields[i]))


if cfg.field:
    print(cat.get_field(cfg.field))

if cfg.type:
    print(cat.get_field("SpectrumType"))

if cfg.powerlaw:
    print(cat.get_field('Powerlaw_Index'),
          cat.get_field('Flux_Density'),
          cat.get_field('Pivot_Energy'))


if cfg.integral_flux:
    print(cat.calc_int_flux(cfg.integral_flux[0], cfg.integral_flux[1]))


if cfg.PL_integral_flux:
    print(cat.calc_PL_int_flux(cfg.PL_integral_flux[0], cfg.PL_integral_flux[1]))

#        print(i,n)
#        src_name=tbdata['Source_Name'][i]
#        spec_type=tbdata['SpectrumType'][i]
##        gamma=tbdata['Spectral_Index'][i]
#        gamma=tbdata['Powerlaw_Index'][i]
#        Epivot=tbdata['Pivot_Energy'][i] # MeV
#        C=tbdata['Flux_Density'][i] # at the pivot energy, ph/cm2/s/MeV
#        F_300_1000=tbdata['Flux300_1000'][i]
#        print(src_name,spec_type, gamma, C, Epivot)
#        print("Flux 300-1000 MeV:",int_flux(C, gamma, Epivot, 300, 1000), F_300_1000)
#        print("Flux 100-300000 MeV:",int_flux(C, gamma, Epivot, 100, 300000))
