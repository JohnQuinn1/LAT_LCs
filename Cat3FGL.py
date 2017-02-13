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
            name=map_name.map_name(name,"LAT_ASSOC1")
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
                break
        else:
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

        import scipy.integrate as integrate
        result=integrate.quad(self.spectral_model,E_low_MeV, E_high_MeV)
        if result[0]/result[1] < 10:
            print("Warning, large error:",*result)
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

            
