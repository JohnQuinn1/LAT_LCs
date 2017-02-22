#! /usr/bin/env python

from astropy.io import fits
import numpy as np

#hdulist = fits.open("gll_psc_v16.fit")                                                                                                                
# np.count_nonzero(c.tbdata['SpectrumType'] == "PowerLaw")
# 2523
#
# np.count_nonzero(c.tbdata['SpectrumType'] == "LogParabola")
# 395
#
# np.count_nonzero(c.tbdata['SpectrumType'] == "PLExpCutoff")
# 110
#
# np.count_nonzero(c.tbdata['SpectrumType'] == "PLSuperExpCutoff")
# 6
# 5 pulsars & 3C454.3


import os
import sys
import map_name


class Cat3FGL:

    catalogue_default="gll_psc_v16.fit"

    def __init__(self, quiet=False):
        """
        The catalogue mist be in the current directory or else
        the environment variable LAT3FGLCAT must be set with
        the path and name of 3FGL FITS file..

        Note: some of the field names in the FITS file do not match the 
        descriptions at http://heasarc.gsfc.nasa.gov/W3Browse/fermi/fermilpsc.html,
        for example: web site: 'Flux_0p3_1_GeV' is 'Flux300_1000' in the FITS file.

        Note, you can access any field for object index or selected index with, e.g.:
        c.tbdata['Spectral_Index'][c.index]
        """

        self.index=None
        self.quiet=quiet

        # suppress warnings from scipy numerical integration 
        if quiet:
            import warnings
            warnings.filterwarnings("ignore")            

        if os.path.isfile(Cat3FGL.catalogue_default):
            self.catalogue=Cat3FGL.catalogue_default
        else:
            self.catalogue=os.environ.get('CAT3FGL')           
            if self.catalogue is None:
                if not self.quiet:
                    print("No {} and environment variable CAT3FGL not set - exiting"
                          .format(Cat3FGL.catalogue_default))
                sys.exit(1) # update to throw exception

            
        try:
            self.hdulist = fits.open(self.catalogue)
        except:
            if not self.quiet:
                print("Error opening",self.catalogue, "- exiting")
            sys.exit(1)  # update to throw exception

        self.tbdata=self.hdulist[1].data


    def _selected(self):
        """Check an object has been selected"""

        if self.index is None:
            if not self.quiet:
                print("No object selected - please use select_object()")
            return False
        else:
            return True


    def select_object(self, name, field="ASSOC1"):
        """
        Find object by Associated name (e.g. Mkn 421) or 3FLGID (field="Source_Name"). 
        Note: case and whitespace insensitive
        """

        if field=="ASSOC1":
            name=map_name.map_name(name,"3FGL_ASSOC1")
            names=self.tbdata['ASSOC1']
        elif field=="Source_Name":
            names=self.tbdata['Source_Name']
        else:
            if not self.quiet:
                print("select_object(): Unknown field,",field,"exiting")
            sys.exit(1) # update to throw exception

        name=name.upper().replace(" ","")

        self.index=None

        for i,n in enumerate(names):
            if name in n.upper().replace(" ",""):
                self.index=i
                if not self.quiet: print("Cat3FGL:select_object() Found",name)
                break
        else:
            if not self.quiet: print("Cat3FGL:select_object() did not find match for",name)
            return None # break not encountered so index not found

        if self.tbdata['SpectrumType'][i]=="PowerLaw":
            K=self.tbdata['Flux_Density'][i]
            Gamma=self.tbdata['Spectral_Index'][i]
            E0=self.tbdata['Pivot_Energy'][i]
            self.spectral_model = lambda E: K*(E/E0)**(-Gamma)

        elif self.tbdata['SpectrumType'][i]=="LogParabola":
            K=self.tbdata['Flux_Density'][i]
            alpha=self.tbdata['Spectral_Index'][i]
            E0=self.tbdata['Pivot_Energy'][i]
            beta=self.tbdata['beta'][i]
            self.spectral_model = lambda E: K*(E/E0)**(-alpha-beta*np.log10(E/E0))

        # elif self.tbdata['SpectrumType']=="PLExpCutoff":
        # I gather "PLExpCutoff" and "PLSuperExpCutoff" distinguished via parameters:
        else:  
            K=self.tbdata['Flux_Density'][i]
            Gamma=self.tbdata['Spectral_Index'][i]
            E0=self.tbdata['Pivot_Energy'][i]
            Ec=self.tbdata['Cutoff'][i]
            b=self.tbdata['Exp_Index'][i]
            self.spectral_model = lambda E: K*(E/E0)**(-Gamma)*np.exp((E0/Ec)**b - (E/Ec)**b)

        return n



    def get_all_fields(self):
        """Return all info about selected object"""
        
        if self._selected():
            return self.tbdata[self.index]



    def get_field(self, field):
        """
        Return a given field - field should be passed as a string.
        Most useful:'Source_Name', 'SpectrumType', 'Spectral_Index', 'Powerlaw_Index',
        'Pivot_Energy', 'Flux_Density', 'Flux300_1000', 
        see: https://fermi.gsfc.nasa.gov/ssc/data/access/lat/4yr_catalog/
        """

        if self._selected():
            return self.tbdata[field][self.index]


    def calc_PL_int_flux(self, E_low_MeV, E_high_MeV):
        """
        Return the calculated integral flux between two energies based on powerlaw model
        if the spectrum type is a PowerLaw
        """ 

        if not self._selected():
            return -1

        if not self.tbdata['SpectrumType'][self.index]=='PowerLaw':
            return -2
        

        E_pivot=self.tbdata['Pivot_Energy'][self.index]
        gamma=self.tbdata['Powerlaw_Index'][self.index]
        C=self.tbdata['Flux_Density'][self.index]

        return C/(1-gamma)*(E_high_MeV**(1-gamma) - E_low_MeV**(1-gamma)) / E_pivot**(-gamma)


    def calc_int_flux(self, E_low_MeV, E_high_MeV):
        """
        Return the calculated integral flux between two by numerically integrating the best-fit model
        """ 

        if not self._selected():
            return -1


        import scipy.integrate as integrate
        result=integrate.quad(self.spectral_model,E_low_MeV, E_high_MeV)
#        if result[0]/result[1] < 10:
#            print("Warning, large error:",*result)
        return result[0]


    def get_field_names(self):
        """Return all of the field names"""

        return self.tbdata.names


    def get_Flux300_1000(self):
        """Return all of the field names"""

        if self._selected():
            return self.tbdata['Flux300_1000'][self.index]


    def get_SpectrumType(self):
        """Return all of the field names"""

        if self._selected():
            return self.tbdata['SpectrumType'][self.index]

            
##########################################################################

if __name__ == "__main__":

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


    cat=Cat3FGL()


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


