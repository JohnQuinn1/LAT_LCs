import os
import sys
import wget

import map_name

class LATLC:
    """
    Class for downloading LAT lightcurves (in FITS format)
    Existing file will be removed first.

    Example usage:
    """

    def __init__(self,quiet=False):
        self.quiet=quiet


    def download(self,name,weekly=False,already_downloaded=False):
        """
        Download and rename the file for the given object.
        If "weekly" is False then it downloads the daily file.".
        Returns filename if download successful or None if file not found.
        Unknown what happens if error, for example, connecting to server.
        """


        if self.quiet:
            bar_style=None
        else:
            bar_style=wget.bar_adaptive


        object=map_name.map_name(name,"LAT_LC")

        if weekly:
            FITS=object+'_604800.lc'
        else:
            FITS=object+'_86400.lc'


        if os.path.isfile(FITS):
            if already_downloaded:
                if not self.quiet: print("Using already-downloaded file:",FITS)
                return FITS
            else:
                if not self.quiet: print("Removing old file:",FITS)
                os.remove(FITS)



        if not self.quiet: print("Downloading latest file:",FITS)

        remote_file='https://fermi.gsfc.nasa.gov/FTP/glast/data/lat/catalogs/asp/current/lightcurves/'+FITS
        
        if not self.quiet: print("wget:",remote_file)

        try:
            from urllib.error import HTTPError # just so I can catch and handle this exception
            x=wget.download(remote_file, bar=bar_style)
        except HTTPError as e:
            self.e=e
            if not self.quiet:
                print("LATLC.download() error:",e)
                return None
        except:
            if not self.quiet:
                print("Some error occurred...")
                raise

        if not self.quiet:
            print()

        return FITS

