import os
import sys
import wget

import map_names

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


    def download(self,name):
        """
        Download and rename the file for the given object.
        Returns filename if download successful or None if file not found.
        Unknown what happens if error, for example, connecting to server.
        """
        
        if not self.quiet:
            bar_style=wget.bar_adaptive
        else:
            bar_style=None

        swift_name=map_names.map_name_to_SwiftLC(name)

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
            return None
        except:
            if not self.quiet:
                print("Some error occurred...")
            raise

        new_filename="Swift_"+map_names.map_name_to_LATLC(name)+".txt"

        if not self.quiet: 
            print()
            print("Renaming",filename,'to',new_filename)
        os.rename(filename,new_filename)

        return new_filename
         

         



            


