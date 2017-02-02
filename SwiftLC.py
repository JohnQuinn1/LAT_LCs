import os
import sys
import wget

class SwiftLC:
"""
Class for dowloading Swift lightcurves ('Overall Light Curve')

Example usage:

In [1]: import SwiftLC

In [2]: sw=SwiftLC.SwiftLC()

In [3]: sw.download("Mrk501")
Downloading latest file: http://www.swift.psu.edu/monitoring/data/Mrk501/lightcurve.txt
100% [..............................................................................] 45425 / 45425
Renaming lightcurve.txt to Swift_Mrk501.txt
"""

    def __init__(self,quiet=False):
        self.quiet=quiet

    def map_name_to_Swift(self,name):
        """map common names of a subset to what is on the Swift page"""

        name=name.replace(" ","")  # all whitespace needs to be removed.
        n=name.upper()            # just for matching.

        # Markarian 421
        if n in ["MRK421", "MARKARIAN421", "MKN421"]:
            return "Mrk421"

        # Markarian 501
        if n in ["MRK501", "MARKARIAN501", "MKN501"]:
            return "Mrk501"

        # W Comae
        if n in ["WCOMAE", "WCOM"]:
            return "WCom"


        # Bl Lacertae
        if n in ["BLLAC", "BLLACERTAE"]:
            return "BLLacertae"
        
        return name 


    def map_name_to_LATLC(self,name):
        """map common names of a subset of objects to Fermi LC names"""

        name=name.replace(" ","")  # all whitespace needs to be removed.
        n=name.upper()            # just for matching.

        # Markarian 421
        if n in ["MRK421", "MARKARIAN421", "MKN421"]:
            return "Mrk421"

        # Markarian 501
        if n in ["MRK501", "MARKARIAN501", "MKN501"]:
            return "Mrk501"

        # W Comae
        if n in ["W Comae", "W Com"]:
            return "WComae"

        # Bl Lacertae
        if n in ["BLLAC", "BLLACERTAE"]:
            return "BLLac"
        
        return name 


    def download(self,name):
        """Download and rename the file for the given object"""
        
        if not self.quiet:
            bar_style=wget.bar_adaptive
        else:
            bar_style=None

        swift_name=self.map_name_to_Swift(name)

        filename='lightcurve.txt'
        if os.path.isfile(filename):
            if not self.quiet: print("Removing local file:",filename)
            os.remove(filename)

        remote_filename="http://www.swift.psu.edu/monitoring/data/"+swift_name+"/lightcurve.txt"
        if not self.quiet: print("Downloading latest file:",remote_filename)


        try:
            from urllib.error import HTTPError # just so I can catch and handle this exception
            x=wget.download(remote_filename, bar=bar_style)
        except HTTPError as e:
            if not self.quiet:
                print(e)
                print("Exiting...")
            sys.exit(1)
        except:
            if not self.quiet:
                print("Some error occurred...")
            raise

        new_filename="Swift_"+self.map_name_to_LATLC(name)+".txt"

        if not self.quiet: 
            print()
            print("Renaming",filename,'to',new_filename)
        os.rename(filename,new_filename)

        return
         

         



            


