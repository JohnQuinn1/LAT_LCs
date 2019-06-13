#!/usr/bin/env python
# coding: utf-8

# In[36]:


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
            ebllogger.warning(str(error)+"is an invalid name of model. I use default 'franceschini'")
            self.ebl=Absorption.read_builtin("franceschini")

    
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
        

    
#######################################################################

if __name__ == "__main__":
    
    logging.basicConfig(level=logging.WARNING,format='%(asctime)s %(message)s',                    datefmt='%m/%d/%Y %I:%M:%S %p')
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-M','--model_and_absorption',help="choose absorption model, state redshift and energy(energy is assumed to be in TeV)",default="franceschini", required=False,nargs=3)

    cfg = parser.parse_args()
    
    if cfg.model_and_absorption:
        try:
            print(EBLAbsorption(str(cfg.model_and_absorption[0])).absorption(float(cfg.model_and_absorption[1]),float(cfg.model_and_absorption[2])))
        except ValueError:
            print("error")


# In[ ]:




