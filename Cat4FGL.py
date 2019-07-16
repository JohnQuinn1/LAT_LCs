#!/usr/bin/env python
# coding: utf-8

# In[1]:


#! /usr/bin/env python


from astropy.io import fits
import numpy as np
import os
import sys
import map_name
import logging
import gammapy
from gammapy.spectrum.models import Absorption
import astropy.units as u
Cat4logger=logging.getLogger("Cat4FGL")


class HaltException(Exception): pass
        
            
class Cat4FGL:

    catalogue_default="gll_psc_v19.fit"

    def __init__(self):
        
        try:
            self.index=None       
            if os.path.isfile(Cat4FGL.catalogue_default):
                self.catalogue=Cat4FGL.catalogue_default
            else:
                self.catalogue=os.environ.get('CAT4FGL')           
                if self.catalogue is None:
                    Cat4logger.critical("No "+str(format(Cat4FGL.catalogue_default))+"and environment variable CAT4FGL not set")
                
            try:
                self.hdulist = fits.open(self.catalogue)
            except:
                Cat4logger.critical("Error opening"+str(self.catalogue))

            self.tbdata=self.hdulist[1].data
        except:
            try:
                
                raise HaltException("Initialisation of catalogue data failed")
            except HaltException as h:
                print(h)
            


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
        try:
            
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
                    Cat4logger.critical("select_object(): Unknown field, "+str(field))

            name=name.upper().replace(" ","")

            self.index=None

            for i,n in enumerate(names):
                if name in n.upper().replace(" ",""):
                    self.index=i
                    Cat4logger.info("Cat4FGL:select_object() Found "+str(name))
                    break
            else:
                Cat4logger.critical("Cat4FGL:select_object() did not find match for "+str(name))
                try:
                    raise HaltException("Task not performed")
                except HaltException as h:
                    print(h)
                # break not encountered so index not found
        
            global K, Gamma, E0, alpha, beta, Ec, b
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
        
        
        except:
            try:
                raise HaltException("Selecting object failed")
            except HaltException as h:
                print(h)



    def get_all_fields(self):
        """Return all info about selected object"""

        if self._selected():
            return self.tbdata[self.index]



    def get_field(self, field):
        """
        Return a given field - field should be passed as a string.
        Most useful:'Source_Name', 'SpectrumType', 'PL_Index', 'LP_Index', 'PLEC_Index',
        'Pivot_Energy', 'PL_Flux_Density', 'LP_Flux_Density', 'PLEC_Flux_Density',
        see: https://fermi.gsfc.nasa.gov/ssc/data/access/lat/8yr_catalog/
        """

        if self._selected():
            return self.tbdata[field][self.index]
        
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


    def get_SpectrumType(self):
        """Return all of the field names"""

        if self._selected():
            return self.tbdata['SpectrumType'][self.index]
    
 ####################################ADDED###################################################################

    def calc_int_flux_gammapy(self,E_low, E_high):
        
        #energy input in MeV
        
        if not self._selected():
            Cat4logger.warning("no object is selected, please use -n option to select an object")
            return None
        try:
            selfmodel=self.tbdata['SpectrumType'][self.index] 
        
            if selfmodel=="PowerLaw":
                var=gammapy.spectrum.models.PowerLaw(index=Gamma,amplitude=K*u.Unit('cm-2 s-1 MeV-1'),reference=E0*u.MeV)
            elif selfmodel=="LogParabola":
                var=gammapy.spectrum.models.LogParabola.from_log10(amplitude=K*u.Unit('cm-2 s-1 MeV-1'),reference=E0*u.MeV,alpha=alpha,beta=beta)
            else:
                var=gammapy.spectrum.models.PLSuperExpCutoff3FGL(amplitude=K*u.Unit('cm-2 s-1 MeV-1'),reference=E0*u.MeV,ecut=Ec,index_1=Gamma,index_2=b)
            return(var.integral(float(E_low)*u.MeV,float(E_high)*u.MeV))
        except ValueError:
            Cat4logger.warning("your input is not a float or int, try again")
            return None
        except:
            Cat4logger.warning("something went wrong while calculating integral flux")
            return None
        #SuperExpCutoff used bacause if you look at website describing 8-yr catalog then the values of flux densities and indexes are for superexpcutoff
        #in select_object function these values of superexpcutoff are used, no values for any other model are given in 4th catalogue
        #website:   https://heasarc.gsfc.nasa.gov/W3Browse/fermi/fermilpsc.html
    

    def calc_int_absorbed_flux_gammapy(self,E_low, E_high,model,redshift):
        
        #input in MeV
       
        if not self._selected():
            Cat4logger.warning("no object is selected, please use -n option to select an object")
            return None
        
        energy=E_low*u.TeV
        readbuiltin=Absorption.read_builtin(model)

        # checking for inputs out of range of models and invalid inputs
        try:
            if ((energy))<min(readbuiltin.energy): 
                    Cat4logger.warning("ENERGY OUT OF RANGE FOR MODEL "+str(model)+", min energy="+str(min(readbuiltin.energy)))
        except TypeError:
            Cat4logger.warning("INCORRECT ENERGY INPUT. See help(EBLAbsorption().absorption)")
            return(None)
        try:
            if (redshift<min(readbuiltin.param)) or (redshift>max(readbuiltin.param)):
                    Cat4logger.warning("REDSHIFT OUT OF RANGE FOR MODEL "+str(model)+" "+"; "+str(min(readbuiltin.param))+"<redshift<"+str(max(readbuiltin.param)))
        except TypeError:
            Cat4logger.warning("INCORRECT REDSHIFT INPUT. See help(EBLAbsorption().absorption)")
            return(None)

        #calculating absorbed flux
        selfmodel=self.tbdata['SpectrumType'][self.index]
        try:
            if selfmodel=="PowerLaw":
                var=gammapy.spectrum.models.PowerLaw(index=Gamma,amplitude=K*u.Unit('cm-2 s-1 MeV-1'),reference=E0*u.MeV)
            elif selfmodel=="LogParabola":
                var=gammapy.spectrum.models.LogParabola.from_log10(amplitude=K*u.Unit('cm-2 s-1 MeV-1'),reference=E0*u.MeV,alpha=alpha,beta=beta)
            else:
                var=gammapy.spectrum.models.PLSuperExpCutoff3FGL(amplitude=K*u.Unit('cm-2 s-1 MeV-1'),reference=E0*u.MeV,ecut=Ec,index_1=Gamma,index_2=b)
            a=gammapy.spectrum.models.AbsorbedSpectralModel(var,Absorption.read_builtin(model),float(redshift))
            return(a.integral(float(E_low)*u.MeV,float(E_high)*u.MeV))
        except ValueError:
            Cat4logger.warning("your input is not a float or int, try again")
            return None
        except:
            Cat4logger.warning("something went wrong while calculating integral flux")
            return None
     
 
##############################################################################

if __name__ == "__main__":

    import wget
    logging.basicConfig(level=logging.INFO)


###############################################################################

    import argparse

    desc="""
         Get information from 3FGL catalogue. It uses environment variable $CAT4FGL to
         point to the 3FGL FITS file location (including name) - if not found the program
         will look in the current (or user specified) directory for the cataloge with default name.

         The catalogue can be dowloaded from: https://fermi.gsfc.nasa.gov/ssc/data/access/lat/8yr_catalog/
         Direct link: https://fermi.gsfc.nasa.gov/ssc/data/access/lat/8yr_catalog/gll_psc_v19.fit
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
    
    
    ##############################ADDED######################################################################
    

    parser.add_argument('-IG','--integral_flux_gammapy', 
                        nargs=2, 
                        metavar=("E_lower_MeV","E_upper_MeV"),
                        help=("print the best-model numerically integrated flux (ph cm^-2 s^-1) in energy range; energy input in MeV"))
    
    parser.add_argument('-IGA','--integral_absorbed_flux_gammapy', 
                        nargs=3,
                        type=float,
                        metavar=("E_lower_MeV","E_upper_MeV", "redshit_z"),
                        help=("print the best-model numerically integrated flux (ph cm^-2 s^-1) in energy range. energy input in MeV. choose model using -m option (default is 'franceschini)')"))
    
    parser.add_argument('-m','--model',
                        type=str,
                        choices=['franceschini','dominguez','finke'],
                        default='franceschini',
                        help="choose absorption model. default is 'franceschnini'")
    
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
        Cat4logger.info("File downloaded - exiting downloading module")
        sys.exit(1)


    cat=Cat4FGL()


    if cfg.Field_names:
        field_names=cat.get_field_names()
        for i in range(len(field_names)):
            print(field_names[i])
        sys.exit(1)


    if not cfg.name:
        parser.print_help()
        Cat4logger.error("Please re-run with an object name or -F or -d options")

        
    if not cat.select_object(cfg.name, field=cfg.Name_field):
        Cat4logger.error("no object selected")

        
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
        print(cat.get_field('PL_Index'),
              cat.get_field('PL_Flux_Density'),
              cat.get_field('Pivot_Energy'))


    if cfg.integral_flux:
        print(cat.calc_int_flux(cfg.integral_flux[0], cfg.integral_flux[1]))
        
        
   ####################################ADDED######################################################################     
        
    if cfg.integral_flux_gammapy:
        print(cat.calc_int_flux_gammapy(cfg.integral_flux_gammapy[0], cfg.integral_flux_gammapy[1])) 
        
        
    if cfg.model:
        chosenmodel=cfg.model
       
        
    if cfg.integral_absorbed_flux_gammapy:
        print(cat.calc_int_absorbed_flux_gammapy(cfg.integral_absorbed_flux_gammapy[0], cfg.integral_absorbed_flux_gammapy[1],chosenmodel,cfg.integral_absorbed_flux_gammapy[2]))









