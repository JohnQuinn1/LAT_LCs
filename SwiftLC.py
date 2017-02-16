import os
import sys
import wget

import map_name

class SwiftLC:
    """
    Class for downloading Swift lightcurves ('Overall Light Curve')
    Existing file will be overwritten.

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


    def download(self,name):
        """
        Download and rename the file for the given object.
        Returns filename if download successful or None if file not found.
        Unknown what happens if error, for example, connecting to server.
        """
        
        if self.quiet:
            bar_style=None
        else:
            bar_style=wget.bar_adaptive

        swift_name=map_name.map_name(name,"Swift_LC")

        filename='lightcurve.txt'
        if os.path.isfile(filename):
            if not self.quiet: print("Removing local file:",filename)
            os.remove(filename)

        self.remote_filename="http://www.swift.psu.edu/monitoring/data/"+swift_name+"/lightcurve.txt"
        if not self.quiet: print("Downloading latest file:",self.remote_filename)


        try:
            from urllib.error import HTTPError # just so I can catch and handle this exception
            x=wget.download(self.remote_filename, bar=bar_style)
        except HTTPError as e:
            if not self.quiet:
                print(e)
            return None
        except:
            if not self.quiet:
                print("Some error occurred...")
            raise

        new_filename="Swift_"+map_name.map_name(name,"LAT_LC")+".txt"

        if not self.quiet: 
            print()
            print("Renaming",filename,'to',new_filename)
        os.rename(filename,new_filename)

        return new_filename
         

         



            


