#!/usr/bin/env python
# coding: utf-8

# In[9]:


#! /usr/bin/env python


# here system exits if it encounters 'critical level' error or 'error level' error
# print calls replaced by logging. exceptions added to places where I had an idea what to add
# quiet was deleted because I found it confusing so I deleted it for my own use, I can add it back
# some program's options were deleted because I am trying to understand what each piece does but I am still not 100% sure what happens
# else:
#            self.catalogue=os.environ.get('CAT3FGL')           
#            if self.catalogue is None:
#  above doesn't seem to work becasue "CAT3FGL" is not defined anywhere, it would work if it was, maybe it is defined somewhere but I can't find it. I tried to test it by raising errors but code never enters that loop.
# what exception to throw in "select_object" function?
#so far only looked at parts of code above "argparse section" and cfg.download

from astropy.io import fits
import numpy as np
import os
import sys
import map_name
import logging
Cat4logger=logging.getLogger("__name__")


class ExitOnExceptionHandler(logging.StreamHandler):
    def emit(self, record):
        super().emit(record)
        if record.levelno in (logging.ERROR, logging.CRITICAL):
            raise SystemExit(1)
            
logging.basicConfig(level=logging.INFO,format='%(asctime)s %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p',handlers=[ExitOnExceptionHandler()])
            
class Cat3FGL:

    catalogue_default="gll_psc_v19.fit"

    def __init__(self):
        
        self.index=None       

        if os.path.isfile(Cat3FGL.catalogue_default):
            self.catalogue=Cat3FGL.catalogue_default
        else:
            self.catalogue=os.environ.get('CAT3FGL')           
            if self.catalogue is None:
                ebllogger.critical("No "+str(format(Cat3FGL.catalogue_default))+"and environment variable CAT3FGL not set") 
                #add critical error and import handler that if catches critical error it exits the program
                
        try:
            self.hdulist = fits.open(self.catalogue)
        except:
            ebllogger.critical("Error opening"+str(self.catalogue)+" - exiting")

        self.tbdata=self.hdulist[1].data


    def _selected(self):
        """Check an object has been selected"""
        if self.index is None:
            Cat4logger.warning("No object selected - please use select_object()")
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
            try:
                name=map_name.map_name(name,"3FGL_ASSOC1")
                names=self.tbdata['ASSOC1']
            except:
                Cat4logger.critical("select_object(): Unknown field, "+str(field)+" exiting")

        name=name.upper().replace(" ","")

        self.index=None

        for i,n in enumerate(names):
            if name in n.upper().replace(" ",""):
                self.index=i
                Cat4logger.info("Cat3FGL:select_object() Found "+str(name))
                break
        else:
            Cat4logger.critical("Cat3FGL:select_object() did not find match for "+str(name))
            return None # break not encountered so index not found

        if self.tbdata['SpectrumType'][i]=="PowerLaw":
            K=self.tbdata['PL_Flux_Density'][i]
            Gamma=self.tbdata['PL_Index'][i]
            E0=self.tbdata['Pivot_Energy'][i]
            self.spectral_model = lambda E: K*(E/E0)**(-Gamma)

        elif self.tbdata['SpectrumType'][i]=="LogParabola":
            K=self.tbdata['LP_Flux_Density'][i]
            alpha=self.tbdata['LP_Index'][i]
            E0=self.tbdata['Pivot_Energy'][i]
            beta=self.tbdata['LP_Beta'][i]
            self.spectral_model = lambda E: K*(E/E0)**(-alpha-beta*np.log10(E/E0))

        # elif self.tbdata['SpectrumType']=="PLExpCutoff":
        # I gather "PLExpCutoff" and "PLSuperExpCutoff" distinguished via parameters:
        else:  
            K=self.tbdata['PLEC_Flux_Density'][i]
            Gamma=self.tbdata['PLEC_Index'][i]
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
        #make another function that gets flux and multiplies it by absorption at some particular redshift value, energy is flux calculated by this function
        #check these with gammapy package built in functions


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
    parser.add_argument("-F","--Field_names", action='store_true',
                        help="Print names of all available fields and exit")
    parser.add_argument('-a','--all_fields', action='store_true',
                        help="print all fields from catalogue for object")
    parser.add_argument('-t','--type', action='store_true',
                        help="prints the spectral type: either PowerLaw, LogParabola, or PLExpCutoff.")

    cfg = parser.parse_args()


###############################################################################



    if cfg.download:
        remote_loc="https://fermi.gsfc.nasa.gov/ssc/data/access/lat/8yr_catalog/"
        file="gll_psc_v19.fit"
        if os.path.isfile(file):
            Cat4logger.critical(str(file)+" exists, please remove first!")
        remote_file=remote_loc+file
        Cat4logger.info("Downloading: "+ str(remote_file))
    
        try:
            from urllib.error import HTTPError # just so I can catch and handle this exception
            x=wget.download(remote_file, bar=wget.bar_adaptive)
        except HTTPError as e:
            Cat4logger.error(str(e))
        except:
            Cat4logger.error("Some error occurred...")
            #raise
        Cat4logger.info("File downloaded - exiting downloading module")
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

    if not cat.select_object(cfg.name, field=cfg.Name_field):
        sys.exit(1)

    if cfg.all_fields:
        field_names=cat.get_field_names()
        fields=cat.get_all_fields()
    
        for i in range(len(fields)):
            print("{:20s}: {}".format(field_names[i],fields[i]))
    if cfg.type:
        print(cat.get_field("SpectrumType"))


   

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


# In[2]:


# hdulist = fits.open("gll_psc_v19.fit")
# tbdata=hdulist[1].data['Source_Type']
# print(tbdata)
# ['Spectral_Index'][c.index]

# c=fits.open("gll_psc_v16.fit")
# c.data()


# In[3]:


# Cat3FGL.select_object("mrk 421")


# In[7]:


# catalogue_default="gll_psc_v.fit"
# # os.path.isfile(Cat3FGL.catalogue_default)
# catalogue=Cat3FGL.catalogue_default
# hdulist = fits.open(catalogue)
# print(hdulist)


# In[ ]:





# In[ ]:




