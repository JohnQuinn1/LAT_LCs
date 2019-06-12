#!/usr/bin/env python
# coding: utf-8

# In[31]:


from gammapy.spectrum.models import Absorption
import astropy.units as u
import logging
import sys
import numpy as np
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
        and returns the 'surviving energy'
        parameters:
                redshift (int or float)
                energy (list*u.unit)
                            where, for example, energy=([2]*u.GeV)
        """
        def goto(linenum):
            global line
            line = linenum

        try:
            line = 1
            if line == 1:
                temp=np.array(energy)
                if len(temp)>1:
                    if (min(energy))<min(self.ebl.energy): 
                            ebllogger.warning("ENERGY OUT OF RANGE FOR MODEL "+str(self.model)+                                    ", min energy="+str(min(self.ebl.energy)))
                            return(1)
                            
                else:
                    if ((energy))<min(self.ebl.energy): 
                            ebllogger.warning("ENERGY OUT OF RANGE FOR MODEL "+str(self.model)+                                    ", min energy="+str(min(self.ebl.energy)))
                            return(1)
                    goto(2)
        except TypeError:
            ebllogger.warning("INCORRECT ENERGY INPUT. See help(EBLAbsorption().absorption)")
        line==2        
        if (redshift<min(self.ebl.param)) or (redshift>max(self.ebl.param)):
                ebllogger.warning("REDSHIFT OUT OF RANGE FOR MODEL "+str(self.model)+" "+"; "                                  +str(min(self.ebl.param))+"<redshift<"+str(max(self.ebl.param)))
        else:
            return self.ebl.evaluate((energy),redshift)
        
    def get_flux(self,redshift,energy):
        return(self.absorption(redshift,energy)*energy)

#######################################################################

if __name__ == "__main__":
    
    logging.basicConfig(level=logging.WARNING,format='%(asctime)s %(message)s',                    datefmt='%m/%d/%Y %I:%M:%S %p')


# In[ ]:




