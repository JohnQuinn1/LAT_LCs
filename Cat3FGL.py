from astropy.io import fits
#hdulist = fits.open("gll_psc_v16.fit")                                                                                                                
import os
import sys

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


    def map_name(self,name):
        """map common names of a subset of objects to 3FGL ASSOC1 name"""

        n=name.upper().replace(" ","")

        # Markarian 421
        if n in ["MRK421", "MARKARIAN421", "MKN421"]:
            return "Mkn 421"

        # Markarian 501
        if n in ["MRK501", "MARKARIAN501", "MKN501"]:
            return "Mkn 501"
        
        return name



    def selected(self):
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

        name=self.map_name(name)

        if field=="ASSOC1":
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

        if self.index is not None:
            return n
        else:
            return None



    def get_all_fields(self):
        """Return all info about selected object"""
        
        if self.selected():
            return self.tbdata[self.index]



    def get_field(self, field):
        """
        Return a given field - field should be passed as a string.
        Most useful:'Source_Name', 'SpectrumType', 'Spectral_Index', 'Powerlaw_Index',
        'Pivot_Energy', 'Flux_Density', 'Flux300_1000', 
        see: https://fermi.gsfc.nasa.gov/ssc/data/access/lat/4yr_catalog/
        """

        if self.selected():
            return self.tbdata[field][self.index]


    def calc_int_flux(self, E_low_MeV, E_high_MeV):
        """
        Return the calculated integral flux between two energies based on powerlaw model
        and irrespective of the best-fit spectrum type.
        """ 

        if not self.selected():
            return -1

        E_pivot=self.tbdata['Pivot_Energy'][self.index]
        gamma=self.tbdata['Powerlaw_Index'][self.index]
        C=self.tbdata['Flux_Density'][self.index]

        return C/(1-gamma)*(E_high_MeV**(1-gamma) - E_low_MeV**(1-gamma)) / E_pivot**(-gamma)


    def get_field_names(self):
        """Retrun all of the field names"""

        return self.tbdata.names
            




