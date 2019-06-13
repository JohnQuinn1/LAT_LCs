#!/usr/bin/env python
# coding: utf-8

# In[11]:


from gammapy.spectrum.models import Absorption
import astropy.units as u
import logging
import sys
import numpy as np
import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
ebllogger=logging.getLogger("__name__")

class EBLAbsorption:
    """ 
        parameters:
                "model" of spectral absorption ("franceschini" or "dominguez" or "finke")
                default model is "franceschini"
        
        downloading models to your compurter (Linux):
                after downloading and installing gammapy, open terminal window and execute:
                            gammapy download tutorials --release 0.12
                            cd gammapy-tutorials
                            export GAMMAPY_DATA=$PWD/datasets-0.12
                run anaconda-navigator and change channel to gammapy-0.12
        """
    def __init__(self,model="franceschini"):
        self.model=model
        try:
            self.ebl=Absorption.read_builtin(str(self.model))
        except KeyError as error:
            ebllogger.warning(str(error)+"is an invalid name of model")
    
    def absorption(self,redshift,energy):
        """ This function calculates absorption of EBL according to model stated in class definition 
        and returns the 'surviving fraction of energy'
        parameters:
                redshift (int or float)
                energy (list)
                            where, for example, energy=[2]
        ONLY TAKES ENERGY IN TeV
        """
        energy=energy*u.TeV
        try:
#             temp=np.array(energy)
#             if len(temp)>1:
#                 if (min(energy))<min(self.ebl.energy): 
#                         ebllogger.warning("ENERGY OUT OF RANGE FOR MODEL "+str(self.model)+\
#                                     ", min energy="+str(min(self.ebl.energy)))
#                         return(1)
                            
            if ((energy))<min(self.ebl.energy): 
                    ebllogger.warning("ENERGY OUT OF RANGE FOR MODEL "+str(self.model)+                                    ", min energy="+str(min(self.ebl.energy)))
                    return(1)
        except TypeError:
            ebllogger.warning("INCORRECT ENERGY INPUT. See help(EBLAbsorption().absorption)")
            return(None)
        if (redshift<min(self.ebl.param)) or (redshift>max(self.ebl.param)):
                ebllogger.warning("REDSHIFT OUT OF RANGE FOR MODEL "+str(self.model)+" "+"; "                                  +str(min(self.ebl.param))+"<redshift<"+str(max(self.ebl.param)))
        else:
            return self.ebl.evaluate((energy),redshift)
        
    def get_flux(self,redshift,energy):
        """ This function calculates absorption of EBL according to model stated in class definition 
        and returns the 'surviving energy'
        parameters:
                redshift (int or float)
                energy (list)
                            where, for example, energy=[2]"""
        return(self.absorption(redshift,energy)*energy)

    
    
#######################################################################

if __name__ == "__main__":
    
    logging.basicConfig(level=logging.WARNING,format='%(asctime)s %(message)s',                    datefmt='%m/%d/%Y %I:%M:%S %p')
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-M','--model',help="choose absorption model,('franceschini' or 'dominguez' or 'finke')",default="franceschini", required=False)
    parser.add_argument('-A','--absorption_coefficient',help="use --model first to choose model or just use commans -A                             (default model is franceschini). -A takes input:                             redshift energy eg.input= 1 2,3,4,5 where z=1 and energy= 2,3,4,5 TeV",nargs=2)
    parser.add_argument('-F','--after_absorption_flux',help="use --model first to choose model or just use commans -A                             (default model is franceschini). -A takes input:                             redshift energy eg.input= 1 2,3,4,5 where z=1 and energy= 2,3,4,5 TeV",nargs=2)

    cfg = parser.parse_args()
    
    if cfg.model:
        cat=EBLAbsorption(cfg.model)
    if cfg.absorption_coefficient:
        for i in cfg.absorption_coefficient[1]:
            try:
                print(cat.absorption(float(cfg.absorption_coefficient[0]),[int(i)]))
            except ValueError:
                continue
    if cfg.after_absorption_flux:
        for i in cfg.after_absorption_flux[1]:
            try:
                print(cat.get_flux(float(cfg.after_absorption_flux[0]),[int(i)])," TeV")
            except ValueError:
                continue


# In[ ]:




