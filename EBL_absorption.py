#!/usr/bin/env python
# coding: utf-8

# In[95]:


from gammapy.spectrum.models import Absorption
import astropy.units as u
import logging
import sys
ebllogger=logging.getLogger(__name__)
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
            sys.stdout.write(str(error) + "isn't a valid name of model. See help(EBLAbsorption())")
#             ebllogger.warning("invalid name of model")
#             sys.exit(1)
    
    def absorption(self,redshift,energy):
        """ This function calculates absorption of EBL according to model stated in class definition 
        and returns the 'surviving energy'
        parameters:
                redshift (int or float)
                energy (tuple*u.unit)
                            where, for example, unit=TeV
                minimum valid energy is 200 GeV"""

        if min(energy)<200*u.GeV:
            sys.stdout.write("energy out of range => too small")
            return(1)
        else:
            return self.ebl.evaluate((energy),redshift)
        
    def get_flux(self,redshift,energy):
        return(self.absorption(redshift,energy)*energy)

#######################################################################

if __name__ == "__main__":
    
    logging.basicConfig(filename='EBLAbsorption.log',level=logging.WARNING,format='%(asctime)s %(message)s',                    datefmt='%m/%d/%Y %I:%M:%S %p')


# In[96]:


a=EBLAbsorption("franceschini")
print(a.absorption(0.1,(100,2000,6000)*u.GeV))
print(a.get_flux(0.1,(1000,2000)*u.GeV))


# In[ ]:




